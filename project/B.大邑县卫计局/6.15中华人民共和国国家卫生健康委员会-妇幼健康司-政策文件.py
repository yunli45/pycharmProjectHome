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
        self.pagelableSelector = "class"
        self.pageTableName = "list"
        self.pageNumS = "pagination_index_last"
        self.compilePageTable = r'<li.*?><span.*?>(.*?)</span>.*?<a .*?href="(.*?)".*?title="(.*?)">.*?</a><span.*?>(.*?)</span></li>'
    # 使用google浏览器的静默模式+ selenium来获取一些--动态加载--的数据
    # 获取一些需要动态加载的网页数据的获取，注意：用与匹配首页总页数和版权归属问题的时候必须使用selenium来动态加载
    def googleSilentMode(self,url):
        print("用于google浏览器动态访问首页返回数据，这一步会稍微慢点")
        option = webdriver.ChromeOptions()
        option.add_argument('headless')  # 使用google浏览器的静默模式
        browser = webdriver.Chrome(chrome_options=option)
        browser.get(url)
        response = browser.page_source
        response = BeautifulSoup(response, 'lxml')
        pageSoup = response.find_all(self.pagelable, attrs={self.pagelableSelector: self.pageNumS})
        pageSRs = re.findall(r'共(.*?)页', str(pageSoup))
        pageS1 = pageSRs[0].replace(' ', '')
        pageS1 = int(pageS1)
        # print("首页的数据"+response)
        # 每条数据
        pageSoup1 = response.find_all(self.pagelable, attrs={self.pagelableSelector: self.pageTableName})
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
    def googlePageDate(self,response):
        response = BeautifulSoup(response, 'lxml')
        # 每条数据
        pageSoup1 = response.find_all(self.pagelable, attrs={self.pagelableSelector: self.pageTableName})
        RSList = re.findall(re.compile(self.compilePageTable), str(pageSoup1))
        print(RSList)
        print("这一页一共有：" + str(len(RSList)) + "条数据")
        # return pageS1, RSList
        return RSList
    def googleGetEveryPage(self,url,pageNo):
        if pageNo == 1:
            url = url
        else:
            url = url[:url.rfind(".shtml")] + "_" + str(pageNo) + ".shtml"
        response = self.googleGetPage(url)
        return response
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
        # 每条数据
        pageSoup1 = response.find_all(self.pagelable, attrs={self.pagelableSelector: self.pageTableName})
        RSList = re.findall(re.compile(self.compilePageTable), str(pageSoup1))
        print(RSList)
        print("这一页一共有："+str(len(RSList))+"条数据")
        # return pageS1, RSList
        return RSList
# 用于的访问--具体的每一条数据--页面的数据
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
    def parePage(self,indexUrl,SavePath):
        总页数, RSList = self.googleSilentMode(indexUrl)
        # for pageNo in range(1,总页数+1):
        for pageNo in range(1,总页数+1):
            response = self.googleGetEveryPage(indexUrl,pageNo)
            每页数据集合 = self.googlePageDate(response)
            print(每页数据集合)
            typeList ,srcList ,titleList,timeList= [] , [], [], []
            for sr in 每页数据集合:
                typeList.append(sr[0])
                srcList.append(sr[1])
                titleList.append(sr[2])
                timeList.append(sr[3])

            if srcList !=[]:
                for ids,src in enumerate(srcList):
                    src = str(src)
                    title = titleList[ids]
                    type1 = typeList[ids]
                    time1 = timeList[ids]
                    print(title)
                    if title.find("视频")!=-1 or title.find("焦点访谈")!=-1:
                        pass
                    else:
                        contenSrc = returnSRC().returnSrc(indexUrl,src,'')
                        print(contenSrc)
                        contResponse = self.googleGetPage(contenSrc)
                        发布时间= time1
                        print("第一条数据的1"+str(contResponse))
                        soup = BeautifulSoup(contResponse,'lxml')
                        soupCont1 = soup.find_all('div',attrs={'class':'content'})
                        soupCont2 = soup.find_all('div',attrs={'class':'con'})
                        if soupCont1!=[]:
                            soupCont =soupCont1
                        elif soupCont2!=[]:
                            soupCont = soupCont2
                        else:
                            print("全文标签除了content、con还有其他的格式")
                        超链接本地地址 = '/datafolder/卫计局数据校正/妇幼健康司/政策文件/'
                        content = 预处理模块.disposeOfData(indexUrl,contenSrc,str(soupCont[0]),SavePath,超链接本地地址)
                        pageNos ="这条数据是第"+str(pageNo)+"页第"+str(ids)+"条"
                        insertTime = datetime.datetime.now().strftime('%Y-%m-%d')
                        版权归属 = '中华人民共和国国家卫生健康委员会'
                        来源库名称 = '妇幼健康司>政策文件'
                        来源模块名称= '政策文件'
                        来源模块首页url = indexUrl
                        类型 = type1
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
                        # 查找数据库种最大id
                        dataBaseMaxID = self.readTableRecord('select max(id) from 大邑县卫生局数据')[0]
                        if dataBaseMaxID == None:
                            dataBaseMaxID = 0
                        id = dataBaseMaxID+1
                        sql = " INSERT INTO [卫计局数据校正].[dbo].[大邑县卫生局数据] ([id], [来源库名称], [来源模块名称], [来源模块首页url], [标题], [类型], [发布时间], [实施时间], [这条数据的url], [这条数据的完整请求url], [这条数据属于第几页第几条], [插入时间],  [packid], [书文号], [标准号], [标准名], [content], [版权归属]) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', NULL , '%s', '%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s') "%(id,来源库名称,来源模块名称,来源模块首页url,title,类型,发布时间,这条数据的url,这条数据的完整请求url ,这条数据属于第几页第几条,插入时间 ,packid,书文号,标准号,标准名,content,版权归属)
                        print(sql)
                        self.writeTableRecod(sql)
            time.sleep(10)
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
    url = "http://www.nhfpc.gov.cn/fys/zcwj2/new_zcwj.shtml"
    SavePath = 'F:\卫计局\妇幼健康司\政策文件\%s'
    res =   AdminiStrative.parePage(url,SavePath)
    # res =   AdminiStrative.readTableRecord()
    # AdminiStrative.pageDate(AdminiStrative.getPage(url))