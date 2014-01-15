#-*- encoding:utf-8 -*-
import wx
import wx.lib.agw.ribbon as RB
from wx.lib.embeddedimage import PyEmbeddedImage
import os
import sys
import global_ID as ID

# end of icon  ----
def CreateBitmap(xpm):
    bmp = eval(xpm).Bitmap
    return bmp

pic_show_pie                   = ID.PIC_SHOW_PIE                   
pic_show_histgram              = ID.PIC_SHOW_HISTGRAM              
pic_show_radia                 = ID.PIC_SHOW_RADIA                 
pic_show_qqplot                = ID.PIC_SHOW_QQPLOT                
pic_show_scarte                = ID.PIC_SHOW_SCARTE                
pic_show_bar                   = ID.PIC_SHOW_BAR                   
pic_show_line                  = ID.PIC_SHOW_LINE                  
                                                              
pic_sshow_pie                  = ID.PIC_SSHOW_PIE                  
pic_sshow_bar                  = ID.PIC_SSHOW_BAR                  
pic_sshow_classify             = ID.PIC_SSHOW_CLASSIFY   


#- end of ID code ---

class show_base_Panel(RB.RibbonPanel):
    def __init__(self, parent):
        RB.RibbonPanel.__init__(self,parent,wx.ID_ANY , label = u"统计分布图" )
	raster_base_Btn = RB.RibbonButtonBar(self )
	raster_base_Btn.AddSimpleButton(ID.ID_SHOW_PIE      ,    u"饼状图", CreateBitmap("pic_show_pie      "), "")
	raster_base_Btn.AddSimpleButton(ID.ID_SHOW_HISTGRAM , u"直方图", CreateBitmap("pic_show_histgram "), "")
	raster_base_Btn.AddSimpleButton(ID.ID_SHOW_RADIA    ,   u"雷达图", CreateBitmap("pic_show_radia    "), "")
	raster_base_Btn.AddSimpleButton(ID.ID_SHOW_QQPLOT   ,    u"QQPlot", CreateBitmap("pic_show_qqplot   "), "")
	raster_base_Btn.AddSimpleButton(ID.ID_SHOW_SCARTE   , u"散点图", CreateBitmap("pic_show_scarte   "), "")
	raster_base_Btn.AddSimpleButton(ID.ID_SHOW_BAR      ,  u"矩状图", CreateBitmap("pic_show_bar      "), "")
	raster_base_Btn.AddSimpleButton(ID.ID_SHOW_LINE     ,  u"折线图", CreateBitmap("pic_show_line     "), "")
		
	#  bind
	raster_base_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.show_pie     , id=ID.ID_SHOW_PIE)
	raster_base_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.show_histgram, id=ID.ID_SHOW_HISTGRAM)
	raster_base_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.show_radia   , id=ID.ID_SHOW_RADIA)
	raster_base_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.show_qqplot  , id=ID.ID_SHOW_QQPLOT)
	raster_base_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.show_scarte  , id=ID.ID_SHOW_SCARTE)
	raster_base_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.show_bar     , id=ID.ID_SHOW_BAR)
	raster_base_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.show_line    , id=ID.ID_SHOW_LINE)

    #----------------------------------------------------------------------
    def show_pie(self , event):
	""" show_pie"""
	print "show_pie"
	ID.ID_LIST.append(ID.ID_SHOW_PIE)
    #----------------------------------------------------------------------
    def show_histgram(self , event):
	""" show_histgram"""
	print "show_histgram"
	ID.ID_LIST.append(ID.ID_SHOW_HISTGRAM)	
    #----------------------------------------------------------------------
    def show_radia(self , event):
	""" show_radia"""
	print "show_radia"
	ID.ID_LIST.append(ID.ID_SHOW_RADIA)
    #----------------------------------------------------------------------
    def show_qqplot(self , event):
	""" show_qqplot db"""
	print "show_qqplot"
	ID.ID_LIST.append(ID.ID_SHOW_QQPLOT)
    #----------------------------------------------------------------------
    def show_scarte(self , event):
	""" db show_scarte"""
	print "show_scarte"
	ID.ID_LIST.append(ID.ID_SHOW_SCARTE)	
    #----------------------------------------------------------------------
    def show_bar(self , event):
	""" show_bar"""
	print "show_bar"
	ID.ID_LIST.append(ID.ID_SHOW_BAR)
    #----------------------------------------------------------------------
    def show_line(self , event):
	""" show_line db"""
	print "show_line"
	ID.ID_LIST.append(ID.ID_SHOW_LINE)

	
	
