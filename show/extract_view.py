# -*- coding: utf-8 -*-
#  时间 + 属性数据抽取
import sys, time, math, os, os.path

import wx
import gettext

import mongo_bll
_ = wx.GetTranslation
import wx.propgrid as wxpg
import OnDataLink_view

############################################################################
#
# computer PROPERTY GRID TEST PANEL
#
############################################################################

global statementValue
global metaData

class MyFrame(wx.Frame):
    def __init__( self, parent ):
	wx.Frame.__init__(self, parent, wx.ID_ANY ,size=(700,500) , title = u"数据抽取")
	#################panel1 
        self.panel_1 = wx.Panel(self, wx.ID_ANY)
        topsizer = wx.BoxSizer(wx.VERTICAL)	
        # Difference between using PropertyGridManager vs PropertyGrid is that
        # the manager supports multiple pages and a description box.
        self.pg = pg = wxpg.PropertyGridManager(self.panel_1,
                        style=wxpg.PG_SPLITTER_AUTO_CENTER |
                              wxpg.PG_AUTO_SORT |                              
                              wxpg.PG_TOOLBAR)
        # Show help as tooltips
        pg.SetExtraStyle(wxpg.PG_EX_HELP_AS_TOOLTIPS)

        pg.Bind( wxpg.EVT_PG_CHANGED, self.OnPropGridChange )
        #pg.Bind( wxpg.EVT_PG_PAGE_CHANGED, self.OnPropGridPageChange )
        pg.Bind( wxpg.EVT_PG_SELECTED, self.OnPropGridSelect )
        #pg.Bind( wxpg.EVT_PG_RIGHT_CLICK, self.OnPropGridRightClick )

        pg.AddPage( "Page 1 - Testing All" )
        
        pg.Append( wxpg.PropertyCategory("1 - Basic Properties")  )

        pg.Append( wxpg.EditEnumProperty(u"数据库名",  "databaseName", "" , "" ))
        pg.Append( wxpg.EditEnumProperty(u"数据库集合","collectionName","", ""))
                                                            
        topsizer.Add(pg, 1, wx.EXPAND)		
	self.panel_1.SetSizer(topsizer)
	topsizer.SetSizeHints(self.panel_1)
	#end of panel 1 #########################
	
        self.attribute_name_lb = wx.ListBox(self, wx.ID_ANY, choices=[])
        self.sizer_5_staticbox = wx.StaticBox(self, wx.ID_ANY, u"属性名")
        self.button_3 = wx.Button(self, wx.ID_ANY, u">")
        self.button_3_copy = wx.Button(self, wx.ID_ANY, u"<")
        self.button_3_copy_1 = wx.Button(self, wx.ID_ANY, u"=")
        self.button_3_copy_copy = wx.Button(self, wx.ID_ANY, u">=")
        self.button_3_copy_copy_1 = wx.Button(self, wx.ID_ANY, u"<=")
        self.button_3_copy_copy_2 = wx.Button(self, wx.ID_ANY, u"!=")
        self.button_3_copy_copy_3 = wx.Button(self, wx.ID_ANY, u"and")
        self.button_3_copy_copy_4 = wx.Button(self, wx.ID_ANY, u"or")
	self.button_3_copy_copy_4_copy = wx.Button(self, wx.ID_ANY, "not\n")
	self.button_3_copy_copy_4_copy_1 = wx.Button(self, wx.ID_ANY, "slice")
	self.button_3_copy_copy_4_copy_1_copy = wx.Button(self, wx.ID_ANY, "sort")
	self.button_3_copy_copy_4_copy_1_copy_1 = wx.Button(self, wx.ID_ANY, "limit")
        self.attribute_value_lb = wx.ListBox(self, wx.ID_ANY, choices=[])
        self.sizer_6_staticbox = wx.StaticBox(self, wx.ID_ANY, u"属性值")
	
        self.text_ctrl_1 = wx.TextCtrl(self, wx.ID_ANY, _("{\"attri\":\"value\",\"attri\":{\"$in\":[\"value\",\"vaue\"]}}\n{\"attri\":1,\"attri\":0}\n""\n""\n""\n"""), \
	                               style=wx.TE_MULTILINE)#limit,skip\nnum\nsort\n{\"attri\":1,\"attri\":0}
        self.sizer_8_staticbox = wx.StaticBox(self, wx.ID_ANY, u"选择表达式")
	

        #self.__set_properties()
	self.SetBackgroundColour(wx.Colour(240, 240, 240))
	self.SetSize((700, 450))
        self.panel_1.SetMinSize((684,100))
        self.button_3.SetMinSize((40, 25))
        self.button_3_copy.SetMinSize((40, 25))
        self.button_3_copy_1.SetMinSize((40, 25))
        self.button_3_copy_copy.SetMinSize((40, 25))
        self.button_3_copy_copy_1.SetMinSize((40, 25))
        self.button_3_copy_copy_2.SetMinSize((40, 25))
        self.button_3_copy_copy_3.SetMinSize((40, 25))
        self.button_3_copy_copy_4.SetMinSize((40, 25))
        self.button_3_copy_copy_4_copy.SetMinSize((40, 25))
        self.button_3_copy_copy_4_copy_1.SetMinSize((40, 25))
        self.button_3_copy_copy_4_copy_1_copy.SetMinSize((40, 25))
        self.button_3_copy_copy_4_copy_1_copy_1.SetMinSize((40, 25))	
	
        #self.__do_layout()
	# begin wxGlade: MyFrame.__do_layout
	sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        self.sizer_8_staticbox.Lower()
        sizer_8 = wx.StaticBoxSizer(self.sizer_8_staticbox, wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_6_staticbox.Lower()
        sizer_6 = wx.StaticBoxSizer(self.sizer_6_staticbox, wx.HORIZONTAL)
        grid_sizer_1 = wx.GridSizer(4, 3, 0, 0)
        self.sizer_5_staticbox.Lower()
        sizer_5 = wx.StaticBoxSizer(self.sizer_5_staticbox, wx.HORIZONTAL)
        sizer_1.Add(self.panel_1, 0, wx.EXPAND, 0)
        sizer_5.Add(self.attribute_name_lb, 1, wx.EXPAND, 0)
        sizer_4.Add(sizer_5, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.button_3, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        grid_sizer_1.Add(self.button_3_copy, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.button_3_copy_1, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.button_3_copy_copy, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.button_3_copy_copy_1, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.button_3_copy_copy_2, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.button_3_copy_copy_3, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.button_3_copy_copy_4, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.button_3_copy_copy_4_copy, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.button_3_copy_copy_4_copy_1, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.button_3_copy_copy_4_copy_1_copy, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_1.Add(self.button_3_copy_copy_4_copy_1_copy_1, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_4.Add(grid_sizer_1, 0, wx.ALL | wx.EXPAND, 10)
        sizer_6.Add(self.attribute_value_lb, 1, wx.EXPAND, 0)
        sizer_4.Add(sizer_6, 1, wx.EXPAND, 0)
        sizer_2.Add(sizer_4, 2, wx.EXPAND, 0)
        sizer_8.Add(self.text_ctrl_1, 1, wx.EXPAND, 0)
        sizer_2.Add(sizer_8, 1, wx.EXPAND, 0)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
	
	# add some button 
	rowsizer = wx.BoxSizer(wx.HORIZONTAL)
	TestBtn = wx.Button(self,-1,u"连接数据库")
	TestBtn.Bind( wx.EVT_BUTTON, self.OnTestBtn )
	CollectBtn = wx.Button(self,-1,u"选择聚集")
	CollectBtn.Bind( wx.EVT_BUTTON, self.OnCollectBtn )         
	sureBtn = wx.Button(self,-1,u"抽取")
	sureBtn.Bind( wx.EVT_BUTTON, self.OnSureBtn )        
	CancelBtn = wx.Button(self,-1,u"取消")
	CancelBtn.Bind( wx.EVT_BUTTON, self.OnCancelBtn )  
	
	rowsizer.Add((20, 20), 5, 0, 0)
	rowsizer.Add(TestBtn,0,0,0) 
	rowsizer.Add(CollectBtn,0,0,0) 
	
	rowsizer.Add(sureBtn,0,0,0) 
	rowsizer.Add(CancelBtn,0,0,0)    
	
	sizer_1.Add(rowsizer, 0, wx.EXPAND, 0)
	self.SetSizer(sizer_1)
	self.Layout()	
	#listbox order
	self.Bind(wx.EVT_LISTBOX_DCLICK, self.EvtListBoxDClick, self.attribute_name_lb)
	self.Bind(wx.EVT_LISTBOX_DCLICK, self.ValueListBoxDClick, self.attribute_value_lb)
	#computer order
        self.Bind(wx.EVT_BUTTON, self.large_btn, self.button_3)
        self.Bind(wx.EVT_BUTTON, self.litter_btn, self.button_3_copy)
        self.Bind(wx.EVT_BUTTON, self.equal_btn, self.button_3_copy_1)
        self.Bind(wx.EVT_BUTTON, self.le_btn, self.button_3_copy_copy)
        self.Bind(wx.EVT_BUTTON, self.lt_btn, self.button_3_copy_copy_1)
        self.Bind(wx.EVT_BUTTON, self.ue_btn, self.button_3_copy_copy_2)
        self.Bind(wx.EVT_BUTTON, self.and_btn, self.button_3_copy_copy_3)
        self.Bind(wx.EVT_BUTTON, self.or_btn, self.button_3_copy_copy_4)
	self.Bind(wx.EVT_BUTTON, self.not_btn, self.button_3_copy_copy_4_copy)
	self.Bind(wx.EVT_BUTTON, self.slice_btn, self.button_3_copy_copy_4_copy_1)
	self.Bind(wx.EVT_BUTTON, self.sort_btn, self.button_3_copy_copy_4_copy_1_copy)
	self.Bind(wx.EVT_BUTTON, self.limit_btn, self.button_3_copy_copy_4_copy_1_copy_1)	
        # end wxGlade
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
	#self.pg.DeleteProperty("databaseName")
	self.pg.DeleteProperty("collectionName")
	self.pg.GetProperty("databaseName").SetValue(databaseName)

        # 连接数据库 ， 获取聚集
        #聚集的名字
        collections = mongo_bll.getCollect_names(databaseName)        
        collectList = range(len(collections))
        self.pg.Append( wxpg.EditEnumProperty(u"数据库集合","collectionName",
                                                            collections,
                                                            collectList,
                                                            " "))
    ###################  sure cancel button        
    #----------------------------------------------------------------------
    def OnTestBtn(self , event ):
        """连接数据库"""
        datalink = OnDataLink_view.OnDataLinkView(None)      	
        datalink.Show()        

    #获取 metaDB 里面的头文件
    #----------------------------------------------------------------------
    def getMetaData(self, collectname):
	""""""
	metaData = mongo_bll.find_one("metaDB", collectname)
	return metaData
	                                            
    #----------------------------------------------------------------------
    def OnSureBtn(self , event):
        """抽取数据"""
	firstState = self.text_ctrl_1.GetLineText(0)
	secondState = self.text_ctrl_1.GetLineText(1)
	thirdState1 = self.text_ctrl_1.GetLineText(2)
	thirdState2 = self.text_ctrl_1.GetLineText(3)
	fourthState1 = self.text_ctrl_1.GetLineText(4)
	fourthState2 = self.text_ctrl_1.GetLineText(5)
	print firstState , secondState
	print thirdState1,thirdState2 , fourthState1,fourthState2
	exec("first_state=" + firstState)
	exec("second_state=" + secondState)
	exec("fourth_state2=" + fourthState2)
	print first_state , second_state ,fourth_state2
	
	databaseValue = self.pg.GetPropertyValue("databaseName")
	collectionValue = self.pg.GetPropertyValueAsString("collectionName")	
	print databaseValue, collectionValue

        #statementValue = self.onDataLink.getStatementValue(databaseValue, collectionValue, firstState , \
	                                                   #secondState, thirdState1 , thirdState2 , fourthState1 , fourthState2)
	
	metaData = self.getMetaData(collectionValue)
	print metaData
	#return statementValue
        
    #----------------------------------------------------------------------
    def OnCancelBtn(self , event):
        """取消按钮"""
        self.Close()
        print "connect to mongodb"
	
    ############### computer button 
    def large_btn(self, event):  # wxGlade: MyFrame.<event_handler>
	start, end = self.text_ctrl_1.GetSelection()
	selectString = self.text_ctrl_1.GetStringSelection()
	self.text_ctrl_1.Replace(start,end,"{\"$gt\":")	
        print "Event handler 'large_btn' not implemented!"
        event.Skip()

    def litter_btn(self, event):  # wxGlade: MyFrame.<event_handler>
	start, end = self.text_ctrl_1.GetSelection()
	selectString = self.text_ctrl_1.GetStringSelection()
	self.text_ctrl_1.Replace(start,end,"{\"$lt\":")	
        print "Event handler 'litter_btn' not implemented!"
        event.Skip()

    def equal_btn(self, event):  # wxGlade: MyFrame.<event_handler>
	start, end = self.text_ctrl_1.GetSelection()
	selectString = self.text_ctrl_1.GetStringSelection()
	self.text_ctrl_1.Replace(start,end,":")	
        print "Event handler 'equal_btn' not implemented!"
        event.Skip()

    def le_btn(self, event):  # wxGlade: MyFrame.<event_handler>
	start, end = self.text_ctrl_1.GetSelection()
	selectString = self.text_ctrl_1.GetStringSelection()
	self.text_ctrl_1.Replace(start,end,"{\"$lte\":")	
        print "Event handler 'le_btn' not implemented!"
        event.Skip()

    def lt_btn(self, event):  # wxGlade: MyFrame.<event_handler>
	start, end = self.text_ctrl_1.GetSelection()
	selectString = self.text_ctrl_1.GetStringSelection()
	self.text_ctrl_1.Replace(start,end,"{\"$lte\":")	
        print "Event handler 'lt_btn' not implemented!"
        event.Skip()

    def ue_btn(self, event):  # wxGlade: MyFrame.<event_handler>
	start, end = self.text_ctrl_1.GetSelection()
	selectString = self.text_ctrl_1.GetStringSelection()
	self.text_ctrl_1.Replace(start,end,"{\"$ne\":")	
        print "Event handler 'ue_btn' not implemented!"
        event.Skip()

    def and_btn(self, event):  # wxGlade: MyFrame.<event_handler>
	start, end = self.text_ctrl_1.GetSelection()
	selectString = self.text_ctrl_1.GetStringSelection()
	self.text_ctrl_1.Replace(start,end,"{\"$in\":[]")	
        print "Event handler 'and_btn' not implemented!"
        event.Skip()

    def or_btn(self, event):  # wxGlade: MyFrame.<event_handler>
	start, end = self.text_ctrl_1.GetSelection()
	selectString = self.text_ctrl_1.GetStringSelection()
	self.text_ctrl_1.Replace(start,end,"{\"$or\":[]")	
        print "Event handler 'or_btn' not implemented!"
        event.Skip()
	
    def not_btn(self, event):  # wxGlade: MyFrame.<event_handler>
	start, end = self.text_ctrl_1.GetSelection()
	selectString = self.text_ctrl_1.GetStringSelection()
	self.text_ctrl_1.Replace(start,end,"{\"$not\":")	
	print "Event handler 'not_btn' not implemented!"
	event.Skip()

    def slice_btn(self, event):  # wxGlade: MyFrame.<event_handler>
	start, end = self.text_ctrl_1.GetSelection()
	selectString = self.text_ctrl_1.GetStringSelection()
	self.text_ctrl_1.Replace(start,end,"{\"$slice\":")	
	print "Event handler 'slice_btn' not implemented!"
	event.Skip()

    def sort_btn(self, event):  # wxGlade: MyFrame.<event_handler>
	start, end = self.text_ctrl_1.GetSelection()
	selectString = self.text_ctrl_1.GetStringSelection()
	self.text_ctrl_1.Replace(start,end,"\"$sort\":")	
	print "Event handler 'sort_btn' not implemented!"
	event.Skip()

    def limit_btn(self, event):  # wxGlade: MyFrame.<event_handler>
	start, end = self.text_ctrl_1.GetSelection()
	selectString = self.text_ctrl_1.GetStringSelection()
	self.text_ctrl_1.Replace(start,end,"\"$limit\":")	
	print "Event handler 'limit_btn' not implemented!"
	event.Skip()    
	
    #### properGrid order
    ####   propGrid  改变
    def OnPropGridChange(self, event):
        p = event.GetProperty()
        if p:
	    if p.GetName() == u"collectionName":
		self.attribute_name_lb.Clear()
		databaseValue = self.pg.GetPropertyValue("databaseName")
		collectionValue = p.GetValueAsString()
		
		attriName = mongo_bll.getAttriName(databaseValue, collectionValue)
		for attri in attriName:
		    self.attribute_name_lb.Append(attri)

    #  propGrid 选择    
    def OnPropGridSelect(self, event):
        p = event.GetProperty()
        if p:
	    if p.GetName() == u"databaseName":
		print "databaseName"
            print '%s selected\n' % (event.GetProperty().GetName())
        else:
            print 'Nothing selected\n'
    
    ########## listbox order
    # attribute name list box order
    def EvtListBoxDClick(self, event):	
	try:
	    # 打开属性值
	    self.attribute_value_lb.Clear()
	    databaseValue = self.pg.GetPropertyValue("databaseName")
	    collectionValue = self.pg.GetPropertyValueAsString("collectionName")
	    print collectionValue , databaseValue
	    attribute = event.GetString()
	    print attribute
	    attriValue = mongo_bll.getAttriValue(databaseValue, collectionValue, attribute)
	    print attriValue
	    for value in attriValue:
		if type(value.values()[0]) == unicode:
		    self.attribute_value_lb.Append(value.values()[0])
		else:
		    self.attribute_value_lb.Append(str(value.values()[0]))
	    # 写入 textctrl

	    start, end = self.text_ctrl_1.GetSelection()
	    selectString = self.text_ctrl_1.GetStringSelection()
	    self.text_ctrl_1.Replace(start,end,attribute)
	except:
	    pass
		

    # attributeValue list box order
    def ValueListBoxDClick(self, event):	
	try:
	    attriValue = event.GetString()
	    start, end = self.text_ctrl_1.GetSelection()
	    selectString = self.text_ctrl_1.GetStringSelection()
	    self.text_ctrl_1.Replace(start,end,attriValue)	    
	    print event.GetString()
	except:    
	    pass	
	
	
# end of class MyFrame
if __name__ == "__main__":
    gettext.install("app") # replace with the appropriate catalog name

    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = MyFrame(None)
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()
    
    
    
    
    
    
    
    
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
        #pg.Append( wxpg.StringProperty(u"集合名",name = "pcname" ,value="localhost") )
        
        
        # When page is added, it will become the target page for AutoFill

        
        topsizer.Add(pg, 1, wx.EXPAND)
        #topsizer.Add(panel2,2,wx.EXPAND)
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
        
        #topsizer.Add(rowsizer,0,wx.EXPAND)
        
        rowsizer = wx.BoxSizer(wx.HORIZONTAL)
        panel.SetSizer(topsizer)
        topsizer.SetSizeHints(panel)
        #topsizer.SetMinSize((600,300))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, 1, wx.EXPAND)
	sizer.Add(panel2, 2,wx.EXPAND)
	#sizer.Add(rowsizer,1,wx.EXPAND)
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
        collections = mongo_bll.getCollection(databaseName)      
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
        
    ##################### the second panel bind order ############
    def large_btn(self, event):  # wxGlade: MyFrame.<event_handler>
        print "Event handler 'large_btn' not implemented!"
        event.Skip()

    def litter_btn(self, event):  # wxGlade: MyFrame.<event_handler>
        print "Event handler 'litter_btn' not implemented!"
        event.Skip()

    def equal_btn(self, event):  # wxGlade: MyFrame.<event_handler>
        print "Event handler 'equal_btn' not implemented!"
        event.Skip()

    def le_btn(self, event):  # wxGlade: MyFrame.<event_handler>
        print "Event handler 'le_btn' not implemented!"
        event.Skip()

    def lt_btn(self, event):  # wxGlade: MyFrame.<event_handler>
        print "Event handler 'lt_btn' not implemented!"
        event.Skip()

    def ue_btn(self, event):  # wxGlade: MyFrame.<event_handler>
        print "Event handler 'ue_btn' not implemented!"
        event.Skip()

    def and_btn(self, event):  # wxGlade: MyFrame.<event_handler>
        print "Event handler 'and_btn' not implemented!"
        event.Skip()

    def or_btn(self, event):  # wxGlade: MyFrame.<event_handler>
        print "Event handler 'or_btn' not implemented!"
        event.Skip()
	
#if __name__ == '__main__':
    #app = wx.PySimpleApp()
    #frame = TestPanel(None)

    #frame.Show(True)
    #app.MainLoop()