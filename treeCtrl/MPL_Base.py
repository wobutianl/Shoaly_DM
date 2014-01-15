# -*- coding: utf-8 -*-  
  
import wx  
import numpy as np  
import matplotlib  
# matplotlib采用WXAgg为后台,将matplotlib嵌入wxPython中  
matplotlib.use("WXAgg")  

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas  
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar  
from matplotlib.ticker import MultipleLocator, FuncFormatter  

import pylab  
from matplotlib import pyplot  
import math
import read_excel
  
######################################################################################  
class MPL_Panel_base(wx.Panel):  
    ''''' #MPL_Panel_base面板,可以继承或者创建实例'''  
    def __init__(self,parent):  
        wx.Panel.__init__(self,parent=parent, id=-1)  
  
        self.Figure = matplotlib.figure.Figure(figsize=(4,3))  
        self.axes = self.Figure.add_axes([0.1,0.1,0.8,0.8])  
        self.FigureCanvas = FigureCanvas(self,-1,self.Figure)  
          
        self.NavigationToolbar = NavigationToolbar(self.FigureCanvas)  
  
        self.StaticText = wx.StaticText(self,-1,label='Show Help String')  
  
        self.SubBoxSizer = wx.BoxSizer(wx.HORIZONTAL)  
        self.SubBoxSizer.Add(self.NavigationToolbar,proportion =0, border = 2,flag = wx.ALL | wx.EXPAND)  
        self.SubBoxSizer.Add(self.StaticText,proportion =-1, border = 2,flag = wx.ALL | wx.EXPAND)  
  
        self.TopBoxSizer = wx.BoxSizer(wx.VERTICAL)  
        self.TopBoxSizer.Add(self.SubBoxSizer,proportion =-1, border = 2,flag = wx.ALL | wx.EXPAND)  
        self.TopBoxSizer.Add(self.FigureCanvas,proportion =-10, border = 2,flag = wx.ALL | wx.EXPAND)  
  
        self.SetSizer(self.TopBoxSizer)  
  
        ###方便调用  
        self.pylab=pylab  
        self.pl=pylab  
        self.pyplot=pyplot  
        self.numpy=np  
        self.np=np  
        self.plt=pyplot  
  
    def UpdatePlot(self):  
        '''''#修改图形的任何属性后都必须使用self.UpdatePlot()更新GUI界面 '''  
        self.FigureCanvas.draw()  
  
    def plot(self,*args,**kwargs):  
        '''''#最常用的绘图命令plot '''  
        self.axes.plot(*args,**kwargs)  
        self.UpdatePlot()  
   
    def semilogx(self,*args,**kwargs):  
        ''''' #对数坐标绘图命令 '''  
        self.axes.semilogx(*args,**kwargs)  
        self.UpdatePlot()  
  
    def semilogy(self,*args,**kwargs):  
        ''''' #对数坐标绘图命令 '''  
        self.axes.semilogy(*args,**kwargs)  
        self.UpdatePlot()  
        
    #----------------------------------------------------------------------
    def plotImg(self, image_path):
        """显示图片"""
        
        image = pyplot.imread(image_path)        
        self.axes.imshow(image)
        #pyplot.show()
        self.UpdatePlot()
        
    #----------------------------------------------------------------------
    def plotHist(self,*args,**kwargs):  #多个数据的 统计显示 plt.hist(x, num_bins, normed=1, facecolor='green', alpha=0.5)
        """直方图绘制"""
        self.axes.hist(*args,**kwargs)
        self.UpdatePlot()
        
    #----------------------------------------------------------------------
    def plotBar(self,*args,**kwargs):  #数据的柱状显示 plt.bar(left = (0,1),height = (1,0.5),width = 0.35,align="center",yerr=0.000001)
                                       #圆形柱状：  bars = ax.bar(theta, radii, width=width, bottom=0.0) 起始角度，横跨角度，竖直长度
        """绘制柱状图"""
        self.axes.bar(*args,**kwargs)
        self.UpdatePlot()
  
    #----------------------------------------------------------------------
    def plotScatter(self,*args,**kwargs): #绘制散点图：plt.scatter(x, y, s=area, alpha=0.5) area为图形
                                         #圆形散点：  c = plt.scatter(theta, r, c=colors, s=area, cmap=plt.cm.hsv)  起点，高度，颜色，大小
        """绘制散点图"""
        self.axes.scatter(*args,**kwargs)
        self.UpdatePlot()
    #----------------------------------------------------------------------
    def plotPie(self,*args,**kwargs): #绘制饼状图：plt.pie(sizes, explode=explode, labels=labels, colors=colors,
                                                               # autopct='%1.1f%%', shadow=True, startangle=90)
        """绘制饼状图"""
        self.axes.pie(*args,**kwargs)
        self.UpdatePlot()
        
    #----------------------------------------------------------------------
    def plotFill(self,*args,**kwargs): #绘制填充图  plt.fill(x, y, 'r') r表示颜色 plt.fill(x, y1, 'b', x, y2, 'r', alpha=0.3)0
        """绘制填充图"""
        self.axes.fill(*args,**kwargs)
        self.UpdatePlot()
    #----------------------------------------------------------------------
    def plotErrorbar(self,*args,**kwargs): #绘制误差线图：ax1.errorbar(x, y, xerr=asymmetric_error, fmt='o')，ax0.errorbar(x, y, yerr=error, fmt='-o')
        """绘制误差线"""
        self.axes.errorbar(*args,**kwargs)
        self.UpdatePlot()
        
        
    def loglog(self,*args,**kwargs):  
        ''''' #对数坐标绘图命令 '''  
        self.axes.loglog(*args,**kwargs)  
        self.UpdatePlot()  
  
    #----------------------------------------------------------------------
    def showAxis(self , flag = "on"):
        """显示 x-，y-axes"""
        if "on" == flag:
            self.axes.axis("on")
        elif "off" == flag:
            self.axes.axis("off")
        elif "equal" == flag:
            self.ax.axis("equal")
            
    def grid(self,flag=True):  
        ''''' ##显示网格  '''  
        if flag:  
            self.axes.grid()  
        else:  
            self.axes.grid(False)  
  
    #----------------------------------------------------------------------
    def setSpine(self , left_flag = "true" , left_ward = 10, right_flag = "False",right_ward = 10, 
                 top_flag = "False",top_ward =10, button_flag = "true", button_ward = 10):
        """设置标尺位置"""
        # Hide the right and top spines
        # Move left and bottom spines outward by 10 points
        if left_flag == "False":
            self.axes.spines['left'].set_visible(False)
        else :
            self.axes.spines['left'].set_position(('outward', left_ward))
        if right_flag == "False":
            self.axes.spines['right'].set_visible(False)
        else:
            self.axes.spines['right'].set_position(('outward', right_ward))
        if top_flag_flag == "False":
            self.axes.spines['top'].set_visible(False) 
        else:
            self.axes.spines['top'].set_position(('outward', top_ward))
        if button_flag_flag == "False":
            self.axes.spines['bottom'].set_visible(False)   
        else:
            self.axes.spines['bottom'].set_position(('outward', bottom_ward))

    def title_MPL(self,TitleString="wxMatPlotLib Example In wxPython"):  
        ''''' # 给图像添加一个标题   '''  
        self.axes.set_title(TitleString)  
  
    def xlabel(self,XabelString="X"):  
        ''''' # Add xlabel to the plotting    '''  
        self.axes.set_xlabel(XabelString)  
  
    def ylabel(self,YabelString="Y"):  
        ''''' # Add ylabel to the plotting '''  
        self.axes.set_ylabel(YabelString)  
  
    #----------------------------------------------------------------------
    def xticks(self,  labels):  #plt.xticks((0,1),(u'男',u'女'))
        """设置x轴的值"""
        self.axes.set_xticklabels( labels)
        
    def xticker(self,major_ticker=1.0,minor_ticker=0.1):  
        ''''' # 设置X轴的刻度大小 '''  
        self.axes.xaxis.set_major_locator( MultipleLocator(major_ticker) )  
        self.axes.xaxis.set_minor_locator( MultipleLocator(minor_ticker) )  
  
    def yticker(self,major_ticker=1.0,minor_ticker=0.1):  
        ''''' # 设置Y轴的刻度大小 '''  
        self.axes.yaxis.set_major_locator( MultipleLocator(major_ticker) )  
        self.axes.yaxis.set_minor_locator( MultipleLocator(minor_ticker) )  
  
    def legend(self,*args,**kwargs):  
        ''''' #图例legend for the plotting  '''  
        self.axes.legend(*args,**kwargs)  
  
    def xlim(self,x_min,x_max):  
        ''''' # 设置x轴的显示范围  '''  
        self.axes.set_xlim(x_min,x_max)  
  
    def ylim(self,y_min,y_max):  
        ''''' # 设置y轴的显示范围   '''  
        self.axes.set_ylim(y_min,y_max)  
  
    def savefig(self,*args,**kwargs):  
        ''''' #保存图形到文件 '''  
        self.Figure.savefig(*args,**kwargs)  
  
    def cla(self):  
        ''''' # 再次画图前,必须调用该命令清空原来的图形  '''  
        self.axes.clear()  
        self.Figure.set_canvas(self.FigureCanvas)  
        self.UpdatePlot()  
          
    def ShowHelpString(self,HelpString="Show Help String"):  
        ''''' #可以用它来显示一些帮助信息,如鼠标位置等 '''  
        self.StaticText.SetLabel(HelpString)  
    
  
