# -*- coding: utf-8 -*-
from matplotlib import pyplot

from descartes import PolygonPatch
import ogr
from shapely.wkb import loads
from shapely.geometry import polygon
import shapely_BLL
from figures import SIZE, BLUE, GRAY

########################################################################
        

#----------------------------------------------------------------------
def plotPolygon(ax , polygon , fcolor = BLUE, bcolor = BLUE , alph = 1.0):
    """画一个polygon"""
    patch1 = PolygonPatch(polygon, fc=fcolor, ec=bcolor, alpha=alph, zorder=2)
    ax.add_patch(patch1)    
    
#----------------------------------------------------------------------
def setPlotAttri(ax , extent):  #, xrange = [0,20], yrange= [0,20]
    """设置plot属性 并显示"""
    xrange = [int(extent[0]) , int(extent[2])]
    yrange = [int(extent[1]) , int(extent[3])]
    ax.set_xlim(*xrange)
    ax.set_xticks(range(*xrange) + [xrange[-1]])
    ax.set_ylim(*yrange)
    ax.set_yticks(range(*yrange) + [yrange[-1]])
    ax.set_aspect(1)    
    

#----------------------------------------------------------------------
def plotShpByFile(ax , file_path , foreColor = "blue" , ec = "black"):
    """"""
    source = ogr.Open(file_path)
    layer = source.GetLayerByIndex(0)
    extents = []
    while 1:
        feature = layer.GetNextFeature()
        if not feature:
            break
        try:
            geom = loads(feature.GetGeometryRef().ExportToWkb())
            ext = shapely_BLL.boundaryValue(geom) #get every polygon extent
            extents.append(ext)

            patch1 = PolygonPatch(geom, fc=foreColor, ec=ec, alpha=0.5, zorder=2)
            ax.add_patch(patch1) 
        except:
            print "error"   
            
    extent = shapely_BLL.getLastExtent(extents)
    setPlotAttri(ax, extent)

        
        
#showPolygon = shapely_polygon000()
#showPolygon.plotShpByFile(r"E:\lab\Data\5W_GRID.shp")
