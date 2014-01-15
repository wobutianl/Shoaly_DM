# -*- coding: utf-8 -*-
# This one shows how to draw images on a DC.
import sys,os,string
import wx
import random
import struct
from array import array
from osgeo import gdal
from osgeo import ogr
import numpy
import math
random.seed()


global colorlist16
global colorlistRGB
colorlist16 = [ "#FFFF00" ,  "#FFF8DC" ,  "#FFEFDB" ,  "#FFE7BA" ,  "#FFE1FF" ,  "#FFD39B" ,  "#FFBBFF" ,  "#FFAEB9" ,  "#FF8C69" ,  "#FF8247" , 
              "#FF7256" ,  "#FF6347" ,  "#FF34B3"  ,"#FF0000" ,  "#FAFAD2" ,  "#F8F8FF" ,  "#F5F5DC" ,  
              "#F2F2F2" ,  "#F0F0F0" ,  "#EEEED1" ,  "#EEE8CD" ,  "#EEE0E5" ,  "#EED5D2" ,  "#EECBAD" ,  "#EEB422" ,  "#EEA2AD" , 
              "#EE82EE" ,  "#EE7942" ,  "#EE6A50" ,  "#EE3B3B"]
              
colorlistRGB = [(127 , 255 , 0 )  ,(118 , 238 , 0 ) ,(102 , 205 , 0 ) ,(69 , 139 , 0 ) ,(192 , 255 , 62 ), (179 , 238 , 58 ), (154 , 205 , 50 ), (105 , 139 , 34 ), 
                (202 , 255 , 112) ,(188 , 238 , 104) ,(162 , 205 , 90 ), (110 , 139 , 61 ), (255 , 246 , 143) ,(238 , 230 , 133) ,(205 , 198 , 115) ,(139 , 134 , 78 ), 
                (255 , 236 , 139) ,(238 , 220 , 130) ,(205 , 190 , 112) ,(139 , 129 , 76) ]

endian_name = sys.byteorder
  
wkbXDR = '>'     # Big Endian
wkbNDR = '<'     # Little Endian
  
def choose(bool, a, b):
    return (bool and [a] or [b])[0]
  
BTOR = choose(endian_name == 'little',wkbNDR,wkbNDR)
  
def up_endian_type(wkb):
    endian_t = struct.unpack('b',wkb[0])[0]
    endian = choose(endian_t,'<','>')
    wkbtype = struct.unpack(endian+'I',wkb[1:5])[0]
    return endian,wkbtype,endian_t
  
def up_len(wkb,beg,endian):
    return struct.unpack(endian+'I',wkb[beg:beg+4])[0]
  
def up_point(wkb):
    endian,wkbtype,et = up_endian_type(wkb)
    points = struct.unpack(endian+"2d",wkb[5:])
    return points
  
def up_linestring(wkb):
    endian,wkbtype,et = up_endian_type(wkb)
    lenght = up_len(wkb,5,endian)
    points = array('d',wkb[9:9+lenght*16])
    if endian != BTOR : points.byteswap()
    return points
  
def up_linearring(wkb,ringcount,endian):
    #endian,wkbtype,et = up_endian_type(wkb)
    points = []
    ptr = 0
    for i in range(ringcount):
        length = up_len(wkb,ptr,endian)
        ps = array('d',wkb[ptr+4:ptr+4+length*16])
        if endian != BTOR : ps.byteswap()
        points.append(ps)
        ptr += 4+length*16
    return points,ptr
  
def up_polygon(wkb,sub=-1):
    endian,wkbtype,et = up_endian_type(wkb)
    if sub == -1:
        ringcount = up_len(wkb,5,endian)
        points = up_linearring(wkb[9:],ringcount,endian)[0]
        return points
    else:
        points = []
        ptr = 5
        ringcount = up_len(wkb,ptr,endian)
        ps,ringlen = up_linearring(wkb[ptr+4:],ringcount,endian)
        points.append(ps)
        ptr += 4+ringlen
        return points,ptr
  
def up_mpoint(wkb):
    endian,wkbtype,et = up_endian_type(wkb)
    subcount = up_len(wkb,5,endian)
    points = []
    ptr = 9
    for i in range(subcount):
        subps = up_point(wkb[ptr:])
        points.append(subps)
        ptr += 9+len(subps)*8
    return points
  
