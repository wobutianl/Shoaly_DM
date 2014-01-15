# -*- coding: utf-8 -*-  
import pymongo
from pymongo import Connection
from pymongo import ASCENDING, DESCENDING   
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
    
#update record  return bool
#----------------------------------------------------------------------
def update(database_name, collection_name, match_dict={}, show_dict={}):
    """"""
    collect = getCollection(database_name, collection_name)
    collect.update(match_dict, show_dict)
    #return record    
   
#delete DB
#----------------------------------------------------------------------
def deleteDB(database_name):
    """"""
    db = getDB(database_name)
    db.remove()   
    
#delete collection
#----------------------------------------------------------------------
def deleteCollection(database_name, collection_name):
    """"""
    db = getDB(database_name)
    db.drop_collection(collection_name)
    
#delete record
#----------------------------------------------------------------------
def deleteRecord(database_name, collection_name, match_dict={}):
    """"""
    collect = getCollection(database_name, collection_name)
    collect.remove(match_dict)    
    
#############################################################
###   other BLL 
###   get collection keys ,  create index (space index)
#############################################################
#----------------------------------------------------------------------
def createIndex(database_name, collection_name, attri_list=[]): #attri_list: [("mike", pymongo.DESCENDING),("eliot", pymongo.ASCENDING)]
    """"""
    collect = getCollection(database_name, collection_name)
    collect.create_index(attri_list)
    
#----------------------------------------------------------------------
def create_spaceIndex(database_name, collection_name):
    """"""
    collect = getCollection(database_name, collection_name)
    collect.create_index([("geom.coordinates", pymongo.GEO2D)])
    
#create_index("img","06")
#create space index 


#kwargs = {"_id":0}
#sort_list = ("yoff")
#string = find("img","06", {}, kwargs , sort_list)
#for one in string :
    #print one