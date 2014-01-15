#-*- encoding:utf-8 -*-

from osgeo import gdal
import numpy
import wx

#----------------------------------------------------------------------
def getDS(file_path):
    """获取ds"""
    ds = gdal.Open(file_path)
    return ds

#----------------------------------------------------------------------
def getRasterBandCount(ds):
    """获取波段数"""
    count = ds.RasterCount
    return count

#----------------------------------------------------------------------
def getRasterBand(ds, num):
    """获取波段"""
    band = ds.GetRasterBand(num)
    return band

#----------------------------------------------------------------------
def getImgSize(ds):
    """获取图像大小"""
    xsize = ds.RasterXSize
    ysize = ds.RasterYSize
    return xsize, ysize

#----------------------------------------------------------------------
def readRaster(ds, xoff, yoff, xsize, ysize, buf_xsize = [], buf_ysize = [], buf_type = '', band_list = []):
    """获取二进制波段数据
    xoff, yoff,  ：读取部分原点位置
    xsize, ysize : 读取部分图片矩形大小
    buf_xsize, buf_ysize : 读取部分缩放
    buf_type: 读取数据类型格式（short , byte)
    band_list: 选择要读取的波段数
    """
    dataRaster = ds.ReadRaster(xoff, yoff, xsize, ysize, buf_xsize, buf_ysize, buf_type, band_list)
    return dataRaster

#----------------------------------------------------------------------
def readAsArray(ds, xoff=0, yoff=0, xsize=None, ysize=None):
    """读取数据（以数组形式）"""
    dataRaster = ds.ReadAsArray(xoff, yoff, xsize, ysize)
    return dataRaster
 
####################
#　对于波段操作
###################
#----------------------------------------------------------------------
def getNoDataValue(band):
    """获取无用值"""
    data = band.GetNoDataValue()
    return data

#----------------------------------------------------------------------
def getMax(band):
    """获取最大值"""
    max = band.GetMaximum()
    return max
#----------------------------------------------------------------------
def getMin(band):
    """获取最小值"""
    min = band.GetMinimum()
    return min

#----------------------------------------------------------------------
def ComputeMinMax(band):
    """获取最大最小值"""
    minMax = band.ComputeRasterMinMax()
    return minMax

def getMinMax(BIL):
    """"""
    BILmax1 = numpy.max(BIL)
    BILmin1 = numpy.min(BIL)
    BILregion1 = BILmax1 - BILmin1	
    return BILmin1, BILmax1, BILregion1
#----------------------------------------------------------------------
def createImg(width , height):
    """新建img图像"""
    image=wx.EmptyImage(width,height)   
    return image

#----------------------------------------------------------------------
def imgColor(image, x, y, R, G, B):
    """给image设置颜色"""
    
    image.SetRGB(x, y , R, G, B)

#----------------------------------------------------------------------
def creatColor(R, G, B):
    """生成颜色"""
    color = wx.Colour(R, G, B)
    return color
    


    