###############################################################################  
#  MPL_Frame添加了MPL_Panel的1个实例  
###############################################################################  
class MPL_Frame(wx.Frame):  
    """MPL_Frame可以继承,并可修改,或者直接使用"""  
    def __init__(self,title="MPL_Frame Example In wxPython",size=(800,500)):  
        wx.Frame.__init__(self,parent=None,title = title,size=size)  
  
        self.MPL = MPL_Panel_base(self)  
  
        #创建FlexGridSizer  
        self.FlexGridSizer=wx.FlexGridSizer( rows=9, cols=1, vgap=5,hgap=5)  
        self.FlexGridSizer.SetFlexibleDirection(wx.BOTH)  
  
        self.RightPanel = wx.Panel(self,-1)  
  
        #测试按钮1  
        self.Button1 = wx.Button(self.RightPanel,-1,"TestButton",size=(100,40),pos=(10,10))  
        self.Button1.Bind(wx.EVT_BUTTON,self.Button1Event)  
  
        #测试按钮2  
        self.Button2 = wx.Button(self.RightPanel,-1,"AboutButton",size=(100,40),pos=(10,10))  
        self.Button2.Bind(wx.EVT_BUTTON,self.Button2Event)  
  
        #加入Sizer中  
        self.FlexGridSizer.Add(self.Button1,proportion =0, border = 5,flag = wx.ALL | wx.EXPAND)  
        self.FlexGridSizer.Add(self.Button2,proportion =0, border = 5,flag = wx.ALL | wx.EXPAND)  
  
        self.RightPanel.SetSizer(self.FlexGridSizer)  
          
        self.BoxSizer=wx.BoxSizer(wx.HORIZONTAL)  
        self.BoxSizer.Add(self.MPL,proportion =-10, border = 2,flag = wx.ALL | wx.EXPAND)  
        self.BoxSizer.Add(self.RightPanel,proportion =0, border = 2,flag = wx.ALL | wx.EXPAND)  
          
        self.SetSizer(self.BoxSizer)      
  
        #状态栏  
        self.StatusBar()  
  
        #MPL_Frame界面居中显示  
        self.Centre(wx.BOTH)  
  
  
  
    #按钮事件,用于测试  
    def Button1Event(self,event):  
        self.MPL.cla()#必须清理图形,才能显示下一幅图  

        file_path = u"C:\\Users\\jerryfive\\Desktop\\市县经济1990.xls"
        excel = read_excel.readExcel()
        data = excel.getColData(file_path, [0,1])
        print data
        sizes = data[1][1:]
        labels = data[0][1:]
        left = np.arange(0,len(sizes))
        print left
        print "sizes :", sizes

        print "lables", labels

        #self.MPL.plotHist(x, num_bins, normed=1, facecolor='green', alpha=0.5)
        self.MPL.xticks( labels)
        #self.MPL.plotBar(left = left,height = sizes, width = 1,align="center",yerr=0.000001)
        
        length = len(sizes)
        min
        max1 = max(sizes)
        print max1
        explode = []
        for i in range(length):
            if i/5==0:
                explode.append(0.1)
            else:
                explode.append(0)
        color = []
        for i in range(length):
            if i/2 ==0:
                color.append("gold")
            else:
                color.append("blue")
        #print "explode,", explode
        #plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)        
        
        
        self.MPL.plotPie(sizes, explode=explode, labels=labels, colors=color, autopct='%1.1f%%', shadow=True)
        
        
