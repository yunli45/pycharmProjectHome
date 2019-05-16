
from 工具包 import 链接数据库


class Utils(object):
    def __init__(self):
        self.i = 5

    def test(self):
        connect_cursor = 链接数据库.get_connect_cursor()
        conn = connect_cursor[0]
        cur = connect_cursor[1]
        sql = """select * from [wj-卫计局] where 标题='国务院办公厅关于改革完善医疗卫生行业综合监管制度的指导意见'"""
        rs = 链接数据库.query(cur, sql)

        print(rs)
        with open(r'D:\Python\pythonProjectHome\卫计局自动抓取\test', 'a') as f:
            for i in range(1,3):
                f.write(str(i)+"\n\n")

# if __name__ == '__main__':
#     until = Utils()
#     until.test()