# -*- coding: utf-8 -*-
# 11/20/2003 - Jeff Grimmett (grimmtooth@softhome.net)
#
# o Updated for wx namespace
# 
# 20040508 - Pierre Hjälm
#
# o Changed to use the python version of OGL
# o Added TextShape, CompositeShape and CompositeShape with divisions
#
# 20040830 - Pierre Hjälm
#
# o Added DrawnShape
#

import wx
import logging
import wx.lib.ogl as ogl
import global_ID as ID

import images


########################################################
pic_new_module		=	ID.PIC_NEW_MODULE		
pic_module_xml		=	ID.PIC_MODULE_XML
pic_population_module	=	ID.PIC_POPULATION_MODULE
pic_density_module	=	ID.PIC_DENSITY_MODULE

pic_db_link		=	ID.PIC_DB_LINK
pic_db_vector		=	ID.PIC_DB_VECTOR
pic_db_raster		=	ID.PIC_DB_RASTER
pic_db_statistic	=	ID.PIC_DB_STATISTIC
pic_db_metadb		=	ID.PIC_DB_METADB
pic_db_maindb		=	ID.PIC_DB_MAINDB
			
pic_search_time_sp	=	ID.PIC_SEARCH_TIME_SP
pic_search_time_attri	=	ID.PIC_SEARCH_TIME_ATTRI

pic_shp_area		=	ID.PIC_SHP_AREA
pic_shp_length		=	ID.PIC_SHP_LENGTH
pic_shp_extent		=	ID.PIC_SHP_EXTENT
pic_shp_center		=	ID.PIC_SHP_CENTER
pic_shp_point		=	ID.PIC_SHP_POINT
pic_shp_out		=	ID.PIC_SHP_OUT
pic_shp_buffer		=	ID.PIC_SHP_BUFFER
pic_shp_simple		=	ID.PIC_SHP_SIMPLE
pic_shp_intersect	=	ID.PIC_SHP_INTERSECT
pic_shp_difference	=	ID.PIC_SHP_DIFFERENCE
pic_shp_union		=	ID.PIC_SHP_UNION

pic_raster_move		=	ID.PIC_RASTER_MOVE
pic_raster_rotate	=	ID.PIC_RASTER_ROTATE
pic_raster_zoom		=	ID.PIC_RASTER_ZOOM
pic_raster_cut		=	ID.PIC_RASTER_CUT
pic_raster_roi		=	ID.PIC_RASTER_ROI
pic_raster_union	=	ID.PIC_RASTER_UNION
pic_raster_reverse	=	ID.PIC_RASTER_REVERSE
pic_raster_balance	=	ID.PIC_RASTER_BALANCE
pic_raster_slop		=	ID.PIC_RASTER_SLOP
pic_raster_sharp	=	ID.PIC_RASTER_SHARP
pic_raster_color	=	ID.PIC_RASTER_COLOR

pic_static_abs		=	ID.PIC_STATIC_ABS
pic_static_average	=	ID.PIC_STATIC_AVERAGE
pic_static_concatenate	=	ID.PIC_STATIC_CONCATENATE
pic_static_density	=	ID.PIC_STATIC_DENSITY	
			
pic_static_frequency	=	ID.PIC_STATIC_FREQUENCY
pic_static_max		=	ID.PIC_STATIC_MAX	
pic_static_min		=	ID.PIC_STATIC_MIN	
pic_static_mod		=	ID.PIC_STATIC_MOD

pic_static_rank		=	ID.PIC_STATIC_RANK
pic_static_subtotal	=	ID.PIC_STATIC_SUBTOTAL
pic_static_sum		=	ID.PIC_STATIC_SUM	
pic_static_stdev	=	ID.PIC_STATIC_STDEV
			
pic_show_pie		=	ID.PIC_SHOW_PIE
pic_show_histgram	=	ID.PIC_SHOW_HISTGRAM
pic_show_radia		=	ID.PIC_SHOW_RADIA
pic_show_qqplot		=	ID.PIC_SHOW_QQPLOT
pic_show_scarte		=	ID.PIC_SHOW_SCARTE
pic_show_bar		=	ID.PIC_SHOW_BAR
pic_show_line		=	ID.PIC_SHOW_LINE

