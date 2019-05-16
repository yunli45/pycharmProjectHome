# -*- coding: UTF-8 -*-
import requests
import re
import time
from bs4 import BeautifulSoup
import pymssql
from selenium import webdriver

# # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#    抓取天津市滨海新区 —银监分局数据
#
# # # # # # # # # # # # # # # # # # # # # # # # # # #


class Utils(object):
    def __init__(self):
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
        self.OnlyID = 1
        self.showId =  12301660


    def getPage(self,url=None):
        response = requests.get(url,headers = self.header)
        response = response.content.decode('UTF-8')
        return response

    def parsePage(self,url=None,pageNo=None,baseUrl="http://www.tjhb.gov.cn/env/environmental_monitoring/administrative_penalty_information/",path="F:\行政处罚数据\天津\环保局\/%s"):

        if pageNo =="1":
            response = self.getPage(url)

        print("+++++++++++++++++++这是第："+pageNo+"页++++++++++++++++")
        # print(response)

        homePageSoup = BeautifulSoup(response,'lxml')
        homePageSoup = homePageSoup.findAll('div',attrs={'class':'infoList infoList2'})
        # print("这也是mmp")
        # print(homePageSoup)
        srcListFind = re.findall(re.compile(r'<a href="(.*?)">(.*?)</a>.*?<span class="date">(.*?)</span>'),str(homePageSoup))

        # print("这是mmp")
        # print(srcListFind)
        titleList=[]
        timeList=[]
        srcList =[]
        for i in srcListFind:
            srcList.append(i[0])
            titleList.append(i[1])
            timeList.append(i[2])
        srcList1 = []
        for num in range(0,29):
            for  src in srcList:
                if  16 == num :
                    src = src.replace("../../../", '/')
                    ContentSrc = "http://www.tjhb.gov.cn" + src
                else:
                    src = src.replace("./", '/')
                    ContentSrc = "http://www.tjhb.gov.cn/env/environmental_monitoring/administrative_penalty_information" + src
                srcList1.append(ContentSrc)
        for src in srcList1:
            ContentSrc = src
            RSTitle = titleList[srcList1.index(src)] # 标题
            RSTime = timeList[srcList1.index(src)] # 时间
            RSdataId = re.sub(r'.*?/', '', src).replace('.html', '')
            # 红牌
            if srcList1.index(src) ==16:
                print("这是红牌")
                print(ContentSrc)
                ConetentResponse = requests.get(ContentSrc, headers=self.header)
                ConetentResponse = ConetentResponse.content.decode('UTF-8')
                ConetentResponseSoup = BeautifulSoup(ConetentResponse, 'lxml')
                ConetentResponseSoupOld = ConetentResponseSoup.find('p', attrs={'align': 'justify'})
                RSdocumentNum =''
                RSbePunished =''
                RSprincipal = ''
                RSlawEnforcement=''
                RSpunishedDate =RSTime
                RScontent = '2016年11月我市未作出环境违法行为红牌处罚'
                RSagency = ''

            # 其他
            else:
                ConetentResponse = requests.get(ContentSrc, headers=self.header)
                ConetentResponse = ConetentResponse.content.decode('UTF-8')
                ConetentResponseSoup = BeautifulSoup(ConetentResponse, 'lxml')
                ConetentResponseSoupOld = ConetentResponseSoup.find('div', attrs={'class': 'pages_content'})

                ConetentResponse = str(ConetentResponseSoupOld)

                ConetentResponse = re.sub('<table.*?>','',ConetentResponse).replace('</table>','')
                ConetentResponse = re.sub('<tbody>','',ConetentResponse).replace('</tbody>','').replace('<tr>','').replace('</tr>','')
                ConetentResponse = re.sub('<td.*?>', '', ConetentResponse).replace('</td>', '')
                ConetentResponse = re.sub('<span.*?>', '', ConetentResponse).replace('</span>', '')
                ConetentResponse = re.sub('<font.*?>', '', ConetentResponse).replace('</font>', '')
                ConetentResponse = re.sub('<p.*?>', '<p>', ConetentResponse)

                # 蓝天
                if 20<= srcList1.index(src):
                    print("这是蓝天")
                    print(ContentSrc)
                    RSdocumentNum = ''
                    RSbePunished = ''
                    RSprincipal = ''
                    RSlawEnforcement = ''
                    RSpunishedDate = RSTime
                    RScontent = ConetentResponse
                    RSagency = ''
                if 0<=  srcList1.index(src)<17:
                    print("这是其他的")
                    print(ContentSrc)
                    ConetentResponse = re.sub(r'<b.*?>','',ConetentResponse).replace('</b>','')
                    ConetentResponse = re.sub('<a.*?>','',ConetentResponse).replace('</a>','')
                    ConetentResponse = re.sub('<p.*?>','<p>',ConetentResponse,flags=re.M|re.S).replace('<o:p></o:p>','')
                    ConetentResponse = re.sub(r'<span.*?>','',ConetentResponse,flags=re.S|re.M)
                    ConetentResponseNow = BeautifulSoup(ConetentResponse, 'lxml')
                    ConetentResponseNow = ConetentResponseNow.findAll('p')
                    print("这是全文")
                    print(ConetentResponseNow)
                    try :
                        for pNum in ConetentResponseNow:

                            RSdocumentNum =ConetentResponseNow[3].text.strip()
                            RSbePunished =  ConetentResponseNow[5].text.strip()
                            RSprincipal1 = ConetentResponseNow[8].text.strip()
                            RSprincipal = re.sub(r'.*?人：','',RSprincipal1)

                            RSlawEnforcement = RSbePunished
                            RSpunishedDate = ConetentResponseNow[-1].text.strip()
                            RScontent = ConetentResponseNow
                            RSagency1 = ConetentResponseNow[7].text.strip()
                            RSagency1 = re.sub("区.*?",'',RSagency1).replace('地址：','')
                            RSagency = RSagency1
                    except IndexError :
                        pass



            #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
            #
            # 提取文书号等信息
            #
            #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #

            # 全文已经所需的部分后，如果找到table，,并且找到的tr的个数为3 或者4个     进行以下处理
             # 全文是一个大表的形式


            """"
            表中的字段 公共部分插入到数据库
            """

            #  来源处的id，没有就以src最后的数字为准
            dataId = RSdataId
            title = RSTitle
            documentNum = RSdocumentNum  # 书文号
            bePunished = RSbePunished  # 被处罚人或机构
            principal = RSprincipal  # 法定代表人
            lawEnforcement = RSlawEnforcement  # 被处罚单位
            punishedDate = RSpunishedDate  # 受处罚时间
            content = RScontent  # 全文RScontent
            uniqueSign = ContentSrc  # url地址
            address = '天津'  # 省份
            area = RSagency  # 地区
            agency =  '天津市环境保护局'  # 处罚机构
            if len(content) <= 100:
                grade = -1  # 级别
            elif 100 < len(content) <= 200:
                grade = 1  # 级别
            elif 200 < len(content) <= 1500:
                grade = 2  # 级别
            elif len(content) > 1500:
                grade = 0  # 级别
            showId = self.showId  # 系统ID


            #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
            #
            #        附件下载部分
            #
            #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #

            if ConetentResponse:
                conn = pymssql.connect(host='(local)', user='sa', password='123456', database='AdministrativePun')
                # 打开游标
                cur = conn.cursor();
                if not cur:
                    raise Exception('数据库连接失败！')
                else:
                    print("数据库链接成功")
                sql1 = " INSERT INTO  crawlData7(dataId,title,documentNum,bePunished,principal,lawEnforcement,punishedDate,content,uniqueSign,address,area,agency,grade,showId) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " % (dataId, title, documentNum, bePunished,principal,lawEnforcement,punishedDate,content,uniqueSign,address, area, agency,grade,showId)
                # sql1 = " INSERT INTO  crawlData5(dataId,title,documentNum,bePunished,uniqueSign,principal,lawEnforcement) values ('%s','%s','%s','%s','%s','%s','%s') " % (  dataId, resTitle, documentNum,bePunished,principal,lawEnforcement,uniqueSign)

                cur.execute(sql1)
                self.OnlyID += 1
                self.showId += 1
            conn.commit()
            conn.close()
        print("下一页开始的id是" + str(self.OnlyID))
        print("这一夜爬取成功相关数据和文件，文件保存的目录在" + path)

#######     执行    ########
if __name__ =="__main__":

    # 共计353页
    url ="http://scjg.tj.gov.cn/jgdt/xzcfxxgs/index"
    # url ="http://scjg.tj.gov.cn/jgdt/xzcfxxgs/index_1.html"
    AdminiStrative =Utils()
    for i in range(1,3):
        AdminiStrative.parsePage(url,str(i))
        time.sleep(2)



























