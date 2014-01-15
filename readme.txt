最终要实现的目标：
    1：构建一个统一的多源异质地学数据库，和基础地理数据操作库。
    2：对提供的地学模型及其XML描述数据进行解析，获取解析接口
    3：针对接口匹配操作库中的操作模型，或者直接数据推送
    
软件表现效果：
    1：地学任务模型 vs 数据操作模型的构建。
    2：数据的抽取（各类抽取方式）
    3：地学任务模型的执行结果示意图
    
1的具体表现：
    1：模型框架
    2：操作库的拖动
    3：各框架之间的连接，画线
    
2的具体表现：
    1：模型XML是否可以直接匹配，可以，则直接抽取
    2：模型操作库识别，自动填充抽取界面，获取数据

3的具体表现：
    1：数据反向执行操作模型
    2：提供给模型应用
    3：模型表现
    
模型识别数据的过程：迭代匹配，第一次利用模型XML去匹配数据库中的元数据库，存在则调用抽取操作，不存在则匹配数据操作。
                数据操作继续迭代匹配数据库中的数据，并将上一次的操作说明带入下一次的操作中去。
空间数据和统计数据的匹配：
    
11-28:
    1: ribbon（文件与模型，数据库，空间数据操作，属性数据操作，数据抽取，数据显示）
        1：文件与模型：（打开，关闭，保存） + 省人均GDP空间关联
        2：数据库：**   #这里要考虑数据分类
        3：间数据操作： （求面积，取波段，坐标转换，缓冲区，剪切，叠加，合并）
        4：属性数据操作：（中位数，密度，
        5：数据抽取：空间维度抽取，时空维度抽取，属性维度抽取，时间属性维度抽取，多维度抽取
        6：数据显示：饼状，柱状，直方图，雷达图，矢量空间分布，线状图
    2：具体操作：
        1：点击模型，双击模型面板则弹出模型，并在数据显示面板显示模型的XML数据 （所以需要构建模型XML）
        2：点击数据操作：通过匹配，暗掉不能操作的数据操作，同上的显示方式
        3：连接到数据抽取时：自动填写数据抽取参数，抽取数据
        4：
        
        
1：连接问题：都通过ID号来连接 ，ID号设置成全局变量，点击则获取这个全局变量
        通过全局ID,来确定操作的函数
        通过ID，来确定XML
        
2：空间数据和属性数据的连接问题：通过城市名匹配（模糊匹配）

3：




MongoDB 
    excel2mongoDB: excel插入MongoDB中
    mongo_bll：    mongo的CRUD
    read_excel：   读取excel数据
    shp2mongoDB：  shp数据插入mongoDB中
panel
    data_extract_panel : 数据库界面
    file_panel：         文件&模型界面
    show_analysis_panel: 可视化界面
    shpAnalysis_panel:   空间数据操作界面
    staticAnalysis_panel:统计数据操作
    
show
    DB_search:  时空维度抽取
    OnDataLink_view:    数据连接界面
    OnUploadData_view:  /excel_insert/shpdata_insert : 数据上传
    db_view：/db_view2 :  数据库查看
    
treeCtrl
    MPL_base:   matplotlib_base
    global_ID:  全局ID
    global_func:    shape操作
    images:         base64图像
    show_shapefile:  展示shapefile
    wxOGL_circle:    wxOGL显示（模型构建界面）
    wxpython_matplot:   wxpython结合matplot界面
    
GridSimple：  显示表格文件
MDE_MainFrame:  主界面

    