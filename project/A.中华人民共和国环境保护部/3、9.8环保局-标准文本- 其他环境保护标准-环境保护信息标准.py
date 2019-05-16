import requests
from bs4 import BeautifulSoup
import time
import re
import datetime
from fake_useragent import UserAgent
from selenium import webdriver
from 中华人民共和国环境保护部.工具包 import 链接数据库,附件下载程序,预处理模块
from  中华人民共和国环境保护部.工具包.判断url前面的点返回完整的请求地址 import returnSRC
import os



class Utils(object):
    # 一些共用的初始化参数
    def __init__(self):
        self.pagelable = "div"
        self.pagelableSelector = "class"
        self.pageTableName = "main_rt_list"
        self.pageNumS = "page"
        self.compilePageTable = r'<span>(.*?)</span>.*?<a href="(.*?)".*?title=".*?">(.*?)</a>'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10-12.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10-12.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'
         }

# 访问网址
    def getPageData(self,indexUrl):
        response = requests.get(indexUrl,headers=self.headers)
        status_code = response.status_code
        print("状态码1"+str(status_code))
        if status_code==200:
            response = response.content.decode('utf-8')
        elif status_code==202:
            while True:
                response = requests.get(indexUrl, headers=self.heders)
                status_code = response.status_code
                print("状态码2" + str(status_code))
                if status_code == 200:
                    response = response.content.decode('utf-8')
                elif status_code ==404:
                    pass
                else:
                    response = requests.get(indexUrl, headers=self.heders)
        elif status_code == 400:
            print("这里出现网址找不到，查看网址是否正确"+str(indexUrl))
        elif status_code == 404:
            print("这里出现网址找不到，查看网址是否正确" + str(indexUrl))
            pass
        print("状态码3" + str(status_code))
        return  response

# 使用动态加载获取首页的数据
    def getIndexPage(self,indexUrl):
        print(indexUrl)
        print("用于google浏览器动态访问首页返回数据，这一步会稍微慢点")
        option = webdriver.ChromeOptions()
        option.add_argument('headless')  # 使用google浏览器的静默模式
        browser = webdriver.Chrome(chrome_options=option)
        # browser = webdriver.Chrome()
        browser.get(indexUrl)
        response = browser.page_source
        response = BeautifulSoup(response, 'lxml')
        print("response" + str(response))
        pageSoup = response.find_all(self.pagelable, attrs={self.pagelableSelector: self.pageNumS})
        print("pageSoup"+str(pageSoup))
        pageSRs = re.findall(r'var countPage=(.*)', str(pageSoup))
        pageS1 = pageSRs[0]
        pageS1 = int(pageS1)
        print("总页数"+str(pageS1))
        # 每条数据
        pageSoup1 = response.find_all(self.pagelable, attrs={self.pagelableSelector: self.pageTableName})
        print("pageSoup1"+str(pageSoup1))
        pageSoup1 = str(pageSoup1).replace("\n",'').replace("  ",'')
        RSList = re.findall(self.compilePageTable, str(pageSoup1),flags=re.S)
        print(str(RSList))
        print("这一页一共有：" + str(len(RSList)) + "条数据")
        return pageS1, RSList
    def getEveryPage(self,url,pageNo):
        if pageNo == 1:
            url = url
        else:
            url = url[:url.rfind(".shtml")] + "_" + str(pageNo-1) + ".shtml"
        response = self.getPageData(url)
        response = BeautifulSoup(response, 'lxml')
        # 每条数据
        pageSoup1 = response.find_all(self.pagelable, attrs={self.pagelableSelector: self.pageTableName})
        pageSoup1 = str(pageSoup1).replace("\n", '').replace("  ", '')
        RSList = re.findall(self.compilePageTable, str(pageSoup1),flags=re.S)
        print(RSList)
        print("这一页一共有：" + str(len(RSList)) + "条数据")
        return RSList