pic_sshow_pie		=	ID.PIC_SSHOW_PIE
pic_sshow_bar		=	ID.PIC_SSHOW_BAR
pic_sshow_classify	=	ID.PIC_SSHOW_CLASSIFY
##########################################


def CreateBitmap(xpm):
    bmp = eval(xpm).Bitmap
    return bmp

#----------------------------------------------------------------------
def drawCircle(diameter):
    """draw circle"""
    circle_shape = ogl.CircleShape(diameter)
    return circle_shape

#----------------------------------------------------------------------
def draw_bmp(bmp_file):  ##  bmp_file == base64 file   没办法改变大小。。。需要重新定义图片。
    """"""
    #bmp = images.getTest2Bitmap()
    bmp = CreateBitmap(bmp_file)
    mask = wx.Mask(bmp, wx.BLUE)
    bmp.SetMask(mask)

    bmp_shape = ogl.BitmapShape()
    bmp_shape.SetBitmap(bmp)
    return bmp_shape
    #self.MyAddShape(s, 225, 130, None, None, "Bitmap")

    #dc = wx.ClientDC(self)
    #self.PrepareDC(dc)  
    
#----------------------------------------------------------------------
class DrawnShape(ogl.DrawnShape):
    def __init__(self):
        ogl.DrawnShape.__init__(self)

        self.SetDrawnBrush(wx.WHITE_BRUSH)
        self.SetDrawnPen(wx.BLACK_PEN)
        self.DrawArc((0, -10), (30, 0), (-30, 0))

        self.SetDrawnPen(wx.Pen("#ff8030"))
        self.DrawLine((-30, 5), (30, 5))

        self.SetDrawnPen(wx.Pen("#00ee10"))
        self.DrawRoundedRectangle((-20, 10, 40, 10), 5)

        self.SetDrawnPen(wx.Pen("#9090f0"))
        self.DrawEllipse((-30, 25, 60, 20))

        self.SetDrawnTextColour(wx.BLACK)
        self.SetDrawnFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.DrawText("DrawText", (-26, 28))

        self.SetDrawnBrush(wx.GREEN_BRUSH)
        self.DrawPolygon([(-100, 5), (-45, 30), (-35, 20), (-30, 5)])

        self.SetDrawnPen(wx.BLACK_PEN)
        self.DrawLines([(30, -45), (40, -45), (40 ,45), (30, 45)])

        # Make sure to call CalculateSize when all drawing is done
        self.CalculateSize()
          
#----------------------------------------------------------------------
class DiamondShape(ogl.PolygonShape):
    def __init__(self, w=0.0, h=0.0):
        ogl.PolygonShape.__init__(self)
        if w == 0.0:
            w = 60.0
        if h == 0.0:
            h = 60.0

        points = [ (0.0,    -h/2.0),
                   (w/2.0,  0.0),
                   (0.0,    h/2.0),
                   (-w/2.0, 0.0),
                   ]

        self.Create(points)


#----------------------------------------------------------------------

class RoundedRectangleShape(ogl.RectangleShape):
    def __init__(self, w=0.0, h=0.0):
        ogl.RectangleShape.__init__(self, w, h)
        self.SetCornerRadius(-0.3)


#----------------------------------------------------------------------

class CompositeDivisionShape(ogl.CompositeShape):
    def __init__(self, canvas):
        ogl.CompositeShape.__init__(self)

        self.SetCanvas(canvas)

        # create a division in the composite
        self.MakeContainer()

        # add a shape to the original division
        shape2 = ogl.RectangleShape(40, 60)
        self.GetDivisions()[0].AddChild(shape2)

        # now divide the division so we get 2
        self.GetDivisions()[0].Divide(wx.HORIZONTAL)

        # and add a shape to the second division (and move it to the
        # centre of the division)
        shape3 = ogl.CircleShape(40)
        shape3.SetBrush(wx.CYAN_BRUSH)
        self.GetDivisions()[1].AddChild(shape3)
        shape3.SetX(self.GetDivisions()[1].GetX())

        for division in self.GetDivisions():
            division.SetSensitivityFilter(0)
        
#----------------------------------------------------------------------

