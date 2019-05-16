from 工具包 import 链接数据库
import re

def cc(table_name, model):
    connect_cursor = 链接数据库.get_connect_cursor()
    conn = connect_cursor[0]
    cursor = connect_cursor[1]
    sql_1 = "select 文本内容1, showid  from {0} where 来自于那个模块= '{1}'".format(table_name, model)
    print(sql_1)
    # 查询
    data_id_rs = 链接数据库.query_1(cursor, sql_1)
    # print(data_id_rs)
    for i in data_id_rs:
        showid = i[1]
        cont = i[0]
        ss = re.findall('<img.*?wps.*?.tmp.png">', cont)
        # ss = re.findall('<img.*?wps.*?.png">', cont)
        # ss = re.findall('.*?2014年度农业行政处罚案件基本情况.*?">', cont)
        if ss!=[]:
            print(showid)
            cont_1 = re.sub('<img.*?wps.*?.tmp.png">', '',cont)
            sql_2 = "update {0} set 文本内容1='{1}' where showid ='{2}' ".format(table_name, cont_1, showid)
            链接数据库.insert(cursor, sql_2)
    链接数据库.break_connect(conn)
table_name ='行政案例数据表'
model = '海南省>临高县'
cc(table_name, model)