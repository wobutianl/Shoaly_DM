# -*- coding: utf-8 -*-  
import pymongo
from pymongo import Connection
import os

########################################
####   base BLL model
########################################

#connection to mongodb and return connection
#----------------------------------------------------------------------
def getConnection():
    """""" 
    connection = Connection("localhost", 27017)
    return connection

#get DB and return db
#----------------------------------------------------------------------
def getDB(database_name):
    """"""   
    connection = getConnection()
    db = connection[database_name]
    return db

#get collection and return 
#----------------------------------------------------------------------
def getCollection(database_name, collection_name):
    """"""
    db = getDB(database_name)
    collection = db[collection_name]
    return collection

#get all db_names  return list
#----------------------------------------------------------------------
def getDB_names():
    """"""
    conn = getConnection()
    db_names = conn.database_names()
    return db_names

#get all collection_names in one db return list
#----------------------------------------------------------------------
def getCollect_names(database_name):
    """"""
    db = getDB(database_name)
    collect_names = db.collection_names()
    return collect_names

#check the num in the collect return int 
#----------------------------------------------------------------------
def getRecordNumInCollect(database_name, collection_name):
    """"""
    collect = getCollection(database_name, collection_name)
    record_num = collect.count()
    return record_num
    
#获得所有属性名
#----------------------------------------------------------------------
def getAttriName(database_name, collection_name):
    """获取某个集合中的所有属性名"""
    collect = getCollection(database_name, collection_name)
    single = collect.find_one()
    return single.viewkeys()  

#获得某个属性的所有属性值
#----------------------------------------------------------------------
def getAttriValue(database_name, collection_name , attribute):
    """获取属性值    返回 cursor"""
    col = getCollection(database_name, collection_name)
    if attribute == "geom":
        attriValue = col.find({},{"geom.type":1 , "_id":0}).limit(20)
        return attriValue
    elif attribute == "_id":
        attriValue = col.find({},{"_id":1}).limit(20)
        return attriValue
    else:
        attriValue = col.find({},{attribute:1, "_id":0}).limit(50)
        return attriValue
    
#print getAttriValue("shapefile", "jiangsu", "_id")   
#print getRecordNumInCollect("img", "06")


########################################
###  CRUD  BLL  index
########################################
#insert data into mongoDB 
#----------------------------------------------------------------------
def insert(database_name, collection_name, data):
    """"""
    #db = getDB(database_name)
    collect = getCollection(database_name, collection_name)
    collect.insert(data)
    
#----------------------------------------------------------------------
def inserts(collect, data):
    """"""
    collect.insert(data)
    
# find one record in collect return bson
#----------------------------------------------------------------------
def find_one(database_name, collection_name , match_dict={}, show_dict={}):
    """"""
    collect = getCollection(database_name, collection_name)
    one_record = collect.find_one(match_dict, show_dict)
    return one_record
    
# find match count return int
#----------------------------------------------------------------------
def matchCount(database_name, collection_name, match_dict={}, show_dict={}):
    """"""
    collect = getCollection(database_name, collection_name)
    count = collect.find(match_dict, show_dict).count()
    return count
    
#find all record in collect return list
#----------------------------------------------------------------------
def find(database_name, collection_name, match_dict={}, show_dict={} , sort_list=(), limit = 0):
    """"""
    collect = getCollection(database_name, collection_name)
    length = len(sort_list)
    if length == 0 and limit == 0 :
        record = collect.find(match_dict, show_dict)
    elif length == 0 and limit != 0:
        record = collect.find(match_dict, show_dict).limit(limit)
    elif length !=0 and limit == 0 :
        record = collect.find(match_dict, show_dict).sort(sort_list)
    elif length !=0 and limit != 0:
        record = collect.find(match_dict, show_dict).sort(sort_list).limit(limit)
    return record

import csv
import datetime
#----------------------------------------------------------------------
def get_jjzx_data(path = r"D:\baiduyundownload\2000W\1-200W.csv"):
    """"""
    jjzx_file = csv.DictReader(open(path, mode="rU"))

    collect = getCollection("hanting", "hanting")

    flag = 0 
    i = 1 
    j = 1
    start = datetime.datetime.now()
    for data in jjzx_file:  
        if flag == 0 and i < 250000:
            i += 1
            try:
                inserts(collect, data)
            except:
                flag = 1
        elif i>= 250000:
            end = datetime.datetime.now()
            interval = (end - start).seconds
            print interval
            i = 1
            j += 1
            print j
            database = "hanting" + str(j)
            collect = getCollection(database, "hanting")  
        else:
            flag = 0
            continue

get_jjzx_data()
#count = matchCount("hotel", "jjzx2")
#print count