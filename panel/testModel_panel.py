#-*- encoding:GBK -*-
import wx
import wx.lib.agw.ribbon as RB
from wx.lib.embeddedimage import PyEmbeddedImage
import os
import sys
#sys.path.append(r"E:\Test\wxGlade\second_one\icon");
import i1212

#--ICON---
circle = i1212.accept

# end of icon  ----
def CreateBitmap(xpm):
    bmp = eval(xpm).Bitmap
    return bmp

#-- ID ----
ID_TESTMODEL_LAND         = 0300
ID_TESTMODEL_DEM = ID_TESTMODEL_LAND + 1
ID_TESTMODEL_DEMCUT = ID_TESTMODEL_LAND + 2
ID_TESTMODEL_LANDUSE = ID_TESTMODEL_LAND + 3

ID_TESTMODEL_TEMPERATURE  = ID_TESTMODEL_LAND + 10
ID_TESTMODEL_TEMP  = ID_TESTMODEL_TEMPERATURE + 1
ID_TESTMODEL_RAIN  = ID_TESTMODEL_TEMPERATURE + 2
ID_TESTMODEL_TEMPOTHER  = ID_TESTMODEL_TEMPERATURE + 3

ID_TESTMODEL_RESOURCE     = ID_TESTMODEL_LAND + 20
ID_TESTMODEL_COASTALECO = ID_TESTMODEL_RESOURCE + 1
ID_TESTMODEL_POPULATION = ID_TESTMODEL_RESOURCE + 2
ID_TESTMODEL_TRIP = ID_TESTMODEL_RESOURCE + 3
ID_TESTMODEL_PUBLIC = ID_TESTMODEL_RESOURCE + 4

ID_TESTMODEL_ENVIRONMENT       = ID_TESTMODEL_LAND + 30
ID_TESTMODEL_WATERLOSE = ID_TESTMODEL_ENVIRONMENT + 1 
ID_TESTMODEL_POLLUTION = ID_TESTMODEL_ENVIRONMENT + 2
ID_TESTMODEL_NATURAL = ID_TESTMODEL_ENVIRONMENT + 3
#- end of ID code ---

class testModel_land_Panel(RB.RibbonPanel):
    def __init__(self, parent):
        RB.RibbonPanel.__init__(self,parent,wx.ID_ANY , label = u"����" )
	testModel_land_BtnBar = RB.RibbonButtonBar(self )
	testModel_land_BtnBar.AddSimpleButton(ID_TESTMODEL_DEM , u"DEM", CreateBitmap("circle"), "")
	testModel_land_BtnBar.AddSimpleButton(ID_TESTMODEL_DEMCUT , u"��������", CreateBitmap("circle"), "")
	testModel_land_BtnBar.AddSimpleButton(ID_TESTMODEL_LANDUSE , u"��������", CreateBitmap("circle"), "")
		
	# bind event 
	testModel_land_BtnBar.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnLandUse, id=ID_TESTMODEL_LANDUSE)
	
    #----------------------------------------------------------------------
    def OnLandUse(self , event):
	"""��shp�ļ�"""
	print "land use file wrong"
	
########################################################################
class testModel_temperature_Panel(RB.RibbonPanel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        RB.RibbonPanel.__init__(self,parent,wx.ID_ANY , label = u"����" )
	testModel_temp_BtnBar = RB.RibbonButtonBar(self )
	testModel_temp_BtnBar.AddSimpleButton(ID_TESTMODEL_TEMP , u"ƽ������", CreateBitmap("circle"), "")
	testModel_temp_BtnBar.AddSimpleButton(ID_TESTMODEL_RAIN , u"��ˮ��", CreateBitmap("circle"), "")
	testModel_temp_BtnBar.AddSimpleButton(ID_TESTMODEL_TEMPOTHER , u"��������ط���", CreateBitmap("circle"), "")
	
	
########################################################################
class testModel_resource_Panel(RB.RibbonPanel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        RB.RibbonPanel.__init__(self,parent,wx.ID_ANY , label = u"��Դ" )
	testModel_resource_BtnBar = RB.RibbonButtonBar(self )
	testModel_resource_BtnBar.AddSimpleButton(ID_TESTMODEL_COASTALECO , u"̲Ϳ����", CreateBitmap("circle"), "")
	testModel_resource_BtnBar.AddSimpleButton(ID_TESTMODEL_POPULATION, u"�˿��ܶ�", CreateBitmap("circle"), "")
	testModel_resource_BtnBar.AddSimpleButton(ID_TESTMODEL_TRIP , u"����", CreateBitmap("circle"), "")
	testModel_resource_BtnBar.AddSimpleButton(ID_TESTMODEL_PUBLIC , u"������Դ", CreateBitmap("circle"), "")

########################################################################
class testModel_environment_Panel(RB.RibbonPanel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        RB.RibbonPanel.__init__(self,parent,wx.ID_ANY , label = u"����" )
	testModel_environment_BtnBar = RB.RibbonButtonBar(self )
	testModel_environment_BtnBar.AddSimpleButton(ID_TESTMODEL_WATERLOSE , u"ˮ����ʧ", CreateBitmap("circle"), "")
	testModel_environment_BtnBar.AddSimpleButton(ID_TESTMODEL_POLLUTION , u"������Ⱦ", CreateBitmap("circle"), "")
	testModel_environment_BtnBar.AddSimpleButton(ID_TESTMODEL_NATURAL , u"��Ȼ�ֺ�", CreateBitmap("circle"), "")