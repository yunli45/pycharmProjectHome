# coding:utf-8
import pyodbc


def getConnect(sql):
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=127.0.0.1;DATABASE=dd;UID=sa;PWD=123456;charset=utf8')
    # 打开游标
    cursor = conn.cursor()

    if not cursor:
        raise Exception('数据库连接失败！')
    else:
        print("数据库链接成功")
    cursor.execute(sql)
    # row = cursor.fetchone()
    # 返回一个连接用于关闭，返回一个游标，
    # 在查询的的时候使用：cursor.fetchone()返回一个元组的结果集
    # 在插入的时候直接传入一个sql语句就行了不用使用后面的语句 ： cursor.execute("insert into tableName( , ) values ('', ' ')")
    # conn.commit()
    return conn, cursor


def breakConnect(conn):
    conn.commit()
    conn.close()
    print("数据库链接已关闭")
# getConnect( "select * from 知识产权局更新记录表 where id = (select max(id) from 知识产权局更新记录表 )")

""""
"""
# if __name__ == '__main__':
#
#     sql = "update  table1 set name='ss'  where id=1;update  table1 set name='ss'  where id=2;update  table1 set name='ss'  where id=1;update  table1 set name='ss'  where id=3;"
#     ss = getConnect(sql)
#     conn = ss[0]
#     cursor = ss[1]
#     breakConnect(conn)