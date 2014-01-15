# -*- coding: utf-8 -*-
import mongo_bll
'''
Created on 2014-1-3
class mongoInsert
@author: tree
'''
__metaclass__ = type

import os
from pymongo.database import Database
import time
import gridfs
#import gdal

class mongoImg(object):
    """mongoInsert is a class for inserting document
    
    """
    def __init__(self, database, dir):
        """Create a new instance of :class:mongoInsert
        :Parameters:
          - `database`: database to use
          - `dir` : directory of document 
          """
        if not isinstance(database, Database):
            raise TypeError("database must be an instance of Database")
        if len(dir) < 1:
            raise TypeError("dir must be an string of directory")
        
#         self.__con = Connection()
        self.__imgdb = database
        self.__imgfs = gridfs.GridFS (self.__imgdb)
        self.__dir = dir
        self.__filelist=[]

    #save filepath in list.txt
    def __dirwalk(self,topdown=True):
        """traverse the documents of self.__dir and save in self.__filelist
        """
        sum=0
        #self.__filelist.clear()
        
        for root,dirs,files in os.walk(self.__dir,topdown):
            for name in files:
                sum+=1
                temp=os.path.join(root,name)
                self.__filelist.append(temp)
        print(sum)

    #insert image 
    def insert(self):
        """insert images in mongodb
        """
        self.__dirwalk()

        tStart = time.time()        
        for fi in self.__filelist:       
            with open (fi,'rb') as myimage:
                data=myimage.read() 
                name = fi.split("\\")[-1]
                self.__imgfs.put(data, content_type = "tif", filename =name)
    
        tEnd =time.time ()
        print ("It cost %f sec" % (tEnd - tStart))
        
    #get image by filename
    def getbyname(self,filename,savepath):
        """get img from mongdb by filename
        """
        if len(savepath) < 1:
            raise TypeError("dir must be an string of directory")
        dataout=self.__imgfs.get_version(filename)
        try:
            imgout=open(savepath,'wb')
            data=dataout.read()            
            imgout.write(data)
        finally:
            pass
            #imgout.close()
            
            
            
from pymongo import Connection


filedir=r'E:\lab\Paper\Data\data\1990.tif'
con = Connection()
db = con.imgdb
imgmongo=mongoImg(db,filedir)
#imgmongo.insert()
imgmongo.getbyname("1990dafeng.tif", filedir)