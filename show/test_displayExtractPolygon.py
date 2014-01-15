# -*- coding: utf-8 -*-
import sys, os
import gettext
import wx
import json

from shapely.geometry import mapping ,shape
#sys.path.append(r"E:\Test\wxGlade\second_one\inspection\shapely");
from shape_BLL import shapely_polygon000
from shape_BLL import shapely_BLL
import OnDataLink
import extract_view

#获取 extract view 界面返回来的数据
#----------------------------------------------------------------------
def getExtractData():
    """"""
    try:
        extractView = extract_view.MyFrame(None)
        data = extractView.statementValue
        metaData = extractView.metaData
        return data , metaData        
    except:
        wx.MessageDialog(u"没有抽取数据")
    

#从返回的数据中抽取 geom 数据 ，并绘制
#----------------------------------------------------------------------
def plotGeomData(data):
    """"""
    try:
        self.shape_poly = shapely_polygon000.shapely_polygon000()
        self.extents = []
        for dat in data:      
            dataGeom =  dat["geom"]
            geoms.append(dataGeom)
            # 绘制
            
            a =  json.dumps(dataGeom)
            q = shape(json.loads(a))  
            self.shape_poly.plotPolygon(q)
            extent = shape_poly.getExtent(q)
            self.extents.append(extent)    
        #获取四至
        lastExtent = shapely_BLL.getLastExtent(self.extents)
        #显示到画布
        self.shape_poly.plot(lastExtent)
    except:
        wx.MessageDialog(u"绘制失败")
 
#画单个polygon
#----------------------------------------------------------------------
def plotSinglePoylgon(data):
    """"""
    # 绘制
    shapeSinglePoly = shapely_polygon000.shapely_polygon000()
    dataGeom =  dat["geom"]
    geoms.append(dataGeom)
    a =  json.dumps(dataGeom)
    q = shape(json.loads(a))  
    shapeSinglePoly.plotPolygon(q)
    extent = shape_poly.getExtent(q) 
    return extent
    
#----------------------------------------------------------------------
def getExtent(data):
    """"""
    a =  json.dumps(data)
    q = shape(json.loads(a))  
    extent = shape_poly.getExtent(q)
    return extent
    
#----------------------------------------------------------------------
def lastPlotPolygon(extent):
    """"""
    #显示到画布
    self.shape_poly.plot(extent)    
    
# 抽取 + 绘制
#----------------------------------------------------------------------
def displayExtractPolygon():
    """抽取 + 绘制"""
    try:
        data = getExtractData()
        plotGeomData(data)
    except:
        wx.MessageDialog(u"抽取失败 or 绘制失败")
    
#if __name__ == "__main__":
    ##gettext.install("app") # replace with the appropriate catalog name
    
    #dataLink = OnDataLink.mongo_connect()
    #dataLink.connection()
    #data = dataLink.getStatementValue("shapefile","jiangsu",{ "name":{"$in":["Nanjingshi","Zhenjiangshi"]} })
    #geoms = []
    #extents = []
    #shape_poly = shapely_polygon000.shapely_polygon000()
    #for dat in data:      
        #dataGeom =  dat["geom"]
        #geoms.append(dataGeom)
        #shape_poly.plotPolygon(dataGeom)
        #a =  json.dumps(dataGeom)
        #q = shape(json.loads(a))    
        #extent = shape_poly.getExtent(q)
        #print extent
        #extents.append(extent)
        
    #lastExtent = shapely_BLL.getLastExtent(extents)
    
    #shape_poly.plot(lastExtent)

