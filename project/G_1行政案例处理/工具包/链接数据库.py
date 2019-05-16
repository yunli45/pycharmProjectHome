# coding:utf-8
import pyodbc


def get_connect_cursor():
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=192.168.31.124\SQLEXPRESS;DATABASE=cnlaw2.0;UID=sa;PWD=123qwe!@#')
    # 打开游标
    cursor = conn.cursor()
    if not cursor:
        raise Exception('数据库连接失败！')
    else:
        # pass
        print("数据库链接成功")

    # 返回一个连接(conn)用于关闭，返回一个游标(cursor)，
    return conn, cursor


# 这个方法可以直查询整个数据库的所有数据
def query_1(cursor, sql):
    rows = cursor.execute(sql)
    # row = cursor.fetchone()
    # 在查询的的时候使用：cursor.fetchone()返回一个元组的结果集
    # 在插入的时候直接传入一个sql语句就行了不用使用后面的语句 ： cursor.execute("insert into tableName( , ) values ('', ' ')")
    #                    conn.commit()
    # 返回一个row（查询的结果集）,注意使用完查询后，记得使用关闭方法
    # 使用如下
    # for r in row:
    #     print (r)

    return rows


# 该方法查询一条数据
def query_12(cursor, sql):
    cursor.execute(sql)
    row = cursor.fetchone()
    return row


def insert(cursor, sql):
    cursor.execute(sql)


def break_connect(conn):
    conn.commit()
    conn.close()
    print("数据库链接已关闭")


# 测试用的，需要才打开下面的注释
# if __name__ == '__main__':
    # sql_1 = "select max(showid)  from 行政案例数据库.dbo.行政案例测试表"
    # sql_2 = "select *  from 行政案例数据库.dbo.行政案例测试表 where dataid='{0}'".format("t20170527_2957568.html")
    # sql = sql_1 +";"+ sql_2
    # rs = get_connect_cursor()
#     conn = rs[0]
#     cursor = rs[1]
#     rs1 = query(cursor, sql_1)
#     rs2 = query(cursor, sql_2)
#     print(rs1)
#     print(rs2)
#     if rs2 is None :
#         print("yes")
#     else:
#         print("No")
#     break_connect(conn)
