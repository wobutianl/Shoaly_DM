#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx

class DrawLineDemo(wx.Frame):
    def __init__(self, parent, title = 'draw a simple line demon'):
        super(DrawLineDemo, self).__init__(parent, title = title, size = (250, 150) )
        self.d = {}
        self.panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)
        button1 = wx.Button(self.panel, -1, "foo")
        box.Add(button1, 0, wx.ALL, 10)
        button2 = wx.Button(self.panel, -1, "bar")
        box.Add(button2, 0, wx.ALL, 10)    
        
        button1.Bind(wx.EVT_LEFT_DOWN, self.MouseDown)
        button2.Bind(wx.EVT_LEFT_DOWN, self.MouseDown)
        
        button1.Bind(wx.EVT_MOTION, self.MouseMove)
        button2.Bind(wx.EVT_MOTION, self.MouseMove)
        
        button1.Bind(wx.EVT_LEFT_UP, self.MouseUp)
        button2.Bind(wx.EVT_LEFT_UP, self.MouseUp)
        
        self.panel.Bind(wx.EVT_RIGHT_DOWN, self.panel_RD)
        self.panel.Bind(wx.EVT_RIGHT_UP, self.panel_RU)
        self.Bind(wx.EVT_PAINT, self.__OnPaint)
        
        self.panel.SetSizer(box) 
        self.panel.Layout()         

        #wx.FutureCall(2000, self.__DrawLine)
        self.Centre()
        self.Show()
        
    
    def __OnPaint(self, event):
        self.__DrawLine()    
        
    #----------------------------------------------------------------------
    def panel_RD(self, e):
        """"""
        o           = e.GetEventObject()
        sx,sy       = self.panel.ScreenToClient(o.GetPositionTuple())
        self.dx1,self.dy1       = self.panel.ScreenToClient(wx.GetMousePosition())
        
    #----------------------------------------------------------------------
    def panel_RU(self):
        """"""
        o           = e.GetEventObject()
        sx,sy       = self.panel.ScreenToClient(o.GetPositionTuple())
        self.dx2,self.dy2       = self.panel.ScreenToClient(wx.GetMousePosition())
           
    
    def __DrawLine(self):
        dc = wx.ClientDC(self)       
        dc.DrawLine(self.dx1,self.dy1, self.dx2, self.dy2)
        
    def MouseDown(self, e):   
        o           = e.GetEventObject()
        sx,sy       = self.panel.ScreenToClient(o.GetPositionTuple())
        dx,dy       = self.panel.ScreenToClient(wx.GetMousePosition())
        o._x,o._y   = (sx-dx, sy-dy)
        self.d['d'] = o
        
    def MouseMove(self, e):
        try:
            if 'd' in self.d:
                o = self.d['d']
                x, y = wx.GetMousePosition()
                o.SetPosition(wx.Point(x+o._x,y+o._y))
        except: pass
    
    def MouseUp(self, e):
        try:
            if 'd' in self.d: 
                del self.d['d']
        except: 
            pass
            
if __name__ == '__main__':
    app = wx.App()
    DrawLineDemo(None)
    app.MainLoop()