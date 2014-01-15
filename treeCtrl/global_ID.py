# -*- coding: utf-8 -*-  
import choosed

#--global ID ----
global ID

#############################
##        module part          ##
#############################

global ID_NEW_MODULE 
global ID_MODULE_XML 

global ID_SOCIAL_MODULE 
global ID_POPULATION_MODULE
global ID_DENSITY_MODULE 

#############################
##        DB part          ##
#############################
global ID_DB_LINK
global ID_DB_VECTOR
global ID_DB_RASTER
global ID_DB_STATISTIC
global ID_DB_METADB
global ID_DB_MAINDB

#############################
##     spatialdata part    ##
#############################
global ID_SHP_AREA
global ID_SHP_LENGTH
global ID_SHP_EXTENT
global ID_SHP_CENTER
global ID_SHP_POINT
global ID_SHP_OUT
global ID_SHP_BUFFER
global ID_SHP_SIMPLE
global ID_SHP_INTERSECT
global ID_SHP_DIFFERENCE
global ID_SHP_UNION

global ID_RASTER_MOVE
global ID_RASTER_ROTATE
global ID_RASTER_ZOOMIN
global ID_RASTER_CUT
global ID_RASTER_ROI
global ID_RASTER_UNION
global ID_RASTER_REVERSE
global ID_RASTER_BALANCE
global ID_RASTER_SLOP
global ID_RASTER_SHARP
global ID_RASTER_COLOR

#############################
##    statistic part       ##
#############################
global ID_STATIC_ABS                #绝对值
global ID_STATIC_AVERAGE            #算术平均值
global ID_STATIC_CONCATENATE        #连接多个单元格（合并函数）
global ID_STATIC_DENSITY	    #密度函数（人数/面积） 
global ID_STATIC_FREQUENCY	    #频率分布
global ID_STATIC_MAX	            #最大值
global ID_STATIC_MIN	            #最小值
global ID_STATIC_MOD                #余数
global ID_STATIC_RANK               #排名函数
global ID_STATIC_SUBTOTAL	    #分类汇总
global ID_STATIC_SUM	            #求和
global ID_STATIC_STDEV              #标准偏差


#############################
##     search part         ##
#############################
global ID_SEARCH_TIME_SP
global ID_SEARCH_TIME_ATTRI
global ID_SEARCH_TIME_SP_ATTRI

#############################
##     show part           ##
#############################
global ID_SHOW_PIE 
global ID_SHOW_HISTGRAM
global ID_SHOW_RADIA
global ID_SHOW_QQPLOT
global ID_SHOW_SCARTE
global ID_SHOW_BAR
global ID_SHOW_LINE

global ID_SSHOW_PIE
global ID_SSHOW_BAR
global ID_SSHOW_CLASSIFY



#--global PIC ----
#####################################################################################################################################
#############################
##        module part          ##
#############################
global PIC_NEW_MODULE 
global PIC_MODULE_XML 

global PIC_SOCIAL_MODULE 
global PIC_POPULATION_MODULE
global PIC_DENSITY_MODULE 

#############################
##        DB part          ##
#############################
global PIC_DB_LINK
global PIC_DB_VECTOR
global PIC_DB_RASTER
global PIC_DB_STATISTIC
global PIC_DB_METADB
global PIC_DB_MAINDB

#############################
##     search part         ##
#############################
global PIC_SEARCH_TIME_SP
global PIC_SEARCH_TIME_ATTRI
global PIC_SEARCH_TIME_SP_ATTRI

#############################
##     spatialdata part    ##
#############################
global PIC_SHP_AREA
global PIC_SHP_LENGTH
global PIC_SHP_EXTENT
global PIC_SHP_CENTER
global PIC_SHP_POINT
global PIC_SHP_OUT
global PIC_SHP_BUFFER
global PIC_SHP_SIMPLE
global PIC_SHP_INTERSECT
global PIC_SHP_DIFFERENCE
global PIC_SHP_UNION

global PIC_RASTER_MOVE
global PIC_RASTER_ROTATE
global PIC_RASTER_ZOOM
global PIC_RASTER_CUT
global PIC_RASTER_ROI
global PIC_RASTER_UNION
global PIC_RASTER_REVERSE
global PIC_RASTER_BALANCE
global PIC_RASTER_SLOP
global PIC_RASTER_SHARP
global PIC_RASTER_COLOR

