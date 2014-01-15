# -*- coding: utf-8 -*-
import mongo_bll

import sys,os,string
import wx
import random
import struct
from array import array
#import GetShpAttri
from osgeo import ogr
#import GridSimple


"""存在的问题：
1：不能添加数据
2：不能实现颜色的改变
3：不能实现属性数据的表格弹出
"""

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
    
class guiFrame(wx.Frame):
    def __init__(self, parent):
	wx.Frame.__init__(self, parent, -1, u'小型GIS原型系统', size=(1000,690))
	self.sketch = sketchWindow(self, -1)
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
	
	#self.sketch.color = wx.Colour(random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
	#self.sketch.brush = wx.Brush(self.sketch.color)
	#filePath = r"E:\lab\Data\5W_GRID.shp"
	#self.sketch.addLayer(filePath, self.sketch.pen, self.sketch.brush)           

    #----------------------------------------------------------------------
    def getShpData(self, database_name = "shapefile", collection_name = "china_town"):
	""""""
	data = mongo_bll.find(database_name, collection_name, show_dict= {"geom":1, "NAME":1,"_id":0},limit=50)
	return data
	

    def OnOpen(self, event):
	data = self.getShpData()
	self.newPage = show_shapefile.sketchWindow(self, wx.ID_ANY) 
	self.newPage.addLayer(data, wx.Pen("black",2,wx.SOLID),wx.Brush('blue'))
	
	#dialog = wx.FileDialog(None, u'打开Shape文件', u'.', u'', u'Shape File (*.shp)|*.shp|All Files (*.*)|*.*', style = wx.OPEN )             
	
	#if dialog.ShowModal() == wx.ID_OK:
	    ##self.sketch.color = wx.Colour(random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
	    #self.sketch.color = wx.Colour(0,0,0,0)
	    #self.sketch.brush = wx.Brush(self.sketch.color)
	    #self.sketch.addLayer(dialog.GetPath(), self.sketch.pen, self.sketch.brush)
	#dialog.Destroy()

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
    
class sketchWindow(wx.Panel):
    def __init__(self, parent, ID ):
	wx.Panel.__init__(self, parent, ID)
	self.SetBackgroundColour('white')
	#默认设置
	self.color = 'black'
	self.brush = wx.Brush('blue')
	self.thickness = 2
	self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)
	self.pos = (0, 0)
	#self.size = size
	self.size = []
	self.extent = []
	self.ratio = 0.0
	#图层设置
	self.geometry = []
	self.layer = []
	self.layers = []
	
	#初始化
	self.InitBuffer()
	self.Bind(wx.EVT_SIZE, self.OnSize)
	self.Bind(wx.EVT_IDLE, self.OnIdle)
	self.Bind(wx.EVT_PAINT, self.OnPaint)
	self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
	self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
	self.Bind(wx.EVT_CONTEXT_MENU,self.OnContextMenu)

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
	    for type, geometry in layer:
		self.geometry = []
		for coords in geometry:
		    x = (coords[0]-self.extent[0]/2-self.extent[1]/2)*self.ratio+self.size.width/2+self.pos[0]
		    y = self.size.height-(coords[1]-self.extent[2]/2-self.extent[3]/2)*self.ratio-self.size.height/2-self.pos[1]
		    
		    self.geometry.append((x,y))
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

    def addFeature(self, list, type):
	#self.geometry = []
	#while len(list):
	    #y = list.pop()
	    #x = list.pop()
	    #self.geometry.append((x,y))
	self.layer.append((type, list))
	#self.reInitBuffer = True

    def addLayer(self, data, pen , brush ):
	self.layer = []	
	#try:
	for i in data:	    
	    print i
	    if i["geom"]["type"].lower() == "point":	
		tmpList=[]
		tmpList.extend(i["geom"]["coordinates"][0])
		self.addFeature(tmpList,'D')
		#print 'single dot'
	    if i["geom"]["type"].lower() == "polyline":
		tmpList = i["geom"]["coordinates"][0]
		self.addFeature(tmpList,'L')
		#print 'single polyline'
	    if i["geom"]["type"].lower() == "polygon":
		tmpList = i["geom"]["coordinates"][0]
		tmpList.extend(tmpList[:2])
		self.addFeature(tmpList,'P')
		#print 'single polygon'
	    if i["geom"]["type"].lower() == "multipoint":
		for i in range(len(i["geom"]["coordinates"][0])):
		    tmpList=[]
		    tmpList.extend(i["geom"]["coordinates"][0][i])
		    self.addFeature(tmpList,'D')
		#print 'multi dots '+str(len(geoList[2]))
	    if i["geom"]["type"].lower() == "multiline":
		for i in range(len(i["geom"]["coordinates"][0])):
		    tmpList = i["geom"]["coordinates"][0][i]
		    self.addFeature(tmpList,'L')
		#print 'multi polylines '+str(len(geoList[2]))
	    if i["geom"]["type"].lower() == "multipolygon":
		for i in range(len(i["geom"]["coordinates"][0])):
		    tmpList = i["geom"]["coordinates"][0][i]
		    #tmpList.extend(tmpList[:2])
		    self.addFeature(tmpList,'P')
		#print 'multi polygons '+str(len(geoList[2]))
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
	    
