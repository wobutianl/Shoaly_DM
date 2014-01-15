# -*- coding: utf-8 -*-
############################
##  抽取数据库矢量数据的显示 + 显示属性数据
############################
import mongo_bll

import sys,os,string
import wx
import random
import struct
from array import array
from osgeo import ogr

import global_func
import json
from shapely.geometry import mapping, shape

from shapely.wkb import loads

"""存在的问题：
1：不能添加数据
2：不能实现颜色的改变
3：不能实现属性数据的表格弹出
"""


    
class guiFrame(wx.Frame):
    def __init__(self, parent):
	wx.Frame.__init__(self, parent, -1, u'小型GIS原型系统', size=(1000,690))
	#self.sketch = sketchWindow(self, -1, )
	#self.sketch = sketchWindow(self, wx.ID_ANY, extent) 
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
	wx.EVT_MENU(self, 102, self.OnSave)
	wx.EVT_MENU(self, 103, self.OnClose)
	wx.EVT_MENU(self, 109, self.OnQuit)
	wx.EVT_MENU(self, 201, self.ZoomIn)
	wx.EVT_MENU(self, 202, self.ZoomOut)
	wx.EVT_MENU(self, 203, self.ZoomPan)
	wx.EVT_MENU(self, 204, self.ZoomAll)
	wx.EVT_MENU(self, 311, self.OnLine)
	wx.EVT_MENU(self, 312, self.OnPolygon)
	
	self.sketch = sketchWindow(self, wx.ID_ANY)
	
	#self.sketch.color = wx.Colour(random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
	#self.sketch.brush = wx.Brush(self.sketch.color)
	#filePath = r"E:\lab\Data\5W_GRID.shp"
	#self.sketch.addLayer(filePath, self.sketch.pen, self.sketch.brush)           

    #----------------------------------------------------------------------
    def getShpData(self, database_name = "shapefile", collection_name = "bou1_4p"):
	""""""
	
	data = mongo_bll.find(database_name, collection_name, show_dict= {"geom":1,"NAME":1, "_id":0})
	return data
    
    #----------------------------------------------------------------------
    def getExtent(self, database_name = "metaDB", collection_name = "bou1_4p"):
	""""""
	data = mongo_bll.find(database_name, collection_name, show_dict={"extent":1,"_id":0})
	for i in data:
	    return i["extent"]
    	    
    def OnOpen(self, event):
	self.data = self.getShpData()
	extent = self.getExtent()
	#self.sketch = sketchWindow(self, wx.ID_ANY)
	self.sketch.addLayer(self.data, wx.Pen("black",2,wx.SOLID),wx.Brush("#0000"), extent)
	
    def OnSave(self, event):
	#self.data = self.getShpData(collection_name="XianCh_point")
	
	# Find the 10 users nearest to the point 40, 40 with max distance 5 degrees
	#box = [[110,30],[120,40]]
	#center = [100,33]
	#radius = 5
	polygon1 = [[100,30],[110,35],[115,33],[105,25]] 
	match_dict = {"geom.coordinates":{"$within":{"$polygon":polygon1}}}
	#{"geom.coordinates":{"$within":{"$center":[center,radius]}}}  #{"geom.coordinates":{"$within":{"$box":box}}}
	#limit = 52
	self.data  = mongo_bll.find(database_name = "shapefile",collection_name="XianCh_point",
	                            match_dict= match_dict, show_dict= {"geom":1, "_id":0}, )

	#mongo_bll.create_spaceIndex(database_name = "shapefile", collection_name = "XianCh_point")
	extent = self.getExtent(collection_name="XianCh_point")
	self.sketch.addLayer(self.data, wx.Pen("red",2,wx.SOLID),wx.Brush("#f0f0f0"), extent)
	
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
	self.layers = [[]]*5
	self.shape_dicts = []
	self.flag = 0
	self.dataNum = 0
	
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
	if self.extent: 
	    self.SetExtent(self.extent)
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
	#self.draw_shape(dc)
	dc.Clear()	

	for i in range(self.dataNum):
	    self.DrawLayers(i, dc)
	if self.flag == 1: 
	    self.DrawText(dc)

	#重设变量状态
	self.reInitBuffer = False

    def SetExtent(self, Extent):
	if self.extent == []:
	    for i in range(4):  
		self.extent.append(Extent[i])
	else:
	    if Extent[0] < self.extent[0]:  self.extent[0] = Extent[0]
	    if Extent[1] > self.extent[1]:  self.extent[1] = Extent[1]
	    if Extent[2] < self.extent[2]:  self.extent[2] = Extent[2]
	    if Extent[3] > self.extent[3]:  self.extent[3] = Extent[3]

	RatioX = self.size.width / (self.extent[1] - self.extent[0])
	RatioY = self.size.height / (self.extent[3] - self.extent[2])
	if RatioX < RatioY:
	    self.ratio = RatioX
	else:
	    self.ratio = RatioY

    
    def SetLayers(self, layers):
	self.layers = layers[:]
	self.InitBuffer()
	self.Refresh()

    #----------------------------------------------------------------------
    def cal_point(self, coord1, coord2, extent):
	""""""
	x = (coord1-self.extent[0]/2-self.extent[1]/2)*self.ratio + self.size.width/2# + self.pos[0]
	y = self.size.height-(coord2-self.extent[2]/2-self.extent[3]/2)*self.ratio-self.size.height/2 #-self.pos[1]	
	return (x,y)
    
    #----------------------------------------------------------------------
    def draw_shape(self, dc ):
	""""""
	dc.Pen = self.pen
	dc.Brush = self.brush
	dc.DrawCirclePoint((700,120),3)	 	

    def DrawLayers(self, i, dc):
	for pen, brush, layer in self.layers[i]:
	    self.pen = pen
	    self.brush = brush
	    
	    for type, geometry in layer:
		self.geometry = []
		for coords in geometry:
		    x = (coords[0]-self.extent[0]/2-self.extent[1]/2)*self.ratio + self.size.width/2 + self.pos[0]
		    y = self.size.height-(coords[1]-self.extent[2]/2-self.extent[3]/2)*self.ratio-self.size.height/2-self.pos[1]		    
		    self.geometry.append((x,y))
		if type == 'D':
		    #dc.SetBrush(self.brush)
		    for point in self.geometry:	
			dc.DrawCirclePoint(point ,2)
		    #print self.cal_point(122, 55, self.extent)
		    #dc.DrawCirclePoint((750.2524900778502, 90.17498341600344),10)
		if type == 'L':
		    #dc.SetBrush(self.brush)
		    dc.DrawLines(self.geometry)		    
		if type == 'P':
		    #dc.SetBrush(self.brush)
		    dc.DrawPolygon(self.geometry)
		else: pass
	
    #----------------------------------------------------------------------
    def DrawText(self, dc):
	"""绘制文字"""
	print len(self.shape_dicts)
	for pen, brush, layer in self.shape_dicts:
	    self.pen = pen
	    self.brush = brush	
	    coords = []
	    coords.append(layer["center"].x)
	    coords.append(layer["center"].y)
	    x = (coords[0]-self.extent[0]/2-self.extent[1]/2)*self.ratio + self.size.width/2 + self.pos[0]
	    y = self.size.height-(coords[1]-self.extent[2]/2-self.extent[3]/2)*self.ratio-self.size.height/2-self.pos[1]		    
 
	    text = layer["name"]
	    print text
	    dc.DrawText(text, x,y)
	    
    #----------------------------------------------------------------------
    def addText(self, data, pen , brush):
	""""""
	self.flag = 1

	for geom in data:
	    shape_dict = {}
	    
	    json_geom = json.dumps(geom["geom"])
	    shape_geom = shape(json.loads(json_geom))
	    center = shape_geom.centroid
	    
	    shape_dict["name"] = geom["NAME"]
	    shape_dict["center"] = center
	    
	    self.shape_dicts.append((pen, brush, shape_dict))
	self.reInitBuffer = True
	    
    def addLayer(self,  data, pen , brush, extent):
	self.SetExtent(extent)
	self.layer = []	
	#try:
	for geom in data:	
	    geom_type = geom["geom"]["type"].lower()
	    geom_data = geom["geom"]["coordinates"]
	    	    
	    if geom_type == "point":	
		tmpList=[]
		tmpList.extend(geom_data)
		geometry = []
		while len(tmpList):
		    y = tmpList.pop()
		    x = tmpList.pop()
		    geometry.append((x,y))
		self.layer.append(("D", geometry))
		
	    if geom_type == "linestring":
		tmpList = geom_data  #[0]
		self.layer.append(("L", tmpList))
		
	    if geom_type == "polygon":
		tmpList= geom_data[0]
		self.layer.append(("P", tmpList))

	    if geom_type == "multipoint":
		for i in range(len(geom_data[0])):
		    tmpList=[]
		    tmpList.extend(geom_data[0][i])
		    self.layer.append(("D", tmpList))

	    if geom_type == "multiline":
		for i in range(len(geom_data[0])):
		    tmpList = geom_data[0].tolist()
		    self.layer.append(("L", tmpList))

	    if geom_type == "multipolygon":
		for i in range(len(geom_data[0])):
		    tmpList = geom_data[0][i]
		    self.layer.append(("P", tmpList))
	    else:
		print geom_type
		print "error"
    
	self.layers[self.dataNum].append((pen, brush, self.layer))
	self.dataNum += 1
	self.reInitBuffer = True
	
    
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
