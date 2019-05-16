# coding:utf-8
import pyodbc

class my_odbc():
    # def __init__(self, driver, server, data_base, uid, pwd):
    #
    #     """ initialization
    #      """
    #     self.driver = driver
    #     self.server = server
    #     self.data_base = data_base
    #     self.uid = uid
    #     self.pwd = pwd
    def __init__(self):

        """ initialization
         """
        # self.driver = '{SQL Server}'
        #         # self.server = '192.168.31.124\SQLEXPRESS'
        #         # self.data_base = 'cnlaw2.0'
        #         # self.uid = 'sa'
        #         # self.pwd = '123qwe!@#'
        self.driver = '{SQL Server}'
        self.server = '127.0.0.1'
        self.data_base = '行政案例数据库'
        self.uid = 'sa'
        self.pwd = '123456'

    def get_connect_cursor(self):

        """ Connect to the DB """

        if not self.data_base:
            raise (NameError, "no setting db info")
        conn = pyodbc.connect(driver=self.driver, server=self.server, data_base=self.data_base, uid=self.uid,
                                   pwd=self.pwd, charset="UTF-8")
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
    def query_all(self, sql):
        cursor = self.get_connect_cursor()[1]  # 建立链接并创建数据库操作指针
        rows = cursor.execute(sql)  # 通过指针来执行sql指令
        return rows

    # 该方法查询一条数据
    def query_one(self, sql):
        cursor = self.get_connect_cursor()[1]  # 建立链接并创建数据库操作指针
        cursor.execute(sql)
        # row = cursor.fetchone()
        row = cursor.fetchall()  # 通过指针来获取sql指令响应数据
        self.conn.close()  # 关闭数据库连接
        return row

    def insert(self, sql):
        conn_cursor = self.get_connect_cursor()
        cursor = conn_cursor[1]
        conn = conn_cursor[0]
        print(cursor)
        # 建立链接并创建数据库操作指针
        cursor.execute(sql)
        conn.commit()
        print("插入成功")
        conn.close()  # 关闭数据库连接

    def break_connect(self, conn):
        conn.commit()
        conn.close()
        print("数据库链接已关闭")