#----------------------------------------------------------------------
def getBitmap(ds, showRect , bandList):
    """
    osgeo.GDAL.Dataset ds
    rectangle showRect
    int[] bandlist"""
    imgWidth = ds.RasterXSize  # 
    imgHeight = ds.RasterYSize
    
    print "img width height", imgWidth, imgHeight
    imgRatio = imgWidth/float(imgHeight)   #影响宽高比
    
    #获取显示控件的大小 （panel）
    boxWidth = showRect["size"][0]
    boxHeight = showRect["size"][1]
    
    boxRatio = boxWidth/float(boxHeight)  #控件的宽高比
    
    bufferWidth = 0
    bufferHeight = 0
    if imgWidth > boxWidth:
	bufferWidth = boxWidth
    elif imgWidth < boxWidth:
	bufferWidth = imgWidth
	
    if imgHeight > boxHeight:
	bufferHeight = boxHeight
    elif imgHeight < boxHeight:
	bufferHeight = imgHeight
	
    #计算实际显示区域大小，防止影响畸变
    #bufferWidth , bufferHeight
    #if boxRatio >= imgRatio:
        #bufferHeight = boxHeight
        #bufferWidth = int(boxHeight * imgRatio)
    #else:
        #bufferHeight = boxWidth
        #bufferWidth  = int(boxHeight*imgRatio)
        
    #构建位图
    bitmap = createImg(imgWidth, imgHeight)
    
    #RGB显示
    if bandList >= 3:
        r =  []   #int[bufferWidth * bufferHeight]
        band1 = ds.GetRasterBand(1)
        r = band1.ReadAsArray(0, 0, bufferWidth, bufferHeight)               #ReadRaster(0,0, imgWidth, imgHeight, r, bufferWidth, bufferHeight, 0, 0) #读取图像到内存
        
        #进行最大最小值拉伸显示
        maxAndMin1 = band1.ComputeRasterMinMax()
        
        g = [] #int[bufferWidth * bufferHeight]
        band2 = ds.GetRasterBand(2)
        g = band2.ReadAsArray(0, 0, bufferWidth, bufferHeight)              #ReadRaster(0,0, imgWidth, imgHeight, g, bufferWidth, bufferHeight, 0, 0) 
        
        #进行最大最小值拉伸显示
        maxAndMin2 = band2.ComputeRasterMinMax()
        
        b =  [] #int[bufferWidth * bufferHeight]
        band3 = ds.GetRasterBand(3)
        b = band3.ReadAsArray(0, 0, bufferWidth, bufferHeight)                 #ReadRaster(0,0, imgWidth, imgHeight, b, bufferWidth, bufferHeight, 0, 0)         
        
        #进行最大最小值拉伸显示
        maxAndMin3 = band3.ComputeRasterMinMax()     
        
	for i in range(0, bufferWidth-1, 1):
	    for j in range(0, bufferHeight-1, 1):
                rVal = r[j][i] #int(r[i + j*bufferWidth])
                rVal = int((rVal - maxAndMin1[0])/(maxAndMin1[1] - maxAndMin1[0])*255)
                
                gVal = g[j][i] #int(g[i + j*bufferWidth])
                gVal = int((gVal - maxAndMin2[0])/(maxAndMin2[1] - maxAndMin2[0])*255)
                           
                bVal = b[j][i] #int(b[i + j*bufferWidth])
                bVal = int((bVal - maxAndMin3[0])/(maxAndMin3[1] - maxAndMin3[0])*255) 

                imgColor(bitmap, i, j, rVal, gVal, bVal)
    else:
        r =  []   # int[bufferWidth * bufferHeight]
        band1 = ds.GetRasterBand(1)
        r = band1.ReadAsArray(0, 0, bufferWidth, bufferHeight) 

        minMax = getMinMax(r)
        
	for hang in range(0, bufferWidth-1 , 1):
	    for lie in range(0, bufferHeight-1 , 1):
		value1 = r[lie][hang]
		value1 = float((value1 - minMax[0]))/minMax[2]*255

		#x = (oringeX + hang*px -extent[0]/2-extent[1]/2)*self.ratio + self.size.width/2
		#y = self.size.height/2 - (oringeY + lie*py - extent[2]/2 - extent[3]/2)*self.ratio 	
		
		imgColor(bitmap, hang, lie, value1, value1, value1)
		#image.SetRGB(hang, lie , value1, value1, value1)
   
    return bitmap        




class MyFrame(wx.Frame):
    
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, u'测试面板Panel', size = (600, 300))
        
	filepath = r"E:\lab\Paper\Data\dafeng\dafengClassify\1975dfmosaic.tif"
	sizer = wx.BoxSizer()
	self.panel = wx.Panel(self, size= (900,600))

	sizer.Add(self.panel, 1, wx.EXPAND)
	self.SetSizerAndFit(sizer)		

	image = self.showImage(filepath)
	
	self.wxbitmap=wx.BitmapFromImage(image) 
	
	self.m_bitmap1 = wx.StaticBitmap(self.panel, wx.ID_ANY,self.wxbitmap, wx.DefaultPosition, wx.DefaultSize , 0 ) 	
        
        #绑定单击事件
        #在Panel上添加Button
        button = wx.Button(self.panel, label = u'打开', pos = (150, 60), size = (30, 30))	
        self.Bind(wx.EVT_BUTTON, self.OnCloseMe, button)
        
    def OnCloseMe(self, event):
	dialog = wx.FileDialog(None, u'打开文件', u'.', u'', u'image File  All Files (*.*)|*.*', style = wx.OPEN )             
	file_path = r"C:\Users\jerryfive\Desktop\07.tiff"
	self.showImage(file_path)
	
	#if dialog.ShowModal() == wx.ID_OK:
	    #file_path = dialog.GetPath()
	    #self.showImage(file_path)
	#dialog.Destroy()
	
    #----------------------------------------------------------------------
    def showImage(self, file_path):
	""""""
	ds = getDS(file_path)
	pictureRect = {}
	pictureRect["x"] = 0
	pictureRect["y"] = 0
	pictureRect["size"] = self.panel.Size
	
	#bandList = [1,2,3]
	bandList = getRasterBandCount(ds)
	image = getBitmap(ds, pictureRect, bandList)
	#image = ShowRaster(ds, bandList)
	return image


if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = MyFrame(parent = None, id = -1)
    frame.Show()
    app.MainLoop()