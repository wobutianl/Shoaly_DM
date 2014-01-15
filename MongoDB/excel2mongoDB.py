# -*- coding: utf-8 -*- 
import os;
import sys;

import read_excel
import mongo_bll

"""excel里面有：多个sheet 
我要做什么？
    3：每个sheet生成一个集合，存入mongodb
    4：每个excel生成一个数据库，存入mongodb
    
生成excel，或者与shp，raster融合？"""
########################################################################
class excel2mongodb:
    """"""
    #----------------------------------------------------------------------
    def __init__(self, file_path):
        """Constructor"""
        self.file_path = file_path
        self.readExcel = read_excel.readExcel(self.file_path)
        
    #----------------------------------------------------------------------
    def insetOneSheet2mongoDB(self, db, sheetIndex = 0):
        """choose one sheet to insert to mongodb"""
        sheetname = self.readExcel.getSheetNameByIndex(sheetIndex)
        #print sheetname
        sheetData = self.readExcel.getOneSheetData(sheetIndex)
        #print sheetData
        mongo_bll.insert(db, sheetname, sheetData)        
        
    #----------------------------------------------------------------------
    def insertAllSheet2mongo(self, db):
        """所有sheet插入mongodb"""
        sheetNum = self.readExcel.getSheetNum()       
        i = 0 
        while i < sheetNum:
            sheetname = self.readExcel.getSheetNameByIndex(i)
            sheetData = self.readExcel.getOneSheetData(i)
            mongo_bll.insert(db, sheetname, sheetData)
            i = i + 1
        print "all excel insert succed"
        
  
if __name__=="__main__":
    #pass
    a = excel2mongodb(r"E:\lab\Paper\Data\module\economy2009.xls")
    a.insertAllSheet2mongo("excel_paper")
    #a.insetOneSheet2mongoDB("share_cup")
    