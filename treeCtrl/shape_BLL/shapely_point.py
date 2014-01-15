# -*- coding: utf-8 -*-
from matplotlib import pyplot
import ogr
from shapely.wkb import loads
from figures import SIZE, BLUE, GRAY

##########
#可以通过 shp文件来画出shp图
#也可以通过shp点数据，来画图
#############

COLOR = {
    True:  '#6699cc',
    False: '#ff3333'
    }
  
def v_color(ob):
    return COLOR[ob.is_valid]
  
def plot_coords(ax, ob ,color ="black"):
    x, y = ob.xy
    ax.plot(x, y, '^', color=color , zorder=2)
    
#----------------------------------------------------------------------
def plotShpByFile(ax , file_path):
    """"""
    fig = pyplot.figure(1, figsize=SIZE, dpi=90)
    ax = fig.add_subplot(111)
    source = ogr.Open(file_path)
    
    layer = source.GetLayerByIndex(0)
    
    ax = fig.add_subplot(111)
    feature = layer.GetNextFeature()
    geom = feature.GetGeometryRef()
    geom_type = geom.GetGeometryName()       
    
    while 1:
        feature = layer.GetNextFeature()       
        if not feature:
            break
        try:
            geom = loads(feature.GetGeometryRef().ExportToWkb())
            plot_coords(ax, geom)     
        except:
            print "error"    

#----------------------------------------------------------------------
def plotShpByData(ax, geoms):
    """plot line shp by data"""
    n = len(geoms)
    if n == 1:
        plot_coords(ax, geom)
    else:
        for geom in geoms:
            plot_coords(ax, geom)
        
#----------------------------------------------------------------------
def getShpData(file_path):
    """get line shp file"""
    source = ogr.Open(file_path)
    layer = source.GetLayerByIndex(0)
    
    geoms = []
    while 1:
        feature = layer.GetNextFeature()
        if not feature:
            break
        try:
            geom = loads(feature.GetGeometryRef().ExportToWkb())
            geoms.append(geom)  
        except:
            print "error"    
    return geoms


#plotShpByData(r"E:\lab\Data\01shp\china\XianCh_point.shp")
#plotShpByFile(r"E:\lab\Data\01shp\china\XianCh_point.shp")
#source = ogr.Open(r"E:\lab\Data\01shp\china\XianCh_point.shp")
# 1: valid ring

#ring = LinearRing([(0, 0), (0, 2), (1, 1), (2, 2), (2, 0), (1, 0.8), (0, 0)])
  
#plot_coords(ax, ring)
#plot_line(ax, ring)
  

  
#xrange = [70,130]
#yrange = [0, 60]
#ax.set_xlim(*xrange)
#ax.set_xticks(range(*xrange) + [xrange[-1]])
#ax.set_ylim(*yrange)
#ax.set_yticks(range(*yrange) + [yrange[-1]])
#ax.set_aspect(1)
  
  

#----------------------------------------------------------------------
#def plotShpByData(geoms):
    #"""plot line shp by data"""
    ##geoms = getShpData(file_path)
    
    ##fig = pyplot.figure(1, figsize=SIZE, dpi=90)
    ##ax = fig.add_subplot(111)   
    
    #n = len(geoms)
    #if n == 1:
        #plot_coords(ax, geom)
    #else:
        #for geom in geoms:
            #plot_coords(ax, geom)
    
    ##ax.set_title(u'Vera中文 valid')
    ##pyplot.show()    
  