# coding:utf-8
import requests
import re
import time
from bs4 import BeautifulSoup
import pymssql

class Util(object):
    def __init__(self):
        self.header =  {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
        self.OnlyID = 1
        self.showId = 12309100

    def getPage(self, url=None):
        response = requests.get(url, headers=self.header)
        response = response.content.decode('UTF-8')
        return response

    def parsePage(self, url=None, pageNo=None, baseUrl="http://scjg.tj.gov.cn", path="F:\行政处罚数据\天津\市场和质量监督管理局_和平区\/%s"):
        if pageNo =="1":
            response = self.getPage(url+".html")
            print(url+".html")
        else:
            response = self.getPage(url+"_"+str(int(pageNo)-1)+".html")

        print("+++++++++++++++++++这是第："+pageNo+"页++++++++++++++++")
        print(response)

#######     执行    ########
if __name__ =="__main__":
    # 共计353页
    url ="http://scjg.tj.gov.cn/heping/zwgk/xzcfxx/index"
    # url ="http://scjg.tj.gov.cn/jgdt/xzcfxxgs/index_1.html"
    AdminiStrative =Util()
    for i in range(1,13):
        AdminiStrative.parsePage(url,str(i))
        time.sleep(2)

























