#############################
##    statistic part       ##
#############################
global PIC_STATIC_ABS                #绝对值
global PIC_STATIC_AVERAGE            #算术平均值
global PIC_STATIC_CONCATENATE        #连接多个单元格（合并函数）
global PIC_STATIC_DENSITY	    #密度函数（人数/面积） 
global PIC_STATIC_FREQUENCY	    #频率分布
global PIC_STATIC_MAX	            #最大值
global PIC_STATIC_MIN	            #最小值
global PIC_STATIC_MOD                #余数
global PIC_STATIC_RANK               #排名函数
global PIC_STATIC_SUBTOTAL	    #分类汇总
global PIC_STATIC_SUM	            #求和
global PIC_STATIC_STDEV              #标准偏差



#############################
##     show part           ##
#############################
global PIC_SHOW_PIE 
global PIC_SHOW_HISTGRAM
global PIC_SHOW_RADIA
global PIC_SHOW_QQPLOT
global PIC_SHOW_SCARTE
global PIC_SHOW_BAR
global PIC_SHOW_LINE

global PIC_SSHOW_PIE
global PIC_SSHOW_BAR
global PIC_SSHOW_CLASSIFY


#------------  global ID VALUE ---------
########################################################################################################################################
ID = 1000

ID_NEW_MODULE	= ID + 100
ID_MODULE_XML	= ID_NEW_MODULE + 1

ID_SOCIAL_MODULE 	= ID_NEW_MODULE + 2
ID_POPULATION_MODULE	= ID_NEW_MODULE + 3
ID_DENSITY_MODULE 	= ID_NEW_MODULE + 4
ID_OTHER_MODULE 	= ID_NEW_MODULE + 5
######################
##   DB part        ##
######################
ID_DB_LINK	= ID + 200

ID_DB_VECTOR	= ID_DB_LINK + 1
ID_DB_RASTER	= ID_DB_LINK + 2
ID_DB_STATISTIC	= ID_DB_LINK + 3
ID_DB_METADB	= ID_DB_LINK + 4
ID_DB_MAINDB	= ID_DB_LINK + 5

ID_SEARCH_TIME_SP         = ID + 250  
ID_SEARCH_TIME_ATTRI      = ID_SEARCH_TIME_SP + 1  
#ID_SEARCH_TIME_SP_ATTRI   = ID_SEARCH_TIME_SP + 2  

######################
##spatialdata part    ##
######################
ID_SHP_AREA		= ID + 300
ID_SHP_LENGTH		= ID_SHP_AREA +1
ID_SHP_EXTENT		= ID_SHP_AREA +2
ID_SHP_CENTER		= ID_SHP_AREA +3
ID_SHP_POINT		= ID_SHP_AREA +4
ID_SHP_OUT		= ID_SHP_AREA +5
ID_SHP_BUFFER		= ID_SHP_AREA +6
ID_SHP_SIMPLE		= ID_SHP_AREA +7
ID_SHP_INTERSECT	= ID_SHP_AREA +8
ID_SHP_DIFFERENCE	= ID_SHP_AREA +9
ID_SHP_UNION		= ID_SHP_AREA +10

ID_RASTER_MOVE  	= ID + 350
ID_RASTER_ROTATE	= ID_RASTER_MOVE+1
ID_RASTER_ZOOM		= ID_RASTER_MOVE+2
ID_RASTER_CUT		= ID_RASTER_MOVE+3	
ID_RASTER_ROI		= ID_RASTER_MOVE+4		
ID_RASTER_UNION		= ID_RASTER_MOVE+5		
ID_RASTER_REVERSE	= ID_RASTER_MOVE+6	
ID_RASTER_BALANCE	= ID_RASTER_MOVE+7	
ID_RASTER_SLOP		= ID_RASTER_MOVE+8
ID_RASTER_SHARP		= ID_RASTER_MOVE+9
ID_RASTER_COLOR		= ID_RASTER_MOVE+10

