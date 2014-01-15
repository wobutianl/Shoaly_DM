#-*- encoding:GBK -*-
import wx

import os
import sys
import wx.aui
#sys.path.append(r"E:\Test\Paper\panel");

import file_panel
import shpAnalysis_panel
import showAnalysis_panel
import staticAnalysis_panel
import data_extract_panel
import help_panel
#import testAnalysis_panel
#import images
# self module
try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.append(os.path.split(dirName)[0])

##try:

#from agw import ribbon as RB
import wx.lib.agw.ribbon as RB
##except ImportError: # if it's not there locally, try the wxPython lib.
##    import wx.lib.agw.ribbon as RB

from wx.lib.embeddedimage import PyEmbeddedImage

# --------------------------------------------------- #
# Some constants for ribbon buttons
ID_CIRCLE = wx.ID_HIGHEST + 1
ID_PRIMARY_COLOUR = ID_CIRCLE + 8
ID_SECONDARY_COLOUR = ID_CIRCLE + 9
ID_DEFAULT_PROVIDER = ID_CIRCLE + 10
ID_AUI_PROVIDER = ID_CIRCLE + 11
ID_MSW_PROVIDER = ID_CIRCLE + 12
ID_TOGGLE_PANELS = ID_CIRCLE + 20

#----------------------------------------------------------------------
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

# --------------------------------------------------- #

def CreateBitmap(xpm):
    bmp = eval(xpm).Bitmap
    return bmp

# --------------------------------------------------- #
class ColourClientData(object):
    def __init__(self, name, colour):
        
        self._name = name
        self._colour = colour

    def GetName(self):
        return self._name

    def GetColour(self):
        return self._colour

