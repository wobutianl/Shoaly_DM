# -*- coding: utf-8 -*-  
import  wx
import  wx.grid             as  gridlib
#import  wx.lib.mixins.grid  as  mixins

#print wx.version()
#import os; print "pid:", os.getpid(); raw_input("Press Enter...")

#---------------------------------------------------------------------------

class SimpleGrid(gridlib.Grid): ##, mixins.GridAutoEditMixin):
    
    def __init__(self, parent,  log):
        gridlib.Grid.__init__(self, parent, -1)
        ##mixins.GridAutoEditMixin.__init__(self)
        self.log = log
        self.moveTo = None

        self.Bind(wx.EVT_IDLE, self.OnIdle)
        data =  [{'1': '\xe5\xb7\xb2\xe6\x9c\x89\xe9\x93\x81\xe8\xb7\xaf'}, {'1':'\xe5\xb7\xb2\xe6\x9c\x89\xe9\x93\x81\xe8\xb7\xaf'}
	         , {'1':'\xe5\xb7\xb2\xe6\x9c\x89\xe9\x93\x81\xe8\xb7\xaf'}, {'1': '\xe5\xb7\xb2\xe6\x9c\x89\xe9\x93\x81\xe8\xb7\xaf'},
	         {'1':'\xe5\xb7\xb2\xe6\x9c\x89\xe9\x93\x81\xe8\xb7\xaf'},{'1':'\xe5\xb7\xb2\xe6\x9c\x89\xe9\x93\x81\xe8\xb7\xaf'}]
  
	
    #----------------------------------------------------------------------
    def make_cell(self, data):
	"""通过数据来建立 Grid cell"""	
        nRow = len(data)
        nCol = len(data[0])
        # 建立一个多大的cell
        
        self.CreateGrid(nRow, nCol)#, gridlib.Grid.SelectRows)

        # simple cell formatting
	i = 0 
	#try:
	for cell  in data:
	   # print cell.keys() , cell.values()
	    for num in range(0, len(cell)):
		if i == 0 :
		    row_label = cell.keys()[num] 
		    if (type(row_label) == int) or (type(row_label) == float) or (type(row_label) == long):
			row_label = str(cell.keys()[num])
			self.SetColLabelValue(num, row_label)  
		    elif isinstance(row_label, unicode):
			row_label = row_label.encode("gb2312")
			self.SetColLabelValue(num, row_label)  
		    else:
			self.SetColLabelValue(num, row_label.decode("utf8"))  
		if (type(cell.values()[num]) == int or type(cell.values()[num]) == float):
		    a = str(cell.values()[num])                    
		    self.SetCellValue(i , num , a)
		elif (type(cell.values()[num]) == unicode or type(cell.values()[num]) == str):
		    renderer = gridlib.GridCellAutoWrapStringRenderer()
		    self.SetCellRenderer(i,num, renderer)         
		    self.SetCellValue(i , num , cell.values()[num].decode("utf8"))
		else:
		    self.SetCellValue(i,num,"null")
	    i = i + 1 
	#except:
	    #print "attri frame error "
	# test all the events
	self.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
	self.Bind(gridlib.EVT_GRID_CELL_RIGHT_CLICK, self.OnCellRightClick)
	self.Bind(gridlib.EVT_GRID_CELL_LEFT_DCLICK, self.OnCellLeftDClick)
	self.Bind(gridlib.EVT_GRID_CELL_RIGHT_DCLICK, self.OnCellRightDClick)
    
	self.Bind(gridlib.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelLeftClick)
	self.Bind(gridlib.EVT_GRID_LABEL_RIGHT_CLICK, self.OnLabelRightClick)
	self.Bind(gridlib.EVT_GRID_LABEL_LEFT_DCLICK, self.OnLabelLeftDClick)
	self.Bind(gridlib.EVT_GRID_LABEL_RIGHT_DCLICK, self.OnLabelRightDClick)
    
	self.Bind(gridlib.EVT_GRID_ROW_SIZE, self.OnRowSize)
	self.Bind(gridlib.EVT_GRID_COL_SIZE, self.OnColSize)
    
	self.Bind(gridlib.EVT_GRID_RANGE_SELECT, self.OnRangeSelect)
	self.Bind(gridlib.EVT_GRID_CELL_CHANGE, self.OnCellChange)
	self.Bind(gridlib.EVT_GRID_SELECT_CELL, self.OnSelectCell)
    
	self.Bind(gridlib.EVT_GRID_EDITOR_SHOWN, self.OnEditorShown)
	self.Bind(gridlib.EVT_GRID_EDITOR_HIDDEN, self.OnEditorHidden)
	self.Bind(gridlib.EVT_GRID_EDITOR_CREATED, self.OnEditorCreated)   
        
        


    def OnCellLeftClick(self, evt):
        self.log.write("OnCellLeftClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()

    def OnCellRightClick(self, evt):
        self.log.write("OnCellRightClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()

    def OnCellLeftDClick(self, evt):
        self.log.write("OnCellLeftDClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()

    def OnCellRightDClick(self, evt):
        self.log.write("OnCellRightDClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()

    def OnLabelLeftClick(self, evt):
        self.log.write("OnLabelLeftClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()

    def OnLabelRightClick(self, evt):
        self.log.write("OnLabelRightClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()

    def OnLabelLeftDClick(self, evt):
        self.log.write("OnLabelLeftDClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()

    def OnLabelRightDClick(self, evt):
        self.log.write("OnLabelRightDClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()

    def OnRowSize(self, evt):
        self.log.write("OnRowSize: row %d, %s\n" %
                       (evt.GetRowOrCol(), evt.GetPosition()))
        evt.Skip()

    def OnColSize(self, evt):
        self.log.write("OnColSize: col %d, %s\n" %
                       (evt.GetRowOrCol(), evt.GetPosition()))
        evt.Skip()

    def OnRangeSelect(self, evt):
        if evt.Selecting():
            msg = 'Selected'
        else:
            msg = 'Deselected'
        self.log.write("OnRangeSelect: %s  top-left %s, bottom-right %s\n" %
                           (msg, evt.GetTopLeftCoords(), evt.GetBottomRightCoords()))
        evt.Skip()


    def OnCellChange(self, evt):
        self.log.write("OnCellChange: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))

        # Show how to stay in a cell that has bad data.  We can't just
        # call SetGridCursor here since we are nested inside one so it
        # won't have any effect.  Instead, set coordinates to move to in
        # idle time.
        value = self.GetCellValue(evt.GetRow(), evt.GetCol())

        if value == 'no good':
            self.moveTo = evt.GetRow(), evt.GetCol()


    def OnIdle(self, evt):
        if self.moveTo != None:
            self.SetGridCursor(self.moveTo[0], self.moveTo[1])
            self.moveTo = None

        evt.Skip()


    def OnSelectCell(self, evt):
        if evt.Selecting():
            msg = 'Selected'
        else:
            msg = 'Deselected'
        self.log.write("OnSelectCell: %s (%d,%d) %s\n" %
                       (msg, evt.GetRow(), evt.GetCol(), evt.GetPosition()))

        # Another way to stay in a cell that has a bad value...
        row = self.GetGridCursorRow()
        col = self.GetGridCursorCol()

        if self.IsCellEditControlEnabled():
            self.HideCellEditControl()
            self.DisableCellEditControl()

        value = self.GetCellValue(row, col)

        if value == 'no good 2':
            return  # cancels the cell selection

        evt.Skip()


    def OnEditorShown(self, evt):
        if evt.GetRow() == 6 and evt.GetCol() == 3 and \
           wx.MessageBox("Are you sure you wish to edit this cell?",
                        "Checking", wx.YES_NO) == wx.NO:
            evt.Veto()
            return

        self.log.write("OnEditorShown: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()


    def OnEditorHidden(self, evt):
        if evt.GetRow() == 6 and evt.GetCol() == 3 and \
           wx.MessageBox("Are you sure you wish to  finish editing this cell?",
                        "Checking", wx.YES_NO) == wx.NO:
            evt.Veto()
            return

        self.log.write("OnEditorHidden: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()


    def OnEditorCreated(self, evt):
        self.log.write("OnEditorCreated: (%d, %d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetControl()))


import mongo_bll
import show_shapefile
import numpy as np
class MyFrame(wx.Frame):
    def __init__(self, parent, log):
	wx.Frame.__init__(self, parent, -1, "Simple Grid Demo", size=(700,400))
	
	#data =  [{'1': '\xe5\xb7\xb2\xe6\x9c\x89\xe9\x93\x81\xe8\xb7\xaf'}, {'1':'\xe5\xb7\xb2\xe6\x9c\x89\xe9\x93\x81\xe8\xb7\xaf'}
		         #, {'1':'\xe5\xb7\xb2\xe6\x9c\x89\xe9\x93\x81\xe8\xb7\xaf'}, {'1': '\xe5\xb7\xb2\xe6\x9c\x89\xe9\x93\x81\xe8\xb7\xaf'},
		         #{'1':'\xe5\xb7\xb2\xe6\x9c\x89\xe9\x93\x81\xe8\xb7\xaf'},{'1':'\xe5\xb7\xb2\xe6\x9c\x89\xe9\x93\x81\xe8\xb7\xaf'}]	
			 	
        self.grid = SimpleGrid(self, log)
        self.sizer_3_staticbox = wx.StaticBox(self, wx.ID_ANY, "data")
        self.MPL = show_shapefile.sketchWindow(self, wx.ID_ANY)
        self.sizer_4_staticbox = wx.StaticBox(self, wx.ID_ANY, "pic")
	
	self.draw_btn = wx.Button(self, wx.ID_ANY, "draw")
	self.clear_btn = wx.Button(self, wx.ID_ANY, "clear")
	
	mongo = mongo_bll.find("excel_paper", "dafeng", show_dict={"_id":0}, )
	self.data = []	
	for i in mongo:
	    self.data.append(i)
	self.grid.make_cell(self.data)
	
	
	path_china = r"E:\lab\Paper\Data\data\JS_town.SHP"
	self.MPL.addLayer(path_china, wx.Pen("black",2,wx.SOLID),wx.Brush('#4c4c4c', wx.TRANSPARENT))
	

        self.__set_properties()
        self.__do_layout()
	
        self.Bind(wx.EVT_BUTTON, self.draw_btn_event, self.draw_btn)
        self.Bind(wx.EVT_BUTTON, self.clear_btn_event, self.clear_btn)	
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("pop_pic")
        self.SetSize((700, 400))
        self.SetBackgroundColour(wx.Colour(240, 240, 240))
        self.grid.SetMinSize((200, 334))
        self.MPL.SetMinSize((334,334))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_4_staticbox.Lower()
        sizer_4 = wx.StaticBoxSizer(self.sizer_4_staticbox, wx.HORIZONTAL)
        self.sizer_3_staticbox.Lower()
        sizer_3 = wx.StaticBoxSizer(self.sizer_3_staticbox, wx.HORIZONTAL)
	
        sizer_5 = wx.BoxSizer(wx.VERTICAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5.Add(self.grid, 2, wx.EXPAND, 0)
        sizer_6.Add((20, 20), 0, 0, 0)
        sizer_6.Add(self.draw_btn, 0, 0, 0)
        sizer_6.Add(self.clear_btn, 0, 0, 0)
        sizer_5.Add(sizer_6, 0, wx.EXPAND, 0)
        sizer_3.Add(sizer_5, 1, wx.EXPAND, 0)
	
        sizer_2.Add(sizer_3, 0, wx.EXPAND, 0)
        sizer_4.Add(self.MPL, 1, wx.EXPAND, 0)
        sizer_2.Add(sizer_4, 1, wx.EXPAND, 0)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()

    def draw_btn_event(self, event):  # wxGlade: MyFrame.<event_handler>
        print "Event handler 'draw_btn_event' not implemented!"
	data = [{"type":"polygon", "value":[122,33,0.5,1]}]
	print data[0]["value"]
	#
	#self.MPL.addData(data["value"])
	
        event.Skip()

    def clear_btn_event(self, event):  # wxGlade: MyFrame.<event_handler>
        print "Event handler 'clear_btn_event' not implemented!"
	self.panel.clear()
        event.Skip()
	
    #----------------------------------------------------------------------
    def getData(self, database="excel_paper", collect="dafeng",attri={"_id":0}):
	"""获取数据"""
	mongo = mongo_bll.find(database, collect, attri)

	for i in mongo:
	    self.data.append(i)
	self.grid.make_cell(self.data)	
	
#---------------------------------------------------------------------------

if __name__ == '__main__':
    import sys
    from wx.lib.mixins.inspection import InspectableApp
    app = InspectableApp(False)
    frame = MyFrame(None, sys.stdout)
    frame.Show(True)
    #import wx.lib.inspection
    #wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()


