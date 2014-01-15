# -*- coding: utf-8 -*-

import sys,os,string
import wx
import random
import struct
import numpy
from array import array
import time
import math

from osgeo import gdal
from osgeo import ogr
import gdalconst


"""存在的问题：
1：不能添加数据
2：不能实现颜色的改变
3：不能实现属性数据的表格弹出
"""


class guiFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, u'小型GIS原型系统', size=(1000,690))

	panel = wx.Panel(self,-1)
	
        self.Center()
        #菜单
        menuBar=wx.MenuBar()
        mFile=wx.Menu()
        mFile.Append(101, u'打开(&O)', u'打开文件')
        mFile.Append(102, u'保存(&S)', u'保存文件')
        mFile.Append(103, u'关闭(&C)', u'关闭文件')
        mFile.AppendSeparator()
        mFile.Append(109, u'退出(&X)', u'退出系统')
        menuBar.Append(mFile, u'文件(&F)')
        mView=wx.Menu()
        mView.Append(201, u'放大(&I)', u'放大视图')
        mView.Append(202, u'缩小(&O)', u'缩小视图')
        mView.Append(203, u'平移(&P)', u'平移视图')
        mView.Append(204, u'全图(&E)', u'整个视图')
        menuBar.Append(mView, u'视图(&V)')
        mLayer=wx.Menu()
        mLayer.Append(301, u'列表(&L)', u'图层列表')
        mLayer.AppendSeparator()
        mLayer.Append(311, u'线划(&L)', u'线段样式')
        mLayer.Append(312, u'填充(&S)', u'填充样式')
	
        mLayer.Append(313, u'线宽(&T)', u'边线宽度')
        mLayer.Append(314, u'线型(&M)', u'边线形状')
        menuBar.Append(mLayer, u'图层(&L)')
        self.SetMenuBar(menuBar)
        #命令
        wx.EVT_MENU(self, 101, self.OnOpen)
        wx.EVT_MENU(self, 103, self.OnClose)
        wx.EVT_MENU(self, 109, self.OnQuit)
        wx.EVT_MENU(self, 201, self.ZoomIn)
        wx.EVT_MENU(self, 202, self.ZoomOut)
        wx.EVT_MENU(self, 203, self.ZoomPan)
        wx.EVT_MENU(self, 204, self.ZoomAll)
        wx.EVT_MENU(self, 311, self.OnLine)
        wx.EVT_MENU(self, 312, self.OnPolygon)
	
	self.size = self.GetClientSize()
	self.sketch = sketchWindow(self, -1 ,self.size)
	
	#状态栏  
	#self.Bind(wx.EVT_MOTION, self.OnPaintMotion)  
	#self.statusbar = self.CreateStatusBar()  
	##将状态栏分割为3个区域,比例为1:2:3  
	#self.statusbar.SetFieldsCount(3)  
	#self.statusbar.SetStatusWidths([-1, -2, -3])  
	  
	  
    #def OnPaintMotion(self, event):  	  
	##设置状态栏1内容  
	#self.statusbar.SetStatusText(u"鼠标位置：" + str(event.GetPositionTuple()), 0)  	  
	##设置状态栏2内容  
	#self.statusbar.SetStatusText(u"当前线条长度：" , 1)  	  
	##设置状态栏3内容  
	#self.statusbar.SetStatusText(u"线条数目：" , 2)                  
        #event.Skip()  	


	
    def OnOpen(self, event):
        dialog = wx.FileDialog(None, u'打开Shape文件', u'.', u'', u'Shape File (*.shp)|*.shp|All Files (*.*)|*.*', style = wx.OPEN )             
        
        if dialog.ShowModal() == wx.ID_OK:
            #self.sketch.color = wx.Colour(random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
	    self.sketch.color = wx.Colour(0,0,0,0)
            self.sketch.brush = wx.Brush(self.sketch.color)
            self.sketch.addLayer(dialog.GetPath(), self.sketch.pen, self.sketch.brush)
        dialog.Destroy()

    def OnClose(self, event):
        self.sketch.SetLayers([])
        self.sketch.extent = []

    def OnQuit(self, event):
        dlg = wx.MessageDialog(None,u'确定退出?',u'提示',wx.YES_NO|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        if result == wx.ID_YES:
            self.Close()
        dlg.Destroy()

    def OnLine(self, event):
        self.sketch.lineColor()

    def OnPolygon(self, event):
        self.sketch.polygonColor()

    def ZoomIn(self, event):
        self.sketch.ratio=self.sketch.ratio*2
        self.sketch.reInitBuffer = True

    def ZoomOut(self, event):
        self.sketch.ratio=self.sketch.ratio/2
        self.sketch.reInitBuffer = True

    def ZoomPan(self, event):
        self.sketch.pos = [i+10 for i in self.sketch.pos]
        self.sketch.reInitBuffer = True

    def ZoomAll(self, event):
        self.sketch.pos = [0,0]
        self.sketch.OnSize(event)        

class sketchWindow(wx.Window):
    def __init__(self, parent, ID , filename):
        wx.Window.__init__(self, parent, ID)
        self.SetBackgroundColour('White')
		
        #默认设置
        self.pos = (0, 0)

        self.extent = []
        self.ratio = 0.0
        #图层设置		
	filepath = r"E:\lab\Paper\Data\dafeng\dafengClassify\1975dfmosaic.tif"	

	sizer = wx.BoxSizer()
	panel = wx.Panel(self,size=(600,600))
	self.size = panel.Size

	sizer.Add(panel, 1, wx.EXPAND)
	self.SetSizerAndFit(sizer)		

	image = self.ShowRaster2(filepath, 900, 600)
	
	#self.wxbitmap=wx.BitmapFromImage(image)  #.Rescale(self.size.width , self.size.height)
	#self.m_bitmap1 = wx.StaticBitmap(panel, wx.ID_ANY,self.wxbitmap, wx.DefaultPosition, wx.DefaultSize , 0 ) 
	
	self.photo = image.ConvertToBitmap()
	self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Show(True)
    
    def OnPaint(self, event):
	# create and clear the DC
	dc = wx.PaintDC(self)
	brush = wx.Brush("sky blue")
	dc.SetBackground(brush)
	dc.Clear()

	# draw the image in random locations
	#for x,y in self.positions:
	dc.DrawBitmap(self.photo, 0, 0, True)
	pen = wx.Pen('#4c4c4c', 10, wx.SOLID)
	
	pen.SetJoin(wx.JOIN_MITER)
	dc.SetPen(pen)
	dc.DrawRectangle(15, 15, 80, 50)
	
    #----------------------------------------------------------------------
    def drawImg(self):
	""""""
	self.filepath = r"C:\Users\jerryfive\Desktop\07.tiff"
	image = self.ShowRaster()
		
	self.wxbitmap=wx.BitmapFromImage(image.Rescale(400,300))  
	##self.wxbitmap=wx.BitmapFromImage(image1)  
	self.m_bitmap1 = wx.StaticBitmap(self, wx.ID_ANY,self.wxbitmap, wx.DefaultPosition, (400,300), 0 )  
	sizer = wx.BoxSizer()

    def SetExtent(self, Extent):
        if self.extent == []:
            for i in range(4):  self.extent.append(Extent[i])
        else:
            if Extent[0] < self.extent[0]:  self.extent[0] = Extent[0]
            if Extent[1] > self.extent[1]:  self.extent[1] = Extent[1]
            if Extent[2] < self.extent[2]:  self.extent[2] = Extent[2]
            if Extent[3] > self.extent[3]:  self.extent[3] = Extent[3]
        #wx.MessageDialog(None,str(self.extent)).ShowModal
        RatioX = float(self.size.width)/ (self.extent[1] - self.extent[0])
        RatioY = float(self.size.height)/ (self.extent[3] - self.extent[2])
	#print self.size.width 
        if RatioX < RatioY:
            self.ratio = RatioX
        else:
            self.ratio = RatioY

    #----------------------------------------------------------------------
    def getDS(self, file_path):
	""""""
	ds = gdal.Open(file_path)
	return ds
	
    #----------------------------------------------------------------------
    def getSpatialInfor(self, ds):
	"""获取栅格空间信息, 左上角的位置 xtopLeft, ytopLeft
	"""
	adfGeoTransform = ds.GetGeoTransform()
	xtopLeft = adfGeoTransform[0]     #/* top left x */
	yresolution = adfGeoTransform[1]  #/* w-e pixel resolution */
	xrotate  = adfGeoTransform[2]     #/* rotation, 0 if image is "north up" */
	ytopLeft = adfGeoTransform[3]     #/* top left y */
	yrotate  = adfGeoTransform[4]     #/* rotation, 0 if image is "north up" */
	yresolution = adfGeoTransform[5]  #/* n-s pixel resolution */ 	
	return xtopLeft, yresolution, xrotate, ytopLeft, yrotate, yresolution
    
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
    def getSize(self , filepath):
	""""""
	self.ds = gdal.Open(filepath)

	# 设置投影坐标范围
	self.bands = self.ds.RasterCount   	
	self.imgWidth = self.ds.RasterXSize
	self.imgHeight = self.ds.RasterYSize 	
	
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
	"""	
	    #for i in range(0, self.imgHeight):
	    #BIL = []  		                         
	    #bandNum = band.ReadAsArray(0,i,self.imgWidth,1)          
	    #BIL = bandNum[0].tolist()
	    #totalBIL.append(BIL)
	"""	
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
	#band = ds.GetRasterBand(num)
	#minMax = band.ComputeRasterMinMax()	
	#return minMax[0], minMax[1], minMax[0]-minMax[1]

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
    def ShowRaster2(self, file_path, imgWidth, imgHeight):
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
	    
	    #rowNum = len(r) -1  #row
	    #colNum = len(r[0])-1  # col
	    
	    for row in range(0, imgWidth-1, 1):
		for col in range(0, imgHeight-1, 1):
		    rvalue = r[col][row]
		    rvalue = float((rvalue - rminMax[0]))/rminMax[2]*255
		    
		    dProjX = gt[0] + gt[1]*1000*col + gt[2]*row
		    dProjY = gt[3] + gt[4]*col - gt[5]*1000*row
		    #print gt[0], gt[1], gt[2]
		    #print gt[3], gt[4], gt[5]
		    #print dProjX, dProjY
		    
		    #x = (oringeX + hang*px) #+ self.size.width/2
		    #y = (oringeY - lie*py)	
		    image.SetRGB(dProjY, dProjX , rvalue, rvalue, rvalue)	
		    #image.SetRGB(row, col , rvalue, rvalue, rvalue)	
		    
	return image

    
    #----------------------------------------------------------------------
    def ShowRaster(self):
	#设置行列号范围
	gt = self.ds.GetGeoTransform() 
	print gt

	oringeX = gt[0]
	oringeY = gt[3]
	px = gt[1]
	py = gt[5]
	
	dataWidth = self.imgWidth
	dataHeight = self.imgHeight

	totalBIL1 =[]    
	for i in range(0, dataHeight):
	    BIL = []        	
	    band = self.ds.GetRasterBand(1)                     
	    bandNum = band.ReadAsArray(0,i,dataWidth,1 )          
	    BIL = bandNum[0].tolist()
	    totalBIL1.append(BIL)
	    
	BILmax1 = numpy.max(totalBIL1)
	BILmin1 = numpy.min(totalBIL1)
	BILregion1 = BILmax1 - BILmin1

	if px>0 and py>0:
	    extent = [oringeX, oringeX + px*dataWidth, oringeY, oringeY + py*dataHeight]
	elif px>0 and py<0:
	    extent = [oringeX, oringeX + px*dataWidth, oringeY + py*dataHeight, oringeY]
	elif px<0 and py<0:
	    extent = [oringeX + px*dataWidth,oringeX,  oringeY + py*dataHeight, oringeY]	
	else:
	    extent = [oringeX + px*dataWidth,oringeX, oringeY ,  oringeY + py*dataHeight]		    

	
	self.SetExtent(extent)
	print extent

	image=wx.EmptyImage(self.size.width+1,self.size.height+1)   
	

	
	for hang in range(0, dataWidth-1 , 1):

	    for lie in range(0, dataHeight-1 , 1):

		value1 = totalBIL1[lie][hang]
		value1 = float((value1 - BILmin1))/BILregion1*255
		#print value1

		#x = (oringeX + hang*px -extent[0]/2-extent[1]/2)*self.ratio + self.size.width/2
		#y = self.size.height/2 - (oringeY + lie*py - extent[2]/2 - extent[3]/2)*self.ratio 	
	
		#image.SetRGB(x, y , value1, value1, value1)
		image.SetRGB(hang, lie , value1, value1, value1)
    
	return image



if __name__ == '__main__':
	
	app = wx.PySimpleApp()
	frame = guiFrame(None)
	
	frame.Show()
	app.MainLoop() 
