# coding:utf-8
from G_1行政案例处理.工具包 import 预处理模块, 链接数据库
import pyodbc
import re
import time



def handle_data(table_name):

    # 链接数据库获取：链接对象（conn）和游标（cursor）
    conn_cursor_1 = 链接数据库.get_connect_cursor()
    conn_1 = conn_cursor_1[0]
    cursor_1 = conn_cursor_1[1]

    # 查询总数
    # total_sql = "select ID,全文,超长内容 from {0}  where 超长内容".format(table_name)
    # 处理全文超长的情况
    total_sql = "select ID,全文,超长内容 FROM [cnlaw2.0].[dbo].[AdministrativeCase] where CAST(超长内容 as nvarchar(max))!='' and 超长内容  is not NULL and CAST(超长内容 as nvarchar(max))!='NULL' and CAST(全文 as nvarchar(max))!='None' and CAST(超长内容 as nvarchar(max))!='None' "
    # print(total_sql)
    # 因为pyodbc查询后返回的结果是一个元组(2375658, )，取第元组的第一元素
    total = 链接数据库.query_1(cursor_1, total_sql)
    i = 0
    update_sql = " "

    # 处理全文超长的情况
    for id_content in total:
        i += 1
        id = id_content[0]
        content_1 = id_content[1]
        content_2 = id_content[2]
        content = str(content_1) + str(content_2)
        content = 预处理模块.dispose_of_data_1(content)
        content = 预处理模块.dispose_of_data_2(content)
        content = 预处理模块.dispose_title(content)
        content = 预处理模块.dispose_inscriber(content)
        content = 预处理模块.dispose_of_data_end(content)

        # 去除标签统计字数
        char_num = len(re.sub('</？[^>]*>', '', content))

        update_sql += "UPDATE {0} set 预处理后的全文='{1}' , 全文的字数={2} where ID={3};\n".format(table_name, content, int(char_num),
                                                                                    id)
        print("update_sql" + str(update_sql))
        time1 = time.time()
        if i == 46:
            conn_cursor = 链接数据库.get_connect_cursor()
            conn = conn_cursor[0]
            cursor = conn_cursor[1]
            链接数据库.insert(cursor, update_sql)
            链接数据库.break_connect(conn)
            print("已处理到： " + str(i) + "行数据")
            print(update_sql)
            update_sql = ''
            time2 = time.time()
            print("用时为："+str(time2-time1))


    # for id_content in total:
    #     i += 1
    #     id = id_content[0]
    #     content = id_content[1]
    #     content = str(content)
    #     content = 预处理模块.dispose_of_data_1(content)
    #     content = 预处理模块.dispose_of_data_2(content)
    #     content = 预处理模块.dispose_title(content)
    #     content = 预处理模块.dispose_inscriber(content)
    #     content = 预处理模块.dispose_of_data_end(content)
    #
    #     # 去除标签统计字数
    #     char_num = len(re.sub('</?\w+[^>]*>', '', content))
    #     char_num = len(re.sub('</？[^>]*>', '', content))
    #     # print(char_num)
    #     update_sql += "UPDATE {0} set 预处理后的全文='{1}' , 全文的字数={2} where ID={3};\n".format(table_name, content, int(char_num), id)
    #     # print(update_sql)
    #     time1 = time.time()
    #     if i % 10 == 0 or id == 2375658:
    #         conn_cursor = 链接数据库.get_connect_cursor()
    #         conn = conn_cursor[0]
    #         cursor = conn_cursor[1]
    #         链接数据库.insert(cursor, update_sql)
    #         链接数据库.break_connect(conn)
    #         print("已处理到： " + str(i) + "行数据")
    #         print(update_sql)
    #         update_sql = ''
    #         time2 = time.time()
    #         print("用时为："+str(time2-time1))




handle_data('[cnlaw2.0].dbo.[AdministrativeCase]')