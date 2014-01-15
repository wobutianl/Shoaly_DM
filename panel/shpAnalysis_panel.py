#-*- encoding:GBK -*-
import wx
import wx.lib.agw.ribbon as RB
from wx.lib.embeddedimage import PyEmbeddedImage
#import FourWaySplitterDemo  as fws
import os
import sys
import global_ID as ID


pic_shp_area                   = ID.PIC_SHP_AREA                   
pic_shp_length                 = ID.PIC_SHP_LENGTH                 
pic_shp_extent                 = ID.PIC_SHP_EXTENT                 
pic_shp_center                 = ID.PIC_SHP_CENTER                 
pic_shp_point                  = ID.PIC_SHP_POINT                  
pic_shp_out                    = ID.PIC_SHP_OUT                    
pic_shp_buffer                 = ID.PIC_SHP_BUFFER                 
pic_shp_simple                 = ID.PIC_SHP_SIMPLE                 
pic_shp_intersect              = ID.PIC_SHP_INTERSECT              
pic_shp_difference             = ID.PIC_SHP_DIFFERENCE                
pic_shp_union                  = ID.PIC_SHP_UNION                  
                                                               
pic_raster_move                = ID.PIC_RASTER_MOVE                
pic_raster_rotate              = ID.PIC_RASTER_ROTATE             
pic_raster_zoom                = ID.PIC_RASTER_ZOOM              
pic_raster_cut                 = ID.PIC_RASTER_CUT                 
pic_raster_roi                 = ID.PIC_RASTER_ROI                 
pic_raster_union               = ID.PIC_RASTER_UNION               
pic_raster_reverse             = ID.PIC_RASTER_REVERSE             
pic_raster_balance             = ID.PIC_RASTER_BALANCE             
pic_raster_slop                = ID.PIC_RASTER_SLOP                
pic_raster_sharp               = ID.PIC_RASTER_SHARP               
pic_raster_color               = ID.PIC_RASTER_COLOR   

# end of icon  ----
def CreateBitmap(xpm):
    bmp = eval(xpm).Bitmap
    return bmp


