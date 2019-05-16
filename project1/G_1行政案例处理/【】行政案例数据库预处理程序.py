# coding:utf-8
from G_1行政案例处理.工具包 import 预处理模块
from G_1行政案例处理.工具包.链接数据库 import my_odbc
import re


def handle_data(table_name):

    # 链接数据库获取：链接对象（conn）和游标（cursor）

    sql_1 = "select ID,全文,超长内容 FROM [cnlaw2.0].dbo.[AdministrativeCase]   where CAST(全文 as nvarchar(max))!='' "

    sql_2 = "and 全文 is not NULL and CAST(全文 as nvarchar(max))!='NULL'  "

    slq_3 = " and CAST(全文 as nvarchar(max))!='None'"

    total_sql = sql_1+sql_2+slq_3
    print(total_sql)
    # 因为pyodbc查询后返回的结果是一个元组(2375658, )，取第元组的第一元素
    ms = my_odbc('{SQL server}', r'192.168.31.124\SQLEXPRESS', 'cnlaw2.0', 'sa', '123qwe!@#')
    ms_cur = ms.get_connect_cursor()
    total = ms.query_all(total_sql)
    i = 0
    update_sql = " "

    for id_content in total:
        i += 1
        id = id_content[0]  # 这是ID
        content_1 = id_content[1]  # 这是全文
        content_2 = id_content[2]  # 这是超长内容

        # if str(content_1) != 'None' and str(content_1) is not None and str(content_1) != '' and str(content_2) != 'NULL':
            # print("正在读取第"+str(id))
        content = (str(content_1) + str(content_2)).replace("None", '')
        content = 预处理模块.dispose_of_data_1(content)
        content = 预处理模块.dispose_title(content)
        content = 预处理模块.dispose_of_data_end(content)

    # 去除标签统计字数
        char_num = len(re.sub('</？[^>]*>', '', content))

        update_sql += "UPDATE [cnlaw2.0].dbo.[AdministrativeCase]   set 预处理后的全文='{0}' , 全文的字数={1} where ID={2};\n".format(content, int(char_num), id)

        if i % 10 == 0 or i == 2082598:
            print(update_sql)
            # ms_cur_1 = ms.get_connect_cursor()
            ms.insert(update_sql)
            print("已处理到： " + str(i) + "行数据")
            update_sql = ''

# handle_data('[cnlaw2.0].dbo.[AdministrativeCase]')
handle_data('AdministrativeCase')