# -*- coding: utf-8 -*-  
#############
## panel that control vector and raster data
## 11-28
#######################

import wx
import wx.lib.agw.ribbon as RB
from wx.lib.embeddedimage import PyEmbeddedImage
import os
import sys

import i1212
import fileIcon

###############
##for shp 
## area, refer_transform, buffer, intersect, union, clip
## for raster
## get_band, clip, refter_transform, 
######
#--ICON---
circle = i1212.accept
openShp = fileIcon.splitpolygonbig
openRaster = fileIcon.OpCategory_Zonal
openTable = fileIcon.OpCategory_Descriptor
addData = fileIcon.OpArithmetic_Add

# ID  number
ID_SHP = 3000
ID_RASTER = 3100

ID_SHP_AREA         = ID_SHP + 1
ID_SHP_REFTER = ID_SHP + 2
ID_SHP_BUFFER = ID_SHP + 3
ID_SHP_INTERSECT   = ID_SHP + 4
ID_SHP_UNION   = ID_SHP + 5
ID_SHP_CLIP   = ID_SHP + 6

ID_RASTER_BAND = ID_RASTER + 1
ID_RASTER_CLIP = ID_RASTER + 2
ID_RASTER_REFTER = ID_RASTER + 3
#- end of ID code ---

class shp_mani_Panel(RB.RibbonPanel):
    def __init__(self, parent):
        RB.RibbonPanel.__init__(self,parent,wx.ID_ANY , label = u"矢量操作" )
	shp_mani_BtnBar = RB.RibbonButtonBar(self)
	shp_mani_BtnBar.AddSimpleButton(ID_SHP_AREA , u"shp面积", CreateBitmap("openShp"), "")
	shp_mani_BtnBar.AddSimpleButton(ID_SHP_BUFFER , u"缓冲区", CreateBitmap("openRaster"), "")
	shp_mani_BtnBar.AddSimpleButton(ID_SHP_CLIP , u"剪切", CreateBitmap("openTable"), "")
	shp_mani_BtnBar.AddSimpleButton(ID_SHP_INTERSECT , u"交集", CreateBitmap("addData"), "")
	shp_mani_BtnBar.AddSimpleButton(ID_SHP_REFTER , u"坐标系转换", CreateBitmap("addData"), "")
	shp_mani_BtnBar.AddSimpleButton(ID_SHP_UNION , u"合并", CreateBitmap("addData"), "")
		
	# bind event 
	shp_mani_BtnBar.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnShpArea, id=ID_SHP_AREA)
	
    #----------------------------------------------------------------------
    def OnShpArea(self , event):
	"""打开shp文件"""
	#shp_area()
	print "open shp file wrong"
	