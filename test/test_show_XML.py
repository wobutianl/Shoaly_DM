# -*- coding: utf-8 -*-
import wx  
import wx.stc as stc

class StaticTextFrame(wx.Frame):  
    def __init__(self):  
        wx.Frame.__init__(self, None, -1, 'Static Text Example',   
                size=(400, 300))  
        panel = wx.Panel(self, -1)  
  
        # 这是一个基本的静态文本  
        #wx.StaticText(panel, -1, "This is an example of static text",   
                #(100, 10))  
  
        ## 指定了前景色和背景色的静态文本  
        #rev = wx.StaticText(panel, -1, "Static Text With Reversed Colors",   
                #(100, 30))  
        #rev.SetForegroundColour('white')  
        #rev.SetBackgroundColour('black')  
  
        ## 指定居中对齐的的静态文本  
        #center = wx.StaticText(panel, -1, "align center", (100, 50),   
                #(160, -1), wx.ALIGN_CENTER)  
        #center.SetForegroundColour('white')  
        #center.SetBackgroundColour('black')  
  
        ## 指定右对齐的静态文本  
        #right = wx.StaticText(panel, -1, "align right", (100, 70),   
                #(160, -1), wx.ALIGN_RIGHT)  
        #right.SetForegroundColour('white')  
        #right.SetBackgroundColour('black')  
  
        ## 指定新字体的静态文本  
        #str = "You can also change the font."  
        #text = wx.StaticText(panel, -1, str, (20, 100))  
        #font = wx.Font(18, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)  
        #text.SetFont(font)  
  
        ## 显示多行文本  
        #wx.StaticText(panel, -1, "Your text\ncan be split\n"  
                #"over multiple lines\n\neven blank ones", (20,150))  
  
        #显示对齐的多行文本
        
        style = stc.StyledTextCtrl(panel, id=wx.ID_ANY, pos=(0,0), size=(400, 300), style=0) 
        style.AddText("""<?xml version="1.0" encoding="gb2312"?>
<bookstore>
<book genre="fantasy" ISBN="2-3631-4">
<title>Oberons Legacy</title>
<author>Corets, Eva</author>
<price>5.95</price>
</book>
</bookstore>""")
  
  
if __name__ == '__main__':  
        app = wx.PySimpleApp()  
        frame = StaticTextFrame()  
        frame.Show()  
        app.MainLoop()  
#wx.StyledTextCtrl