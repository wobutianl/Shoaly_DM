# -*- coding: utf-8 -*-
#from __future__ import print_function

# Used to guarantee to use at least Wx2.8
import wxversion
#wxversion.ensureMinimal('2.8')

import sys, time, os, gc
import matplotlib
matplotlib.use('WXAgg')
import matplotlib.cm as cm
import matplotlib.cbook as cbook
from matplotlib.backends.backend_wxagg import Toolbar, FigureCanvasWxAgg
from matplotlib.figure import Figure
import numpy as np

import wx
import wx.xrc as xrc

from matplotlib import pyplot
import ogr
from shapely.wkb import loads
from figures import SIZE, BLUE, GRAY

#import shape_BLL.shapely_point
ERR_TOL = 1e-5 # floating point slop for peak-detection


matplotlib.rc('image', origin='lower')
import shape_BLL.shapely_point
import shape_BLL.shapely_linestring
import shape_BLL.shapely_polygon
    
class p1(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent, -1,size=(400,400))
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.figure = matplotlib.figure.Figure(figsize=(5,4))
        self.axes = self.figure.add_subplot(111)
        
        #self.canvas = FigureCanvasWxAgg(self, -1, self.figure)
            
        
        self.y_max = 10
        self.canvas = FigureCanvasWxAgg(self,-1,self.figure)
        self.canvas.SetBackgroundColour("Red")        
        self.toolbar = Toolbar(self.canvas) #matplotlib toolbar
        self.toolbar.Realize()         
        self.plotButton = wx.Button(self,001,"Plot")
        
        self.clearButton = wx.Button(self,002,"Clear")
        self.Bind(wx.EVT_BUTTON, self.plot, id=001 )
        self.Bind(wx.EVT_BUTTON, self.clear, id = 002)
        
        self.sizer.Add(self.canvas,proportion =1, border = 5,flag = wx.ALL | wx.EXPAND)
        self.sizer.Add(self.plotButton,proportion = 0, border =2,flag = wx.ALL)
        self.sizer.Add(self.clearButton,proportion = 0, border =2,flag = wx.ALL)
        self.sizer.Add(self.toolbar,0,wx.EXPAND)
        self.SetSizer(self.sizer)
        #self.Fit()
        
    def plot(self,evt , file_path , file_type ):
        if file_type == None:
            print "error"
        elif file_type == "POINT":
            self.plotShpPointByFile(self.axes, file_path)
        self.canvas.draw()
   
    #----------------------------------------------------------------------
    def getShpType(self,file_path):
        """"""
        source = ogr.Open(file_path)       
        layer = source.GetLayerByIndex(0)    
        feature = layer.GetNextFeature()
        geom = feature.GetGeometryRef()
        geom_type = geom.GetGeometryName()  
        return geom_type
        
    #----------------------------------------------------------------------
    def plotShpPointByFile(self, file_path):
        """"""
        shape_BLL.shapely_point.plotShpByFile(self.axes, file_path)
        
        self.axes.set_title('a) valid')     
        self.canvas.draw()
        pass
    #----------------------------------------------------------------------
    def plotShpLineByFile(self,file_path,color = "black",linewidth=1):
        """"""
        shape_BLL.shapely_linestring.plotShapeByFile(self.axes, file_path)
        
        self.axes.set_title('a) valid')     
        self.canvas.draw()        
        pass
    #----------------------------------------------------------------------
    def plotShpPolygonByFile(self,file_path):
        """"""
        shape_BLL.shapely_polygon.plotShpByFile(self.axes, file_path, 
                                               )
        
        self.axes.set_title('a) valid')     
        self.canvas.draw()           
        pass
        
    def clear(self,evt):
        self.figure.set_canvas(self.canvas)
        self.axes.clear()
        self.canvas.draw()    
        

class TestFrame(wx.Frame):
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,title = title,size=(800,400))
 
        self.sp = wx.SplitterWindow(self)
        
        self.p1 = p1(self.sp)  #wx.Panel(self.sp,style = wx.SUNKEN_BORDER)
        self.dir3 = wx.GenericDirCtrl(self.sp, -1 , style=wx.DIRCTRL_SHOW_FILTERS,
                                filter="All files (*.*)|*.*|Python files (*.py)|*.py")
        
        self.sp.SplitVertically(self.p1,self.dir3,400)
 
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText("Hello")
        
        self.dir3.Bind(wx.EVT_TREE_BEGIN_DRAG, self.OnBeginDrag)
        
        
    #----------------------------------------------------------------------
    def OnBeginDrag(self,event):
        """拖拽treectrl事件"""
        item = event.GetItem()
        self.path2 =  self.dir3.GetPath()
        geomType = self.p1.getShpType(self.path2)
        if "POINT" == geomType:
            self.p1.plotShpPointByFile(self.path2)
        elif "LINGSTRING" == geomType:
            self.p1.plotShpLineByFile(self.path2)
        elif "POLYGON" == geomType:
            self.p1.plotShpPolygonByFile(self.path2)
        else:
            print "error"

 
app = wx.App(redirect = False)
frame = TestFrame(None,"Scientific Visualization")
frame.Show()
app.MainLoop()