#数据的柱状显示 plt.bar(left = (0,1),height = (1,0.5),width = 0.35,align="center",yerr=0.000001)
#圆形柱状：  bars = ax.bar(theta, radii, width=width, bottom=0.0) 起始角度，横跨角度，竖直长度

#绘制散点图：plt.scatter(x, y, s=area, alpha=0.5) area为图形
#圆形散点：  c = plt.scatter(theta, r, c=colors, s=area, cmap=plt.cm.hsv)  起点，高度，颜色，大小

#绘制饼状图：plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)

#绘制填充图:  plt.fill(x, y, 'r') r表示颜色  plt.fill(x, y1, 'b', x, y2, 'r', alpha=0.3)0

#绘制误差线图：ax1.errorbar(x, y, xerr=asymmetric_error, fmt='o')，ax0.errorbar(x, y, yerr=error, fmt='-o')
        
        #self.MPL.plotImg(r"C:\Users\jerryfive\Desktop\lunwen_test\dudu.jpg")
        #self.MPL.plot(x,y,'--*g')
        self.MPL.showAxis()
        #self.MPL.xticker(2.0,0.5)  
        #self.MPL.yticker(10,0.1)  
        #self.MPL.ylim(0, 9)
        self.MPL.title_MPL("MPL1")  
        self.MPL.ShowHelpString("You Can Show MPL Helpful String Here !")  
        self.MPL.grid("false")   
        self.MPL.UpdatePlot()#必须刷新才能显示
  
    def Button2Event(self,event):  
        self.AboutDialog()  
  
  
    #打开文件,用于测试  
    def DoOpenFile(self):  
        wildcard = r"Data files (*.dat)|*.dat|Text files (*.txt)|*.txt|ALL Files (*.*)|*.*"  
        open_dlg = wx.FileDialog(self,message='Choose a file',wildcard = wildcard, style=wx.OPEN|wx.CHANGE_DIR)  
        if open_dlg.ShowModal() == wx.ID_OK:  
            path=open_dlg.GetPath()  
            try:  
                file = open(path, 'r')  
                text = file.read()  
                file.close()  
            except IOError, error:  
                dlg = wx.MessageDialog(self, 'Error opening file\n' + str(error))  
                dlg.ShowModal()    
        open_dlg.Destroy()  
  
  
  
    #自动创建状态栏  
    def StatusBar(self):  
        self.statusbar = self.CreateStatusBar()  
        self.statusbar.SetFieldsCount(3)  
        self.statusbar.SetStatusWidths([-2, -2, -1])  
  
  
    #About对话框  
    def AboutDialog(self):  
        dlg = wx.MessageDialog(self, '\twxMatPlotLib\t\nMPL_Panel_base,MPL_Panel,MPL_Frame and MPL2_Frame \n Created by Wu Xuping\n Version 1.0.0 \n 2012-02-01',  
                                'About MPL_Frame and MPL_Panel', wx.OK | wx.ICON_INFORMATION)  
        dlg.ShowModal()  
        dlg.Destroy()  
  

#主程序测试  
if __name__ == '__main__':  
    app = wx.PySimpleApp()  
    #frame = MPL2_Frame()  
    frame =MPL_Frame()  
    frame.Center()  
    frame.Show()  
    app.MainLoop()  
    
    
    
################################################################  
  
#class MPL_Panel(MPL_Panel_base):  
    #''''' #MPL_Panel重要面板,可以继承或者创建实例 '''  
    #def __init__(self,parent):  
        #MPL_Panel_base.__init__(self,parent=parent)  
  
        ##测试一下  
        #self.FirstPlot()  
  
  
    ##仅仅用于测试和初始化,意义不大  
    #def FirstPlot(self):  
        ##self.rc('lines',lw=5,c='r')  
        #self.cla()  
        #x = np.arange(-5,5,0.25)  
        #y = np.sin(x)  
        #self.yticker(0.5,0.1)  
        #self.xticker(1.0,0.2)  
        #self.xlabel('X')  
        #self.ylabel('Y')  
        #self.title_MPL("wxMatPlotLib Example In wxPython")  
        #self.grid()  
        #self.plot(x,y,'--^g')  