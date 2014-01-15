# -*- coding: utf-8 -*-
import sys, os
import gettext
import wx
import json

from shapely.geometry import mapping ,shape
sys.path.append(r"E:\Test\wxGlade\second_one\inspection\shapely");
from shapely import shapely_point000
from shapely import shapely_BLL
import OnDataLink
import extract_view

#获取抽取的线数据
#----------------------------------------------------------------------
def getData():
    """"""
    dataLink = OnDataLink.mongo_connect()
    dataLink.connection()
    data = dataLink.getStatementValue("shapefile","XianCh_point",{"Shape_Leng":{"$in":[2.15924533155,2.34103297023,2.92512052025]} } ,{"geom":1,"_id":0} )    
    return data

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
    
#绘制
#----------------------------------------------------------------------
def plot(data):
    """"""
    shape_line = shapely_linestring000.shapely_linestring()
    for lineData in data:
        dataGeom =  lineData["geom"]
        a =  json.dumps(dataGeom)
        q = shape(json.loads(a))           
        shape_line.plot_line(q)
    shape_line.plotLines()    
    
#组合绘制
#----------------------------------------------------------------------
def plotLine():
    """"""
    try:
        data = getExtractData()
        plot(data)
    except:
        print "plot line error"
        
    
if __name__ == "__main__":
    #gettext.install("app") # replace with the appropriate catalog name
    
    dataLink = OnDataLink.mongo_connect()
    dataLink.connection()
    data = dataLink.getStatementValue("shapefile","XianCh_point",{"NAME":{"$in":["漠河县","呼玛县","额尔古纳左旗","鄂伦春自治旗"]}},{"geom":1,"_id":0} )
    shape_point = shapely_point000.shapely_point000()
    for pointData in data:
        dataGeom =  pointData["geom"]
        a =  json.dumps(dataGeom)
        q = shape(json.loads(a))           
        shape_point.plot_point(q)
    shape_point.plot()
    
    
    #shape_line = shapely_linestring000.shapely_linestring000()
    #for a in data :
        #b = a["geom"]
        #shape_line.plotLineString(b)
    #shape_line.plot([0,20,0,20])
        
    
