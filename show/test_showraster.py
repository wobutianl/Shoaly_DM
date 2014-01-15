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
	print self.size
	self.sketch = sketchWindow(self, -1 ,self.size)


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
	self.getSize(filepath)
	self.getBIL()
	sizer = wx.BoxSizer()
	panel = wx.Panel(self,size=(self.imgWidth,self.imgHeight))
	print self.imgHeight
	self.size = panel.Size
	print self.size
	sizer.Add(panel, 1, wx.EXPAND)
	self.SetSizerAndFit(sizer)		

	image = self.ShowRaster()
	
	self.wxbitmap=wx.BitmapFromImage(image.Rescale(self.size.width , self.size.height)) 

	self.m_bitmap1 = wx.StaticBitmap(panel, wx.ID_ANY,self.wxbitmap, wx.DefaultPosition, wx.DefaultSize , 0 ) 

	
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
    def getSize(self , filepath):
	""""""
	self.ds = gdal.Open(filepath)

	# 设置投影坐标范围
	self.bands = self.ds.RasterCount   	
	self.imgWidth = self.ds.RasterXSize
	self.imgHeight = self.ds.RasterYSize 	
	
    #----------------------------------------------------------------------
    def getGeoTranform(self):
	""""""
	gt = self.ds.GetGeoTransform() 
	''' 
	adfGeoTransform[0] /* top left x */
	adfGeoTransform[1] /* w-e pixel resolution */
	adfGeoTransform[2] /* rotation, 0 if image is "north up" */
	adfGeoTransform[3] /* top left y */
	adfGeoTransform[4] /* rotation, 0 if image is "north up" */
	adfGeoTransform[5] /* n-s pixel resolution */ 	
	'''
	
	self.oringeX = gt[0]   # top left x 
	self.oringeY = gt[3]   #top left y 
	self.px = gt[1]        #w-e pixel resolution
	self.py = gt[5]        #n-s pixel resolution
	
    #----------------------------------------------------------------------
    def getBIL(self ):
	"""获取栅格矩阵数据"""
	totalBIL = []
	for i in range(0, self.bands):
	    oneBIL = []
	    for j in range(0, self.imgHeight):
		BIL = []
		band = self.ds.GetRasterBand(i+1)                     
		bandNum = band.ReadAsArray(0,j,self.imgWidth,1 )          
		BIL = bandNum[0].tolist()
		oneBIL.append(BIL)	
	    #stri = str(i+1)
	    totalBIL.append(oneBIL)
	return totalBIL
    
    #----------------------------------------------------------------------
    def getColorRegion(self , oneBIL):
	""""""
	BILmax = numpy.max(totalBIL1)
	BILmin = numpy.min(totalBIL1)
	BILregion = BILmax - BILmin	
	return BILmin , BILregion
	
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
    def ShowRaster2(self   ):
	#设置行列号范围
	gt = self.ds.GetGeoTransform() 
	oringeX = gt[0]
	oringeY = gt[3]
	px = gt[1]
	py = gt[5]
	
	dataWidth = self.imgWidth
	dataHeight = self.imgHeight

	extent = self.getExtent(px, py, oringeX, oringeY, dataWidth, dataHeight)
	self.SetExtent(extent)
	print extent
	print "ratio :%f" %self.ratio
	
	datas = []  
	totalBIL = self.getBIL()
	for i in range(0, self.bands):
	    datas.append(numpy.reshape(totalBIL[i],(1,-1)))
	datas = numpy.flipud(datas)
	
	colorRegion = self.getColorRegion(totalBIL[1])
	
	image=wx.EmptyImage(self.size.width+1,self.size.height+1)   
	
	print dataWidth, dataHeight
	
	print datas[0][0]
	for hang in range(0, dataWidth-1 , 1):
	    #start1 = time.time()
	    for lie in range(0, dataHeight-1 , 1):
		#start1 = time.time()
		value1 = totalBIL1[lie][hang]
		value1 = float((value1 - BILmin))/BILregion*255
		#end1 =time.time()

		#start2 = time.time()
		x = (oringeX + hang*px -extent[0]/2-extent[1]/2)*self.ratio + self.size.width/2
		y = self.size.height/2 - (oringeY + lie*py - extent[2]/2 - extent[3]/2)*self.ratio 	
		
		#print x,y
		
		#start = time.time()		
		image.SetRGB(x, y , value1, value1, value1)
		#end = time.time()
		#print "time %d" %(end-start)
		
	    #end2 = time.time()
	    #print "calc x, y %d" %(end2 - start1)	    
	return image

    
    #----------------------------------------------------------------------
    def ShowRaster(self):
	#设置行列号范围
	gt = self.ds.GetGeoTransform() 
	print gt
	#adfGeoTransform[0] /* top left x */
	#adfGeoTransform[1] /* w-e pixel resolution */
	#adfGeoTransform[2] /* rotation, 0 if image is "north up" */
	#adfGeoTransform[3] /* top left y */
	#adfGeoTransform[4] /* rotation, 0 if image is "north up" */
	#adfGeoTransform[5] /* n-s pixel resolution */ 	
	oringeX = gt[0]
	oringeY = gt[3]
	px = gt[1]
	py = gt[5]
	
	dataWidth = self.imgWidth
	dataHeight = self.imgHeight
	
	#totalBIL = {}
	#for i in range(0, self.bands):
	    #oneBIL = []
	    #for j in range(0, dataHeight):
		#BIL = []
		#band = self.ds.GetRasterBand(i+1)                     
		#bandNum = band.ReadAsArray(0,j,dataWidth,1 )          
		#BIL = bandNum[0].tolist()
		#oneBIL.append(BIL)	
	    #stri = str(i+1)
	    #totalBIL[stri] = oneBIL
	    
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
	
	
	#print totalBIL1
	    
	#totalBIL2 = []
	#for i in range(0, dataHeight):
	    #BIL = []        	
	    #band =self.ds.GetRasterBand(2)                     
	    #bandNum = band.ReadAsArray(0,i,dataWidth,1 )          
	    #BIL = bandNum[0].tolist()
	    #totalBIL2.append(BIL)
	    
	#BILmax2 = numpy.max(totalBIL2)
	#BILmin2= numpy.min(totalBIL2)
	#BILregion2 = BILmax2 - BILmin2
	
	#totalBIL3 = []
	#for i in range(0, dataHeight):
	    #BIL = []        	
	    ##BIL1 = {}
	    #band = self.ds.GetRasterBand(3)                     
	    #bandNum = band.ReadAsArray(0,i,dataWidth,1 )          
	    #BIL = bandNum[0].tolist()
	    #totalBIL3.append(BIL)    

	#BILmax3 = numpy.max(totalBIL3)
	#BILmin3= numpy.min(totalBIL3)
	#BILregion3 = BILmax3 - BILmin3	
	
	datas = []  
	if px>0 and py>0:
	    extent = [oringeX, oringeX + px*dataWidth, oringeY, oringeY + py*dataHeight]
	elif px>0 and py<0:
	    extent = [oringeX, oringeX + px*dataWidth, oringeY + py*dataHeight, oringeY]
	elif px<0 and py<0:
	    extent = [oringeX + px*dataWidth,oringeX,  oringeY + py*dataHeight, oringeY]	
	else:
	    extent = [oringeX + px*dataWidth,oringeX, oringeY ,  oringeY + py*dataHeight]		    
	#print extent
	
	self.SetExtent(extent)
	print extent
	print "ratio :%f" %self.ratio
	#a = numpy.asanyarray(totalBIL1, dtype=numpy.uint8 )   
	#b = numpy.asanyarray(totalBIL2, dtype=numpy.uint8 )  
	#c = numpy.asanyarray(totalBIL3, dtype=numpy.uint8 )  
	#datas.append(a)
	#datas.append(b)
	#datas.append(c)
	
	#datas = numpy.flipud(datas)
	#datas.append(numpy.reshape(a,(1,-1))) 
	#numpy.flipud(Data).tostring()
	
	image=wx.EmptyImage(self.size.width+1,self.size.height+1)   
	
	print dataWidth, dataHeight
	
	#image.Create(self.size.width , self.size.height)
	#imgdata =  image.GetDataBuffer()
	#image.set
	#print imgdata[1]
	#rint datas[0][0]
	for hang in range(0, dataWidth-1 , 1):
	    #start1 = time.time()
	    for lie in range(0, dataHeight-1 , 1):
		#start1 = time.time()
		value1 = totalBIL1[lie][hang]
		value1 = float((value1 - BILmin1))/BILregion1*255
		print value1
		#end1 =time.time()
		#print "calc value %d" %(end1-start1)
		#print float(value1) - BILmin
		#print float((value1 - BILmin))/BILregion
		#print value1
		#value2 = totalBIL2[row][col]
		#value3 = totalBIL3[row][col]
		#color = wx.Colour(value1  , value1 , value1)

		#x = (oringeX + col*px -extent[0]/2-extent[1]/2)*self.ratio + self.size.width/2
		#y = self.size.height/2 - (oringeY + row*py - extent[2]/2 - extent[3]/2)*self.ratio 
		
		#start2 = time.time()
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
