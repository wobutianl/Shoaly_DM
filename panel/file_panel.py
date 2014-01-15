#-*- encoding:GBK -*-
import wx
import wx.lib.agw.ribbon as RB
from wx.lib.embeddedimage import PyEmbeddedImage
import os
import sys
import global_ID as ID

def CreateBitmap(xpm):
    bmp = eval(xpm).Bitmap
    return bmp

pic_new_module	= ID.ID_New__NAME[ID.ID_NEW_MODULE][1]        #ID.PIC_NEW_MODULE

pic_comp_module	= ID.ID_New__NAME[ID.ID_MODULE_COMP][1]        #ID.ID_MODULE_COMP	
pic_economy	= ID.ID_New__NAME[ID.ID_MODULE_ECONOMY][1]        #ID.ID_MODULE_ECONOMY	
pic_social	= ID.ID_New__NAME[ID.ID_MODULE_SOCIAL][1]        #ID.ID_MODULE_SOCIAL	
pic_environ	= ID.ID_New__NAME[ID.ID_MODULE_ENVIRON][1]        #ID.ID_MODULE_ENVIRON

pic_module_xml  = ID.PIC_MODULE_XML                 
                                                                         
pic_population_module          = ID.PIC_POPULATION_MODULE          
pic_density_module             = ID.PIC_DENSITY_MODULE    

ID_MAIN_TOOLBAR = 0002
ID_POSITION_LEFT = 0003
ID_POSITION_TOP = 0004
#----------------------------------------------------------------------
align_left = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAPCAYAAADtc08vAAAABHNCSVQICAgIfAhkiAAAADxJ"
    "REFUKJFjZGRiZqAEMFGkm4GBgYWBgYHh/7+//4lRzMjEzIghRqkX8LoAm430dQExLhoNg2ER"
    "BhRnJgDCqhhOM7rMkQAAAABJRU5ErkJggg==")
align_center = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAPCAYAAADtc08vAAAABHNCSVQICAgIfAhkiAAAADpJ"
    "REFUKJFjZGRiZqAEMFGkm4GBgQWZ8//f3//EaGJkYmaEsyn1Ags2QVwuQbaZNi4YDYMRGwYU"
    "ZyYAopsYTgbXQz4AAAAASUVORK5CYII=")
align_right = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAPCAYAAADtc08vAAAABHNCSVQICAgIfAhkiAAAADdJ"
    "REFUKJFjZGRiZqAEMFGkm4GBgQWb4P9/f/8To5mRiZmRkVIvYHUBsS6inQtGw2DEhQHFmQkA"
    "gowYTpdfxvkAAAAASUVORK5CYII=")
position_left = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAPCAYAAADtc08vAAAABHNCSVQICAgIfAhkiAAAAExJ"
    "REFUKJHtkzEKwDAMA0/yx/z/P7XqVOiQDmmHLDEIBEKCGyy5yHmEDyeXACIX3YlcPP2dvQkI"
    "QEblqYFRuTuZGtgIG2EpguR/33gBsoRzDlCsBR0AAAAASUVORK5CYII=")
position_top = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAPCAYAAADtc08vAAAABHNCSVQICAgIfAhkiAAAAFJJ"
    "REFUKJHtkzEKwDAMA092H5b//ylRppRCpzhToTd50RljJEXi0U0BRQrAiqQ1W5HszIABXAkr"
    "kltQCb8E3z1By1Llev5zF4/uONkO8AtAp22caOhgKT6Nla4AAAAASUVORK5CYII=")
#----------------------------------------------------------------------
class file_tool_Panel(RB.RibbonPanel):
    """"""
    #----------------------------------------------------------------------
    def __init__(self , parent):
	"""Constructor"""
	RB.RibbonPanel.__init__(self,parent,wx.ID_ANY , u"基本操作" )
	toolbar_panel = RB.RibbonPanel(self )
		
	toolbar = RB.RibbonToolBar(toolbar_panel, ID_MAIN_TOOLBAR)
	toolbar.AddTool(wx.ID_ANY, CreateBitmap("align_left"))
	toolbar.AddTool(wx.ID_ANY, CreateBitmap("align_center"))
	toolbar.AddTool(wx.ID_ANY, CreateBitmap("align_right"))
	toolbar.AddSeparator()
	toolbar.AddHybridTool(wx.ID_NEW, wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_OTHER, wx.Size(16, 15)))
	toolbar.AddTool(wx.ID_ANY, wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, wx.Size(16, 15)))
	toolbar.AddTool(wx.ID_ANY, wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_OTHER, wx.Size(16, 15)))
	toolbar.AddTool(wx.ID_ANY, wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE_AS, wx.ART_OTHER, wx.Size(16, 15)))
	toolbar.AddSeparator()
	toolbar.AddDropdownTool(wx.ID_UNDO, wx.ArtProvider.GetBitmap(wx.ART_UNDO, wx.ART_OTHER, wx.Size(16, 15)))
	toolbar.AddDropdownTool(wx.ID_REDO, wx.ArtProvider.GetBitmap(wx.ART_REDO, wx.ART_OTHER, wx.Size(16, 15)))
	toolbar.AddSeparator()
	toolbar.AddTool(wx.ID_ANY, wx.ArtProvider.GetBitmap(wx.ART_REPORT_VIEW, wx.ART_OTHER, wx.Size(16, 15)))
	toolbar.AddTool(wx.ID_ANY, wx.ArtProvider.GetBitmap(wx.ART_LIST_VIEW, wx.ART_OTHER, wx.Size(16, 15)))
	toolbar.AddSeparator()
	toolbar.AddHybridTool(ID_POSITION_LEFT, CreateBitmap("position_left"), "Align ribbonbar vertically\non the left\nfor demonstration purposes")
	toolbar.AddHybridTool(ID_POSITION_TOP, CreateBitmap("position_top"), "Align the ribbonbar horizontally\nat the top\nfor demonstration purposes")
	toolbar.AddSeparator()
	toolbar.AddHybridTool(wx.ID_PRINT, wx.ArtProvider.GetBitmap(wx.ART_PRINT, wx.ART_OTHER, wx.Size(16, 15)),
		                      "This is the Print button tooltip\ndemonstrating a tooltip")
	toolbar.SetRows(2, 3)