######################
##tatistic part       ##
######################
ID_STATIC_ABS         	= ID + 400    
ID_STATIC_AVERAGE	= ID_STATIC_ABS + 1         
ID_STATIC_CONCATENATE	= ID_STATIC_ABS + 2      
ID_STATIC_DENSITY	= ID_STATIC_ABS + 3 	    #
ID_STATIC_FREQUENCY	= ID_STATIC_ABS + 4 	    #
ID_STATIC_MAX		= ID_STATIC_ABS + 5 	         
ID_STATIC_MIN		= ID_STATIC_ABS + 6 	         
ID_STATIC_MOD		= ID_STATIC_ABS + 7              
ID_STATIC_RANK		= ID_STATIC_ABS + 8             
ID_STATIC_SUBTOTAL	= ID_STATIC_ABS + 9 	    #
ID_STATIC_SUM		= ID_STATIC_ABS + 10 	         
ID_STATIC_STDEV		= ID_STATIC_ABS + 11            


######################
##show part         ##
######################
ID_SHOW_PIE 		= ID + 500
ID_SHOW_HISTGRAM	= ID_SHOW_PIE + 1
ID_SHOW_RADIA		= ID_SHOW_PIE + 2
ID_SHOW_QQPLOT		= ID_SHOW_PIE + 3
ID_SHOW_SCARTE		= ID_SHOW_PIE + 4
ID_SHOW_BAR		= ID_SHOW_PIE + 5
ID_SHOW_LINE		= ID_SHOW_PIE + 6

ID_SSHOW_PIE  		= ID + 550
ID_SSHOW_BAR		= ID_SSHOW_PIE + 1
ID_SSHOW_CLASSIFY	= ID_SSHOW_PIE +2


#---------  globale pic value ----------------
#####################################################################################################################################

#############################
##        module part      ##
#############################
PIC_NEW_MODULE		          = choosed.new_module                
PIC_MODULE_XML                    = choosed.module_xml                               
PIC_POPULATION_MODULE             = choosed.population_module
PIC_DENSITY_MODULE                = choosed.density_module
                                   
#############################     
##     DB PART          ##        
#############################     
PIC_DB_LINK                       = choosed.DB_link     
PIC_DB_VECTOR                     = choosed.db_vector
PIC_DB_RASTER                     = choosed.db_raster
PIC_DB_STATISTIC                  = choosed.db_statistic
PIC_DB_METADB                     = choosed.db_metadb
PIC_DB_MAINDB                     = choosed.db_maindb
                                   
#############################      
##     SEARCH PART         ##      
#############################      
PIC_SEARCH_TIME_SP                = choosed.search_time_sp
PIC_SEARCH_TIME_ATTRI             = choosed.search_time_attri
PIC_SEARCH_TIME_SP_ATTRI          = choosed.search_time_sp_attri
                                   
#############################     
##     SPATIALDATA PART    ##     
#############################     
PIC_SHP_AREA                      = choosed.shp_area       
PIC_SHP_LENGTH                    = choosed.shp_length
PIC_SHP_EXTENT                    = choosed.shp_extent
PIC_SHP_CENTER                    = choosed.shp_center
PIC_SHP_POINT                     = choosed.shp_point
PIC_SHP_OUT                       = choosed.shp_out
PIC_SHP_BUFFER                    = choosed.shp_buffer
PIC_SHP_SIMPLE                    = choosed.shp_simple
PIC_SHP_INTERSECT                 = choosed.shp_intersect
PIC_SHP_DIFFERENCE                = choosed.shp_difference
PIC_SHP_UNION                     = choosed.shp_union
                                  
PIC_RASTER_MOVE                   = choosed.raster_move    
PIC_RASTER_ROTATE                 = choosed.raster_rotate
PIC_RASTER_ZOOM                   = choosed.raster_zoom
PIC_RASTER_CUT                    = choosed.raster_cut
PIC_RASTER_ROI                    = choosed.raster_roi
PIC_RASTER_UNION                  = choosed.raster_union
PIC_RASTER_REVERSE                = choosed.raster_reverse
PIC_RASTER_BALANCE                = choosed.raster_balance
PIC_RASTER_SLOP                   = choosed.raster_slop
PIC_RASTER_SHARP                  = choosed.raster_sharp
PIC_RASTER_COLOR                  = choosed.raster_color
                                  
