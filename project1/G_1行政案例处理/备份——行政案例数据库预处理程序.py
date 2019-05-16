# coding:utf-8
from G_1行政案例处理.工具包 import 预处理模块, 链接数据库
import re
import pyodbc


def handle_data(table_name):

    # 链接数据库获取：链接对象（conn）和游标（cursor）


    sql_1 = "select ID,全文,超长内容 FROM [AdministrativeCase]  where CAST(全文 as nvarchar(max))!='' "

    sql_2 = "and 全文 is not NULL and CAST(全文 as nvarchar(max))!='NULL'  "

    slq_3 = " and CAST(全文 as nvarchar(max))!='None'"

    total_sql = sql_1+sql_2+slq_3
    print(total_sql)
    # print(total_sql)
    # # 因为pyodbc查询后返回的结果是一个元组(2375658, )，取第元组的第一元素
    conn_cursor_1 = 链接数据库.get_connect_cursor()
    conn_1 = conn_cursor_1[0]
    cursor_1 = conn_cursor_1[1]
    total = 链接数据库.query_all(cursor_1, total_sql)
    链接数据库.break_connect(conn_1)
    i = 0
    update_sql = " "

    # 处理全文
    for id_content in total:
        print(id_content)
        i += 1
        id = id_content[0]  # 这是ID
        content_1 = id_content[1]  # 这是全文
        content_2 = id_content[2]  # 这是超长内容
        content = (str(content_1) + str(content_2)).replace("None", '')
        content = 预处理模块.dispose_of_data_1(content)
        content = 预处理模块.dispose_title(content)
        content = 预处理模块.dispose_of_data_end(content)

    # 去除标签统计字数
        char_num = len(re.sub('</？[^>]*>', '', content))
        update_sql += "UPDATE {0} set 预处理后的全文='{1}' , 全文的字数={2} where ID={3};\n".format(table_name, content, int(char_num),id)

        if i % 10== 0 or i == 2082598:
            print("更新的语句" + update_sql)
            conn_cursor_2 = 链接数据库.get_connect_cursor()
            conn_2 = conn_cursor_2[0]
            cursor_2 = conn_cursor_2[1]
            链接数据库.insert(conn_2, cursor_2, update_sql)
            链接数据库.break_connect(conn_2)
            update_sql = ''


if __name__ == '__main__':
    handle_data('[AdministrativeCase]')