#  edit view panel
class shp_Panel(RB.RibbonPanel):
    def __init__(self, parent):
        RB.RibbonPanel.__init__(self,parent,wx.ID_ANY , label = u"ʸ���ռ����ݲ���" )
	shp_real_Btn = RB.RibbonButtonBar(self )
	
	shp_real_Btn.AddSimpleButton(ID.ID_SHP_AREA       ,  u"��� " ,CreateBitmap("pic_shp_area"), "")
	shp_real_Btn.AddSimpleButton(ID.ID_SHP_LENGTH    ,   u"����" , CreateBitmap("pic_shp_length"), "")
	shp_real_Btn.AddSimpleButton(ID.ID_SHP_EXTENT    ,   u"����" , CreateBitmap("pic_shp_extent"), "")
	shp_real_Btn.AddSimpleButton(ID.ID_SHP_CENTER    ,   u"����" , CreateBitmap("pic_shp_center"), "")
	shp_real_Btn.AddSimpleButton(ID.ID_SHP_POINT     ,   u"�ؼ���" ,   CreateBitmap("pic_shp_point"), "")
	shp_real_Btn.AddSimpleButton(ID.ID_SHP_OUT        ,  u"�������" , CreateBitmap("pic_shp_out "), "")
	shp_real_Btn.AddSimpleButton(ID.ID_SHP_BUFFER    ,   u"������" ,   CreateBitmap("pic_shp_buffer"), "")
	shp_real_Btn.AddSimpleButton(ID.ID_SHP_SIMPLE    ,   u"��" ,     CreateBitmap("pic_shp_simple"), "")
	shp_real_Btn.AddSimpleButton(ID.ID_SHP_INTERSECT  ,  u"��" ,     CreateBitmap("pic_shp_intersect"), "")
	shp_real_Btn.AddSimpleButton(ID.ID_SHP_DIFFERENCE ,  u"��� " ,    CreateBitmap("pic_shp_difference"), "")
	shp_real_Btn.AddSimpleButton(ID.ID_SHP_UNION      ,  u"��� " ,    CreateBitmap("pic_shp_union"), "")    
	
	#  bind
	shp_real_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.shp_area      , id=ID.ID_SHP_AREA      )
	shp_real_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.shp_length    , id=ID.ID_SHP_LENGTH    )
	shp_real_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.shp_extent    , id=ID.ID_SHP_EXTENT    )
	shp_real_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.shp_center    , id=ID.ID_SHP_CENTER    )
	shp_real_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.shp_point     , id=ID.ID_SHP_POINT     )
	shp_real_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.shp_out       , id=ID.ID_SHP_OUT       )
	shp_real_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.shp_buffer    , id=ID.ID_SHP_BUFFER    )
	shp_real_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.shp_simple    , id=ID.ID_SHP_SIMPLE    )
	shp_real_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.shp_intersect , id=ID.ID_SHP_INTERSECT )
	shp_real_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.shp_difference, id=ID.ID_SHP_DIFFERENCE)
	shp_real_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.shp_union     , id=ID.ID_SHP_UNION     )
	
    #----------------------------------------------------------------------
    def shp_area(self , event):
	""" shp_area"""
	print "shp_area"
	ID.ID_LIST.append(ID.ID_SHP_AREA)
    #----------------------------------------------------------------------
    def shp_length(self , event):
	""" shp_length"""
	print "shp_length"
	ID.ID_LIST.append(ID.ID_SHP_LENGTH)	
    #----------------------------------------------------------------------
    def shp_extent(self , event):
	""" shp_extent"""
	print "shp_extent"
	ID.ID_LIST.append(ID.ID_SHP_EXTENT)
    #----------------------------------------------------------------------
    def shp_center(self , event):
	""" shp_center db"""
	print "shp_center"
	ID.ID_LIST.append(ID.ID_SHP_CENTER)
    #----------------------------------------------------------------------
    def shp_point(self , event):
	""" db shp_point"""
	print "shp_point"
	ID.ID_LIST.append(ID.ID_SHP_POINT)	
    #----------------------------------------------------------------------
    def shp_out(self , event):
	""" shp_out"""
	print "shp_out"
	ID.ID_LIST.append(ID.ID_SHP_OUT)
    #----------------------------------------------------------------------
    def shp_buffer(self , event):
	""" shp_buffer"""
	print "shp_buffer"
	ID.ID_LIST.append(ID.ID_SHP_BUFFER)	
    #----------------------------------------------------------------------
    def shp_simple(self , event):
	""" shp_simple"""
	print "shp_simple"
	ID.ID_LIST.append(ID.ID_SHP_SIMPLE)
    #----------------------------------------------------------------------
    def shp_intersect(self , event):
	""" shp_intersect"""
	print "shp_intersect"
	ID.ID_LIST.append(ID.ID_SHP_INTERSECT)	
    #----------------------------------------------------------------------
    def shp_difference(self , event):
	""" shp_difference"""
	print "shp_difference"
	ID.ID_LIST.append(ID.ID_SHP_DIFFERENCE)
    #----------------------------------------------------------------------
    def shp_union(self , event):
	""" shp_union"""
	print "shp_union"
	ID.ID_LIST.append(ID.ID_SHP_UNION)	
		    		    