#############################   
##    STATISTIC PART       ##   
#############################   
PIC_STATIC_ABS                    = choosed.static_abs                    #绝对值
PIC_STATIC_AVERAGE                = choosed.static_average            #算术平均值
PIC_STATIC_CONCATENATE            = choosed.static_concatenate        #连接多个单元
PIC_STATIC_DENSITY	          = choosed.static_density	    #密度函数（人数/面
PIC_STATIC_FREQUENCY	          = choosed.static_frequency	    #频率分布
PIC_STATIC_MAX	                  = choosed.static_max	            #最大值
PIC_STATIC_MIN	                  = choosed.static_min	            #最小值
PIC_STATIC_MOD                    = choosed.static_mod                #余数
PIC_STATIC_RANK                   = choosed.static_rank               #排名函数
PIC_STATIC_SUBTOTAL	          = choosed.static_subtotal	    #分类汇总
PIC_STATIC_SUM	                  = choosed.static_sum	            #求和
PIC_STATIC_STDEV                  = choosed.static_stdev              #标准偏差
                                                                     
#############################    
##     SHOW PART           ##    
#############################
PIC_SHOW_PIE                      = choosed.show_pie 
PIC_SHOW_HISTGRAM                 = choosed.show_histgram
PIC_SHOW_RADIA                    = choosed.show_radia
PIC_SHOW_QQPLOT                   = choosed.show_QQPlot
PIC_SHOW_SCARTE                   = choosed.show_scarte
PIC_SHOW_BAR                      = choosed.show_bar
PIC_SHOW_LINE                     = choosed.show_line
                                  
PIC_SSHOW_PIE                     = choosed.sshow_pie
PIC_SSHOW_BAR                     = choosed.sshow_bar
PIC_SSHOW_CLASSIFY                = choosed.sshow_classify
               




#####################################################################################################################################
##    global return ID list       ######
global ID_LIST          # ID号
global ID_NAME          # ID与对应的名字
global ID_PIC           # ID与对应的图片
global ID_FUNC          # ID号与应的函数功能

ID_LIST = []
ID_NAME = {}
ID_PIC  = {}
ID_FUNC = {}

#ID_FUNC_LIST = {ID_FILE_SHP: "printa"}           ID.ID_POPULATION_MODULE        :u"人口空间分布      ",
#ID_MODULE_NAME= {ID_FILE_SHP: u"打开shp文件" , ID_FILE_RASTER:u"打开栅格文件"}ID_LIST = []

ID_NAME = {ID_NEW_MODULE	       :u"新建模型",
           ID_MODULE_XML               :u"模型描述",
           ID_POPULATION_MODULE        :u"人口空间分布",
           ID_DENSITY_MODULE           :u"人口密度",
                                       
           ID_DB_LINK                  :u"库连接",
           ID_DB_VECTOR                :u"矢量数据",
           ID_DB_RASTER                :u"栅格数据",
           ID_DB_STATISTIC             :u"统计数据",
           ID_DB_METADB                :u"元数据库查看",
           ID_DB_MAINDB                :u"主数据库查看",
                                       
           ID_SEARCH_TIME_SP           :u"时空维度抽取",
           ID_SEARCH_TIME_ATTRI        :u"时间属性维度抽取",
                                       
           ID_SHP_AREA                 :u"面积",
           ID_SHP_LENGTH               :u"长度",
           ID_SHP_EXTENT               :u"四至",
           ID_SHP_CENTER               :u"质心",
           ID_SHP_POINT                :u"关键点",
           ID_SHP_OUT                  :u"外包矩形",
           ID_SHP_BUFFER               :u"缓冲区",
           ID_SHP_SIMPLE               :u"简化",
           ID_SHP_INTERSECT            :u"求交",
           ID_SHP_DIFFERENCE           :u"求差",
           ID_SHP_UNION                :u"求合",
                                       
           ID_RASTER_MOVE              :u"移动",
           ID_RASTER_ROTATE            :u"旋转",
           ID_RASTER_ZOOM              :u"缩放",
           ID_RASTER_CUT               :u"剪切",
           ID_RASTER_ROI               :u"ROI",
           ID_RASTER_UNION             :u"合并",
           ID_RASTER_REVERSE           :u"反色",
           ID_RASTER_BALANCE           :u"色彩平衡",
           ID_RASTER_SLOP              :u"平滑",
           ID_RASTER_SHARP             :u"锐化",
           ID_RASTER_COLOR             :u"色彩增强",
                                       
           ID_STATIC_ABS               :u"绝对值",
           ID_STATIC_AVERAGE           :u"算术平均值",
           ID_STATIC_CONCATENATE       :u"合并函数",
           ID_STATIC_DENSITY	       :u"密度函数",
                                       
           ID_STATIC_FREQUENCY	       :"频率分布",
           ID_STATIC_MAX	       :u"最大值",
           ID_STATIC_MIN	       :u"最小值",
           ID_STATIC_MOD               :u"余数",
                                       
           ID_STATIC_RANK              :u"排名函数",
           ID_STATIC_SUBTOTAL	       :u"分类汇总",
           ID_STATIC_SUM	       :u"求和",
           ID_STATIC_STDEV             :u"标准偏差",
                                       
           ID_SHOW_PIE                 :u"饼状图",
           ID_SHOW_HISTGRAM            :u"直方图",
           ID_SHOW_RADIA               :u"雷达图",
           ID_SHOW_QQPLOT              :u"QQPlot",
           ID_SHOW_SCARTE              :u"散点图",
           ID_SHOW_BAR                 :u"矩状图",
           ID_SHOW_LINE                :u"折线图",
                                       
           ID_SSHOW_PIE                :u"空间饼状分布图",
           ID_SSHOW_BAR                :u"空间矩状分布图",
           ID_SSHOW_CLASSIFY           :u"空间分层分布图" }