# --------------------------------------------------- #
class RibbonFrame(RB.RibbonBar):

    def __init__(self, parent, id=wx.ID_ANY, title="Ribbon Demo" , pos=wx.DefaultPosition,
                 size=(800, 600), agwStyle=RB.RIBBON_BAR_DEFAULT_STYLE|RB.RIBBON_BAR_SHOW_PANEL_EXT_BUTTONS):
	RB.RibbonBar.__init__(self, parent, wx.ID_ANY, agwStyle=RB.RIBBON_BAR_DEFAULT_STYLE|RB.RIBBON_BAR_SHOW_PANEL_EXT_BUTTONS)
        self._bitmap_creation_dc = wx.MemoryDC()
        self._colour_data = wx.ColourData()
        
        
        ###################################--FILE PAGE----------------------
        file_ribbon = RB.RibbonPage(self, wx.ID_ANY, u"文件&模型", CreateBitmap("ribbon"))
	file_tool = file_panel.file_tool_Panel(file_ribbon)
	file_module = file_panel.file_module_Panel(file_ribbon)
	file_social = file_panel.file_social_module_Panel(file_ribbon)
	#file_exit = file_panel.file_exit_Panel(file_ribbon)
	
	#############################-数据抽取 page --------------------------------
	database = RB.RibbonPage(self, wx.ID_ANY, u"数据库", CreateBitmap("ribbon"))
	database_link = data_extract_panel.data_link_Panel(database)		
	database_insert = data_extract_panel.data_insert_Panel(database)		
	database_view = data_extract_panel.data_view_Panel(database)			
	database_search = data_extract_panel.data_search_Panel(database)	
	
	
	###############-###########-shp 数据分析 page -------------------------	
	shpAnalysis = RB.RibbonPage(self, wx.ID_ANY, u"空间数据操作", CreateBitmap("ribbon"))
	spatial_shp = shpAnalysis_panel.shp_Panel(shpAnalysis)
	spatial_raster = shpAnalysis_panel.raster_Panel(shpAnalysis)
	
	############################################----任务分析 page ------------------------------		
	static_panel = RB.RibbonPage(self, wx.ID_ANY, u"统计数据操作", CreateBitmap("ribbon"))
	testAnalysis_data_panel = staticAnalysis_panel.static_data_Panel(static_panel)	
	testAnalysis_display_panel = staticAnalysis_panel.static_view_Panel(static_panel)	
	testAnalysis_class_panel = staticAnalysis_panel.static_classify_Panel(static_panel)	
			
	##############################-栅格数据分析 page -------------------------
	show_panel = RB.RibbonPage(self, wx.ID_ANY, u"可视化操作", CreateBitmap("ribbon"))
	static_show = showAnalysis_panel.show_base_Panel(show_panel)
	spatial_show= showAnalysis_panel.show_advance_Panel(show_panel)	
	
		
	###############################---外观 page -----------------------------	
	scheme = RB.RibbonPage(self, wx.ID_ANY, u"外观", CreateBitmap("ribbon"))
	print "b"
	self._default_primary, self._default_secondary, self._default_tertiary = self.GetArtProvider().GetColourScheme(1, 1, 1)
		
	provider_panel = RB.RibbonPanel(scheme, wx.ID_ANY, u"配置", wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize,
                                        agwStyle=RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
	provider_bar = RB.RibbonButtonBar(provider_panel, wx.ID_ANY)
	provider_bar.AddSimpleButton(ID_DEFAULT_PROVIDER, u"默认配置",
                                     wx.ArtProvider.GetBitmap(wx.ART_QUESTION, wx.ART_OTHER, wx.Size(32, 32)), "")
	provider_bar.AddSimpleButton(ID_AUI_PROVIDER, u"AUI 配置", CreateBitmap("ribbon"), "")
	provider_bar.AddSimpleButton(ID_MSW_PROVIDER, u"MSW 配置", CreateBitmap("ribbon"), "")
	
	primary_panel = RB.RibbonPanel(scheme, wx.ID_ANY, u"主色", CreateBitmap("ribbon"))
	self._primary_gallery = self.PopulateColoursPanel(primary_panel, self._default_primary, ID_PRIMARY_COLOUR)

	secondary_panel = RB.RibbonPanel(scheme, wx.ID_ANY, u"次色", CreateBitmap("ribbon"))
	self._secondary_gallery = self.PopulateColoursPanel(secondary_panel, self._default_secondary, ID_SECONDARY_COLOUR)	
	
	###################################help page ######################
	help = RB.RibbonPage(self, wx.ID_ANY, u"帮助", CreateBitmap("ribbon"))
	help_pan = help_panel.help_Panel(help)
	#############################  end of pages #######################	

	
	self.Realize()
	self.BindEvents(provider_bar)
	
    def BindEvents(self, bars):

	provider_bar = bars       
        provider_bar.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnDefaultProvider, id=ID_DEFAULT_PROVIDER)
        provider_bar.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnAUIProvider, id=ID_AUI_PROVIDER)
        provider_bar.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnMSWProvider, id=ID_MSW_PROVIDER)

        self.Bind(RB.EVT_RIBBONGALLERY_HOVER_CHANGED, self.OnHoveredColourChange, id=ID_PRIMARY_COLOUR)
        self.Bind(RB.EVT_RIBBONGALLERY_HOVER_CHANGED, self.OnHoveredColourChange, id=ID_SECONDARY_COLOUR)
        self.Bind(RB.EVT_RIBBONGALLERY_SELECTED, self.OnPrimaryColourSelect, id=ID_PRIMARY_COLOUR)
        self.Bind(RB.EVT_RIBBONGALLERY_SELECTED, self.OnSecondaryColourSelect, id=ID_SECONDARY_COLOUR)
	
    def OnDefaultProvider(self, event):

        self.DismissExpandedPanel()
        self.SetArtProvider(RB.RibbonDefaultArtProvider())
	self.Realize()

    def OnAUIProvider(self, event):

        self.DismissExpandedPanel()
        self.SetArtProvider(RB.RibbonAUIArtProvider())
	self.Realize()

    def OnMSWProvider(self, event):

        self.DismissExpandedPanel()
        self.SetArtProvider(RB.RibbonMSWArtProvider())
	self.Realize()
		
    def GetGalleryColour(self, gallery, item, name=None):
	"""获取面板颜色"""
        data = gallery.GetItemClientData(item)    
        if name != None:
            name = data.GetName()          
        return data.GetColour(), name
    
    def OnHoveredColourChange(self, event):
	""" 颜色该变事件"""
        # Set the background of the gallery to the hovered colour, or back to the
        # default if there is no longer a hovered item.

        gallery = event.GetGallery()
        provider = gallery.GetArtProvider()

        if event.GetGalleryItem() != None:        
            if provider == self.GetArtProvider():
                provider = provider.Clone()
                gallery.SetArtProvider(provider)
            
            provider.SetColour(RB.RIBBON_ART_GALLERY_HOVER_BACKGROUND_COLOUR,
                               self.GetGalleryColour(event.GetGallery(), event.GetGalleryItem(), None)[0])       
        else:        
            if provider != self.GetArtProvider():            
                gallery.SetArtProvider(self.GetArtProvider())
                del provider
            
    def OnPrimaryColourSelect(self, event):
	"""  主色选择"""
        colour, name = self.GetGalleryColour(event.GetGallery(), event.GetGalleryItem(), "")
        #self.AddText("Colour %s selected as primary."%name)

        dummy, secondary, tertiary = self.GetArtProvider().GetColourScheme(None, 1, 1)
        self.GetArtProvider().SetColourScheme(colour, secondary, tertiary)
        self.ResetGalleryArtProviders()
        self.Refresh()
	
    def ResetGalleryArtProviders(self):
	""" 颜色集重置 """
        if self._primary_gallery.GetArtProvider() != self.GetArtProvider():
            self._primary_gallery.SetArtProvider(self.GetArtProvider())
        
        if self._secondary_gallery.GetArtProvider() != self.GetArtProvider():        
            self._secondary_gallery.SetArtProvider(self.GetArtProvider()) 
	    
    def OnSecondaryColourSelect(self, event):
	""" 次色 选择 """
        colour, name = self.GetGalleryColour(event.GetGallery(), event.GetGalleryItem(), "")
        #self.AddText("Colour %s selected as secondary."%name)
        
        primary, dummy, tertiary = self.GetArtProvider().GetColourScheme(1, None, 1)
        self.GetArtProvider().SetColourScheme(primary, colour, tertiary)
        self.ResetGalleryArtProviders()
        self.Refresh()
	
	
    def PopulateColoursPanel(self, panel, defc, gallery_id):
	"""颜色面板"""
        gallery = wx.FindWindowById(gallery_id, panel)
        
        if gallery:
            gallery.Clear()
        else:
            gallery = RB.RibbonGallery(panel, gallery_id)
            
        dc = self._bitmap_creation_dc
        def_item = self.AddColourToGallery(gallery, "Default", dc, defc)
        gallery.SetSelection(def_item)
        
        self.AddColourToGallery(gallery, "BLUE", dc)
        self.AddColourToGallery(gallery, "BLUE VIOLET", dc)
        self.AddColourToGallery(gallery, "BROWN", dc)
        self.AddColourToGallery(gallery, "CADET BLUE", dc)
        self.AddColourToGallery(gallery, "CORAL", dc)
        self.AddColourToGallery(gallery, "CYAN", dc)
        self.AddColourToGallery(gallery, "DARK GREEN", dc)
        self.AddColourToGallery(gallery, "DARK ORCHID", dc)
        self.AddColourToGallery(gallery, "FIREBRICK", dc)
        self.AddColourToGallery(gallery, "GOLD", dc)
        self.AddColourToGallery(gallery, "GOLDENROD", dc)
        self.AddColourToGallery(gallery, "GREEN", dc)
        self.AddColourToGallery(gallery, "INDIAN RED", dc)
        self.AddColourToGallery(gallery, "KHAKI", dc)
        self.AddColourToGallery(gallery, "LIGHT BLUE", dc)
        self.AddColourToGallery(gallery, "LIME GREEN", dc)
        self.AddColourToGallery(gallery, "MAGENTA", dc)
        self.AddColourToGallery(gallery, "MAROON", dc)
        self.AddColourToGallery(gallery, "NAVY", dc)
        self.AddColourToGallery(gallery, "ORANGE", dc)
        self.AddColourToGallery(gallery, "ORCHID", dc)
        self.AddColourToGallery(gallery, "PINK", dc)
        self.AddColourToGallery(gallery, "PLUM", dc)
        self.AddColourToGallery(gallery, "PURPLE", dc)
        self.AddColourToGallery(gallery, "RED", dc)
        self.AddColourToGallery(gallery, "SALMON", dc)
        self.AddColourToGallery(gallery, "SEA GREEN", dc)
        self.AddColourToGallery(gallery, "SIENNA", dc)
        self.AddColourToGallery(gallery, "SKY BLUE", dc)
        self.AddColourToGallery(gallery, "TAN", dc)
        self.AddColourToGallery(gallery, "THISTLE", dc)
        self.AddColourToGallery(gallery, "TURQUOISE", dc)
        self.AddColourToGallery(gallery, "VIOLET", dc)
        self.AddColourToGallery(gallery, "VIOLET RED", dc)
        self.AddColourToGallery(gallery, "WHEAT", dc)
        self.AddColourToGallery(gallery, "WHITE", dc)
        self.AddColourToGallery(gallery, "YELLOW", dc)
        return gallery
	
    def AddColourToGallery(self, gallery, colour, dc, value=None):
        item = None
        if colour != "Default":
            c = wx.NamedColour(colour)         
        if value is not None:
            c = value      
        if c.IsOk():            
            iWidth = 64
            iHeight = 40
            bitmap = wx.EmptyBitmap(iWidth, iHeight)
            dc.SelectObject(bitmap)
            b = wx.Brush(c)
            dc.SetPen(wx.BLACK_PEN)
            dc.SetBrush(b)
            dc.DrawRectangle(0, 0, iWidth, iHeight)

            colour = colour[0] + colour[1:].lower()
            size = wx.Size(*dc.GetTextExtent(colour))
            notcred = min(abs(~c.Red()), 255)
            notcgreen = min(abs(~c.Green()), 255)
            notcblue = min(abs(~c.Blue()), 255)

            foreground = wx.Colour(notcred, notcgreen, notcblue)          
            if abs(foreground.Red() - c.Red()) + abs(foreground.Blue() - c.Blue()) + abs(foreground.Green() - c.Green()) < 64:
                # Foreground too similar to background - use a different
                # strategy to find a contrasting colour
                foreground = wx.Colour((c.Red() + 64) % 256, 255 - c.Green(),
                                       (c.Blue() + 192) % 256)           
            dc.SetTextForeground(foreground)
            dc.DrawText(colour, (iWidth - size.GetWidth() + 1) / 2, (iHeight - size.GetHeight()) / 2)
            dc.SelectObjectAsSource(wx.NullBitmap)

            item = gallery.Append(bitmap, wx.ID_ANY)
            gallery.SetItemClientData(item, ColourClientData(colour, c))       
        return item
    


