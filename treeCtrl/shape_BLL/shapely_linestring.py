# -*- coding: utf-8 -*-
from matplotlib import pyplot
from osgeo import ogr
from shapely.wkb import loads
from figures import SIZE, BLUE, GRAY

##########
#可以通过 shp文件来画出shp图
#也可以通过shp数据，来画图
#############

COLOR = {
    True:  '#6699cc',
    False: '#ff3333'
    }
  
def v_color(ob):
    return COLOR[ob.is_valid]
  

def plot_line(ax, ob , color = "black",alpha=1,linewidth = 3,solid_capstyle='round', zorder=2):
    x, y = ob.xy
    ax.plot(x, y, color=color , alpha=alpha, linewidth=linewidth, solid_capstyle=solid_capstyle, zorder=zorder)
  

#----------------------------------------------------------------------
def plotShapeByFile(ax , file_path , color = "blue", linewidth = 1):
    """plot line shp file"""  
    source = ogr.Open(file_path)
    layer = source.GetLayerByIndex(0)

    while 1:
        feature = layer.GetNextFeature()
        if not feature:
            break
        try:
            geom = loads(feature.GetGeometryRef().ExportToWkb())
            plot_line(ax, geom,color= color,linewidth=linewidth)     
        except:
            print "error"    

#----------------------------------------------------------------------
def plotShpByData(ax , geoms, color = "black" , linewidth = 1):
    """plot line shp by data"""
    n = len(geoms)
    if n == 1:
        plot_line(ax, geoms, color=color, linewidth=line)
    else:
        for geom in geoms:
            plot_line(ax, geom)
            
#----------------------------------------------------------------------
def plotMultiLineShapeByFile(ax , file_path , color = "blue", linewidth = 1):
    """plot line shp file"""  
    source = ogr.Open(file_path)
    layer = source.GetLayerByIndex(0)

    geoms = []
    while 1:
        feature = layer.GetNextFeature()
        if not feature:
            break
        try:             
            geom = loads(feature.GetGeometryRef().ExportToWkb())
            geom_type = geom.geometryType()
            if (geom_type == "MultiLineString") or (geom_type == "MULTILINESTRING"):
                for line in geom:
                    plot_line(ax, line,color= color,linewidth=linewidth)    
            else:
                plot_line(ax, geom,color= color,linewidth=linewidth)         
        except:
            print "error"    

#----------------------------------------------------------------------
def plotMultiLineShpByData(ax , geoms, color = "black" , linewidth = 1):
    """plot line shp by data"""
    n = len(geoms)
    if n == 1:
        plot_line(ax, geoms, color=color, linewidth=line)
    else:
        for geom in geoms:
            plot_line(ax, geom)
            
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

def getMultiLineData(file_path):
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
            geom_type = geom.geometryType()
            if (geom_type == "MultiLineString") or (geom_type == "MULTILINESTRING"):
                for line in geom:
                    geoms.append(line)
            else:
                geoms.append(geom)  
        except:
            print "error"    
    return geoms

#multiLine_path = r"E:\lab\showdata\js_road\road1990.shp"
#getMultiLineData(multiLine_path)
#plotShapeByFile(r"E:\lab\Data\01shp\china\bou1_4l.shp")
  
#source = ogr.Open(r"E:\lab\Data\01shp\china\bou1_4l.shp")
##borders = source.GetLayerByName("bou1_4l")
#borders = source.GetLayerByIndex(0)




        
        
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
  
  

  
  