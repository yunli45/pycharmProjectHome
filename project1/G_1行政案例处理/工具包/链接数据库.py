# coding:utf-8
import pyodbc


def get_connect_cursor():
    # conn = pyodbc.connect('DRIVER={SQL Server};SERVER=127.0.0.1;DATABASE=行政案例数据库;UID=sa;PWD=123456', charset="UTF-8")
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=192.168.31.124\SQLEXPRESS;DATABASE=cnlaw2.0;UID=sa;PWD=123qwe!@#', charset="UTF-8")
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
def query_all(cursor, sql):
    cursor.execute(sql)
    rows = cursor.fetchall()

    return rows


# 该方法查询一条数据
def query_one(cursor, sql):
    cursor.execute(sql)
    row = cursor.fetchone()
    return row


def insert(conn, cursor, sql):
    if not cursor:
        raise Exception('没有传递指针（游标）进来')
    else:
        print("ggg")
        cursor.execute(sql)
        conn.commit()
        print("插入成功")


def break_connect(conn):

    conn.close()
    print("数据库链接已关闭")


# 测试用的，需要才打开下面的注释
# if __name__ == '__main__':
#     sql = """
#     UPDATE AdministrativeCase set 预处理后的全文='
#     	<p>2017年1月1日，当事人董立群在千岛湖许源水域使用钓竿4根进行无证捕捞（垂钓）作业，钓起渔获物3尾（已当场放流），其行为违反了《中华人民共和国渔业法》第二十三条第一款之规定，依据《中华人民共和国渔业法》第四十一条之规定，对当事人作出罚款1000元的行政处罚。</p><br/>
#     ' , 全文的字数=155 where ID=2;
#     UPDATE AdministrativeCase set 预处理后的全文='
#     	<p>2017年1月1日，当事人董立群在千岛湖许源水域使用钓竿4根进行无证捕捞（垂钓）作业，钓起渔获物3尾（已当场放流），其行为违反了《中华人民共和国渔业法》第二十三条第一款之规定，依据《中华人民共和国渔业法》第四十一条之规定，对当事人作出罚款1000元的行政处罚。</p><br/>
#     ' , 全文的字数=155 where ID=3;
#     UPDATE AdministrativeCase set 预处理后的全文='
#     	<p>2017年1月1日，当事人董立群在千岛湖许源水域使用钓竿4根进行无证捕捞（垂钓）作业，钓起渔获物3尾（已当场放流），其行为违反了《中华人民共和国渔业法》第二十三条第一款之规定，依据《中华人民共和国渔业法》第四十一条之规定，对当事人作出罚款1000元的行政处罚。</p><br/>
#     ' , 全文的字数=155 where ID=4;
#     """
#     rs = get_connect_cursor()
#     conn = rs[0]
#     cursor = rs[1]
#     sql = " select * from 行政案例数据库.dbo.中华人民共和国环境生态部"
#     insert(cursor, conn, sql_1)
#     insert(cursor, sql)
#     print(query_all(cursor, sql))
    # break_connect(conn)