class file_module_Panel(RB.RibbonPanel):
    def __init__(self, parent):
        RB.RibbonPanel.__init__(self,parent,wx.ID_ANY , label = u"基本模型操作")
	file_module_BtnBar = RB.RibbonButtonBar(self )
	#file_module_BtnBar.AddSimpleButton(ID.ID_NEW_MODULE  , u"新建模型", CreateBitmap("pic_new_module"), "")
	file_module_BtnBar.AddSimpleButton(ID.ID_NEW_MODULE  , ID.ID_New__NAME[ID.ID_NEW_MODULE][0], CreateBitmap("pic_new_module"), "")
	file_module_BtnBar.AddSimpleButton(ID.ID_MODULE_XML , u"模型描述", CreateBitmap("pic_module_xml"), "")
		
	# bind event 
	file_module_BtnBar.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.New_Module, id=ID.ID_NEW_MODULE)
	#file_module_BtnBar.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.New_Module, id=ID.ID_MODULE_XML)
    #----------------------------------------------------------------------
    def New_Module(self , event):
	"""打开shp文件"""
	print "new_module"
	#ID.ID_LIST.append(ID.ID_NEW_MODULE)
	

#######################################################################
class file_social_module_Panel(RB.RibbonPanel):
    """project panel parent is file ribbon page"""
    #----------------------------------------------------------------------
    def __init__(self, parent):
	"""Constructor"""
	RB.RibbonPanel.__init__(self,parent,wx.ID_ANY , label = u"社会经济模型")
	file_social_BtnBar = RB.RibbonButtonBar(self)
	file_social_BtnBar.AddSimpleButton(ID.ID_POPULATION_MODULE , u"人口空间分布", CreateBitmap("pic_population_module"), "")
	file_social_BtnBar.AddSimpleButton(ID.ID_DENSITY_MODULE , u"人口密度", CreateBitmap("pic_density_module"), "")
	
	# bind event 
	file_social_BtnBar.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.population, id=ID.ID_POPULATION_MODULE)
	file_social_BtnBar.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.density, id=ID.ID_DENSITY_MODULE)
    #----------------------------------------------------------------------
    def population(self , event):
	""" 人口模型"""
	print "population"
	ID.ID_LIST.append(ID.ID_POPULATION_MODULE)
	
    #----------------------------------------------------------------------
    def density(self , event):
	"""密度模型"""
	print "density module"
	ID.ID_LIST.append(ID.ID_DENSITY_MODULE)


#######################################################################
class file_comp_module_Panel(RB.RibbonPanel):
    """project panel parent is file ribbon page"""
    #----------------------------------------------------------------------
    def __init__(self, parent):
	"""Constructor"""
	RB.RibbonPanel.__init__(self,parent,wx.ID_ANY , label = u"综合评价模型")
	file_comp_BtnBar = RB.RibbonButtonBar(self)
	file_social_BtnBar.AddSimpleButton(ID.ID_MODULE_COMP , u"综合评价模型", CreateBitmap("pic_population_module"), "")
	file_social_BtnBar.AddSimpleButton(ID.ID_MODULE_ECONOMY , u"经济评价指标", CreateBitmap("pic_population_module"), "")
	file_social_BtnBar.AddSimpleButton(ID.ID_MODULE_SOCIAL , u"社会评价指标", CreateBitmap("pic_density_module"), "")
	file_social_BtnBar.AddSimpleButton(ID.ID_MODULE_ENVIRON , u"环境评价指标", CreateBitmap("pic_density_module"), "")
	
	# bind event 
	file_social_BtnBar.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.population, id=ID.ID_POPULATION_MODULE)
	file_social_BtnBar.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.density, id=ID.ID_DENSITY_MODULE)
    #----------------------------------------------------------------------
    def population(self , event):
	""" 人口模型"""
	print "population"
	ID.ID_LIST.append(ID.ID_POPULATION_MODULE)
	
    #----------------------------------------------------------------------
    def density(self , event):
	"""密度模型"""
	print "density module"
	ID.ID_LIST.append(ID.ID_DENSITY_MODULE)
	
# exit panel
########################################################################
class file_exit_Panel(RB.RibbonPanel):
    """project panel parent is file ribbon page"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
	"""Constructor"""
	RB.RibbonPanel.__init__(self,parent,wx.ID_ANY , label = u"退出")
	file_exit_BtnBar = RB.RibbonButtonBar(self)
	file_exit_BtnBar.AddSimpleButton(0001 , u"退出", wx.ART_OTHER, "")


	# bind event 
	file_exit_BtnBar.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnFileDo, id=0001)
	
    #----------------------------------------------------------------------
    def OnFileDo(self , event):
	"""打开shp文件"""
	self.Close()
	#ID.ID_FIEL_LIST.append(ID.ID_FILE_SHP)
    
    

        
        