# 用于解析具体的页面：判断初始的src是否有跳转、是否是附件、以及具体页面数据的提取
    def parePage(self,indexUrl,SavePath,tableName,超链接本地地址,来源库名称,来源模块名称,版权归属):
        总页数, RSList = self.getIndexPage(indexUrl)
        for pageNo in range(1,总页数+3):
        # 总页数 = 28
        # for pageNo in range(16,总页数+3):
            print("================这是第几"+str(pageNo)+"页==============================")
            每页数据集合 = self.getEveryPage(indexUrl,pageNo)
            print(每页数据集合)
            timeList, srcList, titleList= [], [], []
            for sr in 每页数据集合:
                timeList.append(sr[0])
                srcList.append(sr[1])
                titleList.append(sr[2])
            if srcList != []:
                for ids, src in enumerate(srcList):
                    src1 = str(src)
                    键值对1 = src[src.rfind("/")+1:]
                    键值对比较 = self.readTableRecord("select 键值对 from %s where 键值对='%s'" % (tableName,键值对1))
                    键值对比较 = str(键值对比较)
                    if 键值对比较 =='None':
                        print("这条数据的url" + src1)
                        title = titleList[ids]
                        time1 = timeList[ids]
                        contenSrc = returnSRC().returnSrc(indexUrl, src, '')
                        print("全文的请求地址" + contenSrc)
                        contResponse = self.getPageData(contenSrc)
                        发布时间1 = time1.replace("-", '').replace("/", '')  # 发布时间需要6位数字形式的
                        print("第一条数据的1" + str(contResponse))

                        if str(contResponse) == '<Response [404]>':
                            pass
                        else:
                            soup = BeautifulSoup(contResponse, 'lxml')
                            # 匹配文章的头部信息 headInfo
                            headInfomation1 = soup.find_all('div', attrs={'class': 'headInfo'})
                            headInfomation2 = soup.find_all('div', attrs={'class': 'content_top_box'})
                            if headInfomation1 != [] or headInfomation2 != []:
                                if headInfomation1 != []:
                                    headInfomation = headInfomation1
                                    headInfomation = str(headInfomation).replace("\n", '').replace('\xa0', '').replace(
                                        " ",
                                        '').replace(
                                        "	", '')
                                    索引号 = re.findall('<td.*?>.*?索.*?引.*?号.*?</b>(.*?)</td>', str(headInfomation))
                                    索引号 = 索引号[0]
                                    分类 = re.findall('<td.*?>.*?分.*?类.*?</b>(.*?)</td>', str(headInfomation), flags=re.S)
                                    分类 = re.sub('<span.*?>', '', str(分类[0])).replace("</span>", '')
                                    发布机关1 = re.findall('<td.*?>.*?发.*?布.*?机.*?关.*?</b>(.*?)</td>', str(headInfomation),
                                                       flags=re.S)
                                    发布单位 = re.findall('<td.*?>.*?发.*?布.*?单.*?位.*?</b>(.*?)</td>', str(headInfomation),
                                                      flags=re.S)
                                    if 发布机关1 != []:
                                        发布机关 = 发布机关1
                                    elif 发布单位 != []:
                                        发布机关 = 发布单位
                                    发布机关 = re.sub('<span.*?>', '', str(发布机关[0])).replace("</span>", '')
                                    生成日期 = re.findall('<td.*?>.*?生.*?成.*?日.*?期.*?</b>(.*?)</td>', str(headInfomation),
                                                      flags=re.S)
                                    生成日期 = re.sub('<span.*?>', '', str(生成日期[0])).replace("</span>", '')
                                    文号 = re.findall('<td.*?>.*?文.*?号.*?</b>(.*?)</td>', str(headInfomation), flags=re.S)
                                    文号 = re.sub('<span.*?>', '', str(文号[0])).replace("</span>", '')
                                    主题词 = re.findall('<td.*?>.*?主.*?题.*?词.*?</b>(.*?)</td>', str(headInfomation),
                                                     flags=re.S)
                                    主题词 = re.sub('<span.*?>', '', str(主题词[0])).replace("</span>", '')
                                    内容提要 = re.findall('<td.*?>.*?内.*?容.*?提.*?要.*?</b>(.*?)</td>', str(headInfomation),
                                                      flags=re.S)
                                    内容提要 = re.sub('<span.*?>', '', str(内容提要[0])).replace("</span>", '')
                                elif headInfomation2 != []:
                                    headInfomation = headInfomation2
                                    headInfomation = str(headInfomation).replace("\n", '').replace('\xa0', '').replace(
                                        " ",
                                        '').replace(
                                        "	", '')

                                    索引号 = re.findall(r'<div><span>.*?索.*?引.*?号.*?</span>(.*?)</div>',
                                                     str(headInfomation))
                                    索引号 = 索引号[0]
                                    分类 = re.findall(r'<div><span>.*?分.*?类.*?</span>(.*?)</div>', str(headInfomation))
                                    分类 = 分类[0]
                                    发布机关 = re.findall(r'<div><span>.*?发.*?布.*?机.*?关.*?</span>(.*?)</div>',
                                                      str(headInfomation))
                                    发布机关 = 发布机关[0]
                                    生成日期 = re.findall(r'<div><span>.*?生.*?成.*?日.*?期.*?</span>(.*?)</div>',
                                                      str(headInfomation))
                                    生成日期 = 生成日期[0]
                                    文号 = re.findall(r'<div><span>.*?文.*?号.*?</span>(.*?)</div>', str(headInfomation))
                                    文号 = 文号[0]
                                    主题词 = re.findall(r'<div><span>.*?主.*?题.*?词.*?</span>(.*?)</div>',
                                                     str(headInfomation))
                                    主题词 = 主题词[0]
                            else:
                                索引号 = ''
                                发布机关 = ''
                                文号 = ''
                                分类 = ''
                                主题词 = ''
                            soupCont1 = soup.find_all('div', attrs={'class': 'wzxq_neirong2'})  # z正文
                            soupCont2 = soup.find_all('div', attrs={'class': 'content'})
                            soupCont3 = soup.find_all('div', attrs={'class': 'TRS_Editor'})
                            soupCont4 = soup.find_all('div', attrs={'class': 'wzxq_neirong2'})
                            if soupCont1 != [] or soupCont2 != [] or soupCont3 != [] or soupCont4 != []:
                                if soupCont1 != []:
                                    soupCont = soupCont1
                                elif soupCont2 != []:
                                    soupCont = soupCont2
                                elif soupCont3 != []:
                                    soupCont = soupCont3
                                elif soupCont4 != []:
                                    soupCont = soupCont4

                                soupCont = soupCont
                                超链接本地地址 = 超链接本地地址
                                content = 预处理模块.disposeOfData(indexUrl, contenSrc, str(soupCont[0]), SavePath, 超链接本地地址)
                                pageNos = "这条数据是第" + str(pageNo) + "页第" + str(ids) + "条"
                                insertTime = datetime.datetime.now().strftime('%Y-%m-%d')
                                版权归属 = 版权归属
                                来源库名称 = 来源库名称
                                来源模块名称 = 来源模块名称
                                来源模块首页url = indexUrl
                                标题 = title
                                生成日期 = 发布时间1
                                发布时间 = ''
                                这条数据的url = src
                                这条数据的完整请求url = contenSrc
                                这条数据属于第几页第几条 = str(pageNos)
                                插入时间 = insertTime
                                版权所有 = 版权归属
                                # 唯一标识ID = dataBaseMaxID+1
                                packid = 1
                                if 0 < len(content) <= 30000:
                                    全文内容 = content
                                    全文内容2 = ''
                                    全文内容3 = ''
                                elif 0 < len(content) < 60000:
                                    全文内容 = content[:30000]
                                    全文内容2 = content[30000:]
                                    全文内容3 = ''
                                else:
                                    全文内容 = content[:30000]
                                    全文内容2 = content[30000:60000]
                                    全文内容3 = content[60000:]
                                键值对 = src[src.rfind("/") + 1:]
                                # 查找数据库种最大id
                                dataBaseMaxID = self.readTableRecord('select max(id) from %s' % (tableName))[0]
                                print('select max(id) from %s' % (tableName))
                                if dataBaseMaxID == None:
                                    dataBaseMaxID = 0
                                id = dataBaseMaxID + 1
                                Max唯一标识ID = self.readTableRecord('select max(唯一标识ID) from %s' % (tableName))[0]
                                # print('select max(id) from %s' % (tableName))
                                if Max唯一标识ID == None:
                                    Max唯一标识ID = 0
                                唯一标识ID = Max唯一标识ID + 1

                                sql = " INSERT INTO [环境保护局].[dbo].[%s]([id] ,[来源库名称] ,[来源模块名称] ,[来源模块首页url] ,[标题] ,[发布时间] ,[这条数据的url] ,[这条数据的完整请求url] ,[这条数据属于第几页第几条] ,[插入时间] ,[唯一标识ID] ,[packid] ,[索引号] ,[发布机关] ,[文号] ,[分类] ,[生成日期] ,[主题词] ,[版权所有] ,[全文内容] ,[全文内容2] ,[全文内容3] ,[键值对]  ) VALUES ('%s', '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " % (
                                    tableName, id, 来源库名称, 来源模块名称, 来源模块首页url, 标题, 发布时间, 这条数据的url, 这条数据的完整请求url,
                                    这条数据属于第几页第几条,
                                    插入时间,
                                    int(唯一标识ID), packid, 索引号, 发布机关, 文号, 分类, 生成日期, 主题词, 版权所有, 全文内容, 全文内容2, 全文内容3, 键值对)
                                print(sql)
                                self.writeTableRecod(sql)
                                # time.sleep(1)
                            else:
                                print("全文标签除了Custom_UnionStyle还有其他的格式")
                                os._exit(0)
                    else:
                        print("存在该条数据，未保存该数据")
                        pass
            time.sleep(1)
