import requests
from bs4 import BeautifulSoup
import time
import re
import datetime
from fake_useragent import UserAgent
from selenium import webdriver
from 大邑县卫计局.工具包 import 链接数据库,附件下载程序,预处理模块
from 大邑县卫计局.工具包.判断url前面的点返回完整的请求地址 import returnSRC




class Utils(object):
    # 一些共用的初始化参数
    def __init__(self):
       self.id='大爷进来玩一玩嘛'

    # 使用google浏览器的静默模式+ selenium来获取一些--动态加载--的数据
    # 获取一些需要动态加载的网页数据的获取，注意：用与匹配首页总页数和版权归属问题的时候必须使用selenium来动态加载
    def googleSilentMode(self,url):
        print("用于google浏览器动态访问首页返回数据，这一步会稍微慢点")
        option = webdriver.ChromeOptions()
        option.add_argument('headless')  # 使用google浏览器的静默模式
        browser = webdriver.Chrome(chrome_options=option)
        browser.get(url)
        response = browser.page_source
        # print("首页的数据" + response)
        response = BeautifulSoup(response, 'lxml')
        pageSoup = response.find_all(self.pagelable, attrs={self.pagelableSelector: self.pageNumS})
        pageSRs = re.findall(r'共(.*?)页', str(pageSoup))
        pageS1 = pageSRs[0].replace(' ', '')
        pageS1 = int(pageS1)
        # print("总页数"+str(pageS1))
        # 每条数据
        pageSoup1 = response.find_all(self.pagelable, attrs={self.pagelableSelector: self.pageTableName})
        # print("标签、选择器、名字"+str(self.pagelable)+str(self.pagelableSelector)+(self.pageTableName))
        # print(pageSoup1)
        RSList = re.findall(re.compile(self.compilePageTable), str(pageSoup1))
        print(RSList)
        print("这一页一共有：" + str(len(RSList)) + "条数据")
        return pageS1, RSList

    def googleGetPage(self,url):
        option = webdriver.ChromeOptions()
        option.add_argument('headless')  # 使用google浏览器的静默模式
        browser = webdriver.Chrome(chrome_options=option)
        browser.get(url)
        response = browser.page_source
        return response

# 用于解析具体的页面：判断初始的src是否有跳转、是否是附件、以及具体页面数据的提取
    def parePage(self,indexUrl,contenSrc,SavePath,超链接本地地址):
        print("首页地址"+str(indexUrl))
        contResponse = self.googleGetPage(contenSrc)
        print("第一条数据的1" + str(contResponse))
        soup = BeautifulSoup(contResponse, 'lxml')
        soupCont1 = soup.find_all('div', attrs={'class': 'content'})
        soupCont2 = soup.find_all('div', attrs={'class': 'con'})
        if soupCont1 != []:
            soupCont = soupCont1
        elif soupCont2 != []:
            soupCont = soupCont2
        else:
            print("全文标签除了content、con还有其他的格式")
        content = 预处理模块.disposeOfData(indexUrl, contenSrc, str(soupCont[0]), SavePath, 超链接本地地址)
        print("\n\n一下是完整的")
        print(content)

# 用于读取数据库当前数据表中的最大id
    def readTableRecord(self,sql):
        # sql ="select max(id) from 大邑县卫生局数据"
        con = 链接数据库.getConnect(sql)
        conn = con[0]
        cursor = con[1]
        row = cursor.fetchone()
        # print(row)  # (None, )
        return row

 # 写入本次插入数据的记录(保存爬取记录的--知识产权局更新记录表)
    def writeTableRecod(self, sql):
        con = 链接数据库.getConnect(sql)
        conn = con[0]
        链接数据库.breakConnect(conn)

if __name__ =="__main__":
    AdminiStrative = Utils()
    indexUrl = "http://kjs.mee.gov.cn/hjbhbz/bzwb/other/hbcpjsyq/201208/t20120803_234327.shtml"
    # 他
    contenSrc= 'http://kjs.mee.gov.cn/hjbhbz/bzwb/other/hbcpjsyq/201208/t20120803_234327.shtml'
    SavePath = 'F:\环境保护局\%s'
    超链接本地地址 = '/datafolder/环保局/标准文本/'
    res =   AdminiStrative.parePage(indexUrl,contenSrc,SavePath,超链接本地地址)
    # res =   AdminiStrative.readTableRecord()
    # AdminiStrative.pageDate(AdminiStrative.getPage(url))