class CompositeShape(ogl.CompositeShape):
    def __init__(self, canvas):
        ogl.CompositeShape.__init__(self)

        self.SetCanvas(canvas)

        constraining_shape = ogl.RectangleShape(120, 100)
        constrained_shape1 = ogl.CircleShape(50)
        constrained_shape2 = ogl.RectangleShape(80, 20)

        constraining_shape.SetBrush(wx.BLUE_BRUSH)
        constrained_shape2.SetBrush(wx.RED_BRUSH)
        
        self.AddChild(constraining_shape)
        self.AddChild(constrained_shape1)
        self.AddChild(constrained_shape2)

        constraint = ogl.Constraint(ogl.CONSTRAINT_MIDALIGNED_BOTTOM, constraining_shape, [constrained_shape1, constrained_shape2])
        self.AddConstraint(constraint)
        self.Recompute()

        # If we don't do this, the shapes will be able to move on their
        # own, instead of moving the composite
        constraining_shape.SetDraggable(False)
        constrained_shape1.SetDraggable(False)
        constrained_shape2.SetDraggable(False)

        # If we don't do this the shape will take all left-clicks for itself
        constraining_shape.SetSensitivityFilter(0)

        
#----------------------------------------------------------------------

class DividedShape(ogl.DividedShape):
    def __init__(self, width, height, canvas):
        ogl.DividedShape.__init__(self, width, height)

        region1 = ogl.ShapeRegion()
        region1.SetText('DividedShape')
        region1.SetProportions(0.0, 0.2)
        region1.SetFormatMode(ogl.FORMAT_CENTRE_HORIZ)
        self.AddRegion(region1)

        region2 = ogl.ShapeRegion()
        region2.SetText('This is Region number two.')
        region2.SetProportions(0.0, 0.3)
        region2.SetFormatMode(ogl.FORMAT_CENTRE_HORIZ|ogl.FORMAT_CENTRE_VERT)
        self.AddRegion(region2)

        region3 = ogl.ShapeRegion()
        region3.SetText('Region 3\nwith embedded\nline breaks')
        region3.SetProportions(0.0, 0.5)
        region3.SetFormatMode(ogl.FORMAT_NONE)
        self.AddRegion(region3)

        self.SetRegionSizes()
        self.ReformatRegions(canvas)


    def ReformatRegions(self, canvas=None):
        rnum = 0

        if canvas is None:
            canvas = self.GetCanvas()

        dc = wx.ClientDC(canvas)  # used for measuring

        for region in self.GetRegions():
            text = region.GetText()
            self.FormatText(dc, text, rnum)
            rnum += 1


    def OnSizingEndDragLeft(self, pt, x, y, keys, attch):
        print "***", self
        ogl.DividedShape.OnSizingEndDragLeft(self, pt, x, y, keys, attch)
        self.SetRegionSizes()
        self.ReformatRegions()
        self.GetCanvas().Refresh()


#----------------------------------------------------------------------

class MyEvtHandler(ogl.ShapeEvtHandler):
    def __init__(self, log, frame):
        ogl.ShapeEvtHandler.__init__(self)
        self.log = log
        self.statbarFrame = frame
	self.flag = 0
	
    def UpdateStatusBar(self, shape):
        x, y = shape.GetX(), shape.GetY()
        width, height = shape.GetBoundingBoxMax()
        #self.statbarFrame.SetStatusText("Pos: (%d, %d)  Size: (%d, %d)" %
                                       # (x, y, width, height))


    def OnLeftClick(self, x, y, keys=0, attachment=0):
        shape = self.GetShape()
	print type(shape.GetId())
	num = shape.GetId()
	
        canvas = shape.GetCanvas()
        dc = wx.ClientDC(canvas)
        canvas.PrepareDC(dc)

        if shape.Selected():
            shape.Select(False, dc)
            #canvas.Redraw(dc)
            canvas.Refresh(False)
        else:
            redraw = False
            shapeList = canvas.GetDiagram().GetShapeList()
            toUnselect = []

            for s in shapeList:
                if s.Selected():
                    # If we unselect it now then some of the objects in
                    # shapeList will become invalid (the control points are
                    # shapes too!) and bad things will happen...
                    toUnselect.append(s)

            shape.Select(True, dc)

            if toUnselect:
                for s in toUnselect:
                    s.Select(False, dc)

                ##canvas.Redraw(dc)
                canvas.Refresh(False)

    def OnEndDragLeft(self, x, y, keys=0, attachment=0):
        shape = self.GetShape()
        ogl.ShapeEvtHandler.OnEndDragLeft(self, x, y, keys, attachment)

        if not shape.Selected():
            self.OnLeftClick(x, y, keys, attachment)
	
    def OnSizingEndDragLeft(self, pt, x, y, keys, attch):
        ogl.ShapeEvtHandler.OnSizingEndDragLeft(self, pt, x, y, keys, attch)
        #self.UpdateStatusBar(self.GetShape())


    def OnMovePost(self, dc, x, y, oldX, oldY, display):
        shape = self.GetShape()
        ogl.ShapeEvtHandler.OnMovePost(self, dc, x, y, oldX, oldY, display)
        #self.UpdateStatusBar(shape)
        if "wxMac" in wx.PlatformInfo:
            shape.GetCanvas().Refresh(False)

    