# 用于读取数据库当前数据表中的最大id
    def readTableRecord(self,sql):
        # sql ="select max(id) from 大邑县卫生局数据"
        con = 链接数据库.getConnect(sql)
        conn = con[0]
        cursor = con[1]
        row = cursor.fetchone()
        print(row)  # (None, )
        return row
# 写入本次插入数据的记录(保存爬取记录的--知识产权局更新记录表)
    def writeTableRecod(self, sql):
        con = 链接数据库.getConnect(sql)
        conn = con[0]
        链接数据库.breakConnect(conn)
    def testCs(self,tableName):
        # 键值对1= 't20091010_162150.shtml'
        键值对1= 't20091010_162151.shtml'
        键值对比较 = self.readTableRecord("select 键值对 from %s where 键值对='%s'" % (tableName,键值对1))
        键值对比较 = str(键值对比较)
        print(type(键值对比较))

        if 键值对比较== 'None':
            print("yes")
        else:
            print("No")
if __name__ =="__main__":
    AdminiStrative = Utils()
    # IndexUrl = "http://www.mee.gov.cn/gzfw_13107/zcfg/zcfgjd/"
    IndexUrl = "http://kjs.mee.gov.cn/hjbhbz/bzwb/other/xxbz/index.shtml"
    SavePath = 'F:\环保局\标准文本\%s'
    tableName = '环境保护局'
    超链接本地地址 = '/datafolder/环保局/标准文本/'
    来源库名称 = '中华人民共和国生态环境部>环境保护标准>标准文本>其他环境保护标准>环境保护信息标准'
    版权归属 = '中华人民共和国生态环境部'
    来源模块名称 = '标准文本'
    # AdminiStrative.testCs(tableName)
    AdminiStrative.parePage(IndexUrl,SavePath,tableName,超链接本地地址,来源库名称,来源模块名称,版权归属)
    # sql="select 键值对 from 环境保护局 where 键值对='./other/hjbz/201212/t20121205_243275.shtml'"
    # sql = "select 键值对 from %s where 键值对='%s' " % (tableName,'./other/hjbz/201212/t20121205_243275.shtml')
    # print(sql)
    # res =   AdminiStrative.readTableRecord(sql)
    # print(res)
    # AdminiStrative.getIndexPage(IndexUrl)
    # AdminiStrative.readTableRecord("select 键值对 from 环境保护局1  where 键值对='sdsdf'")