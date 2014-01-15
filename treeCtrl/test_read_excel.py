# -*- coding: utf-8 -*- 
import os;
import re;
import sys;
import  xdrlib 
import xlrd
import xlwt

"""excel里面有：多个sheet 
我要做什么？
    1：读取每个sheet 的名字
    2：读取每个sheet中的属性
    3：每个sheet生成一个集合，      #存入mongodb
    4：每个excel生成一个数据库，    #存入mongodb
    
生成excel，或者与shp，raster融合？"""
########################################################################
class readExcel:
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        
    def open_excel(self , file= 'file.xls'):
        try:
            data = xlrd.open_workbook(file)
            return data
        except Exception,e:
            print str(e)
    
    #----------------------------------------------------------------------
    def getSheetNames(self , data):
        """获取每个sheet的名字"""
        a = data.sheet_names()
        return len(a) , a
    
    #----------------------------------------------------------------------
    def getSheetNum(self , file = 'file.xls'):
        """获取多少个sheet"""
        data = self.open_excel(file)
        return data.nsheets

    #----------------------------------------------------------------------
    def getRowNum(self, file_path, sheetIndex = 0):
        """多少行"""
        data = self.open_excel(file_path)       
         
        table = data.sheets()[sheetIndex]
        nrows = table.nrows #行数     
        return nrows

    #----------------------------------------------------------------------
    def getColNum(self, file_path, sheetIndex = 0):
        """多少列"""
        data = self.open_excel(file_path)       
         
        table = data.sheets()[sheetIndex]
        ncols = table.ncols #行数           
        return ncols
    
    #----------------------------------------------------------------------
    def getSheetNameByIndex(self , data , n):
        """获取sheet名，通过索引"""
        a = data.sheet_names()
        return  a[n]
     
    def getFileName(self , filepath):
        'Validate shapefile extension'
        filenamewithextention = os.path.basename(filepath) 
        filename = filenamewithextention.split(r".")[0]
        return filename
    
    #----------------------------------------------------------------------
    def getColData(self, file_path, col_num, sheetIndex = 0):
        """获取某列，或者几列数据"""
        data = self.open_excel(file_path)       
        table = data.sheets()[sheetIndex]
        
        if type(col_num) == int:
            col_data =  table.col_values(col_num) #某一行数据    
            return col_data
        else:
            col_data = []
            for i in col_num:
                data =  table.col_values(i)
                col_data.append(data)
            return col_data        

    
    #----------------------------------------------------------------------
    def getRowData(self, file_path, Row_num , sheetIndex = 0):
        """获取某行，或者某几行数据"""
        data = self.open_excel(file_path)       
        table = data.sheets()[sheetIndex]
        
        if type(Row_num) == int:
            row_data =  table.row_values(Row_num) #某一行数据    
            return row_data
        else:
            row_data = []
            for i in Row_num:
                data =  table.row_values(i)
                row_data.append(data)
            return row_data

    #----------------------------------------------------------------------
    def getAllData(self, file_path , sheetIndex = 0,colIndex=0):
        """获取excel的所有数据"""
        data = self.open_excel(file_path)       
        table = data.sheets()[sheetIndex]
        nrows = table.nrows #行数
        ncols = table.ncols #列数
        colnames =  table.row_values(colIndex) #某一行数据  实际上是获取第一行的数据也就是 属性名
    
        oneSheetData =[]    
        for rownum in range(1,nrows):
            row = table.row_values(rownum)
            if row:
                app = {}
                for i in range(len(colnames)):
                    app[colnames[i]] = row[i]
                oneSheetData.append(app)        
        return oneSheetData
    
    #根据索引获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的索引  ，by_index：表的索引
    def insertExcel(self , file= 'file.xls',colnameindex=0,by_index=0):
        data = self.open_excel(file)
        sheetname = self.getSheetNameByIndex(data, by_index)
         
        table = data.sheets()[by_index]
        nrows = table.nrows #行数
        ncols = table.ncols #列数
        colnames =  table.row_values(colnameindex) #某一行数据  实际上是获取第一行的数据也就是 属性名
    
        list =[]    
        for rownum in range(1,nrows):
            row = table.row_values(rownum)
            if row:
                app = {}
                for i in range(len(colnames)):
                    app[colnames[i]] = row[i]
                #print app
                list.append(app)

        
    #excel_table_byindex(r"C:\Users\Administrator\Desktop\townEconomy1990.xls")
    
    #根据名称获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_name：Sheet1名称
    def excel_table_byname(self , file= 'file.xls',colnameindex=0,by_name=u'Sheet1'):
        data = open_excel(file)
        table = data.sheet_by_name(by_name)
        nrows = table.nrows #行数 
        colnames =  table.row_values(colnameindex) #某一行数据 
        list =[]
        for rownum in range(1,nrows):
                row = table.row_values(rownum)
                if row:
                    app = {}
                    for i in range(len(colnames)):
                        app[colnames[i]] = row[i]
                    list.append(app)
        return list



if __name__=="__main__":

    a = readExcel()
    file_path = r"C:\Users\jerryfive\Desktop\xlrd-0.9.2\tests\Formate.xls"
    a.open_excel(file_path)
    data2 = a.getRowData(file_path, 0)
    print data2
    data = a.getAllData(file_path)
    print data 
    #a.open_excel(r"C:\Users\Administrator\Desktop\townEconomy1990.xls")
    #a.insertAllSheet2mongo(file =r"C:\Users\Administrator\Desktop\townEconomy1990.xls" )
    

        
        
        
    
    
        