#----------------------------------------------------------------------

class TestWindow(ogl.ShapeCanvas):
    def __init__(self, parent, log, frame):
        ogl.ShapeCanvas.__init__(self, parent)

        maxWidth  = 1000
        maxHeight = 1000
        self.SetScrollbars(20, 20, maxWidth/20, maxHeight/20)
        ogl.OGLInitialize()
        self.log = log
        self.frame = frame
        self.SetBackgroundColour("LIGHT BLUE") #wx.WHITE)
        # 1 create a diagram
        self.diagram = ogl.Diagram()
        self.SetDiagram(self.diagram)
        # 2 set canvas in diagram
        self.diagram.SetCanvas(self)
        self.shapes = []
        self.save_gdi = []
	
	self.flag = 0
	
        rRectBrush = wx.Brush("MEDIUM TURQUOISE", wx.SOLID)
        dsBrush = wx.Brush("WHEAT", wx.SOLID)

    #----------------------------------------------------------------------
    def drawConLine(self, fromShape, toShape):
	""""""   
	line = ogl.LineShape()
	line.SetCanvas(self)
	line.SetPen(wx.BLACK_PEN)
	line.SetBrush(wx.BLACK_BRUSH)
	line.AddArrow(ogl.ARROW_ARROW)
	line.MakeLineControlPoints(2)
	fromShape.AddLine(line, toShape)
	self.diagram.AddShape(line)
	line.Show(True)

    def MyAddShape(self, shape, x, y, pen, brush, text, ID ):
        # Composites have to be moved for all children to get in place
        if isinstance(shape, ogl.CompositeShape):
            dc = wx.ClientDC(self)
            self.PrepareDC(dc)
            shape.Move(dc, x, y)
        else:
            shape.SetDraggable(True, True)
        shape.SetCanvas(self)
	#shape.AddConstraint(ID_NAME)
        shape.SetX(x)
        shape.SetY(y)
	if ID :    shape.SetId(ID)
        if pen:    shape.SetPen(pen)
        if brush:  shape.SetBrush(brush)
        if text:
            for line in text.split('\n'):
                shape.AddText(line)
        self.diagram.AddShape(shape)
        shape.Show(True)

        evthandler = MyEvtHandler(self.log, self.frame)
        evthandler.SetShape(shape)
        evthandler.SetPreviousHandler(shape.GetEventHandler())
        shape.SetEventHandler(evthandler)

        self.shapes.append(shape)
        return shape


import wx.aui
import os
import sys
from wx.lib.embeddedimage import PyEmbeddedImage
try:
    from agw import ribbon as RB
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.ribbon as RB
ribbon = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAYxJ"
    "REFUOI19krtKA0EUhr8xMcYbRIJgk87KBSsRBK0UROMi6y3Wig+wpLQTLMUHsLNSBEVCIoKd"
    "gpAyEBBMISKIiDeSmLhqxiLuZrPjeqrhXH6+c/4RoiWAX2iGKQHyR9vCryf43+D4zBLWtwTw"
    "FRJeAs0wpbEQ5+4Jql8BIl1tTu385EARCXqHB0bihIKwuxH+zdZY2xQIIRibWgSQbpEWL1Jf"
    "j+S5VH/ryQp6ssLOuvS5gItAM0w5ObtMb1eRd6ueS221O0JVq41wKKhQOAT5o21xerzHQ7GV"
    "SGeDwI630ge1mlTuoKzQHQ5RsRppPVkhtdVOTcJb+UNZ4U8XVlfmuX385LX0xUu5UStkM4oL"
    "ioAtAqDP6Vzff3N1mXHW9PYqH0kzTDk0bhDpCJE63AdgQk/wWr+s/JdAM0zZPzzt4E7oCQDO"
    "Uvu4826RJhsHR+O8Ww3Pbx6KynqDo/EmkiYbcxdpYlFBIZtRBgvZDLGoIHeR/pvAFrHVNcOU"
    "sWi9r+Cp+d7AHbYTHnElfgAFJbH0Sf7mkQAAAABJRU5ErkJggg==")
