#-*- encoding:GBK -*-
import wx
import wx.lib.agw.ribbon as RB
from wx.lib.embeddedimage import PyEmbeddedImage
import os
import sys

import OnDataLink_view
import shpdata_insert
import raster_insert
import excel_insert
import db_view
import db_view2
import global_ID as ID

def CreateBitmap(xpm):
    bmp = eval(xpm).Bitmap
    return bmp

pic_db_link                    = ID.PIC_DB_LINK                    
pic_db_vector                  = ID.PIC_DB_VECTOR                  
pic_db_raster                  = ID.PIC_DB_RASTER                  
pic_db_statistic               = ID.PIC_DB_STATISTIC               
pic_db_metadb                  = ID.PIC_DB_METADB                  
pic_db_maindb                  = ID.PIC_DB_MAINDB                  
                                                              
pic_search_time_sp             =  ID.PIC_SEARCH_TIME_SP                   
pic_search_time_attri          =  ID.PIC_SEARCH_TIME_ATTRI                
#pic_search_time_sp_attri       =  ID.PIC_SEARCH_TIME_SP_ATTRI 


class data_link_Panel(RB.RibbonPanel):
    def __init__(self, parent):
        RB.RibbonPanel.__init__(self,parent,wx.ID_ANY , label = u"连接")
	data_link_BtnBar = RB.RibbonButtonBar(self )
	data_link_BtnBar.AddSimpleButton(ID.ID_DB_LINK  , u"库连接", CreateBitmap("pic_db_link"), "")
		
	# bind event 
	data_link_BtnBar.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnDataLink, id=ID.ID_DB_LINK)
	
    #----------------------------------------------------------------------
    def OnDataLink(self, event):
	"""连接数据库"""
	datalink = OnDataLink_view.OnDataLinkView(None)      
        datalink.Show() 
	
########################################################################
class data_insert_Panel(RB.RibbonPanel):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, parent):
        RB.RibbonPanel.__init__(self,parent,wx.ID_ANY , label = u"数据插入" )
	data_easy_BtnBar = RB.RibbonButtonBar(self )
	data_easy_BtnBar.AddSimpleButton(ID.ID_DB_VECTOR   , u"矢量数据", CreateBitmap("pic_db_vector"), "")
	data_easy_BtnBar.AddSimpleButton(ID.ID_DB_RASTER  , u"栅格数据", CreateBitmap("pic_db_raster"), "")
	data_easy_BtnBar.AddSimpleButton(ID.ID_DB_STATISTIC , u"统计数据", CreateBitmap("pic_db_statistic"), "")
	
	#  bind
	data_easy_BtnBar.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.db_shp, id=ID.ID_DB_VECTOR)
	data_easy_BtnBar.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.db_raster, id=ID.ID_DB_RASTER)
	data_easy_BtnBar.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.db_statistic, id=ID.ID_DB_STATISTIC)
    #----------------------------------------------------------------------
    def db_shp(self , event):
	""" shp db"""
	print "db_shp"
	dataUpdata1 = shpdata_insert.DataInsertPanel(None)   
	dataUpdata1.Show() 	
	#ID.ID_LIST.append(ID.ID_DB_RASTER)
    #----------------------------------------------------------------------
    def db_raster(self , event):
	""" db raster"""
	print "db_raster"
	raster = raster_insert.DataInsertPanel(None)   
	raster.Show() 	
	#ID.ID_LIST.append(ID.ID_DB_VECTOR)	
    #----------------------------------------------------------------------
    def db_statistic(self , event):
	""" db_statistic"""
	print "db_statistic"
	excel = excel_insert.DataInsertPanel(None)   
	excel.Show() 	
	#ID.ID_LIST.append(ID.ID_DB_STATISTIC)
	
########################################################################
class data_view_Panel(RB.RibbonPanel):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, parent):
        RB.RibbonPanel.__init__(self,parent,wx.ID_ANY , label = u"数据库查看" )
	data_dim_BtnBar = RB.RibbonButtonBar(self )
	data_dim_BtnBar.AddSimpleButton(ID.ID_DB_METADB   , u"元数据库查看", CreateBitmap("pic_db_metadb"), "")
	data_dim_BtnBar.AddSimpleButton(ID.ID_DB_MAINDB  , u"主数据库查看", CreateBitmap("pic_db_maindb"), "")
	
	#  bind
	data_dim_BtnBar.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.meta_db, id=ID.ID_DB_METADB)
	data_dim_BtnBar.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.main_db, id=ID.ID_DB_MAINDB)

    #----------------------------------------------------------------------
    def meta_db(self , event):
	""" meta_db"""
	#print "meta_db"
	dbview = db_view.DB_view(None)
	dbview.Show() 	
	print u"要写一个打开 元数据库的界面和类"
	
    #----------------------------------------------------------------------
    def main_db(self , event):
	""" main_db"""
	#print "main_db"
	dbview2 = db_view2.DB_view(None)
	dbview2.Show() 	
	print u"写一个查询主数据库的界面和类"
		

import DB_search
import extract_view
########################################################################
class data_search_Panel(RB.RibbonPanel):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, parent):
        RB.RibbonPanel.__init__(self,parent,wx.ID_ANY , label = u"数据库抽取操作" )
	data_special_BtnBar = RB.RibbonButtonBar(self )
	data_special_BtnBar.AddSimpleButton(ID.ID_SEARCH_TIME_SP ,    u"矢量数据", CreateBitmap("pic_search_time_sp"), "")
	data_special_BtnBar.AddSimpleButton(ID.ID_SEARCH_TIME_ATTRI , u"栅格数据", CreateBitmap("pic_search_time_attri"), "")
	data_special_BtnBar.AddSimpleButton(ID.ID_SEARCH_TIME_ATTRI , u"统计数据", CreateBitmap("pic_search_time_attri"), "")


	#  bind
	data_special_BtnBar.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.search_ts, id=ID.ID_SEARCH_TIME_SP)
	data_special_BtnBar.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.search_ta, id=ID.ID_SEARCH_TIME_ATTRI)

    #----------------------------------------------------------------------
    def search_ts(self , event):
	""" db search_ts"""
	print "search_ts"
	db_search = DB_search.DB_search(None)
	db_search.Show() 	
    #----------------------------------------------------------------------
    def search_ta(self , event):
	""" search_ta"""
	print "search_ta"
	extractview = extract_view.MyFrame(None)
	extractview.Show() 	   
    