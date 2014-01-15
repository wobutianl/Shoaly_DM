# -*- coding: utf-8 -*-
import mongo_bll

import  wx
import  wx.grid             as  gridlib

#########################
##  完成 数据库抽取属性数据的显示
#############################
#---------------------------------------------------------------------------

class SimpleGrid(gridlib.Grid): ##, mixins.GridAutoEditMixin):
    def __init__(self, parent,  log):
        gridlib.Grid.__init__(self, parent, -1)
        ##mixins.GridAutoEditMixin.__init__(self)
        self.log = log
        self.moveTo = None

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
	    print cell.keys() , cell.values()
	    for num in range(0, len(cell)):
		if i == 0 :
		    row_label = cell.keys()[num] 
		    if (type(row_label) == int) or (type(row_label) == float) or (type(row_label) == long):
			row_label = str(cell.keys()[num])
			print row_label
		    self.SetColLabelValue(num, row_label.encode('gb18030'))  
		if (type(cell.values()[num]) == int or type(cell.values()[num]) == float):
		    a = str(cell.values()[num])                    
		    self.SetCellValue(i , num , a)
		elif (type(cell.values()[num]) == unicode or type(cell.values()[num]) == str):
		    renderer = gridlib.GridCellAutoWrapStringRenderer()
		    self.SetCellRenderer(i,num, renderer)         
		    self.SetCellValue(i , num , cell.values()[num].encode('gb18030'))
		else:
		    self.SetCellValue(i,num,"null")
	    i = i + 1 

#---------------------------------------------------------------------------

class TestFrame(wx.Frame):
    def __init__(self, parent, log):
        wx.Frame.__init__(self, parent, -1, "Simple Grid Demo", size=(640,480))
        self.grid = SimpleGrid(self, log)
	
	cursor = self.getAttriData()
	data = []
	for i in cursor:
	    data.append(i)
	    #print i
	self.grid.make_cell(data)

    #----------------------------------------------------------------------
    def getAttriData(self, database_name = "share_cup", collection_name = u"2000经济"):
	""""""
	data = mongo_bll.find(database_name, collection_name, show_dict= {"_id":0},limit=50)
	return data


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


#---------------------------------------------------------------------------


