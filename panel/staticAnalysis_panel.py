#-*- encoding:GBK -*-
import wx
import wx.lib.agw.ribbon as RB
from wx.lib.embeddedimage import PyEmbeddedImage
import sys

import global_ID as ID

##### icon  #########
pic_static_abs                 = ID.PIC_STATIC_ABS                 
pic_static_average             = ID.PIC_STATIC_AVERAGE             
pic_static_concatenate         = ID.PIC_STATIC_CONCATENATE         
pic_static_density	       = ID.PIC_STATIC_DENSITY	  

pic_static_frequency	       = ID.PIC_STATIC_FREQUENCY	       
pic_static_max	               = ID.PIC_STATIC_MAX	               
pic_static_min	               = ID.PIC_STATIC_MIN	               
pic_static_mod                 = ID.PIC_STATIC_MOD   

pic_static_rank                = ID.PIC_STATIC_RANK                
pic_static_subtotal	       = ID.PIC_STATIC_SUBTOTAL	           
pic_static_sum	               = ID.PIC_STATIC_SUM	               
pic_static_stdev               = ID.PIC_STATIC_STDEV   


def CreateBitmap(xpm):
    bmp = eval(xpm).Bitmap
    return bmp

	
########################################################################
class static_data_Panel(RB.RibbonPanel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        RB.RibbonPanel.__init__(self,parent, label = u"数据处理")
	testAnaly_data_Btn = RB.RibbonButtonBar(self)
	testAnaly_data_Btn.AddSimpleButton(ID.ID_STATIC_ABS        ,     u"比重",    CreateBitmap("pic_static_abs"), "" )
	testAnaly_data_Btn.AddSimpleButton(ID.ID_STATIC_AVERAGE     ,    u"算术平均值", CreateBitmap(" pic_static_average"), "")
	testAnaly_data_Btn.AddSimpleButton(ID.ID_STATIC_CONCATENATE ,    u"增长率", CreateBitmap(" pic_static_concatenate"), "")	
	testAnaly_data_Btn.AddSimpleButton(ID.ID_STATIC_DENSITY	 , u"密度函数", CreateBitmap(" pic_static_density"), "")	
	
	#bind
	testAnaly_data_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.static_abs          , id=ID.ID_STATIC_ABS        )
	testAnaly_data_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.static_average      , id=ID.ID_STATIC_AVERAGE       )
	testAnaly_data_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.static_concatenate  , id=ID.ID_STATIC_CONCATENATE  )
	testAnaly_data_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.static_density	, id=ID.ID_STATIC_DENSITY	 )
		
    #----------------------------------------------------------------------
    def static_abs(self , event):
	""" static_abs"""
	print "static_abs"
	ID.ID_LIST.append(ID.ID_STATIC_ABS)
    #----------------------------------------------------------------------
    def static_average(self , event):
	""" static_average"""
	print "static_average"
	ID.ID_LIST.append(ID.ID_STATIC_AVERAGE)	
    #----------------------------------------------------------------------
    def static_concatenate(self , event):
	""" static_concatenate"""
	print "static_concatenate"
	ID.ID_LIST.append(ID.ID_STATIC_CONCATENATE)
    #----------------------------------------------------------------------
    def static_density(self , event):
	""" static_density db"""
	print "static_density"
	ID.ID_LIST.append(ID.ID_STATIC_DENSITY)
	    
    
########################################################################
class static_view_Panel(RB.RibbonPanel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        RB.RibbonPanel.__init__(self,parent, label = u"分类")
	testAnaly_view_Btn = RB.RibbonButtonBar(self)
	testAnaly_view_Btn.AddSimpleButton( ID.ID_STATIC_FREQUENCY   , u"比重",  CreateBitmap("pic_static_frequency"), "")
	testAnaly_view_Btn.AddSimpleButton( ID.ID_STATIC_MAX	     , u"最大值 ",  CreateBitmap("pic_static_max	    "), "")
	testAnaly_view_Btn.AddSimpleButton( ID.ID_STATIC_MIN	     , u"最小值 ",  CreateBitmap("pic_static_min	    "), "")	
	testAnaly_view_Btn.AddSimpleButton( ID.ID_STATIC_MOD        , u"余数",  CreateBitmap("pic_static_mod      "), "")
	
	#bind
	testAnaly_view_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.static_frequency, id=ID.ID_STATIC_FREQUENCY)
	testAnaly_view_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.static_max	    , id=ID.ID_STATIC_MAX	     )
	testAnaly_view_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.static_min	    , id=ID.ID_STATIC_MIN	    )
	testAnaly_view_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.static_mod      , id=ID.ID_STATIC_MOD        )
		
    #----------------------------------------------------------------------
    def static_frequency(self , event):
	""" static_frequency"""
	print "static_frequency"
	ID.ID_LIST.append(ID.ID_STATIC_FREQUENCY)
    #----------------------------------------------------------------------
    def static_max(self , event):
	""" static_max"""
	print "static_max"
	ID.ID_LIST.append(ID.ID_STATIC_MAX)	
    #----------------------------------------------------------------------
    def static_min(self , event):
	""" static_min"""
	print "static_min"
	ID.ID_LIST.append(ID.ID_STATIC_MIN)
    #----------------------------------------------------------------------
    def static_mod(self , event):
	""" static_mod db"""
	print "static_mod"
	ID.ID_LIST.append(ID.ID_STATIC_MOD)
	    
    

########################################################################
class static_classify_Panel(RB.RibbonPanel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        RB.RibbonPanel.__init__(self,parent, label = u"分析")
	testAnaly_classify_Btn = RB.RibbonButtonBar(self)
	testAnaly_classify_Btn.AddSimpleButton(ID.ID_STATIC_RANK     , u"排名函数",    CreateBitmap("pic_static_rank    "), "")
	testAnaly_classify_Btn.AddSimpleButton(ID.ID_STATIC_SUBTOTAL , u"分类汇总 ",    CreateBitmap("pic_static_subtotal"), "")
	testAnaly_classify_Btn.AddSimpleButton(ID.ID_STATIC_SUM	   ,      u"求和 ",    CreateBitmap("pic_static_sum	   "), "")	
	testAnaly_classify_Btn.AddSimpleButton(ID.ID_STATIC_STDEV    ,     u"标准偏差",    CreateBitmap("pic_static_stdev   "), "")	
	
	#bind
	testAnaly_classify_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.static_rank    , id=ID.ID_STATIC_RANK    )
	testAnaly_classify_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.static_subtotal, id=ID.ID_STATIC_SUBTOTAL   )
	testAnaly_classify_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.static_sum	   , id=ID.ID_STATIC_SUM     )
	testAnaly_classify_Btn.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.static_stdev   , id=ID.ID_STATIC_STDEV     )
		
    #----------------------------------------------------------------------
    def static_rank(self , event):
	""" static_rank"""
	print "static_rank"
	ID.ID_LIST.append(ID.ID_STATIC_RANK)
    #----------------------------------------------------------------------
    def static_subtotal(self , event):
	""" static_subtotal"""
	print "static_subtotal"
	ID.ID_LIST.append(ID.ID_STATIC_SUBTOTAL)	
    #----------------------------------------------------------------------
    def static_sum(self , event):
	""" static_sum"""
	print "static_sum"
	ID.ID_LIST.append(ID.ID_STATIC_SUM)
    #----------------------------------------------------------------------
    def static_stdev(self , event):
	""" static_stdev db"""
	print "static_stdev"
	ID.ID_LIST.append(ID.ID_STATIC_STDEV)
	    
            