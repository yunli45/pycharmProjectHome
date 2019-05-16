import requests
from bs4 import BeautifulSoup
import time
import re
import datetime
from 大邑县卫计局.工具包 import 链接数据库,附件下载程序,预处理模块

本次更新时间 = datetime.datetime.now().strftime('%Y-%m-%d')

class Utils(object):
    # 一些共用的初始化参数
    def __init__(self):
        self.header = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
        self.pagelable = "div"
        self.pagelableSelector = "class"
        self.pageTableName = "zwgklist"
        self.pageNumS = "pagination_index_last"

    # 用于匹配-首页的总页数 、 每页的记录数的,返回总页数和每页数据的集合（url、标题、时间）
    def pageDate(self, response):
        response = BeautifulSoup(response, 'lxml')
        # 总记录数
        pageSoup = response.find_all(self.pagelable, attrs={self.pagelableSelector: self.pageNumS})
        pageS = re.findall(re.compile("<font.*?>共(.*?)页"),str(pageSoup))
        pageS1 =pageS[0]
        print(pageS1)
        # 每条数据
        pageSoup1 = response.find_all(self.pagelable, attrs={self.pagelableSelector: self.pageTableName})
        RSList = re.findall(re.compile(self.compilePageTable), str(pageSoup1))
        print("这一页一共有："+str(len(RSList))+"条数据")
        return pageS1,RSList
 # 用于的访问--页面的数据
    def getPage(self,url):
        response = requests.get(url,headers=self.header)
        print(response.url)
        if response.status_code == 404:
            pass
        else:
            response = response.content.decode('utf-8', errors='ignore')
        print(response)
        return response
# 用于的访问首页，返回每页的数据
    def getEveryPage(self,url,pageNo):
        if pageNo == "1":
            url = url
        else:
            url = url + str(int(pageNo) - 1) + ".htm"
        response = requests.get(url, headers=self.header)
        print(response.url)
        if response.status_code == 404:
            pass
        else:
            response = response.content.decode('utf-8', errors='ignore')
        print(response)
        return response
  # 用于解析具体的页面：判断初始的src是否有跳转、是否是附件、以及具体页面数据的提取
    def parePage(self,src,baseUrl,):
        pass
# 用于读取数据库当前数据表中的最大id
    def readTableRecord(self):
        sql ="select max(id) from 大邑县卫生局数据"
        con = 链接数据库.getConnect(sql)
        conn = con[0]
        cursor = con[1]
        row = cursor.fetchone()
        # print(row)  # (None, )
        pass

 # 写入本次插入数据的记录(保存爬取记录的--知识产权局更新记录表)
    def writeTableRecod(self, sql):
        con = 链接数据库.getConnect(sql)
        conn = con[0]
        链接数据库.breakConnect(conn)

if __name__ =="__main__":
    AdminiStrative = Utils()
    url = "http://www.nhfpc.gov.cn/zwgk/jdjd/ejlist.shtml"
    AdminiStrative.getPage(url)

    # AdminiStrative.getPage( )