########################################################################
class raster_Panel(RB.RibbonPanel):
    """edit base panel"""
    #----------------------------------------------------------------------
    def __init__(self, parent):
	"""Constructor"""
	RB.RibbonPanel.__init__(self,parent,wx.ID_ANY , label = u"դ��ռ����ݲ���" )
	shp_topo_Btn = RB.RibbonButtonBar(self )	
	shp_topo_Btn.AddSimpleButton(ID.ID_RASTER_MOVE   ,  u"�ƶ�" ,  CreateBitmap("pic_raster_move"), "")
	shp_topo_Btn.AddSimpleButton(ID.ID_RASTER_ROTATE ,  u"��ת" ,  CreateBitmap("pic_raster_rotate"), "")
	shp_topo_Btn.AddSimpleButton(ID.ID_RASTER_ZOOM   ,  u"����" ,  CreateBitmap("pic_raster_zoom"), "")
	shp_topo_Btn.AddSimpleButton(ID.ID_RASTER_CUT    ,  u"����" ,  CreateBitmap("pic_raster_cut"), "")
	shp_topo_Btn.AddSimpleButton(ID.ID_RASTER_ROI    ,  u"ROI" ,   CreateBitmap("pic_raster_roi"), "")
	shp_topo_Btn.AddSimpleButton(ID.ID_RASTER_UNION  ,  u"�ϲ�" ,  CreateBitmap("pic_raster_union"), "")
	shp_topo_Btn.AddSimpleButton(ID.ID_RASTER_REVERSE,  u"��ɫ" ,  CreateBitmap("pic_raster_reverse"), "")
	shp_topo_Btn.AddSimpleButton(ID.ID_RASTER_BALANCE,  u"ɫ��ƽ��" ,  CreateBitmap("pic_raster_balance"), "")
	shp_topo_Btn.AddSimpleButton(ID.ID_RASTER_SLOP   ,  u"ƽ��" ,  CreateBitmap("pic_raster_slop"), "")	
	shp_topo_Btn.AddSimpleButton(ID.ID_RASTER_SHARP  ,  u"��" ,  CreateBitmap("pic_raster_sharp"), "")	
	shp_topo_Btn.AddSimpleButton(ID.ID_RASTER_COLOR  ,  u"ɫ����ǿ" ,  CreateBitmap("pic_raster_color"), "")
    
	#  bind
	shp_topo_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.raster_move   , id=ID.ID_RASTER_MOVE   )
	shp_topo_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.raster_rotate , id=ID.ID_RASTER_ROTATE )
	shp_topo_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.raster_zoom   , id=ID.ID_RASTER_ZOOM   )
	shp_topo_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.raster_cut    , id=ID.ID_RASTER_CUT    )
	shp_topo_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.raster_roi    , id=ID.ID_RASTER_ROI    )
	shp_topo_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.raster_union  , id=ID.ID_RASTER_UNION  )
	shp_topo_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.raster_reverse, id=ID.ID_RASTER_REVERSE)
	shp_topo_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.raster_balance, id=ID.ID_RASTER_BALANCE)
	shp_topo_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.raster_slop   , id=ID.ID_RASTER_SLOP   )
	shp_topo_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.raster_sharp  , id=ID.ID_RASTER_SHARP  )
	shp_topo_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.raster_color  , id=ID.ID_RASTER_COLOR  )
	
    #----------------------------------------------------------------------
    def raster_move(self , event):
	""" raster_move"""
	print "raster_move"
	ID.ID_LIST.append(ID.ID_RASTER_MOVE)
    #----------------------------------------------------------------------
    def raster_rotate(self , event):
	""" raster_rotate"""
	print "raster_rotate"
	ID.ID_LIST.append(ID.ID_RASTER_ROTATE)	
    #----------------------------------------------------------------------
    def raster_zoom(self , event):
	""" raster_zoom"""
	print "raster_zoom"
	ID.ID_LIST.append(ID.ID_RASTER_ZOOM)
    #----------------------------------------------------------------------
    def raster_cut(self , event):
	""" raster_cut db"""
	print "raster_cut"
	ID.ID_LIST.append(ID.ID_RASTER_CUT)
    #----------------------------------------------------------------------
    def raster_union(self , event):
	""" db raster_union"""
	print "raster_union"
	ID.ID_LIST.append(ID.ID_RASTER_UNION)	
    #----------------------------------------------------------------------
    def raster_balance(self , event):
	""" raster_balance"""
	print "raster_balance"
	ID.ID_LIST.append(ID.ID_RASTER_BALANCE)
    #----------------------------------------------------------------------
    def raster_reverse(self , event):
	""" raster_reverse"""
	print "raster_reverse"
	ID.ID_LIST.append(ID.ID_RASTER_REVERSE)	
    #----------------------------------------------------------------------
    def raster_slop(self , event):
	""" raster_slop"""
	print "raster_slop"
	ID.ID_LIST.append(ID.ID_RASTER_SLOP)
    #----------------------------------------------------------------------
    def raster_sharp(self , event):
	""" raster_sharp"""
	print "raster_sharp"
	ID.ID_LIST.append(ID.ID_RASTER_SHARP)	
    #----------------------------------------------------------------------
    def raster_color(self , event):
	""" raster_color"""
	print "raster_color"
	ID.ID_LIST.append(ID.ID_RASTER_COLOR)
    #----------------------------------------------------------------------
    def raster_roi(self , event):
	""" raster_roi"""
	print "raster_roi"
	ID.ID_LIST.append(ID.ID_RASTER_ROI)	
	
