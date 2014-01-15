# -*- coding: utf-8 -*-
import shapely
import shapely.geometry
import shapely.ops
_basegeom = shapely.geometry.base.BaseGeometry
import pysal
from shapely.wkb import loads
import ogr
#import shapely_linestring000
#import shapely_polygon000

__all__ = ["to_wkb", "to_wkt", "area", "distance", "length", "boundary", "boundaryValue", "getLastExtent", "centroid","centroidPoint", "representative_point", "convex_hull", "envelope", "buffer", "simplify", "difference", "intersection", "symmetric_difference", "union", "unary_union", "cascaded_union", "has_z", "is_empty", "is_ring", "is_simple", "is_valid", "relate", "contains", "crosses", "disjoint", "equals", "intersects", "overlaps", "touches", "within", "equals_exact", "almost_equals", "project", "interpolate"]
  
# shape 到 wkb   
def to_wkb(shape):
    if not hasattr(shape,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    o = shapely.geometry.asShape(shape)
    return o.to_wkb()
  
# shp 到 wkt 
def to_wkt(shape):
    if not hasattr(shape,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    o = shapely.geometry.asShape(shape)
    return o.to_wkt()
  
# Real-valued properties and methods
# ----------------------------------
# 求 shp 面积
def area(shape):
    if not hasattr(shape,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    o = shapely.geometry.asShape(shape)
    return o.area
  
# 两个shp 之间的距离
def distance(shape, other):
    if not hasattr(shape,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    if not hasattr(other,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    o = shapely.geometry.asShape(shape)
    o2 = shapely.geometry.asShape(other)
    return o.distance(o2)
 
# shp 的长度 
def length(shape):
    if not hasattr(shape,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    o = shapely.geometry.asShape(shape)
    return o.length

# Topological properties
# ----------------------
# shp 的边界 四至 组成的面
def boundary(shape):
    if not hasattr(shape,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    o = shapely.geometry.asShape(shape)
    res = o.bondary
    return pysal.cg.shapes.asShape(res)

# 边界四至 值 
def boundaryValue(shape):
    if not hasattr(shape,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    o = shapely.geometry.asShape(shape)
    return o.bounds

#多个shapes 的 四至值
#----------------------------------------------------------------------
def getLastExtent(extent):
    """extent type is : [[a,b,c,d],[],[],....]"""
    d = zip(*extent)
    ext = []
    ext.append(min(d[0])-1)
    ext.append(min(d[1])-1)
    ext.append(max(d[2])+1)
    ext.append(max(d[3])+1)
    return ext
        

# shp 质心 组成的面  
def centroid(shape):
    if not hasattr(shape,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    o = shapely.geometry.asShape(shape)
    res = o.centroid
    return pysal.cg.shapes.asShape(res)

# shp 质心 组成的面  
def centroidPoint(shape):
    if not hasattr(shape,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    o = shapely.geometry.asShape(shape)
    res = o.centroid
    return res

#  shp 代表点（典型点） 
def representative_point(shape):
    if not hasattr(shape,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    o = shapely.geometry.asShape(shape)
    res = o.representative_point
    return pysal.cg.shapes.asShape(res)

# shp 的凸包 组成的shape  
def convex_hull(shape):
    if not hasattr(shape,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    o = shapely.geometry.asShape(shape)
    res = o.convex_hull
    return pysal.cg.shapes.asShape(res)

# shp 的外包矩形  
def envelope(shape):
    if not hasattr(shape,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    o = shapely.geometry.asShape(shape)
    res = o.envelope
    return pysal.cg.shapes.asShape(res)

# shp 缓冲 +缓冲范围 +  分辨率（也就是光滑度） 
def buffer(shape, radius, resolution=16):
    if not hasattr(shape,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    o = shapely.geometry.asShape(shape)
    res = o.buffer(radius, resolution)
    return pysal.cg.shapes.asShape(res)

# shp 化简 + 容差 +  保留拓扑关系
def simplify(shape, tolerance, preserve_topology=True):
    if not hasattr(shape,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    o = shapely.geometry.asShape(shape)
    res = o.simplify(tolerance, preserve_topology)
    return pysal.cg.shapes.asShape(res)
  
# Binary operations
# -----------------
# shp 求差 与其他shp
def difference(shape, other):
    if not hasattr(shape,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    if not hasattr(other,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    o = shapely.geometry.asShape(shape)
    o2 = shapely.geometry.asShape(other)
    res = o.difference(o2)
    return pysal.cg.shapes.asShape(res)

# shp 与其他shp 求交集  
def intersection(shape, other):
    if not hasattr(shape,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    if not hasattr(other,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    o = shapely.geometry.asShape(shape)
    o2 = shapely.geometry.asShape(other)
    res = o.intersection(o2)
    return pysal.cg.shapes.asShape(res)

#   shp 与其他shp 对称差
def symmetric_difference(shape, other):
    if not hasattr(shape,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    if not hasattr(other,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    o = shapely.geometry.asShape(shape)
    o2 = shapely.geometry.asShape(other)
    res = o.symmetric_difference(o2)
    return pysal.cg.shapes.asShape(res)

# shp 与其他shp 求并  
def union(shape, other):
    if not hasattr(shape,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    if not hasattr(other,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    o = shapely.geometry.asShape(shape)
    o2 = shapely.geometry.asShape(other)
    res = o.union(o2)
    return pysal.cg.shapes.asShape(res)

# 级联求并  
def cascaded_union(shapes):
    o = []
    for shape in shapes:
        if not hasattr(shape,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
        o.append(shapely.geometry.asShape(shape))
    res = shapely.ops.cascaded_union(o)
    return pysal.cg.shapes.asShape(res)

#  shp 一元求并
def unary_union(shapes):
    # seems to be the same as cascade_union except that it handles multipart polygons
    if shapely.__version__ < '1.2.16':
        raise Exception, "shapely 1.2.16 or higher needed for unary_union; upgrade shapely or try cascade_union instead"
    o = []
    for shape in shapes:
        if not hasattr(shape,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
        o.append(shapely.geometry.asShape(shape))
    res = shapely.ops.unary_union(o)
    return pysal.cg.shapes.asShape(res)
  
# Unary predicates
# ----------------
# 是否有 z 值
def has_z(shape):
    if not hasattr(shape,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    o = shapely.geometry.asShape(shape)
    return o.has_z
# 是否为空  
def is_empty(shape):
    if not hasattr(shape,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    o = shapely.geometry.asShape(shape)
    return o.is_empty
# 是否为环  
def is_ring(shape):
    if not hasattr(shape,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    o = shapely.geometry.asShape(shape)
    return o.is_ring
# 是否为简单shp  
def is_simple(shape):
    if not hasattr(shape,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    o = shapely.geometry.asShape(shape)
    return o.is_simple
# 是否正确 
def is_valid(shape):
    if not hasattr(shape,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    o = shapely.geometry.asShape(shape)
    return o.is_valid
  
# Binary predicates 二元判断式
# -----------------
# shp 与其他shp 是否相关
def relate(shape, other):
    if not hasattr(shape,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    if not hasattr(other,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    o = shapely.geometry.asShape(shape)
    o2 = shapely.geometry.asShape(other)
    return o.relate(o2)
# shp 与其他shp 是否包含
def contains(shape, other):
    if not hasattr(shape,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    if not hasattr(other,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    o = shapely.geometry.asShape(shape)
    o2 = shapely.geometry.asShape(other)
    return o.contains(o2)
# shp 与其他shp 是否相交   
def crosses(shape, other):
    if not hasattr(shape,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    if not hasattr(other,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    o = shapely.geometry.asShape(shape)
    o2 = shapely.geometry.asShape(other)
    return o.crosses(o2)
# shp 与其他shp 是否不相交 
def disjoint(shape, other):
    if not hasattr(shape,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    if not hasattr(other,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    o = shapely.geometry.asShape(shape)
    o2 = shapely.geometry.asShape(other)
    return o.disjoint(o2)
# shp 与其他shp 是否相等   
def equals(shape, other):
    if not hasattr(shape,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    if not hasattr(other,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    o = shapely.geometry.asShape(shape)
    o2 = shapely.geometry.asShape(other)
    return o.equals(o2)
# shp 与其他shp 求交 
def intersects(shape, other):
    if not hasattr(shape,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    if not hasattr(other,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    o = shapely.geometry.asShape(shape)
    o2 = shapely.geometry.asShape(other)
    return o.intersects(o2)
# shp 与其他shp 叠加  
def overlaps(shape, other):
    if not hasattr(shape,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    if not hasattr(other,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    o = shapely.geometry.asShape(shape)
    o2 = shapely.geometry.asShape(other)
    return o.overlaps(o2)
# shp 与其他shp 相切  
def touches(shape, other):
    if not hasattr(shape,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    if not hasattr(other,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    o = shapely.geometry.asShape(shape)
    o2 = shapely.geometry.asShape(other)
    return o.touches(o2)
# shp 与其他shp 在……里面 
def within(shape, other):
    if not hasattr(shape,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    if not hasattr(other,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    o = shapely.geometry.asShape(shape)
    o2 = shapely.geometry.asShape(other)
    return o.within(o2)
# shp 与其他shp 在一定容差范围内，是否相等
def equals_exact(shape, other, tolerance):
    if not hasattr(shape,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    if not hasattr(other,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    o = shapely.geometry.asShape(shape)
    o2 = shapely.geometry.asShape(other)
    return o.equals_exact(o2, tolerance)
# shp 与其他shp 在一定精度范围内是否相等 
def almost_equals(shape, other, decimal=6):
    if not hasattr(shape,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    if not hasattr(other,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    o = shapely.geometry.asShape(shape)
    o2 = shapely.geometry.asShape(other)
    return o.almost_equals(o2, decimal)
  
# Linear referencing
# ------------------
# shp A 投影 到 shp B   
def project(shape, other, normalized=False):
    if not hasattr(shape,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    if not hasattr(other,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    o = shapely.geometry.asShape(shape)
    o2 = shapely.geometry.asShape(other)
    return o.project(o2, normalized)
 
#  shp 插值 ， 插值间距 
def interpolate(shape, distance, normalized=False):
    if not hasattr(shape,'__geo_interface__'): raise TypeError, "%r does not appear to be a shape"%shape
    o = shapely.geometry.asShape(shape)
    res = o.interpolate(distance, normalized)
    return pysal.cg.shapes.asShape(res)
  
  
# Copy doc strings from shapely
for method in __all__:
    if hasattr(_basegeom, method):
        locals()[method].__doc__ = getattr(_basegeom,method).__doc__
  
if __name__=='__main__':
    #step 0, create 2 points
    pt1 = pysal.cg.shapes.Point((0,0))
    pt2 = pysal.cg.shapes.Point((10,10))
    #o = pysal.open('step0.shp','w')
    #o.write(pt1)
    #o.write(pt2)
    #o.close()
  
    #step 1, buffer 2 points
    b1 = buffer(pt1,10)
    b2 = buffer(pt2,10)
    #print area(b1)
    #print length(b2)
    #o = pysal.open('step1.shp','w')
    #o.write(b1)
    #o.write(b2)
    #o.close()
  
    #step 2, intersect 2 buffers
    
    #shapely_poly = shapely_polygon000.shapely_polygon000("polygon")
    #source = ogr.Open(r"E:\lab\Data\01shp\china\XianCh_point.shp")
    #borders = source.GetLayerByName("XianCh_point")    
    #bound = borders.GetExtent()
    
    #point2 = pysal.cg.shapes.Point((50.51603999515176, 50.769768023031244))
    #pBuffer = buffer(point2,10)
    #shapely_poly.plotPolygon(pBuffer)
    
    
    #while 1:
        #feature = borders.GetNextFeature()   
        #if not feature:
            #break
        #try:
            #geom = loads(feature.GetGeometryRef().ExportToWkb())
            #pyGeom = pysal.cg.shapes.asShape(geom)
            #geomBuffer = buffer(pyGeom, 0.5) 
            #shapely_poly.plotPolygon(geomBuffer , alph= 0.5)
        #except:
            #print "error"   
            
    #xrange = [int(bound[2]),int(bound[0])]
    #yrange = [int(bound[3]),int(bound[1])]
    #shapely_poly.plot([66,145],[17,63])
    
    
    #i = intersection(b1,b2)
    
    #shapely_poly.plotPolygon(b1, alph=0.5)
    #shapely_poly.plotPolygon(b2, alph=0.5)
    #shapely_poly.plotPolygon(i, alph=1)
    
    #bound1 =  boundaryValue(b1)
    #bound2 = boundaryValue(b2)
    #print bound1
    #shapely_poly.plot([int(bound1[0]) , int(bound2[2])],[int(bound1[1]), int(bound2[3])] )
    
    #o = pysal.open('step2.shp','w')
    #o.write(i)
    #o.close()
  
    ##step 3, union 2 buffers
    #u = union(b1, b2)
    #o = pysal.open('step3.shp','w')
    #o.write(u)
    #o.close()
  
    ##step 4, find convex_hull of union
    #c = convex_hull(u)
    #o = pysal.open('step4.shp','w')
    #o.write(c)
    #o.close()
  