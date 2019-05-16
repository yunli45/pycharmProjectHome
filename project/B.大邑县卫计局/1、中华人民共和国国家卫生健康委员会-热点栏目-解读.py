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

        self.pagelable = "div"
        self.pagelable1 = "ul"
        self.pagelableSelector = "class"
        self.pageTableName = "zwgklist"
        self.pageNumS = "pagination_index"
        self.compilePageTable = '<li><h3.*?><a.*?href="(.*?)".*?title="(.*?)">.*?</a></h3>'

    # 因为经常会遇到cookie过期i，需要多次设置header 和 cookie就直接写成一个方法，保证每次不一致
    def creatCookie(self):
        header = {"User-Agent": UserAgent().random}
        jar = requests.cookies.RequestsCookieJar()
        # 不加cookie会返回202状态吗
        jar.set(name='banggoo.nuva.cookie', value='1|W71xc|W71xb', path='/', domain='www.nhfpc.gov.cn')
        cookies = jar
        return   header,cookies


    # 用于匹配-首页的总页数 、 每页的记录数的,返回总页数和每页数据的集合（url、标题、时间）
    def pageDate(self, response):
        print("KKKKK")
        print(response)
        response = BeautifulSoup(response, 'lxml')
        # 总页数：动态加载，暂时搞不定直接写死
        pageS1 = 125
        # print(pageS1)
        # 每条数据
        pageSoup1 = response.find_all(self.pagelable1, attrs={self.pagelableSelector: self.pageTableName})
        # print(pageSoup1)
        RSList = re.findall(re.compile(self.compilePageTable), str(pageSoup1))
        # print(RSList)
        print("这一页一共有："+str(len(RSList))+"条数据")
        return pageS1,RSList
 # 用于的访问--页面的数据
    def getPage(self,url):
        header,cookies = self.creatCookie()
        print("1")
        response = requests.get(url,headers=header,cookies=cookies)
        print(response.url)
        status_code = response.status_code
        if status_code == 404:
            pass
        elif status_code == 202:
            while True:
                header1, cookies1 = self.creatCookie()
                print("hh")
                print("heders"+str(header1))
                if status_code==200:
                    print("mmp,又是200")
                    print("mmpresponse"+str(response))
                    break
                else:
                    print("mmp,又是202")
                    time.sleep(1)
                    response = requests.get(url, headers=header1, cookies=cookies1)
                    status_code = response.status_code
                    response = response.content.decode('utf-8', errors='ignore')
        elif status_code == 200:
            response = response.content.decode('utf-8', errors='ignore')
            # response = response.content.decode('UTF-8')
        print(status_code)
        print("3")
        print("response"+str(response))
        return response
# 用于的访问首页，返回每页的数据
    def getEveryPage(self,url,pageNo):
        header, cookies = self.creatCookie()
        if pageNo == 1:
            url = url
        else:
            print(pageNo)
            url = url[:url.rfind(".shtml")] + "_"+str(pageNo) + ".shtml"
        response = requests.get(url, headers=header,cookies=cookies)
        print(response.url)
        status_code = response.status_code
        if status_code == 404:
            pass
        elif status_code == 202:
            while True:
                print("jj")
                header1, cookies1 = self.creatCookie()
                if status_code == 200:
                    break
                else:
                    time.sleep(1)
                    response = requests.get(url, headers=header1, cookies=cookies1)
                    status_code = response.status_code
                    response = response.content.decode('utf-8', errors='ignore')
        elif  status_code == 200:
            response = response.content.decode('utf-8', errors='ignore')
        # print(response)
        return response
  # 用于解析具体的页面：判断初始的src是否有跳转、是否是附件、以及具体页面数据的提取
    def parePage(self,indexUrl,baseUrl,SavePath):
        response = self.getPage(indexUrl)
        print(response)
        总页数,RSList = self.pageDate(response)
        print(type(总页数))
        print(总页数)
        for pageNo in range(1,总页数+1):
            response = self.getEveryPage(indexUrl,pageNo)
            总页数, 每页数据集合 = self.pageDate(response)
            print(每页数据集合)
            srcList=[]
            titleList =[]
            for sr in 每页数据集合:
                srcList.append(sr[0])
                titleList.append(sr[1])

            if srcList !=[]:
                for ids,src in enumerate(srcList):
                    # 查找数据库种最大id
                    dataBaseMaxID = self.readTableRecord('select max(id) from 大邑县卫生局数据')[0]
                    if dataBaseMaxID == None:
                        dataBaseMaxID = 0
                        src = str(src)
                    title = titleList[ids]
                    print(title)
                    if title.find("视频")!=-1 or title.find("焦点访谈")!=-1 or title.find("卫生部药政司司长郑宏、国家食品药品监督管理局政法司副司长许嘉齐做客新华网向广大网友解读国家基本药物制度")!=-1 :
                        pass
                    else:
                        contenSrc = returnSRC().returnSrc(indexUrl,src)
                        print(contenSrc)
                        contResponse = self.getPage(contenSrc)
                        time1= re.findall(r'<span class="time">发布时间：(.*?)</span>',contResponse)
                        if time1!=[]:
                            发布时间= time1[0]
                        else:
                            发布时间=''
                        print("第一条数据的1"+str(contResponse))
                        soup = BeautifulSoup(contResponse,'lxml')
                        soupCont = soup.find_all('div',attrs={'class':'content'})
                        content = 预处理模块.disposeOfData(str(soupCont[0]))
                        pageNos ="这条数据是第"+str(pageNo)+"页第"+str(ids)+"条"
                        insertTime = datetime.datetime.now().strftime('%Y-%m-%d')
                        版权归属 = '中华人民共和国国家卫生健康委员会'
                        来源库名称 = '中华人民共和国国家卫生健康委员会>热点栏目>解读'
                        来源模块名称= '解读'
                        来源模块首页url = indexUrl
                        类型 = ''
                        # 实施时间=''
                        这条数据的url = src
                        这条数据的完整请求url = contenSrc
                        这条数据属于第几页第几条 = str(pageNos)
                        插入时间 = insertTime
                        # 唯一标识ID = dataBaseMaxID+1
                        packid = 1
                        书文号=''
                        标准号=''
                        标准名 =''
                        content = content
                        id = dataBaseMaxID+1
                        sql = " INSERT INTO [卫计局数据校正].[dbo].[大邑县卫生局数据] ([id], [来源库名称], [来源模块名称], [来源模块首页url], [标题], [类型], [发布时间], [实施时间], [这条数据的url], [这条数据的完整请求url], [这条数据属于第几页第几条], [插入时间],  [packid], [书文号], [标准号], [标准名], [content], [版权归属]) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', NULL , '%s', '%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s') "%(id,来源库名称,来源模块名称,来源模块首页url,title,类型,发布时间,这条数据的url,这条数据的完整请求url ,这条数据属于第几页第几条,插入时间 ,packid,书文号,标准号,标准名,content,版权归属)
                        print(sql)
                        self.writeTableRecod(sql)
            time.sleep(10)
# 用于读取数据库当前数据表中的最大id
    def readTableRecord(self,sql):

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
    url = "http://www.nhfpc.gov.cn/zwgk/jdjd/ejlist.shtml"
    SavePath = ''
    # res =   AdminiStrative.parePage(url,'','')
    # res =   AdminiStrative.readTableRecord( "select max(id) from 大邑县卫生局数据")
    AdminiStrative.pageDate(AdminiStrative.getPage(url))