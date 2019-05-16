import pymssql


def getConnect(sql):
    conn = pymssql.connect(host='(local)', user='sa', password='123456', database='AdministrativePunNingXia')
    # 打开游标
    cur = conn.cursor();
    if not cur:
        raise Exception('数据库连接失败！')
    else:
        print("数据库链接成功")
    cur.execute(sql)
    return conn
def breakConnect(conn):
    conn.commit()
    conn.close()

# getConnect(sql='')