class modulePopupMenu(wx.Menu):  
    def __init__(self,parent):  
        super(modulePopupMenu,self).__init__()  
        self.parent = parent  
	
	mark = wx.MenuItem(self,wx.NewId(),'Mark')  
	self.AppendItem(mark)  
	self.Bind(wx.EVT_MENU, self.OnMark, mark)           

	open = wx.MenuItem(self,wx.NewId(),'open')  
	self.AppendItem(open)  
	self.Bind(wx.EVT_MENU, self.OnOpen, open)   
	
        mmi = wx.MenuItem(self,wx.NewId(),'MiniSize')  
        self.AppendItem(mmi)  
        self.Bind(wx.EVT_MENU, self.OnMinimize, mmi)  
          
        cmi = wx.MenuItem(self,wx.NewId(),'Close')  
        self.AppendItem(cmi)  
        self.Bind(wx.EVT_MENU, self.OnClose, cmi)  
	
    def OnMark(self,e):  
        pass	
    def OnOpen(self,e):  
        print ID.ID_LIST           
    def OnMinimize(self,e):  
        self.parent.Iconize()  
    def OnClose(self,e):  
	print "close"
        self.parent.Close() 

import wx_matplot_panel
import GridSimple
import read_excel
import logging
import wxOGL_circle
import shp2mongoDB
import global_ID as ID
import global_func as func

