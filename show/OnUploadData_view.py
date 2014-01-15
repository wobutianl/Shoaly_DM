# -*- coding: utf-8 -*-
import sys, time, math, os, os.path

import wx
import mongo_bll
_ = wx.GetTranslation
import wx.propgrid as wxpg

import OnDataLink_view

# myself module
import shp2mongoDB
import excel2mongoDB


############################################################################
#
# MAIN PROPERTY GRID TEST PANEL
#
############################################################################

class TestPanel( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__(self, parent, wx.ID_ANY ,size=(700,400) , title = u"数据库上传")
        #self.log = log

        self.panel = panel = wx.Panel(self, wx.ID_ANY)
        #self.SetMinSize((700,400))
        topsizer = wx.BoxSizer(wx.VERTICAL)

        # Difference between using PropertyGridManager vs PropertyGrid is that
        # the manager supports multiple pages and a description box.
        self.pg = pg = wxpg.PropertyGridManager(panel,
                        style=wxpg.PG_SPLITTER_AUTO_CENTER |
                              wxpg.PG_AUTO_SORT |
                              wxpg.PG_DESCRIPTION |
                              wxpg.PG_TOOLBAR)

        # Show help as tooltips
        pg.SetExtraStyle(wxpg.PG_EX_HELP_AS_TOOLTIPS)    

        #
        # Let's use some simple custom editor
        #
        # NOTE: Editor must be registered *before* adding a property that
        # uses it.
        #
        # Add properties
        #

        pg.AddPage( "Page 1 - Testing All" )
        
        pg.Append( wxpg.PropertyCategory("1 - Basic Properties")  )
        
            
        #try:
            #pg.Append( wxpg.EditEnumProperty(u"数据库名","databaseName",
                                                                     #dbValues,
                                                                     #listValues,
                                                                     #"Text Not in List"))  
            #pg.Append( wxpg.EditEnumProperty(u"集合名","collectionName",
                                                                    #dbValues,
                                                                    #listValues,
                                                                    #"Text Not in List"))             
        #except:
            #print "error" #
             
        pg.Append( wxpg.FileProperty(label = u"文件名", name = "fileName", value=r"E:\lab\Data" ))
        #pg.Append( wxpg.StringProperty(u"集合名",name = "pcname" ,value="localhost"))
        
        
        # When page is added, it will become the target page for AutoFill
        # calls (and for other property insertion methods as well)
        

        topsizer.Add(pg, 1, wx.EXPAND)
        # add some button 
        rowsizer = wx.BoxSizer(wx.HORIZONTAL)
        TestBtn = wx.Button(panel,-1,u"连接数据库")
        TestBtn.Bind( wx.EVT_BUTTON, self.OnTestBtn )
        CollectBtn = wx.Button(panel,-1,u"选择聚集")
        CollectBtn.Bind( wx.EVT_BUTTON, self.OnCollectBtn )         
        sureBtn = wx.Button(panel,-1,u"上传")
        sureBtn.Bind( wx.EVT_BUTTON, self.OnSureBtn )        
        CancelBtn = wx.Button(panel,-1,u"取消")
        CancelBtn.Bind( wx.EVT_BUTTON, self.OnCancelBtn )        
        rowsizer.Add((20, 20), 5, 0, 0)
        rowsizer.Add(TestBtn,0,0,0) 
        rowsizer.Add(CollectBtn,0,0,0) 
        rowsizer.Add(sureBtn,0,0,0) 
        rowsizer.Add(CancelBtn,0,0,0)    
        
        topsizer.Add(rowsizer,0,wx.EXPAND)
        
        rowsizer = wx.BoxSizer(wx.HORIZONTAL)
        panel.SetSizer(topsizer)
        topsizer.SetSizeHints(panel)
        #topsizer.SetMinSize((600,300))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        

    #----------------------------------------------------------------------
    def OnCollectBtn(self , event):
        """选择聚集"""
        #dbvalues : database link里面获得  所有数据库 数据
        dbValues = OnDataLink_view.dbValues
        # database link 里面获得的 所有参数的数据
        datalinkValues = OnDataLink_view.datalinkValues
        listValues = OnDataLink_view.listValues    
        # 获得的 选择的数据库名字
        databaseName = OnDataLink_view.databaseName
        self.pg.Append( wxpg.StringProperty(u"数据库名","databaseName",
                                                            databaseName))  
        # 连接数据库 ， 获取聚集
        #聚集的名字
        collections = mongo_bll.getConnection(databaseName)        
        collectList = range(len(collections))
        self.pg.Append( wxpg.EditEnumProperty(u"数据库集合","collectionName",
                                                            collections,
                                                            collectList,
                                                            "Text Not in List"))
            
    #----------------------------------------------------------------------
    def OnTestBtn(self , event ):
        """连接数据库"""
        datalink = OnDataLink_view.OnDataLinkView(None)      
        datalink.Show()        

    #----------------------------------------------------------------------
    def OnSureBtn(self , event):
        """上传数据"""
        filePath = self.pg.GetPropertyValue("fileName")
        dbValues = OnDataLink_view.dbValues
        databaseName = OnDataLink_view.databaseName
        collectName = self.pg.GetPropertyValueAsString("collectionName")     
        #判断 文件后缀名，从而采用不同的上传 方法
        #上传 shp文件
        print os.path.splitext(filePath)[1]
        if ((os.path.splitext(filePath)[1]  == ".shp") or (os.path.splitext(filePath)[1]  == ".SHP")): 
            shp2mongo = shp2mongo.insert_shp_mongo(filePath)
            shp2mongo.InsertShpmongo(databaseName, collectName , "metaDB", collectName)              
            shp2mongo = importShp2Mongodb.insert_shp_mongo(filePath)
            shp2mongo.InsertShpmongo(databaseName, collectName , "metaDB", collectName)  
        #上传 excel 文件
        elif ((os.path.splitext(filePath)[1]  == ".xls") or (os.path.splitext(filePath)[1]  == ".XLS")):
            excel2mongo = importExcel2Mongodb.excel2mongodb()
            excel2mongo.insertAllSheet2mongo(databaseName, filePath)
            
        print "connect to mongodb"    
        
    #----------------------------------------------------------------------
    def OnCancelBtn(self , event):
        """取消按钮"""
        self.Close()
        print "connect to mongodb"
        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = TestPanel(None)

    frame.Show(True)
    app.MainLoop()