ID_PIC = {ID_NEW_MODULE		  :  "pic_new_module",
          ID_MODULE_XML           :  "pic_module_xml",
          ID_POPULATION_MODULE    :  "pic_population_module",
          ID_DENSITY_MODULE       :  "pic_density_module",
                                     
          ID_DB_LINK              :  "pic_db_link",
          ID_DB_VECTOR            :  "pic_db_vector",
          ID_DB_RASTER            :  "pic_db_raster",
          ID_DB_STATISTIC         :  "pic_db_statistic",
          ID_DB_METADB            :  "pic_db_metadb",
          ID_DB_MAINDB            :  "pic_db_maindb",
                                     
          ID_SEARCH_TIME_SP       :  "pic_search_time_sp",
          ID_SEARCH_TIME_ATTRI    :  "pic_search_time_attri",
                                     
          ID_SHP_AREA             :  "pic_shp_area",
          ID_SHP_LENGTH           :  "pic_shp_length",
          ID_SHP_EXTENT           :  "pic_shp_extent",
          ID_SHP_CENTER           :  "pic_shp_center",
          ID_SHP_POINT            :  "pic_shp_point",
          ID_SHP_OUT              :  "pic_shp_out",
          ID_SHP_BUFFER           :  "pic_shp_buffer",
          ID_SHP_SIMPLE           :  "pic_shp_simple",
          ID_SHP_INTERSECT        :  "pic_shp_intersect",
          ID_SHP_DIFFERENCE       :  "pic_shp_difference",
          ID_SHP_UNION            :  "pic_shp_union",
                                     
          ID_RASTER_MOVE          :  "pic_raster_move",
          ID_RASTER_ROTATE        :  "pic_raster_rotate",
          ID_RASTER_ZOOM          :  "pic_raster_zoom",
          ID_RASTER_CUT           :  "pic_raster_cut",
          ID_RASTER_ROI           :  "pic_raster_roi",
          ID_RASTER_UNION         :  "pic_raster_union",
          ID_RASTER_REVERSE       :  "pic_raster_reverse",
          ID_RASTER_BALANCE       :  "pic_raster_balance",
          ID_RASTER_SLOP          :  "pic_raster_slop",
          ID_RASTER_SHARP         :  "pic_raster_sharp",
          ID_RASTER_COLOR         :  "pic_raster_color",
                                     
          ID_STATIC_ABS           :  "pic_static_abs",
          ID_STATIC_AVERAGE       :  "pic_static_average",
          ID_STATIC_CONCATENATE   :  "pic_static_concatenate",
          ID_STATIC_DENSITY	   : "pic_static_density",
                                     
          ID_STATIC_FREQUENCY	   : "pic_static_frequency",
          ID_STATIC_MAX	           : "pic_static_max",
          ID_STATIC_MIN	           : "pic_static_min",
          ID_STATIC_MOD            : "pic_static_mod",
                                     
          ID_STATIC_RANK          :  "pic_static_rank",
          ID_STATIC_SUBTOTAL	  :  "pic_static_subtotal",
          ID_STATIC_SUM	          :  "pic_static_sum",
          ID_STATIC_STDEV         :  "pic_static_stdev",
                                     
          ID_SHOW_PIE             :  "pic_show_pie",
          ID_SHOW_HISTGRAM        :  "pic_show_histgram",
          ID_SHOW_RADIA           :  "pic_show_radia",
          ID_SHOW_QQPLOT          :  "pic_show_qqplot",
          ID_SHOW_SCARTE          :  "pic_show_scarte",
          ID_SHOW_BAR             :  "pic_show_bar",
          ID_SHOW_LINE            :  "pic_show_line",
                                     
          ID_SSHOW_PIE            :  "pic_sshow_pie",
          ID_SSHOW_BAR            :  "pic_sshow_bar",
          ID_SSHOW_CLASSIFY       :  "pic_sshow_classify" }



