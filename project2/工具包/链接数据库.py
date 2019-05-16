# coding:utf-8
import pyodbc


def get_connect_cursor():
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=127.0.0.1;DATABASE=行政案例数据库;UID=sa;PWD=123456')
    # conn = pyodbc.connect('DRIVER={SQL Server};SERVER=192.168.31.124\SQLEXPRESS;DATABASE=cnlaw2.0;UID=sa;PWD=123qwe!@#')
    # 打开游标
    cursor = conn.cursor()
    if not cursor:
        raise Exception('数据库连接失败！')
    else:
        # pass
        print("数据库链接成功")

    # 返回一个连接(conn)用于关闭，返回一个游标(cursor)，
    return conn, cursor


def query(cursor, sql):
    cursor.execute(sql)
    row = cursor.fetchone()
    # 在查询的的时候使用：cursor.fetchone()返回一个元组的结果集
    # 在插入的时候直接传入一个sql语句就行了不用使用后面的语句 ： cursor.execute("insert into tableName( , ) values ('', ' ')")
    #                    conn.commit()
    # 返回一个row（查询的结果集）,注意使用完查询后，记得使用关闭方法

    return row


def query_1(cursor, sql):
    cursor.execute(sql)
    row = cursor.fetchall()
    # 在查询的的时候使用：cursor.fetchone()返回一个元组的结果集
    # 在插入的时候直接传入一个sql语句就行了不用使用后面的语句 ： cursor.execute("insert into tableName( , ) values ('', ' ')")
    #                    conn.commit()
    # 返回一个row（查询的结果集）,注意使用完查询后，记得使用关闭方法

    return row

def insert(cursor, sql):
    cursor.execute(sql)


def break_connect(conn):
    conn.commit()
    conn.close()
    print("数据库链接已关闭")


# 测试用的，需要才打开下面的注释
# if __name__ == '__main__':
#     connect_cursor = get_connect_cursor()
#     connect = connect_cursor[0]
#     cursor = connect_cursor[1]
#     qu_sql = "select * from [中华人民共和国环境生态部-2]  where 这条数据的完整请求url='http://www.mee.gov.cn/xxgk2018/xxgk/xxgk01/201810/t20181024_665301.h'"
#     qu_rs = query(cursor, qu_sql)
#     print(qu_rs)
#     if qu_rs != None:
#         print("ss")
#     else:
#         print(qu_rs)