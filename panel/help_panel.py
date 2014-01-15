#-*- encoding:GBK -*-
import wx
import wx.lib.agw.ribbon as RB
from wx.lib.embeddedimage import PyEmbeddedImage
import os
import sys
#sys.path.append(r"E:\Test\wxGlade\second_one\icon");
import helpIcon

#--ICON---
help = helpIcon.Help
about = helpIcon.Apply

# end of icon  ----
def CreateBitmap(xpm):
    bmp = eval(xpm).Bitmap
    return bmp

#-- ID ----
ID_HELP       = 0700
ID_ABOUT = ID_HELP + 10 
#- end of ID code ---

class help_Panel(RB.RibbonPanel):
    def __init__(self, parent):
        RB.RibbonPanel.__init__(self,parent,wx.ID_ANY , label = u"帮助" )
	help_BtnBar = RB.RibbonButtonBar(self )
	help_BtnBar.AddSimpleButton(ID_HELP , u"帮助", CreateBitmap("help"), "")
	help_BtnBar.AddSimpleButton(ID_ABOUT , u"关于", CreateBitmap("about"), "")
	
	# bind event 
	help_BtnBar.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.OnAbout, id=ID_ABOUT)
	
    #----------------------------------------------------------------------
    def OnAbout(self , event):
	"""数据库连接"""
	wx.MessageBox(u"沿海滩涂生态管护软件")