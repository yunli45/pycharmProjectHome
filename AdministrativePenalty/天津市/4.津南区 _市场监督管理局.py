# -*-coding:utf-8 -*-
import requests
import re
import time
from bs4 import BeautifulSoup
import pymssql
import sys
# # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#    抓取天津市-- 津南区  —工商局（市场监督管理局）
#
# # # # # # # # # # # # # # # # # # # # # # # # # # #


class Utils(object):
    def __init__(self):
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
        self.OnlyID = 1
        self.showId = 12300470

    def getPage(self,url=None):
        response = requests.get(url,headers = self.header)
        response = response.content.decode('UTF-8')
        return response

    def parsePage(self,url=None,pageNo=None,baseUrl="http://www.cbrc.gov.cn",path="F:\行政处罚数据\天津\滨海新区\%s"):

        if pageNo=='1':
            response = self.getPage(url+".html")
        else:
            response = self.getPage(url+"_"+str((int(pageNo)-1))+".html")

        print("+++++++++++++++++++这是第："+pageNo+"页++++++++++++++++")
        print(url+str((int(pageNo)-1))+".html")
        soup = BeautifulSoup(response, 'lxml')
        table1 = soup.findAll('ul', attrs={'class': 'info_list'})
        # print(table1)
        rsList = re.findall(re.compile(r'<a href="(.*?)" target="_blank" title="(.*?)">.*?</a>.*?<span>(.*?)</span>', re.S | re.M),str(table1))
        # print(rsList)
        srcList= []
        titleList = []
        timeList = []

        for i in rsList :
            srcList.append(i[0])
            titleList.append(i[1])
            timeList.append(i[2])
        for src in srcList:
            resTitle = titleList[srcList.index(src)]
            resTime = timeList[srcList.index(src)]

            if src.find("http") == -1:
                ContentSrc = baseUrl + src
            else:
                ContentSrc = src
            # print(ContentSrc)
            response = requests.get(ContentSrc,headers = self.header)
            response = response.content.decode('UTF-8')
            print("这是全文")
            print(response)
            soup1 = BeautifulSoup(response, 'lxml')
            contenttable = soup1.findAll('div', attrs={'class': 'news_content'})
            print(contenttable)
            if str(contenttable).find('<table')!=-1:

                RS = re.sub('<span.*?>', '', str(contenttable), flags=re.S | re.M).replace('</span>', '')
                RS = re.sub('<col.*?>', '', RS)
                RS = re.sub('<tr.*?>', '', RS)
                RS = re.sub('<td.*?>', '', RS)
                RS = re.sub('<table.*?>', '', RS).replace('<td>', '<p><p>').replace('</td>', '</p><p>').replace('tr','p').replace('tbody', 'p').replace('table', '')

                soup2 = BeautifulSoup(RS, 'lxml')
                MsoNormal = soup2.findAll('p')
                #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
                #
                # 提取文书号等信息
                #
                #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
                for i in MsoNormal:
                   if re.findall(re.compile(r'.*?津.*?号'),str(i)):

                        dataId = re.sub(r'.*/','',src).replace(".html",'')
                        documentNum = str(MsoNormal[MsoNormal.index(i)]).replace('<p>','').replace('</p>','')# 书文号
                        bePunished  = str(MsoNormal[MsoNormal.index(i)-4]).replace('<p>','').replace('</p>','') # 被处罚人或机构
                        principal = str(MsoNormal[MsoNormal.index(i)-1]).replace('<p>','').replace('</p>','') # 法定代表人
                        lawEnforcement= str(MsoNormal[MsoNormal.index(i)-4]).replace('<p>','').replace('</p>','')  # 被处罚机构或单位
                        punishedDate = str(MsoNormal[MsoNormal.index(i)+6]).replace('<p>','').replace('</p>','')  # 受处罚时间
                        content = "主要违法事实:"+str(MsoNormal[MsoNormal.index(i)+1])+"。处罚种类："+str(MsoNormal[MsoNormal.index(i)+2])+"。处罚依据："+str(MsoNormal[MsoNormal.index(i)+3])+"。行政处罚的履行方式和期限："+str(MsoNormal[MsoNormal.index(i)+4])+"。"
                        uniqueSign = ContentSrc # url地址
                        address =  '天津'# 省份
                        area  =  '津南区'# 地区
                        agency =  "天津市津南区市场和质量监督管理局"  # 处罚机构
                        if len(content) <= 100:
                            grade = -1 # 级别
                        elif 100 < len(content)<= 200:
                            grade = 1  # 级别
                        elif 200< len(content)<= 1500:
                            grade = 2  # 级别
                        elif len(content)>1500:
                            grade = 0  # 级别
                        showId = self.showId # 系统ID
                        showAddress = None
                        showArea = None
            elif str(contenttable).find('<table')==-1 and len(str(contenttable))>1000 :
                print("这里时")
                conntent1 = str(contenttable).encode(sys.getfilesystemencoding())
                conntent1 = str(conntent1)
                conntent1 = re.sub('<span.*?>','',conntent1,flags=re.M|re.S).replace('</span>','')
                conntent1 = re.sub('<p.*?>','<p>',conntent1,flags=re.M|re.S)
                soup = BeautifulSoup(conntent1, 'lxml')
                table = soup.findAll('div', attrs={'class': 'news_content'})
                documentNum = str(re.findall(re.compile(r'行政处罚决定书编号.*?</p>',re.M|re.S),str(table))).replace('</p>','')
                lawEnforcement = str(re.findall(re.compile(r'违法企业名称.*?</p>',re.M|re.S),str(table))).replace('</p>','')
                principal = str(re.findall(re.compile(r'法定代表人.*?</p>',re.M|re.S),str(table))).replace('</p>','')
                punishedDate = str(re.findall(re.compile(r'日期.*?</p>',re.M|re.S),str(table))).replace('</p>','')
                content = conntent1
                content= content.replace('\xa0','').replace('\u3000','').replace("'","''")
                content = content
                uniqueSign = ContentSrc  # url地址
                address = '天津'  # 省份
                area = '津南区'  # 地区
                agency = "天津市津南区市场和质量监督管理局"  # 处罚机构
                if len(content) <= 100:
                    grade = -1  # 级别
                elif 100 < len(content) <= 200:
                    grade = 1  # 级别
                elif 200 < len(content) <= 1500:
                    grade = 2  # 级别
                elif len(content) > 1500:
                    grade = 0  # 级别
                showId = self.showId  # 系统ID
                showAddress = None
                showArea = None

            else:
                content = contenttable
                content = str(content).replace('\xa0', '').replace('\u3000', '').replace("'", "''")
                dataId = re.sub(r'.*/', '', src).replace(".html", '')
                documentNum = ''  # 书文号
                bePunished = '' # 被处罚人或机构
                principal = ''  # 法定代表人
                lawEnforcement = ''  # 被处罚机构或单位
                punishedDate ='' # 受处罚时间

                uniqueSign = ContentSrc  # url地址
                address = '天津'  # 省份
                area = '津南区'  # 地区
                agency = "天津市津南区市场和质量监督管理局	"  # 处罚机构
                if len(content) <= 100:
                    grade = -1  # 级别
                elif 100 < len(content) <= 200:
                    grade = 1  # 级别
                elif 200 < len(content) <= 1500:
                    grade = 2  # 级别
                elif len(content) > 1500:
                    grade = 0  # 级别
                showId = self.showId  # 系统ID
                showAddress = None
                showArea = None
            #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
            #
            # 附件下载
            #
            #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #

            adjunct = re.findall(re.compile(r'<a.*?href="(.*?)".*?>(.*?)</a>', re.I | re.S), str(contenttable))

            if  contenttable:
                conn = pymssql.connect(host='(local)', user='sa', password='123456', database='AdministrativePun')
                # 打开游标
                cur = conn.cursor();
                if not cur:
                    raise Exception('数据库连接失败！')
                else:
                    print("数据库链接成功")
                sql1 = " INSERT INTO  crawlData4(dataId,title,documentNum,bePunished,principal,lawEnforcement,punishedDate,content,uniqueSign,address,area,agency,grade,showId,showAddress,showArea) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " % (  dataId, resTitle, documentNum, bePunished,principal,lawEnforcement,punishedDate,content,uniqueSign,address, area, agency,grade,showId,showAddress,showArea)
                print(sql1)
                if adjunct:
                    print("这条数据存在附件，可能会很大，请稍等，已经自动开始下载.....")
                    for xiaZai in adjunct:
                        rsDocuniqueSign = xiaZai[0]
                        rsDocName = xiaZai[1]
                        xiaZai = str(xiaZai)
                        rsDoc1 = re.findall(re.compile(r'.*?.doc', re.I), xiaZai)
                        rsPdF = re.findall(re.compile(r'.*?.pdf', re.I), xiaZai)
                        rsXlsx = re.findall(re.compile(r'.*?.xlsx|xls', re.I), xiaZai)
                        rsZip = re.findall(re.compile(r'.*?.zip', re.I), xiaZai)
                        rsRar = re.findall(re.compile(r'.*?.rar', re.I), xiaZai)
                        reJpg = re.findall(re.compile(r'.*?.jpg', re.I), xiaZai)
                        if rsDoc1:
                            rsDocName = rsDocName + ".doc"
                            rsDocName = rsDocName.replace("/", '_')

                            path1 = path % (rsDocName)

                            if rsDocuniqueSign.find("http") == -1:
                                rsDocuniqueSign = "%s" % (baseUrl) + rsDocuniqueSign
                            else:
                                rsDocuniqueSign = rsDocuniqueSign
                            # print(rsDocuniqueSign)
                            r = requests.get(rsDocuniqueSign, headers=self.header, timeout=300)
                            with open(path1, "wb") as f:
                                f.write(r.content)
                            f.close()
                        elif rsPdF:
                            rsDocName = rsDocName + ".PDF"
                            rsDocName = rsDocName.replace("/", '_')
                            path1 = path % (rsDocName)

                            if rsDocuniqueSign.find("http") == -1:
                                rsDocuniqueSign = baseUrl + rsDocuniqueSign
                            else:
                                rsDocuniqueSign = rsDocuniqueSign
                            # print(rsDocuniqueSign)
                            r = requests.get(rsDocuniqueSign, headers=self.header)
                            with open(path1, "wb") as f:
                                f.write(r.content)
                            f.close()
                        elif rsXlsx:
                            rsDocName = rsDocName + ".xlsx"
                            rsDocName = rsDocName.replace("/", '_')
                            path1 = path % (rsDocName)

                            if rsDocuniqueSign.find("http") == -1:
                                rsDocuniqueSign = baseUrl + rsDocuniqueSign
                            else:
                                rsDocuniqueSign = rsDocuniqueSign

                            # print(rsDocuniqueSign)
                            r = requests.get(rsDocuniqueSign, headers=self.header)
                            with open(path1, "wb") as f:
                                f.write(r.content)
                            f.close()
                        elif rsZip:
                            rsDocName = rsDocName + ".zip"
                            rsDocName = rsDocName.replace("/", '_')
                            path1 = path % (rsDocName)

                            if rsDocuniqueSign.find("http") == -1:
                                rsDocuniqueSign = baseUrl + rsDocuniqueSign
                            else:
                                rsDocuniqueSign = rsDocuniqueSign

                            # print(rsDocuniqueSign)
                            r = requests.get(rsDocuniqueSign, headers=self.header)
                            with open(path1, "wb") as f:
                                f.write(r.content)
                            f.close()
                        elif rsRar:
                            rsDocName = rsDocName + ".rar"
                            rsDocName = rsDocName.replace("/", '_')
                            path1 = path % (rsDocName)

                            if rsDocuniqueSign.find("http") == -1:
                                rsDocuniqueSign = baseUrl + rsDocuniqueSign
                            else:
                                rsDocuniqueSign = rsDocuniqueSign

                            # print(rsDocuniqueSign)
                            r = requests.get(rsDocuniqueSign, headers=self.header)
                            with open(path1, "wb") as f:
                                f.write(r.content)
                            f.close()
                        elif reJpg:
                            rsDocName = rsDocName + ".jpg"
                            rsDocName = rsDocName.replace("/", '_')
                            path1 = path % (rsDocName)

                            if rsDocuniqueSign.find("http") == -1:
                                rsDocuniqueSign = "%s" % (baseUrl) + rsDocuniqueSign
                            else:
                                rsDocuniqueSign = rsDocuniqueSign
                            # print(rsDocuniqueSign)
                            r = requests.get(rsDocuniqueSign, headers=self.header, timeout=300)
                            with open(path1, "wb") as f:
                                f.write(r.content)
                            f.close()

                cur.execute(sql1)
                self.OnlyID += 1
                self.showId += 1
                conn.commit()
                conn.close()
        print("下一页开始的id是" + str(self.OnlyID))
        print("这一夜爬取成功相关数据和文件，文件保存的目录在" + path)

#######     执行    ########
if __name__ =="__main__":

    url ="http://scjg.tj.gov.cn/jinnan/zwgk/xzcfxx/index"
    AdminiStrative =Utils()
    #cnblog.parsePage(url)
    for i in range(0,14):
        AdminiStrative.parsePage(url,str(i+1))
        time.sleep(3)



