global ID_MODULE_NAME    #设置模型的名字
ID_MODULE_NAME = ""

ID_FUNC = {}


import newIcon


global ID_MODULE_COMP       #综合评价模型
global ID_MODULE_ECONOMY    #经济
global ID_MODULE_SOCIAL     #社会
global ID_MODULE_ENVIRON    #环境
global ID_SEARCH_RASTER     #抽取栅格

ID_MODULE_COMP      =  ID_NEW_MODULE + 110
ID_MODULE_ECONOMY   =  ID_MODULE_COMP + 1
ID_MODULE_SOCIAL    =  ID_MODULE_COMP + 2
ID_MODULE_ENVIRON   =  ID_MODULE_COMP + 3
ID_SEARCH_RASTER    =  ID_SEARCH_TIME_SP + 2

ID_New__NAME = {
                ID_MODULE_COMP            : [u"综合评价模型",  newIcon.comp_module ]  ,     
                ID_MODULE_ECONOMY         : [u"经济评价指标",  newIcon.economy ]  , 
                ID_MODULE_SOCIAL          : [u"社会评价指标",  newIcon.social ]  , 
                ID_MODULE_ENVIRON         : [u"环境评价指标",  newIcon.environ ]  , 
                ID_SEARCH_RASTER          : [u"栅格抽取"    ,  newIcon.search_raster ]  , 
    
                ID_NEW_MODULE	           :  [u"新建模型",         choosed.new_module        ,   ]    ,        
                ID_MODULE_XML               :  [u"模型描述",         choosed.module_xml        ,   ]    ,        
                ID_POPULATION_MODULE        :  [u"人口空间分布",     choosed.population_module ,   ]    ,        
                ID_DENSITY_MODULE           :  [u"人口密度",         choosed.density_module    ,   ]    ,        
                                                                                       
                ID_DB_LINK                  :  [u"库连接",           choosed.DB_link           ,   ]    ,    
                ID_DB_VECTOR                :  [u"矢量数据",         choosed.db_vector         ,   ]    , 
                ID_DB_RASTER                :  [u"栅格数据",         choosed.db_raster         ,   ]    , 
                ID_DB_STATISTIC             :  [u"统计数据",         choosed.db_statistic      ,   ]    ,    
                ID_DB_METADB                :  [u"元数据库查看",     choosed.db_metadb         ,   ]    , 
                ID_DB_MAINDB                :  [u"主数据库查看",     choosed.db_maindb         ,   ]    , 
                                                                                          
                ID_SEARCH_TIME_SP           :  [u"时空维度抽取",     choosed.search_time_sp    ,   ]    ,      
                ID_SEARCH_TIME_ATTRI        :  [u"时间属性维度抽取", choosed.search_time_attri ,   ]    ,         
                                                                                   
                ID_SHP_AREA                 :  [u"面积",             choosed.shp_area          ,   ]    ,       
                ID_SHP_LENGTH               :  [u"长度",             choosed.shp_length        ,   ]    ,  
                ID_SHP_EXTENT               :  [u"四至",             choosed.shp_extent        ,   ]    ,  
                ID_SHP_CENTER               :  [u"质心",             choosed.shp_center        ,   ]    ,  
                ID_SHP_POINT                :  [u"关键点",           choosed.shp_point         ,   ]    , 
                ID_SHP_OUT                  :  [u"外包矩形",         choosed.shp_out           ,   ]    ,
                ID_SHP_BUFFER               :  [u"缓冲区",           choosed.shp_buffer        ,   ]    ,  
                ID_SHP_SIMPLE               :  [u"简化",             choosed.shp_simple        ,   ]    ,  
                ID_SHP_INTERSECT            :  [u"求交",             choosed.shp_intersect     ,   ]    ,     
                ID_SHP_DIFFERENCE           :  [u"求差",             choosed.shp_difference    ,   ]    ,      
                ID_SHP_UNION                :  [u"求合",             choosed.shp_union         ,   ]    , 
                                                                                   
                ID_RASTER_MOVE              :  [u"移动",             choosed.raster_move       ,   ]    ,       
                ID_RASTER_ROTATE            :  [u"旋转",             choosed.raster_rotate     ,   ]    ,     
                ID_RASTER_ZOOM              :  [u"缩放",             choosed.raster_zoom       ,   ]    ,   
                ID_RASTER_CUT               :  [u"剪切",             choosed.raster_cut        ,   ]    ,  
                ID_RASTER_ROI               :  [u"ROI",              choosed.raster_roi        ,   ]    ,  
                ID_RASTER_UNION             :  [u"合并",             choosed.raster_union      ,   ]    ,    
                ID_RASTER_REVERSE           :  [u"反色",             choosed.raster_reverse    ,   ]    ,      
                ID_RASTER_BALANCE           :  [u"色彩平衡",         choosed.raster_balance    ,   ]    ,      
                ID_RASTER_SLOP              :  [u"平滑",             choosed.raster_slop       ,   ]    ,   
                ID_RASTER_SHARP             :  [u"锐化",             choosed.raster_sharp      ,   ]    ,    
                ID_RASTER_COLOR             :  [u"色彩增强",         choosed.raster_color      ,   ]    ,    
                                                                                                   
                ID_STATIC_ABS               :  [u"绝对值",           choosed.static_abs        ,   ]    ,            
                ID_STATIC_AVERAGE           :  [u"算术平均值",       choosed.static_average    ,   ]    ,            
                ID_STATIC_CONCATENATE       :  [u"合并函数",         choosed.static_concatenate,   ]    ,            
                ID_STATIC_DENSITY	       :  [u"密度函数",         choosed.static_density	  ,   ]    ,        
                                                                                           
                ID_STATIC_FREQUENCY	       :  ["频率分布",          choosed.static_frequency  ,   ]    ,            
                ID_STATIC_MAX	       	   :  [u"最大值",           choosed.static_max	      ,   ]    ,            
                ID_STATIC_MIN	       	   :  [u"最小值",           choosed.static_min	      ,   ]    ,            
                ID_STATIC_MOD               :  [u"余数",             choosed.static_mod        ,   ]    ,            
                                                                                             
                ID_STATIC_RANK              :  [u"排名函数",         choosed.static_rank    	  ,   ]    ,            
                ID_STATIC_SUBTOTAL	       :  [u"分类汇总",         choosed.static_subtotal   ,   ]    ,            
                ID_STATIC_SUM	       :  [u"求和",            choosed.static_sum	      ,   ]    ,        
                ID_STATIC_STDEV             :  [u"标准偏差",         choosed.static_stdev      ,   ]    ,       
                                                                                        
                ID_SHOW_PIE                 :  [u"饼状图",           choosed.show_pie          ,   ]    , 
                ID_SHOW_HISTGRAM            :  [u"直方图",           choosed.show_histgram     ,   ]    ,     
                ID_SHOW_RADIA               :  [u"雷达图",           choosed.show_radia        ,   ]    ,  
                ID_SHOW_QQPLOT              :  [u"QQPlot",           choosed.show_QQPlot       ,   ]    ,   
                ID_SHOW_SCARTE              :  [u"散点图",           choosed.show_scarte       ,   ]    ,   
                ID_SHOW_BAR                 :  [u"矩状图",           choosed.show_bar          ,   ]    ,
                ID_SHOW_LINE                :  [u"折线图",           choosed.show_line         ,   ]    , 
                                                                                                
                ID_SSHOW_PIE                :  [u"空间饼状分布图",   choosed.sshow_pie         ,   ]    , 
                ID_SSHOW_BAR                :  [u"空间矩状分布图",   choosed.sshow_bar         ,   ]    , 
                ID_SSHOW_CLASSIFY           :  [u"空间分层分布图",  choosed.sshow_classify     ,   ]       }