import images




def CreateBitmap(xpm):
    bmp = eval(xpm).Bitmap
    return bmp

class OGLFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        wx.Frame.__init__(self,size=(1047,650), *args, **kwds)

        
        self.mgr = wx.aui.AuiManager(self)
        
        self.SetTitle("OGL TEST")
        self.SetBackgroundColour(wx.Colour(8, 197, 248))
        
        self._ribbon = RB.RibbonBar(self, wx.ID_ANY)
        home = RB.RibbonPage(self._ribbon, wx.ID_ANY, "Examples", CreateBitmap("ribbon"))
        
        dir1 = wx.GenericDirCtrl(self, -1,  style=0)    
        
        log = logging.getLogger(r"C:\Users\jerryfive\Desktop\OGL.log")          
        self.canvas = TestWindow(self, log, self)
        
        panel = wx.Panel(self)
        self.mgr.AddPane(panel, wx.aui.AuiPaneInfo().Center().Layer(1))
        #self.mgr.AddPane(self._ribbon, wx.UP)       #BottomDockable(False).FloatingSize((150,250)).PinButton().Left().Layer(1).Position(1).CloseButton(True).GripperTop()
        self.mgr.AddPane(self._ribbon,wx.aui.AuiPaneInfo().Name(u"RibbonBar").
                                          MinSize((120,120)).TopDockable(True).Top())               
        self.mgr.AddPane(self.canvas, wx.aui.AuiPaneInfo().Name(u"模型").Center().Layer(1))
        self.mgr.AddPane(dir1, wx.aui.AuiPaneInfo().Name(u"目录").MaxSize((120,120)).Left())
        self.mgr.Update()
	
	self.flag = 0
        #dir1.Bind(wx.EVT_TREE_BEGIN_DRAG, self.OnBeginDrag)
	self.canvas.Bind(wx.EVT_RIGHT_DCLICK, self.OnRightMouseDClick)
	self.canvas.Bind(wx.EVT_RIGHT_DOWN, self.OnRightMouseDown)
	
    #----------------------------------------------------------------------
    def OnRightMouseDClick(self,event):
	"""get mouse point"""
	self.dx,self.dy  = self.canvas.ScreenToClient(wx.GetMousePosition())
	id_length = len(ID.ID_FIEL_LIST)
	if id_length == 1 :
	    id_num = ID.ID_FIEL_LIST[0]
	    self.canvas.MyAddShape(ogl.CircleShape(80), 
		    self.dx, self.dy, wx.Pen(wx.BLUE, 3), wx.GREEN_BRUSH, "Circle",id_num
		    )
	    self.canvas.Refresh()
	    ID.ID_FIEL_LIST.pop()
	elif id_length == 0 and id_length > 1:
	    pass
	#elif id_length > 1:
	    
	
    #----------------------------------------------------------------------
    def OnRightMouseDown(self, event):
	"""mouse down get from shape"""
	self.dx,self.dy  = self.canvas.ScreenToClient(wx.GetMousePosition())
	if self.flag == 0:
	    print "flag = 0"
	    self.from_shape = self.canvas.FindShape(self.dx,self.dy)
	    if self.from_shape[0] != None:		
		self.flag = 1
	elif self.flag == 1:
	    print "flag = 1"	
	    self.to_shape = self.canvas.FindShape(self.dx,self.dy)
	    if self.to_shape[0] != None:		
		self.canvas.drawConLine(self.from_shape[0], self.to_shape[0])
		self.canvas.Refresh()
		self.flag = 0
	pass

	    
if __name__ == "__main__":
    app = wx.PySimpleApp(False)
    wx.InitAllImageHandlers()
    ogl.OGLInitialize()
    frame = OGLFrame(None, -1, "")
    app.SetTopWindow(frame)
    frame.Show(True)
    app.MainLoop()