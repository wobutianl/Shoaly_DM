# -*- coding: utf-8 -*-
import read_excel

excel_file = u"E:\\lab\\Paper\\Data\\data\\大丰社会经济（1975、1990、2000、2004、2006）\市县经济2006.xls"
out_file = open(r"C:\Users\jerryfive\Desktop\dafeng.csv","w")

readExcel = read_excel.readExcel(excel_file)

sheetNum = readExcel.getSheetNum()



firstData = []   
secondData =[]
for sheet in range(sheetNum):
    firstCol = readExcel.getColData(0, sheet)
    j =  0
    rowNum = 0  
    for i in firstCol:
        if (i == u"大丰县") or (i == u"大丰") or (i == u"大丰市"):
            rowNum = j
        j += 1    
    
    data = readExcel.getRowData([0, rowNum], sheet)
    firstData.append(data[0])
    secondData.append(data[1])

for k in firstData:
    for m in k:
        if m == u"市县":
            continue
        out_file.write(m.encode("gb2312"))
        out_file.write(",")
    
out_file.write("\n")
for j in secondData:
    for n in j:
        #isinstance(n, unicode)
        if isinstance(n, unicode):
            if (n == u"大丰县") or (n == u"大丰") or (n == u"大丰市"):
                continue            
            out_file.write(n.encode("gb2312"))
            out_file.write(",")
        else:        
            out_file.write(str(n))
            out_file.write(",")