def up_mlinestring(wkb):
    endian,wkbtype,et = up_endian_type(wkb)
    subcount = up_len(wkb,5,endian)
    points = []
    ptr = 9
    for i in range(subcount):
        subps = up_linestring(wkb[ptr:])
        points.append(subps)
        ptr += 9+len(subps)*8
    return points 
  
def up_mpolygon(wkb):
    endian,wkbtype,et = up_endian_type(wkb)
    subcount = up_len(wkb,5,endian)
    points = []
    ptr = 9
    for i in range(subcount):
	subps,size = up_polygon(wkb[ptr:],i)
	points.append(subps)
	ptr += size
    return points

fun_map = {
         ogr.wkbPoint : up_point,
         ogr.wkbLineString : up_linestring,
         ogr.wkbPolygon : up_polygon,
         ogr.wkbMultiPoint : up_mpoint,
         ogr.wkbMultiLineString : up_mlinestring,
         ogr.wkbMultiPolygon : up_mpolygon
         }
def WkbUnPacker(wkb):
    endian,wkbtype,endian_t = up_endian_type(wkb)
    foo = fun_map[wkbtype]
    points = foo(wkb)
    return [endian_t,wkbtype,points]

########################################################################
class raster2img():
    """栅格转为图片"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
	pass
	
    #----------------------------------------------------------------------
    def getDS(self, file_path):
	""""""
	ds = gdal.Open(file_path)
	return ds
	
    #----------------------------------------------------------------------
    def getSpatialInfor(self, ds):
	"""获取栅格空间信息, 左上角的位置 xtopLeft, ytopLeft
	"""
	gt = ds.GetGeoTransform()
	"""
	xtopLeft = adfGeoTransform[0]     #/* top left x */
	yresolution = adfGeoTransform[1]  #/* w-e pixel resolution */
	xrotate  = adfGeoTransform[2]     #/* rotation, 0 if image is "north up" */
	ytopLeft = adfGeoTransform[3]     #/* top left y */
	yrotate  = adfGeoTransform[4]     #/* rotation, 0 if image is "north up" */
	yresolution = adfGeoTransform[5]  #/* n-s pixel resolution */ 
	"""	
	return gt
    
    #----------------------------------------------------------------------
    def getRightDown(self, ds):
	"""获取右下角的坐标"""
	adfGeoTransform = ds.GetGeoTransform()
	imgWidth = ds.RasterXSize()
	imgHeight = ds.RasterYSize()
	Xgeo = adfGeoTransform[0] + imgWidth * adfGeoTransform[1] + imgHeight * adfGeoTransform[2]
	Ygeo = adfGeoTransform[3] + imgWidth * adfGeoTransform[4] + imgHeight * adfGeoTransform[5]
	return Xgeo, Ygeo
	
    #----------------------------------------------------------------------
    def getWiHe(self, ds):
	"""获取图片的长宽"""
	imgWidth = ds.RasterXSize
	imgHeight = ds.RasterYSize 
	return imgWidth, imgHeight
    
    #----------------------------------------------------------------------
    def getRasterCount(self, ds):
	"""获取波段数"""
	bandNum = ds.RasterCount 
	return bandNum
    
    #----------------------------------------------------------------------
    def getRasterColorInter(self, band):
	"""获取颜色索引表"""
	colorInter = band.GetRasterColorInterpretation()
	return colorInter
    
    #----------------------------------------------------------------------
    def getColorMap(self, band):
	"""获取颜色表"""
	colorMap = band.GetRasterColorTable()
	return colorMap
    
	
    #----------------------------------------------------------------------
    def getGeoTranform(self, ds):
	""" 获取栅格空间信息, 左上角的位置 xtopLeft, ytopLeft """	
	''' 
	adfGeoTransform[0] /* top left x */
	adfGeoTransform[1] /* w-e pixel resolution */
	adfGeoTransform[2] /* rotation, 0 if image is "north up" */
	adfGeoTransform[3] /* top left y */
	adfGeoTransform[4] /* rotation, 0 if image is "north up" */
	adfGeoTransform[5] /* n-s pixel resolution */ 	
	'''
	gt = ds.GetGeoTransform() 
	oringeX = gt[0]   # top left x 
	oringeY = gt[3]   #top left y 
	px = gt[1]        #w-e pixel resolution
	py = gt[5]        #n-s pixel resolution
	return oringeX, oringeY, px, py
	
    #----------------------------------------------------------------------
    #"""xoff=0, yoff=0, win_xsize=None, win_ysize=None, buf_xsize=None, buf_ysize=None, buf_obj=None"""
    def getBIL(self, ds, num, xoff=0 , yoff=0, win_xsize=None,win_ysize=None, buf_xsize=None, buf_ysize=None, buf_obj=None):
	"""获取栅格矩阵数据"""   
	band = ds.GetRasterBand(num)
	totalBIL = band.ReadAsArray(xoff, yoff, win_xsize, win_ysize, buf_xsize, buf_ysize, buf_obj)
	return totalBIL

    #----------------------------------------------------------------------
    def readRaster(self, ds, xoff=0, yoff=0, xsize=0, ysize=0, buf_xsize = None, buf_ysize = None, buf_type = None, band_list = None):
	"""获取二进制波段数据	
	xoff,yoff,xsize,ysize 你可能不想读取整张图像。只想读取其中的一部分。
	用xoff，yoff指定想要读取的部分原点位置在整张图像中距离全图原点的位置。
	xsize和 ysize指定要读取部分图像的矩形大小。
	buf_xsize buf_ysize 你可以在读取出一部分图像后进行缩放。那么就用这两个参数来定义缩放后图像最终的宽和高，gdal将帮你缩放到这个大小。
	buf_type 如果你要读取的图像的数据类型不是你想要的(比如原图数据类型是short，你要把它们缩小成byte)，就可以设置它。
	band_list 适应上面多波段的情况。你可以指定读取的波段序列。要哪几个波段，不要哪几个波段，你说了算。
	"""
	dataRaster = ds.ReadRaster(xoff, yoff, xsize, ysize, buf_xsize, buf_ysize, buf_type, band_list)
	return dataRaster
    
    #----------------------------------------------------------------------
    def getMinMax(self , BIL):
	""""""
	BILmax1 = numpy.max(BIL)
	BILmin1 = numpy.min(BIL)
	BILregion1 = BILmax1 - BILmin1	
	return BILmin1, BILmax1, BILregion1

    #----------------------------------------------------------------------
    def getBandMinMax(self,ds,  num):
	""""""
	band = ds.GetRasterBand(num)
	minMax = band.ComputeRasterMinMax()	
	return minMax[0], minMax[1], minMax[0]-minMax[1]	
	
    #----------------------------------------------------------------------
    def getExtent(self ,px , py , oringeX ,oringeY , dataWidth , dataHeight):
	""""""
	if px>0 and py>0:
	    extent = [oringeX, oringeX + px*dataWidth, oringeY, oringeY + py*dataHeight]
	elif px>0 and py<0:
	    extent = [oringeX, oringeX + px*dataWidth, oringeY + py*dataHeight, oringeY]
	elif px<0 and py<0:
	    extent = [oringeX + px*dataWidth,oringeX,  oringeY + py*dataHeight, oringeY]	
	else:
	    extent = [oringeX + px*dataWidth,oringeX, oringeY ,  oringeY + py*dataHeight]	
	return extent
	
    #----------------------------------------------------------------------
    def ShowRaster(self, file_path, imgWidth, imgHeight):
	#设置行列号范围
	ds = self.getDS(file_path)
	wh = self.getWiHe(ds)
	bandLen = self.getRasterCount(ds)
	
	gt = ds.GetGeoTransform() 
	
	dataWidth = wh[0]
	dataHeight = wh[1]
	print dataWidth, dataHeight

	#extent = self.getExtent(px, py, oringeX, oringeY, dataWidth, dataHeight)
	#self.SetExtent(extent)
	
	image=wx.EmptyImage(imgWidth ,imgHeight) # 新建画布

	if bandLen >= 3:	    
	    r = self.getBIL(ds, 1)
	    rminMax = self.getMinMax(r)
	    
	    g = self.getBIL(ds, 2)
	    gminMax = self.getMinMax(g)
    
	    b = self.getBIL(ds, 3)
	    bminMax = self.getMinMax(b)	    

	    for hang in range(0, dataWidth-1 , 1):
		for lie in range(0, dataHeight-1 , 1):
		    rvalue = r[lie][hang]
		    rvalue = float((rvalue - rminMax[0]))/rminMax[2]*255

		    gvalue = g[lie][hang]
		    gvalue = float((gvalue - gminMax[0]))/gminMax[2]*255
		    
		    bvalue = b[lie][hang]
		    bvalue = float((bvalue - bminMax[0]))/bminMax[2]*255
		    
		    #x = (oringeX + hang*px -extent[0]/2-extent[1]/2)*self.ratio + self.size.width/2
		    #y = self.size.height/2 - (oringeY + lie*py - extent[2]/2 - extent[3]/2)*self.ratio 	

		    image.SetRGB(hang, lie , rvalue, gvalue, bvalue)
	else:
	    r = self.getBIL(ds,  1, xoff=0 , yoff=0, win_xsize=None,win_ysize=None, buf_xsize=imgWidth, buf_ysize=imgHeight, buf_obj=None )
	    rminMax = self.getMinMax(r)
	    
	    xratio = float(dataWidth/imgWidth)
	    yratio = float(dataHeight/imgHeight)
	    print xratio, yratio
	    #rowNum = len(r) -1  #row
	    #colNum = len(r[0])-1  # col
	    l = r.tolist()
	    alist = set()
	    clist = set()
	    for i in l:		
		alist = set(i)
		clist = clist|alist
	    length_value = len(clist)
	    color_value_dict = {}
	    i = 0 
	    for x in clist:
		if x == 255:
		    color_value_dict[str(x)] = (255,255,255)
		    continue
		color_value_dict[str(x)] = colorlistRGB[i]
		i += 1
	    print gt
	    #print color_value_dict
	    for row in range(0, imgWidth-1, 1):
		for col in range(0, imgHeight-1, 1):
		    rvalue = r[col][row]
		    #if 
		    #rvalue = float((rvalue - rminMax[0]))/rminMax[2]*255
		    
		    #dProjX = gt[0] + gt[1]*xratio*10*col + gt[2]*row
		    #dProjY = gt[3] + gt[4]*col - gt[5]*yratio*10*row
		    #print dProjX, dProjY
		    #print gt[0], gt[1], gt[2]
		    #print gt[3], gt[4], gt[5]
		    #print dProjX, dProjY
		    
		    #x = (oringeX + hang*px) #+ self.size.width/2
		    #y = (oringeY - lie*py)	
		    color = color_value_dict[str(rvalue)]
		    image.SetRGB(x, y , color[0], color[1], color[2])	
		    #image.SetRGB(row, col , rvalue, rvalue, rvalue)	
		    
	return image  
    
    

class RandomImagePlacementWindow(wx.Panel):
    def __init__(self, parent, image):
        wx.Panel.__init__(self, parent)
	
	self.raster = raster2img()
	self.img = self.raster.ShowRaster(image, 640, 480)
        self.photo = self.img.ConvertToBitmap()

        # choose some random positions to draw the image at:
        self.positions = [(10,10)]
            
        # Bind the Paint event
        self.Bind(wx.EVT_PAINT, self.OnPaint)


    def OnPaint(self, evt):
        # create and clear the DC
        dc = wx.PaintDC(self)
        brush = wx.Brush("sky blue")
        dc.SetBackground(brush)
        dc.Clear()

        # draw the image in random locations
        for x,y in self.positions:
            dc.DrawBitmap(self.photo, x, y, True)
        pen = wx.Pen('#4c4c4c', 10, wx.SOLID)
        
        pen.SetJoin(wx.JOIN_MITER)
        dc.SetPen(pen)
        dc.DrawRectangle(15, 15, 80, 50)


class sketch(wx.Panel):
    def __init__(self, parent, rasterPath, shpPath ):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour('white')
        #默认设置
        self.color = 'black'
        self.brush = wx.Brush('blue')
        self.thickness = 2
        self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)
        self.pos = (0, 0)
	#self.size = size
        self.size = self.Parent.GetSize()
        self.extent = []
        self.ratio = 0.0
        #图层设置
        self.geometry = []
        self.layer = []
        self.layers = []
	
        #初始化
        
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
	self.Bind(wx.EVT_CONTEXT_MENU,self.OnContextMenu)
	
	self.raster = raster2img()
	self.img = self.raster.ShowRaster(rasterPath, 640, 480)
        self.photo = self.img.ConvertToBitmap()	
	
	self.addLayer(shpPath, self.pen, self.brush)	
	self.InitBuffer()

    def OnSize(self, event):
        #self.size = self.GetClientSize()
        if self.extent: self.SetExtent(self.extent)
        self.reInitBuffer = True

    def OnIdle(self, event):
        if self.reInitBuffer:
            self.InitBuffer()
            self.Refresh(False)
            
    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self, self.buffer)        

    def InitBuffer(self):
	#self.size = self.GetParent().GetWinSize()
        self.size = self.GetClientSize()
        self.buffer = wx.EmptyBitmap(self.size.width, self.size.height)
        dc = wx.BufferedDC(None, self.buffer)
	
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))

        dc.Clear()
	
	dc.DrawBitmap(self.photo, 0, 0, True)
        self.DrawLayers(dc)
        #重设变量状态
        self.reInitBuffer = False

    def SetExtent(self, Extent):
        if self.extent == []:
            for i in range(4):  self.extent.append(Extent[i])
        else:
            if Extent[0] < self.extent[0]:  self.extent[0] = Extent[0]
            if Extent[1] > self.extent[1]:  self.extent[1] = Extent[1]
            if Extent[2] < self.extent[2]:  self.extent[2] = Extent[2]
            if Extent[3] > self.extent[3]:  self.extent[3] = Extent[3]
        #wx.MessageDialog(None,str(self.extent)).ShowModal()
        RatioX = self.size.width / (self.extent[1] - self.extent[0])
        RatioY = self.size.height / (self.extent[3] - self.extent[2])
        if RatioX < RatioY:
            self.ratio = RatioX
        else:
            self.ratio = RatioY

    def GetLayers(self):
        return self.layers[:]
    
    def SetLayers(self, layers):
        self.layers = layers[:]
        self.InitBuffer()
        self.Refresh()

    def DrawLayers(self, dc):
        for name, pen, brush, layer in self.layers:
            self.pen = pen
            self.brush = brush
            for OID, type, geometry in layer:
                self.geometry = []
                for coords in geometry:
                    x = (coords[0]-self.extent[0]/2-self.extent[1]/2)*self.ratio+self.size.width/2+self.pos[0]
                    y = self.size.height-(coords[1]-self.extent[2]/2-self.extent[3]/2)*self.ratio-self.size.height/2-self.pos[1]
		    
		    #print x, y 
                    self.geometry.append((x, y))
                if type == 'D':
		    #dc.DrawPointList(self.geometry)
		    dc.SetBrush(self.brush)
		    for point in self.geometry:			
			dc.DrawCirclePoint(point ,2)
                if type == 'L':
                    dc.DrawLines(self.geometry)
                if type == 'P':
                    dc.SetBrush(self.brush)
                    dc.DrawPolygon(self.geometry)
                else: pass

    def addFeature(self, list, type, OID):
        self.geometry = []
        while len(list):
            y = list.pop()
            x = list.pop()
            self.geometry.append((x,y))
        self.layer.append((OID, type, self.geometry))
        #self.reInitBuffer = True

    def addLayer(self, fileIn, pen , brush ):
        self.layer = []
        shpFile=ogr.Open(str(fileIn))
	self.lyr = shpFile.GetLayer()
        shpLayer=shpFile.GetLayer()
        shpExtent=shpLayer.GetExtent()
        self.SetExtent(shpExtent)
        shpFeature=shpLayer.GetNextFeature()
	
        #try:
	while shpFeature:
	    geoFeature=shpFeature.GetGeometryRef()
	    geoWKB=geoFeature.ExportToWkb()
	    geoList=WkbUnPacker(geoWKB)
	    if geoList[1]==1:
		tmpList=[]		
		tmpList.extend(geoList[2])		
		self.addFeature(tmpList,'D',shpFeature.GetFID())
	    if geoList[1]==2:
		tmpList=geoList[2].tolist()
		self.addFeature(tmpList,'L',shpFeature.GetFID())
	    if geoList[1]==3:
		tmpList=geoList[2][0].tolist()
		
		tmpList.extend(tmpList[:2])
		self.addFeature(tmpList,'P',shpFeature.GetFID())
	    if geoList[1]==4:
		for i in range(len(geoList[2])):
		    tmpList=[]
		    tmpList.extend(geoList[2][i])
		    self.addFeature(tmpList,'D',shpFeature.GetFID())
	    if geoList[1]==5:
		for i in range(len(geoList[2])):
		    tmpList=geoList[2][i].tolist()
		    self.addFeature(tmpList,'L',shpFeature.GetFID())
	    if geoList[1]==6:
		for i in range(len(geoList[2])):
		    tmpList=geoList[2][i][0][0].tolist()
		    tmpList.extend(tmpList[:2])
		    self.addFeature(tmpList,'P',shpFeature.GetFID())
	    else:
		pass
	    shpFeature=shpLayer.GetNextFeature()     
            
        #except:
            #print "get wrong"
        
        self.layers.append((shpLayer.GetName(), pen, brush, self.layer))
        self.reInitBuffer = True
	
    def GetShpAttributes(self ):
	"""读取shp 的attributes 数据"""
	feat = self.lyr.GetNextFeature()
	feat_defn = self.lyr.GetLayerDefn() 
	attriValue = []
	while feat:       
	    attri_data  = {}
	    for i in range(feat_defn.GetFieldCount()):                 
		value = feat.GetField(i) 
		if isinstance(value, str): 
		    pass
		    #value = unicode(value, u"gb2312")
		field = feat.GetFieldDefnRef(i) 
		fieldname = field.GetName() 
		attri_data[fieldname] = value
	    feat.Destroy() 
	    attriValue.append(attri_data)
	    feat = self.lyr.GetNextFeature() 
	return attriValue

    def lineColor(self):
        colorData = wx.ColourData()
        colorData.SetColour(self.color)
        dlg = wx.ColourDialog(self, colorData)
        if dlg.ShowModal() == wx.ID_OK:
            colorData = dlg.GetColourData()
	    #color = colorData.GetColour()
            self.SetColor(colorData.GetColour())
	    #self.pen = color
        dlg.Destroy()

    def polygonColor(self):
        colorData = wx.ColourData()
        colorData.SetColour(self.brush.GetColour())
        dlg = wx.ColourDialog(self, colorData)
        if dlg.ShowModal() == wx.ID_OK:
            colorData = dlg.GetColourData()
            self.brush = wx.Brush(colorData.GetColour())
        dlg.Destroy()

    def SetColor(self, color):
        self.color = color
        self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)
        
    def SetThickness(self, num):
        self.thickness = num
        self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)

    def OnLeftDown(self, event):
        self.oldx = event.GetPositionTuple()[0]
        self.oldy = event.GetPositionTuple()[1]
        self.CaptureMouse()
        self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        
    def OnLeftUp(self, event):
        if self.HasCapture():
            self.newx = event.GetPositionTuple()[0]
            self.newy = event.GetPositionTuple()[1]
            self.pos = (self.newx-self.oldx+self.pos[0], self.oldy-self.newy+self.pos[1])
            self.ReleaseMouse()
            self.reInitBuffer = True
            self.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))
	
    def GetShpAttri(self , shp_path):
	"""获得shp的属性值
	return  data= [{},{}...]"""
	data = GetShpAttri.GetShpAttri(shp_path)
	return data
	    
    def OnContextMenu(self, event):
	#print ("OnContextMenu\n")
	# only do this part the first time so the events are only bound once
	# Yet another anternate way to do IDs. Some prefer them up top to
	# avoid clutter, some prefer them close to the object of interest
	# for clarity.
	if not hasattr(self, u"popupID1"):
	    self.zoomIn = wx.NewId()	    
	    self.zoomOut = wx.NewId()
	    self.zoomAll = wx.NewId()
	    self.palm = wx.NewId()
	    self.addData = wx.NewId()
	    self.setLineColor = wx.NewId()
	    self.setPolygonColor = wx.NewId()
	    self.attriFrame = wx.NewId()
	    self.popupID7 = wx.NewId()
	    self.popupID8 = wx.NewId()
	    self.popupID9 = wx.NewId()
	    self.Bind(wx.EVT_MENU, self.ZoomIn, id=self.zoomIn)
	    self.Bind(wx.EVT_MENU, self.ZoomOut, id=self.zoomOut)
	    self.Bind(wx.EVT_MENU, self.ZoomAll, id=self.zoomAll)
	    self.Bind(wx.EVT_MENU, self.Palm, id=self.palm)
	    self.Bind(wx.EVT_MENU, self.AddData, id=self.addData)
	    self.Bind(wx.EVT_MENU, self.SetLineColor, id=self.setLineColor)
	    self.Bind(wx.EVT_MENU, self.SetPolygonColor, id=self.setPolygonColor)
	    self.Bind(wx.EVT_MENU, self.AttriFrame, id=self.attriFrame)

	# make a menu
	menu = wx.Menu()
	# Show how to put an icon in the menu
	item = wx.MenuItem(menu, self.popupID8,"One")
	
	menu.AppendItem(item)
	# add some other items
	menu.Append(self.zoomIn, u"放大")
	menu.Append(self.zoomOut, u"缩小")
	menu.Append(self.zoomAll, u"全图")
	menu.Append(self.palm, u"拖拽")
	menu.Append(self.addData, u"添加数据")
	menu.Append(self.setLineColor, u"设置线颜色")
	menu.Append(self.setPolygonColor, u"设置面颜色")
	menu.Append(self.attriFrame, u"属性窗口")
	
	# make a submenu
	sm = wx.Menu()
	sm.Append(self.popupID8, "sub item 1")
	sm.Append(self.popupID9, "sub item 1")
	menu.AppendMenu(self.popupID7, "Test Submenu", sm)

	# Popup the menu.   If an item is selected then its handler
	# will be called before PopupMenu returns.
	self.PopupMenu(menu)
	menu.Destroy()
	

    def SetLineColor(self, event):
        self.lineColor()
	self.reInitBuffer = True

    def SetPolygonColor(self, event):
        self.polygonColor()
	self.reInitBuffer = True

    #----------------------------------------------------------------------
    def zoom_in(self):
	""""""
        try:
	    self.ratio=self.ratio*2
	    self.reInitBuffer = True	
	    print ("Popup nine\n") 	    
	except:
	    print "zoomin wrong"
	    
    def zoom_out(self):
        self.ratio=self.ratio/2
        self.reInitBuffer = True
	
    def zoom_all(self):
        self.pos = [0,0]
	self.reInitBuffer = True
        #self.OnSize(event)
	
    def move(self, move):
	self.pos = move
	self.reInitBuffer = True    
	
    def ZoomIn(self, event):
        try:
	    self.ratio=self.ratio*2
	    self.reInitBuffer = True	
	    print ("Popup nine\n") 	    
	except:
	    print "zoomin wrong"

    def ZoomOut(self, event):
        self.ratio=self.ratio/2
        self.reInitBuffer = True

    def Palm(self, event):
        self.pos = [i+10 for i in self.pos]
        self.reInitBuffer = True

    def ZoomAll(self, event):
        self.pos = [0,0]
        self.OnSize(event)
	
    #----------------------------------------------------------------------
    def AddData(self , event):
	""""""
	pass
    #----------------------------------------------------------------------
    #----------------------------------------------------------------------
    def AttriFrame(self,event):
	"""shp 属性表"""
	data = self.GetShpAttributes()
	#MDISashDemo.MyParentFrame().NewMdiWindow(data)
	#GridSimple.SimpleGrid(win, data, sys.stdout)
	pass

        
class TestFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Loading Images",
                          size=(640,480))
        pic_path = r"E:\lab\Paper\Data\dafeng\dafengClassify\1975dfmosaic.tif"	
	shp_path = r"E:\lab\Paper\Data\country_shp\bou1_4l.shp"
        #img = wx.Image(r"C:\Users\jerryfive\Desktop\hsq\splash.png")
        #win = RandomImagePlacementWindow(self, pic_path)
	win = sketch(self, pic_path, shp_path)
        

app = wx.PySimpleApp()
frm = TestFrame()
frm.Show()
app.MainLoop()
