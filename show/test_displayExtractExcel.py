# -*- coding: utf-8 -*-
import sys, os
import gettext
import wx

from shapely.geometry import mapping ,shape
#sys.path.append(r"E:\Test\wxGlade\second_one\inspection\shapely");
#from shapely import shapely_BLL
import OnDataLink
import extract_view
import  wx.grid   as  gridlib

#import  wx.lib.mixins.grid  as  mixins

#---------------------------------------------------------------------------


class SimpleGrid(gridlib.Grid): ##, mixins.GridAutoEditMixin):
    def __init__(self, parent , log):
        gridlib.Grid.__init__(self, parent, -1)
        ##mixins.GridAutoEditMixin.__init__(self)
        self.log = log
        self.moveTo = None


	dataLink = OnDataLink.mongo_connect()
	dataLink.connection()
	data = dataLink.getStatementValue("townEconomy1990", u"人口", {u"市县":{"$in":[u"南京市",u"扬州市"]} , u"年平均人口":{"$gt":200}})	
	
	print "data in put :"
	print len(data[0])
	print data.count()
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        self.CreateGrid(data.count() , len(data[0]))#, gridlib.Grid.SelectRows)
	
	
        
        #print len(data) , len(data[0])
        ##self.EnableEditing(False)
            
        i = 0 
        try:
	    for cell  in data:
		print cell.keys() , cell.values()
		for num in range(0, len(cell)):
		    if i == 0 :
			self.SetColLabelValue(num, cell.keys()[num])        
		    if (type(cell.values()[num]) == int or type(cell.values()[num]) == float):
			a = str(cell.values()[num])                    
			self.SetCellValue(i , num , a)
		    elif (type(cell.values()[num]) == unicode or type(cell.values()[num]) == str):
			renderer = gridlib.GridCellAutoWrapStringRenderer()
			self.SetCellRenderer(i,num, renderer)         
			self.SetCellValue(i , num , cell.values()[num])
		    else:
			self.SetCellValue(i,num,"null")
		i = i + 1             
        except:
            print "attri frame error "
           
                   
        # test all the events
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        self.Bind(gridlib.EVT_GRID_CELL_RIGHT_CLICK, self.OnCellRightClick)
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_DCLICK, self.OnCellLeftDClick)
        self.Bind(gridlib.EVT_GRID_CELL_RIGHT_DCLICK, self.OnCellRightDClick)

        self.Bind(gridlib.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelLeftClick)
        self.Bind(gridlib.EVT_GRID_LABEL_RIGHT_CLICK, self.OnLabelRightClick)
        self.Bind(gridlib.EVT_GRID_LABEL_LEFT_DCLICK, self.OnLabelLeftDClick)
        self.Bind(gridlib.EVT_GRID_LABEL_RIGHT_DCLICK, self.OnLabelRightDClick)

        self.Bind(gridlib.EVT_GRID_COL_SORT, self.OnGridColSort)

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

    def OnGridColSort(self, evt):
        self.log.write("OnGridColSort: %s %s" % (evt.GetCol(), self.GetSortingColumn()))
        self.SetSortingColumn(evt.GetCol())
        
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


#---------------------------------------------------------------------------

class TestFrame(wx.Frame):
    def __init__(self, parent, log):
		
	#dialog = wx.FileDialog(None, '打开Shape文件', '.', '', 'Shape File (*.shp)|*.shp|All Files (*.*)|*.*', style = wx.OPEN )   
	#filepath = ''
	#if dialog.ShowModal() == wx.ID_OK:
		#filepath = dialog.GetPath()
	#dialog.Destroy()	        
        #shpAttri = GetShpAttri.GetShpAttri(filepath)
        #data = shpAttri.GetShpAttributes()
        #print data
        wx.Frame.__init__(self, parent, -1, "Simple Grid Demo", size=(640,480))
	data = [[u'\u5e74\u672b\u603b\u4eba\u53e3\uff08\u4e07\u4eba\uff09', u'\u5e02\u53bf', u'\u5e74\u51fa\u751f\u4eba\u6570\uff08\u4eba\uff09', u'\u5e74\u5e73\u5747\u4eba\u53e3', u'\u5e74\u6b7b\u4ea1\u4eba\u6570\uff08\u4eba\uff09', u'\u5e74\u672b\u603b\u4eba\u53e3#\u975e\u519c\u4e1a\u4eba\u53e3\uff08\u4e07\u4eba\uff09', u'_id'],
[u'\u5e74\u672b\u603b\u4eba\u53e3\uff08\u4e07\u4eba\uff09', u'\u5e02\u53bf', u'\u5e74\u51fa\u751f\u4eba\u6570\uff08\u4eba\uff09', u'\u5e74\u5e73\u5747\u4eba\u53e3', u'\u5e74\u6b7b\u4ea1\u4eba\u6570\uff08\u4eba\uff09', u'\u5e74\u672b\u603b\u4eba\u53e3#\u975e\u519c\u4e1a\u4eba\u53e3\uff08\u4e07\u4eba\uff09', u'_id']]

        self.grid = SimpleGrid(self , log)


    #获取 extract view 界面返回来的数据
    #----------------------------------------------------------------------
    def getExtractData():
	""""""
	try:
	    extractView = extract_view.MyFrame(None)
	    data = extractView.statementValue
	    metaData = extractView.metaData
	    return data , metaData        
	except:
	    wx.MessageDialog(u"没有抽取数据")

#---------------------------------------------------------------------------

if __name__ == '__main__':
    import sys
    from wx.lib.mixins.inspection import InspectableApp
    app = InspectableApp(False)
    frame = TestFrame(None, sys.stdout)
    frame.Show(True)
    #import wx.lib.inspection
    #wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()