########################################################################
#class shp_binary_Panel(RB.RibbonPanel):
    #"""edit base panel"""
    ##----------------------------------------------------------------------
    #def __init__(self, parent):
	#"""Constructor"""
	#RB.RibbonPanel.__init__(self,parent,wx.ID_ANY , label = u"�����Ʋ���" )
	#shp_binary_Btn = RB.RibbonButtonBar(self )	
	#shp_binary_Btn.AddSimpleButton(ID_SHP_DIFFERENCE, u"���" ,CreateBitmap("difference"), "")
	#shp_binary_Btn.AddSimpleButton(ID_SHP_INTERSECT,u"��" , CreateBitmap("intersect"), "")	
	#shp_binary_Btn.AddSimpleButton(ID_SHP_UNION, u"��" ,CreateBitmap("union"), "")	
		
		
########################################################################
#class shp_real_Panel(RB.RibbonPanel):
    #"""edit base panel"""
    ##----------------------------------------------------------------------
    #def __init__(self, parent):
	#"""Constructor"""
	#RB.RibbonPanel.__init__(self,parent,wx.ID_ANY , label = u"���湤��" )
	#edit_interface_Btn = RB.RibbonButtonBar(self )		
	#edit_interface_Btn.AddSimpleButton(ID_EDIT_SWAP24, u"2&4����ת��" ,CreateBitmap("circle"),"")
	#edit_interface_Btn.AddSimpleButton(ID_EDIT_SWAP13, u"1&3����ת��",CreateBitmap("circle"),"")	
	#edit_interface_Btn.AddDropdownButton(ID_EDIT_EXPANDWIN, u"�л���ͼ",CreateBitmap("circle"),"")
	
	#edit_interface_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_DROPDOWN_CLICKED, self.OnInterfaceDropdown, id=ID_EDIT_EXPANDWIN)
	#edit_interface_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnSwap24, id=ID_EDIT_SWAP24)
	#edit_interface_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnSwap13, id=ID_EDIT_SWAP13)
	
    #def OnInterfaceDropdown(self, event):

	#menu = wx.Menu()
	#menu.Append(ID_EDIT_EXPANDWIN + 1, u"��һ����")
	#menu.Append(ID_EDIT_EXPANDWIN + 2, u"�ڶ�����")
	#menu.Append(ID_EDIT_EXPANDWIN + 3, u"��������")
	#menu.Append(ID_EDIT_EXPANDWIN + 4, u"���Ľ���")
	#menu.Append(ID_EDIT_EXPANDWIN + 5, u"Ĭ�Ͻ���")

	#event.PopupMenu(menu)    
	
	#self.Bind(wx.EVT_MENU, self.OnFirst, ID_EDIT_EXPANDWIN + 1)
	
    ##----------------------------------------------------------------------
    #def OnFirst(self,event):
	#"""the first win expand"""

	#pass
    ##----------------------------------------------------------------------
    #def OnSwap24(self,event):
	#"""exchange interface 2 & 4"""
	
	#pass
    
    ##----------------------------------------------------------------------
    #def OnSwap13(self,event):
	#"""exchange interface 1 & 3"""

	#pass