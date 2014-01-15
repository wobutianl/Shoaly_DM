# -*- coding: utf-8 -*-
#from __future__ import print_function
# Used to guarantee to use at least Wx2.8
import wxversion
#wxversion.ensureMinimal('2.8')

import matplotlib
matplotlib.use('WXAgg')
import matplotlib.cm as cm
import matplotlib.cbook as cbook
from matplotlib.backends.backend_wxagg import Toolbar, FigureCanvasWxAgg
from matplotlib.figure import Figure
import numpy as np

import wx
import ogr
import wx.xrc as xrc
ERR_TOL = 1e-5 # floating point slop for peak-detection


matplotlib.rc('image', origin='lower')

import shape_BLL.shapely_point
import shape_BLL.shapely_linestring
import shape_BLL.shapely_polygon
    
class wx_matplot_panel(wx.Panel):
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
   
        self.sizer.Add(self.canvas,proportion =1, border = 5,flag = wx.ALL | wx.EXPAND)
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
    def plotShpMultiLineByFile(self,file_path,color = "black",linewidth=1):
        """"""
        shape_BLL.shapely_linestring.plotMultiLineShapeByFile(self.axes, file_path)
        
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
        
        
class wx_matplot_panel2(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent, -1,size=(300,400))
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.figure = matplotlib.figure.Figure(figsize=(5,4))
        self.axes = self.figure.add_subplot(111)
        self.y_max = 10
        self.canvas = FigureCanvasWxAgg(self,-1,self.figure)
        self.plotButton = wx.Button(self,001,"Plot")
        
        self.clearButton = wx.Button(self,002,"Clear")
        self.Bind(wx.EVT_BUTTON, self.plot, id=001 )
        self.Bind(wx.EVT_BUTTON, self.clear, id = 002)
        
        self.sizer.Add(self.canvas,proportion =1, border = 5,flag = wx.ALL | wx.EXPAND)
        self.sizer.Add(self.plotButton,proportion = 0, border =2,flag = wx.ALL)
        self.sizer.Add(self.clearButton,proportion = 0, border =2,flag = wx.ALL)
 
        self.SetSizer(self.sizer)
        
    def plot(self,evt):
        t = np.arange(0.0,10.0,1.0)
        s = [0,1,0,1,0,2,1,2,1,0]
        self.axes.plot(t,s)
        self.canvas.draw()
        
    def clear(self,evt):
        self.figure.set_canvas(self.canvas)
        self.axes.clear()
        self.canvas.draw() 
        
        
class PlotPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        self.fig = Figure((5,4), 75)
        
        self.canvas = FigureCanvasWxAgg(self, -1, self.fig)
        self.canvas.SetBackgroundColour("Red")
        self.toolbar = Toolbar(self.canvas) #matplotlib toolbar
        self.toolbar.Realize()
        #self.toolbar.set_active(1)

        # Now put all into a sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        # This way of adding to sizer allows resizing
        sizer.Add(self.canvas,1,wx.EXPAND)
        #sizer.Add(self.canvas, 1, wx.LEFT|wx.TOP|wx.GROW)
        # Best to allow the toolbar to resize!
        sizer.Add(self.toolbar,0,wx.EXPAND)
        #sizer.Add(self.toolbar, 0, wx.GROW)
        self.SetSizer(sizer)
        self.Fit()

    def init_plot_data(self):
        a = self.fig.add_subplot(111)

        x = np.arange(120.0)*2*np.pi/60.0
        y = np.arange(100.0)*2*np.pi/50.0
        self.x, self.y = np.meshgrid(x, y)
        z = np.sin(self.x) + np.cos(self.y)
        self.im = a.imshow( z, cmap=cm.jet)#, interpolation='nearest')

        zmax = np.amax(z) - ERR_TOL
        ymax_i, xmax_i = np.nonzero(z >= zmax)
        if self.im.origin == 'upper':
            ymax_i = z.shape[0]-ymax_i
        self.lines = a.plot(xmax_i,ymax_i,'ko')

        self.toolbar.update() # Not sure why this is needed - ADS

    def GetToolBar(self):
        # You will need to override GetToolBar if you are using an
        # unmanaged toolbar in your frame
        return self.toolbar

    def OnWhiz(self,evt):
        self.x += np.pi/15
        self.y += np.pi/20
        z = np.sin(self.x) + np.cos(self.y)
        self.im.set_array(z)

        zmax = np.amax(z) - ERR_TOL
        ymax_i, xmax_i = np.nonzero(z >= zmax)
        if self.im.origin == 'upper':
            ymax_i = z.shape[0]-ymax_i
        self.lines[0].set_data(xmax_i,ymax_i)

        self.canvas.draw()

    def onEraseBackground(self, evt):
        # this is supposed to prevent redraw flicker on some X servers...
        pass
    