########################################################################
class show_advance_Panel(RB.RibbonPanel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        RB.RibbonPanel.__init__(self,parent,wx.ID_ANY , label = u"空间分布" )
	raster_advance_Btn = RB.RibbonButtonBar(self )
	raster_advance_Btn.AddSimpleButton( ID.ID_SSHOW_PIE      , u"空间饼状分布图", CreateBitmap("pic_sshow_pie     "), " ")
	raster_advance_Btn.AddSimpleButton( ID.ID_SSHOW_BAR      , u"空间矩状分布图", CreateBitmap("pic_sshow_bar     "), " ")
	raster_advance_Btn.AddSimpleButton( ID.ID_SSHOW_CLASSIFY , u"空间分层分布图", CreateBitmap("pic_sshow_classify"), " ")

	#  bind
	raster_advance_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.sshow_pie     , id=ID.ID_SSHOW_PIE     )
	raster_advance_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.sshow_bar     , id=ID.ID_SSHOW_BAR     )
	raster_advance_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.sshow_classify, id=ID.ID_SSHOW_CLASSIFY )
    #----------------------------------------------------------------------
    def sshow_pie(self , event):
	""" sshow_pie db"""
	print "sshow_pie"
	ID.ID_LIST.append(ID.ID_SSHOW_PIE)
    #----------------------------------------------------------------------
    def sshow_bar(self , event):
	""" db sshow_bar"""
	print "sshow_bar"
	ID.ID_LIST.append(ID.ID_SSHOW_BAR)	
    #----------------------------------------------------------------------
    def sshow_classify(self , event):
	""" sshow_classify"""
	print "sshow_classify"
	ID.ID_LIST.append(ID.ID_SSHOW_CLASSIFY)
	
########################################################################
#class testModel_resource_Panel(RB.RibbonPanel):
    #""""""

    ##----------------------------------------------------------------------
    #def __init__(self, parent):
        #RB.RibbonPanel.__init__(self,parent,wx.ID_ANY , label = u"资源" )
	#testModel_resource_BtnBar = RB.RibbonButtonBar(self )
	#testModel_resource_BtnBar.AddSimpleButton(ID_TESTMODEL_COASTALECO , u"滩涂经济", CreateBitmap("circle"), "")
	#testModel_resource_BtnBar.AddSimpleButton(ID_TESTMODEL_POPULATION, u"人口密度", CreateBitmap("circle"), "")
	#testModel_resource_BtnBar.AddSimpleButton(ID_TESTMODEL_TRIP , u"旅游", CreateBitmap("circle"), "")
	#testModel_resource_BtnBar.AddSimpleButton(ID_TESTMODEL_PUBLIC , u"公共资源", CreateBitmap("circle"), "")

#########################################################################
#class testModel_environment_Panel(RB.RibbonPanel):
    #""""""

    ##----------------------------------------------------------------------
    #def __init__(self, parent):
        #RB.RibbonPanel.__init__(self,parent,wx.ID_ANY , label = u"环境" )
	#testModel_environment_BtnBar = RB.RibbonButtonBar(self )
	#testModel_environment_BtnBar.AddSimpleButton(ID_TESTMODEL_WATERLOSE , u"水土流失", CreateBitmap("circle"), "")
	#testModel_environment_BtnBar.AddSimpleButton(ID_TESTMODEL_POLLUTION , u"环境污染", CreateBitmap("circle"), "")
	#testModel_environment_BtnBar.AddSimpleButton(ID_TESTMODEL_NATURAL , u"自然灾害", CreateBitmap("circle"), "")