import show_shapefile
import highlight_XML
import module_name

class TestPanel(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY, title="", pos=wx.DefaultPosition,
                 size=(1047,650), style=wx.DEFAULT_FRAME_STYLE, log=None):
        wx.Frame.__init__(self, parent, id, title, pos, size, style)
	self.flag = 0
	self.win = RibbonFrame(self, wx.ID_ANY)
	self.nb = wx.Notebook(self,-1,style= wx.NB_BOTTOM)
	self.dirCtrl = wx.GenericDirCtrl(self, -1, size=(200,225), style=wx.DIRCTRL_SHOW_FILTERS,
                                filter="All files (*.*)|*.*|Python files (*.py)|*.py|Shape files (*.shp)|*.shp|Excel files (*.xls)|*.xls")
	
	#self.excel = read_excel.readExcel()
	#self.excel_data = self.excel.getAllData(file_path)
    
	self.page_model = wx.Panel(self.nb,-1)
	#self.page_Grid = GridSimple.SimpleGrid(self.nb, log)
	#self.page_Spatial = wx_matplot_panel.wx_matplot_panel(self.nb)
	#self.page_Analysis = wx_matplot_panel.wx_matplot_panel(self.nb)
	
	self.nb.AddPage(self.page_model, u"模型")
	#self.nb.AddPage(self.page_Grid, u"表格")
	#self.nb.AddPage(self.page_Spatial, u"图示")
	#self.nb.AddPage(self.page_Analysis, u"分析图")

	self.mgr = wx.aui.AuiManager(self)
	self.SetTitle("OGL TEST")
	self.SetBackgroundColour(wx.Colour(8, 197, 248))

	self.log = logging.getLogger(r"C:\Users\jerryfive\Desktop\OGL.log")          
	self.canvas = wxOGL_circle.TestWindow(self, self.log, self)

	self.mgr.AddPane(self.nb, wx.aui.AuiPaneInfo().Center().Layer(1))
	self.mgr.AddPane(self.win,wx.aui.AuiPaneInfo().
                                          MinSize((120,125)).TopDockable(True).Top())               
	self.mgr.AddPane(self.canvas, wx.aui.AuiPaneInfo().Center().Layer(1))
	self.mgr.AddPane(self.dirCtrl, wx.aui.AuiPaneInfo().MaxSize((60,60)).Left())

	self.mgr.Update()	
	
	self.dirCtrl.Bind(wx.EVT_TREE_BEGIN_DRAG, self.OnBeginDrag)
	self.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging)
	#self.canvas.Bind(wx.EVT_RIGHT_DCLICK, self.OnRightMouseDClick)
	self.canvas.Bind(wx.EVT_RIGHT_DOWN, self.OnRightMouseDown)
	#self.canvas.Bind(wx.EVT_CONTEXT_MENU , self.OnContextMenu)

    #----------------------------------------------------------------------
    def OnRightMouseDown(self, event):
	"""mouse down get from shape"""
	self.popMenu()
 
	#self.PopupMenu(modulePopupMenu(self.canvas),event.GetPosition()) 
	
	#self.dx,self.dy  = self.canvas.ScreenToClient(wx.GetMousePosition())
	#if self.flag == 0:
	    #print "flag = 0"
	    #self.from_shape = self.canvas.FindShape(self.dx,self.dy)
	    #print "dx1,dy1 ", self.dx, self.dy
	    #print self.from_shape
	    #if self.from_shape[0] != None:		
		#self.flag = 1
	#elif self.flag == 1:
	    #print "flag = 1"
	    #self.to_shape = self.canvas.FindShape(self.dx,self.dy)
	    #if self.to_shape[0] != None:		
		#self.canvas.drawConLine(self.from_shape[0], self.to_shape[0])
		#self.canvas.Refresh()
		#self.flag = 0
	pass

    #----------------------------------------------------------------------
    def popMenu(self ):
	""""""
	popMenu = wx.Menu()
	
	mark = wx.MenuItem(popMenu,wx.NewId(),'Mark')  
	popMenu.AppendItem(mark)  
	self.canvas.Bind(wx.EVT_MENU, self.OnMark, mark)           

	draw = wx.MenuItem(popMenu,wx.NewId(),'draw')  
	popMenu.AppendItem(draw)  
	self.canvas.Bind(wx.EVT_MENU, self.OnDraw, draw)   
	
	open = wx.MenuItem(popMenu,wx.NewId(),'open')  
	popMenu.AppendItem(open)  
	self.canvas.Bind(wx.EVT_MENU, self.OnOpen, open)   
	
        mmi = wx.MenuItem(popMenu,wx.NewId(),'MiniSize')  
        popMenu.AppendItem(mmi)  
        self.canvas.Bind(wx.EVT_MENU, self.OnMinimize, mmi)  
          
	cmi = wx.MenuItem(popMenu,wx.NewId(),'Close')  
        popMenu.AppendItem(cmi)  	
        self.canvas.Bind(wx.EVT_MENU, self.OnClose, cmi)  
	
	self.canvas.PopupMenu(popMenu)
	
    def OnMark(self,event):  
	dx, dy  = self.canvas.ScreenToClient(wx.GetMousePosition())  #wx.GetMousePosition()
	if self.flag == 0:
	    print "flag = 0"
	    self.from_shape = self.canvas.FindShape(dx-20 ,dy-20)
	    print "dx, dy", dx, dy
	    print self.from_shape
	    if self.from_shape[0] != None:	
		print "mark"
		self.flag = 1
	elif self.flag == 1:
	    print "flag = 1"
	    self.to_shape = self.canvas.FindShape(dx-20,dy-20)
	    if self.to_shape[0] != None:		
		self.canvas.drawConLine(self.from_shape[0], self.to_shape[0])
		self.canvas.Refresh()
		self.flag = 0
	
    #----------------------------------------------------------------------
    #----------------------------------------------------------------------
    def OnDraw(self,event):
	"""get mouse point"""
	self.dx,self.dy  = self.canvas.ScreenToClient(wx.GetMousePosition())
	id_length = len(ID.ID_LIST)
	if id_length == 1 :

	    id_num = ID.ID_LIST[0]
	    #func.func_list[id_num]("abcd")
	    bmp_file = ID.ID_PIC[id_num]
	    self.canvas.MyAddShape(wxOGL_circle.draw_bmp(bmp_file), 
	            self.dx, self.dy, wx.Pen(wx.BLUE, 3), wx.GREEN_BRUSH, ID.ID_NAME[id_num] ,id_num
	            )
	    self.canvas.Refresh()
	    ID.ID_LIST.pop()
	    
	    #添加一个nb.page 显示xml描述
	    #ed = p = highlight_XML.PythonSTC(self, -1)
	    p = wx.Panel(self.nb, -1)
	    highlight_XML.text_panel(p) #file_path
		
	    self.nb.AddPage(p, u"模型XML")
	elif id_length == 0 :
	    pass
	elif id_length > 1:
	    try:
		for j in range(0, id_length):
		    ID.ID_LIST.pop(j)		
	    except:
		print "id.id_list error"
	
    def OnOpen(self,e):  
        print ID.ID_LIST           
    def OnMinimize(self,e):  
        self.Iconize()  
    def OnClose(self,e):  
	print "close"
        self.parent.Close() 

    def OnPageChanging(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
	self.sel = self.nb.GetSelection()
	if self.sel == 1:
	    print "new"
	size = self.GetClientSize()
	#self.model_panel = wx_matplot_panel(self.page_Analysis,size)
	print size
        print "changing"
        event.Skip()
	


    #----------------------------------------------------------------------
    def OnBeginDrag(self,event):
	"""拖拽treectrl事件"""
	item = event.GetItem()
	self.path2 =  self.dirCtrl.GetPath()
	#获取扩展名
	read_shp = shp2mongoDB.shp2mongodb(self.path2)
	ds = read_shp.getDS()
	fileName = os.path.basename(self.path2)
	extent_name = self.path2.split('.')[-1]
	file_name = fileName.split(".")[0]
	if ("shp" == extent_name) or ("SHP" == extent_name) or ("Shp" == extent_name):
	    
	    attri_data = read_shp.getAttributeData(ds)	    
	    attri_frame = GridSimple.SimpleGrid(self.nb, self.log)
	    attri_frame.make_cell(attri_data)
	    self.nb.AddPage(attri_frame , u"属性表")
	    
	    #geomType = self.page_Spatial.getShpType(self.path2)
	    #print geomType
	    self.newPage = show_shapefile.sketchWindow(self.nb, wx.ID_ANY)    #wx_matplot_panel.wx_matplot_panel(self.nb)
	    self.nb.AddPage(self.newPage,file_name)
	    self.newPage.addLayer(self.path2, wx.Pen("black",2,wx.SOLID),wx.Brush('blue'))
		
	elif "xls" == extent_name:
	    excel_data = self.excel.getAllData(self.path2)
	    grid_frame = GridSimple.SimpleGrid(self.nb, self.log)
	    grid_frame.make_cell(excel_data)
	    self.nb.AddPage(grid_frame , u"excel")
	    
#----------------------------------------------------------------------

#overview = RB.__doc__

if __name__ == '__main__':
    class MyApp(wx.App):
        def OnInit(self):
            wx.InitAllImageHandlers()
            frame = TestPanel(None)    
            frame.Show(True)
            #self.SetTopWindow(frame)
            return True
	
    app = MyApp(False)
    app.MainLoop()
