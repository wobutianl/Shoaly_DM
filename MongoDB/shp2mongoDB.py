# -*- coding: utf-8 -*-
"""将shp存入mongodb中，不是用wkt的形式，用json的形式（这样可以用空间索引和空间查询）

""""""
Created on Fri Apr 26 09:38:57 2013
@author: Administrator
"""
import os;
import re;
import sys;
import json 
from osgeo import ogr

import mongo_bll

class shp2mongodb:

    shape_path =""   #""r'E:\lab\Data\01shp\china\XianCh_point.shp'""
    
    def __init__(self, shp_path):  #, db, collect 
        self.shape_path = shp_path
        #self.database = db 
        #self.collection = collect
        
    #----------------------------------------------------------------------
    def  insert(self, shp_db, shp_collect, meta_db, meta_collect):
        """"""
        ds = self.getDS()
        meta_data = self.get_metedata(ds)
        self.insertShp2mongo(ds, shp_db, shp_collect, meta_db, meta_collect, meta_data)
        
    #----------------------------------------------------------------------
    def getDS(self):
        """"""
        driver = ogr.GetDriverByName('ESRI Shapefile') 
        ds = driver.Open(self.shape_path, 0) 
        if ds is None: 
            print u'Can not open', ds 
            sys.exit(1) 
        return ds
        
    #get layer just use for get lyr
    #----------------------------------------------------------------------
    def getLyr(self):
        """"""
        ds = self.getDS()
        lyr = ds.GetLayer()
        return lyr
        
    #----------------------------------------------------------------------
    def getFeature(self):
        """"""
        ds = self.getDS()
        lyr = ds.GetLayer()
        feat = lyr.GetNextFeature()
        return feat
    
    def get_metedata(self,ds):  
        """ 插入元数据 到元数据库
        包括四周的范围值 ， 坐标系统 ，数据类型 """   
        lyr = ds.GetLayer() 
        feat = lyr.GetNextFeature()
 
        extent = lyr.GetExtent()
        geom = feat.GetGeometryRef()
        geom_type = geom.GetGeometryName()
        spatialRef = lyr.GetSpatialRef()
        spatialWkt = spatialRef.ExportToWkt()  
       
        metedata = {} 
        metedata["extent"] = extent
        metedata["type"] = geom_type
        metedata["spatialRef"]= spatialWkt       
        return metedata

    #----------------------------------------------------------------------
    def getOneGeomData(self, feat):
        """读取shp的geom 数据"""      
        geom = feat.GetGeometryRef() 
        geom_json = geom.ExportToJson()       
        # store the geometry data with json format 
        geom_data = {}
        geom_data["geom"] =  json.loads(geom_json)        
        return geom_data    
    
    #----------------------------------------------------------------------
    def getGeomData(self, ds):
        """get all geom data"""
        lyr = ds.GetLayer()     
        feat = lyr.GetNextFeature()
        geomValue = []
        while feat:       
            oneGeom = {}            
            geom = feat.GetGeometryRef() 
            geom_json = geom.ExportToJson() 
            # store the geometry data with json format 
            oneGeom['geom'] = json.loads(geom_json)
            feat.Destroy() 
            feat = lyr.GetNextFeature() 
            geomValue.append(oneGeom)
        return geomValue 
    
    #----------------------------------------------------------------------
    def getOneAttributeData(self, feat, feat_defn):
        """get one attribute """
        attri_data  = {}
        for i in range(feat_defn.GetFieldCount()):                
            value = feat.GetField(i) 
            if type(value) != str: 
                value = str(value).decode("utf8")
                #value = str(value)
            field = feat.GetFieldDefnRef(i) 
            fieldname = field.GetName() 
            attri_data[fieldname] = value 
        return attri_data

    #----------------------------------------------------------------------
    def getAttributeData(self, ds):
        """读取shp 的attributes数据"""
        lyr = ds.GetLayer()     
        feat = lyr.GetNextFeature()
        feat_defn = lyr.GetLayerDefn() 
        attriValue = []
        while feat:       
            attri_data  = self.getOneAttributeData(feat, feat_defn)
            feat.Destroy() 
            attriValue.append(attri_data)
            feat = lyr.GetNextFeature() 
        return attriValue

    #----------------------------------------------------------------------
    def  insertShp2mongo(self, ds, shp_db, shp_collect, meta_db, meta_collect, meta_data):
        """把shp 插入 到 db库 和 collect 集合中"""
        lyr = ds.GetLayer()     
        feat = lyr.GetNextFeature()  
        totfeats = lyr.GetFeatureCount() 
        
        meta_data = self.get_metedata(ds)
        mongo_bll.insert(meta_db, meta_collect, meta_data)
        flag = 0
        while feat: 
            mongofeat = {}            
            geom_data = self.getOneGeomData(feat)
            feat_defn = lyr.GetLayerDefn() 
            attri_data = self.getOneAttributeData(feat, feat_defn)
            mongofeat = dict(geom_data , **attri_data)
            
            # insert the feature in the collection     
            mongo_bll.insert(shp_db, shp_collect, mongofeat)

            feat.Destroy() 
            feat = lyr.GetNextFeature() 
        print u'%s features loaded in MongoDb from shapefile.' % lyr.GetFeatureCount() 

    
#input_shape = r'E:\lab\Data\01shp\china\bou2_4p.shp'
#a = shp2mongodb(input_shape,"shp" , "XianCh_point")
#lyr = a.getLayer(input_shape)
#feature = a.getFeature(lyr)
##a.insertShp2mongo()#


#input_shape = r'E:\lab\showdata\js_road\2015rail.shp'
#a = shp2mongodb(input_shape)
#ds = a.getDS()
#b = a.insertShp2mongo(ds)

#b = a.getGeomData(ds)
#for c in b:
    #print c
#ds = a.getLayer()
#a.insert_metedata(ds, "meta_db", "meta_collection")
#mongodb_server = 'localhost' 
#mongodb_port = 27017 
#mongodb_db = 'gisdb' 
#mongodb_collection = 'xqpoint' 



#collection = a.collection()
#mete = mongo_connect('metedata','xqpoint', 'false')
#mete_collection = mete.collection()

#b = shp2mongodb(input_shape ,"gisdb" , "XianCh" )
#attri = b.readShpAttributes()
#print attri
#for a in attri:  
    #print a
#b.InsertShpmongo("gisdb" , "XianCh" , "metedata" , "XianCh")