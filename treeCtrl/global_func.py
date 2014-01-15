# -*- coding: utf-8 -*-
import shapely
import shapely.geometry
import shapely.ops
_basegeom = shapely.geometry.base.BaseGeometry
import pysal
from shapely.wkb import loads
import ogr
import global_ID as ID

from shapely.geometry import Polygon,base

__all__ = ["printa", "to_wkb", "to_wkt", "area", "distance", "length", "boundary", "boundaryValue", "getLastExtent", "centroid", "centroidPoint", "representative_point", "convex_hull", "envelope", "buffer", "simplify", "difference", "intersection", "symmetric_difference", "union", "unary_union", "cascaded_union", "has_z", "is_empty", "is_ring", "is_simple", "is_valid", "relate", "contains", "crosses", "disjoint", "equals", "intersects", "overlaps", "touches", "within", "equals_exact", "almost_equals", "project", "interpolate"]

#----------------------------------------------------------------------
def printa(text):
    """test"""
    print text
  
global func_list 
#func_list = {ID.ID_FILE_SHP: printa}

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

# shp 质心  
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
 
import json
from shapely.geometry import mapping, shape

if __name__=='__main__':
    #step 0, create 2 points
    #pt1 = pysal.cg.shapes.Point((0,0))
    #pt2 = pysal.cg.shapes.Point((10,10))
    #o = pysal.open('step0.shp','w')
    #o.write(pt1)
    #o.write(pt2)
    #o.close()
  
    #step 1, buffer 2 points
    #b1 = buffer(pt1,10)
    #b2 = buffer(pt2,10)
    #print area(b1)
    #print length(b2)
    
    polygon = Polygon([(0, 0), (1, 1), (1, 0)])
    data = "{'type': 'Polygon', 'coordinates': [[[-245946.52616690792, 4691467.454085786], [-242328.88116664492, 4689766.020711581], [-236874.04193105723, 4687043.289454822], [-232967.49188609782, 4686035.973609137], [-229952.0670412617, 4685466.556249501], [-226099.934177477, 4684904.0479922015], [-221985.99334840223, 4683208.899139431], [-219207.44448567973, 4681751.249328275], [-216754.95515687007, 4678564.328296977], [-217651.58643884302, 4675054.722623017], [-219241.41984765846, 4671687.686224567], [-218511.9796756474, 4668239.5295029385], [-218512.2398336545, 4663898.4582502], [-219018.38065251202, 4660637.339950528], [-217448.10257590126, 4657097.145796055], [-217796.273405904, 4652998.862631587], [-217267.19784413624, 4649844.818796451], [-216236.68908667317, 4646102.334126126], [-214133.38176898137, 4643454.2018077215], [-211934.32311562652, 4641250.908875023], [-209288.50436581636, 4638755.295812046], [-208788.0929957961, 4633971.418925177], [-206867.57452199652, 4630186.528115618], [-204032.3687577267, 4628482.412684236], [-199927.034512906, 4628072.859785343], [-196306.55032440723, 4626870.334100238], [-193287.70130969174, 4622304.688845129], [-192748.35656621912, 4618557.304643852], [-191945.46972104596, 4613429.345611869], [-191847.108073671, 4609430.173663308], [-194626.20193190168, 4606195.131646889], [-199482.29991729587, 4603189.685102238], [-204289.08806000443, 4604136.479041956], [-209228.97959211783, 4603798.509664984], [-214005.68525493608, 4602278.116235613], [-218246.53379591505, 4601404.02730325], [-222938.39453798268, 4600972.348098653], [-228013.1079498254, 4599451.487020103], [-231566.08086147954, 4598831.176579186], [-234864.2103232798, 4597621.361826913], [-237252.50501410363, 4594442.252031336], [-240682.34342095538, 4591552.375083827], [-245703.86777269386, 4589442.019552752], [-249326.15911622162, 4586944.825281709], [-253210.88110909396, 4588500.987211747], [-256382.53422690378, 4589171.326730257], [-259513.02526791644, 4590682.06448286], [-262750.0058345113, 4592884.86233055], [-265483.3417580865, 4594250.597163879], [-268456.2356342471, 4594824.966082635], [-271719.21879844076, 4594804.426116667], [-276372.10469375685, 4595369.882415638], [-280134.7885629848, 4595940.514018536], [-281890.880888479, 4593410.864206387], [-284995.8164172827, 4592306.318768196], [-286752.1091855451, 4595063.285434855], [-290515.019809061, 4595487.096941796], [-294011.6411371402, 4594085.142189012], [-296612.0870386044, 4591996.547828353], [-299762.8597654637, 4590349.839668014], [-303366.9914433359, 4589738.894990095], [-306880.5445605347, 4590067.395482048], [-306170.2177921786, 4593480.204184927], [-304330.6595943138, 4597836.357664428], [-302832.8923978228, 4601647.509387157], [-300138.19771614514, 4604278.424256401], [-297739.10422162566, 4606909.008023548], [-297087.20735263056, 4611159.458954516], [-298359.5859953857, 4615005.150688346], [-299239.560065885, 4619346.585778988], [-300513.731222292, 4623734.365358431], [-303847.9706362222, 4626433.440299634], [-305951.08008532476, 4629434.878381551], [-302955.8207981311, 4631424.392623642], [-299260.85580317985, 4632479.744544928], [-295427.23043357, 4634572.695445708], [-294811.7476234677, 4637389.428326893], [-295185.846581062, 4640497.55935068], [-295026.1511927261, 4644545.640128898], [-295266.17566978186, 4649085.635399165], [-294946.09909190057, 4651949.12179126], [-294634.2618275535, 4655553.5534688365], [-294127.7291947339, 4659503.889520438], [-289567.0082149985, 4662670.920262029], [-283450.17849211843, 4656339.155977803], [-275317.89705335215, 4659436.459142331], [-273138.14365083026, 4657833.718635341], [-270285.773670824, 4655726.54170177], [-265219.7551916152, 4655479.873037089], [-262966.4849980321, 4656454.809326453], [-261395.06144741617, 4662283.40982023], [-257113.62589791193, 4669104.183697103], [-251654.86978549403, 4672783.5807021735], [-244153.70513492945, 4679837.277870939], [-252895.1330824239, 4692086.788701184], [-249356.35078315952, 4692134.454270597], [-245946.52616690792, 4691467.454085786]]]}"
    #shp_link = r'E:\lab\Paper\Data\triangle\china_town.shp'
    
    s = shape(json.loads('{"type": "Point", "coordinates": [0.0, 0.0]}'))
    #s = shape(json.loads(data))
    print s
    
    #shape = pysal.cg.shapes.asShape(data["geom"])
    #shape = base.geom_from_wkb(str(data["geom"]))
    #print shape
    
    #shp = pysal.open(shp_link)
    #print shp.header
    #print shp[0]
    #for i in shp:
        #print i.centroid
    #pysal.cg.shapes.asShape(data["geom"])
    #poly_collect = viz.map_poly_shp(shp_link)

    
    
    
    
  
    #step 2, intersect 2 buffers
    
    #shapely_poly = shapely_polygon000.shapely_polygon000("polygon")
    #source = ogr.Open(r"E:\lab\Paper\Data\jiangsu_shp\JS_city.shp")
    #borders = source.GetLayerByName("JS_city")    
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
            #print feature.GetGeometryRef()
            
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
  