class sketchWindow2(wx.Window):
    def __init__(self, ID):
	wx.Window.__init__(self,  ID)
	self.SetBackgroundColour('White')
	#默认设置
	self.color = 'Black'
	self.brush = wx.Brush('Blue')
	self.thickness = 2
	self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)
	self.pos = (0, 0)
	self.size = []
	self.extent = []
	self.ratio = 0.0
	#图层设置
	self.geometry = []
	self.layer = []
	self.layers = []
	
	#初始化
	self.InitBuffer()
	self.Bind(wx.EVT_SIZE, self.OnSize)
	self.Bind(wx.EVT_IDLE, self.OnIdle)
	self.Bind(wx.EVT_PAINT, self.OnPaint)
	self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
	self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
	self.Bind(wx.EVT_CONTEXT_MENU,self.OnContextMenu)

    def OnSize(self, event):
	self.size = self.GetClientSize()
	if self.extent: self.SetExtent(self.extent)
	self.reInitBuffer = True

    def OnIdle(self, event):
	if self.reInitBuffer:
	    self.InitBuffer()
	    self.Refresh(False)
	    
    def OnPaint(self, event):
	dc = wx.BufferedPaintDC(self, self.buffer)        

    def InitBuffer(self):
	self.size = self.GetClientSize()
	self.buffer = wx.EmptyBitmap(self.size.width, self.size.height)
	dc = wx.BufferedDC(None, self.buffer)
	dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
 
	try:
	    gcdc = wx.GCDC(dc)
	except:
	    gcdc = dc
	
	alphaColor = wx.Colour(0,0,0,128)#半透明
	brush = wx.Brush(alphaColor)
	gcdc.SetBrush(brush)
	
	dc.Clear()
	
	self.DrawLayers(gcdc)
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
		    self.geometry.append((x,y))
		if type == 'D':
		    dc.DrawPointList(self.geometry)
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

    def addLayer(self, fileIn, pen, brush):
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
		#print 'single dot'
	    if geoList[1]==2:
		tmpList=geoList[2].tolist()
		self.addFeature(tmpList,'L',shpFeature.GetFID())
		#print 'single polyline'
	    if geoList[1]==3:
		tmpList=geoList[2][0].tolist()
		tmpList.extend(tmpList[:2])
		self.addFeature(tmpList,'P',shpFeature.GetFID())
		#print 'single polygon'
	    if geoList[1]==4:
		for i in range(len(geoList[2])):
		    tmpList=[]
		    tmpList.extend(geoList[2][i])
		    self.addFeature(tmpList,'D',shpFeature.GetFID())
		#print 'multi dots '+str(len(geoList[2]))
	    if geoList[1]==5:
		for i in range(len(geoList[2])):
		    tmpList=geoList[2][i].tolist()
		    self.addFeature(tmpList,'L',shpFeature.GetFID())
		#print 'multi polylines '+str(len(geoList[2]))
	    if geoList[1]==6:
		for i in range(len(geoList[2])):
		    tmpList=geoList[2][i][0].tolist()
		    tmpList.extend(tmpList[:2])
		    self.addFeature(tmpList,'P',shpFeature.GetFID())
		#print 'multi polygons '+str(len(geoList[2]))
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
	    self.SetColor(colorData.GetColour())
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
    
    
if __name__ == '__main__':
    
    app = wx.PySimpleApp()
    frame = guiFrame(None)
    frame.Show()
    app.MainLoop() 
