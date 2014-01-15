# -*- coding: utf-8 -*-

"""
Created on Fri Apr 26 09:31:11 2013

@author: Administrator

负责连接到数据库和集合 ，包含，获得数据库， 集合，两个函数
存在问题：
    数据库的操作不完整：
    删除数据库，插入数据，查询数据，修改数据，更新数据，等等。
"""

from pymongo.connection import Connection 

class mongo_connect:
    """
        getDB :获得数据库的名字
        getCollection：获得集合名字   
        getAttri；获取集合中的属性值
    """
    
    #mongodb_server = 'localhost' 
    #mongodb_port = 27017 
    #mongodb_db = 'gisdb' 
    #mongodb_collection = 'XianCh_point' 
    #append1 = 'false'
    filter = ""
    
    #初始化，获得数据库 和 集合名
    def __init__(self ):
        """Constructor"""
        pass
    
    #----------------------------------------------------------------------
    def connection(self , mongodb_server = 'localhost' , mongodb_port = 27017 ):
        """"""
        try:
            self.connect = Connection(mongodb_server, mongodb_port )  
            print "connect"
            return self.connect
        except:
            return False        
        
    #获得数据库       
    
    def database(self , database):
        #print 'Getting database %s' % database 
        connection = Connection( 'localhost' ,  27017 )
        db = connection[database]         
        return db    
    
    #获得集合    
    def collection(self , database , collection):
        #print 'Getting database %s' % database
        connect = self.connection()
        db = self.database(database)
        #print 'Getting the collection %s' % collection 
        collect = db[collection] 
        return  collect
    
    #----------------------------------------------------------------------
    def getCollections(self , dbname):
        """获取某个数据库的所有集合"""
        db = self.connect[dbname] 
        try:
            collect_names = db.collection_names()
            print collect_names
            return collect_names            
        except:
            return None

       
    #----------------------------------------------------------------------
    def getDBs(self):
        """show all db names """  
        try:
            db_names = self.connect.database_names()
            return db_names            
        except:
            return False
        
    #获得所有属性名
    #----------------------------------------------------------------------
    def getAttri(self , dbname , collectname):
        """获取某个集合中的所有属性名"""
        col = self.collection(dbname,collectname)
        single = col.find_one()
        return single.viewkeys()   
    
        
    #获得某个属性的所有属性值
    #----------------------------------------------------------------------
    def getAttriValue(self , dbname , collectname , attribute):
        """获取属性值
        返回 cursor"""
        col = self.collection(dbname,collectname)
        if attribute == "geom" :
            attriValue = col.find({},{attribute:1, "_id":0}).limit(2)
        elif attribute == "_id":
            attriValue = col.find({},{"_id":1}).limit(20)
        else:
            attriValue = col.find({},{attribute:1, "_id":0})
        return attriValue
    
    
        #pass    
    # 根据条件 ， 抽取需要的shp数据
    #----------------------------------------------------------------------
    def getStatementValue(self, dbname , collectname , firstState = {} , secondState = {}, \
                          thirdState1 = "" ,thirdState2 = 100 , fourthState1 = "", fourthState2 = {}):
        """根据statement ， 查询数据 """
        collection = self.collection(dbname,collectname)
        print dbname, collectname
        #value = collection.find({u"市县":{"$in":[u"南京市",u"扬州市"]} , u"年平均人口":{"$gt":200}})
        #value = collection.find({ "name":{"$in":["Nanjingshi","Zhenjiangshi"]} } )

        try:
            if fourthState1 == "":
                if thirdState1=="":
                    if secondState == {}:
                        value = collection.find(firstState )
                    else:
                        value = collection.find(firstState ,secondState)
                elif thirdState1 == "skip":
                    if secondState == {}:
                        value = collection.find(firstState ).skip(thirdState2)
                    else:
                        value = collection.find(firstState ,secondState).skip(thirdState2)                    
                elif thirdState1 == "limit":
                    if secondState == {}:
                        value = collection.find(firstState ).limit(thirdState2)
                    else:            
                        value = collection.find(firstState ,secondState).limit(thirdState2)
                #for a in value:
                    #print a.values()
                return value
            else :
                if thirdState1=="":
                    if secondState == {}:
                        value = collection.find(firstState ).sort(fourthState2)
                    else:
                        value = collection.find(firstState ,secondState).sort(fourthState2)
                elif thirdState1 == "skip":
                    if secondState == {}:
                        value = collection.find(firstState ).skip(thirdState2).sort(fourthState2)
                    else:                   
                        value = collection.find(firstState ,secondState).skip(thirdState2).sort(fourthState2)
                elif thirdState1 == "limit":
                    if secondState == {}:
                        value = collection.find(firstState ).limit(thirdState2).sort(fourthState2)
                    else:                   
                        value = collection.find(firstState ,secondState).limit(thirdState2).sort(fourthState2)                    
                return value
        except:
            print "error"
 

a = mongo_connect()
a.connection()
#a.getStatementValue("shapefile","jiangsu",{ "name":{"$in":["Nanjingshi","Zhenjiangshi"]} })


#b = a.getStatementValue("townEconomy1990", u"人口", {u"市县":{"$in":[u"南京市",u"扬州市"]} , u"年平均人口":{"$gt":200}})
#for c in b :
    #print c
    
