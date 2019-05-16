# -*- coding:utf-8 -*-
import requests
import re
import time
from bs4 import BeautifulSoup
from 宁夏.工具包 import 链接数据库, 替换标签, 附件下载程序, 只有行政处罚信息公开表


class Utils(object):

    def __init__(self):
        self.header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
        self.OnlyID = 1
        self.showId = 12370000

    def getPage(self, url=None):
        response = requests.get(url, headers=self.header)
        response = response.content.decode('utf-8')
        return response

    def parsePage(self, url=None, pageNo=None, baseUrl=None, SavePath=None):
        if pageNo == "1":
            response = self.getPage(url + pageNo)
        else:
            response = self.getPage(url + pageNo)

        print("+++++++++++++++++++这是第：" + pageNo + "页++++++++++++++++")
        # print(response)
        response = response.replace("\n", '').replace("\r", '').replace("\t", '')
        # 每页包含的每条数据的div
        responseList = BeautifulSoup(response, 'lxml')
        responseList = responseList.find_all('div', attrs={'class': 'pcjg_fffbg'})
        # print(responseList)
        RSlist = re.findall(re.compile(r'<a href="(.*?)".*?title="(.*?)">.*?</a></div>.*?<div class=".*?">(.*?)</div>', re.S | re.M),str(responseList))
        print(RSlist)
        print(len(RSlist))
        SrcList = []
        TitleList = []
        TimeList = []
        for i in RSlist:
            SrcList.append(i[0])
            TitleList.append(i[1])
            TimeList.append(i[2])
        for src in SrcList:

            RSTitle = TitleList[SrcList.index(src)]
            RSTime = TimeList[SrcList.index(src)]
            RSdataId = re.sub(r'.*?/', '', src).replace('.html', '')
            if src.find("http") != -1:
                ContentSrc = src
            else:
                src = src.replace('../../', '/')
                ContentSrc = baseUrl + src

            print(ContentSrc)
            ConetentResponse =  self.getPage(ContentSrc)
            ConetentResponseSoup = BeautifulSoup(ConetentResponse, 'lxml')
            ConetentResponseSoupOld = ConetentResponseSoup.find('div', attrs={'class': 'Section1'})
            ConetentResponseSoupOld = re.sub("<strong.*?>", '', str(ConetentResponseSoupOld)).replace("</strong>", '')
            ConetentResponseSoupOld = re.sub("<u.*?>", '', ConetentResponseSoupOld, flags=re.S | re.M).replace("</u>",
                                                                                                               '')
            ConetentResponseSoupOld = re.sub("<b.*?>", '', ConetentResponseSoupOld, flags=re.S | re.M).replace("</b>",
                                                                                                               '')
            ConetentResponseSoupOld = re.sub('<span.*?>', '', ConetentResponseSoupOld, flags=re.S | re.M).replace(
                '</span>', '').replace(r'<a name="TCSignMonth"></a>','').replace('<a name="TCSignDay"></a>','')
            ConetentResponseSoupOld = str(ConetentResponseSoupOld)

            ContentNum = BeautifulSoup(str(ConetentResponseSoupOld), 'lxml')
            print("这条数据一共有：" + str(len(ContentNum.findAll('tr'))) + "个tr")
            print("这条数据有：" + str(len(ContentNum.findAll('p'))) + "个P")

            # print("还没修改完全的全文+" + ConetentResponseSoupOld)
            #   #  #  #  #  #  #  #  #  #  #  #  #  #  #
            #
            #           替换掉表格的所有的格式为p标签
            #
            #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
            # print("11111"+str(ConetentResponseSoupOld))
            ConetentResponse = 替换标签.replaceLable(ConetentResponseSoupOld)
            # 只有行政处罚信息表
            # print("22222"+ConetentResponse)
            if ConetentResponseSoupOld.find("行政处罚信息公开表") != -1:
                MsoNormalTableResList = 只有行政处罚信息公开表.Table(ConetentResponseSoupOld)
                # print("biaofe"+str(MsoNormalTable))
                RSdocumentNum = MsoNormalTableResList[0]     # 书文号
                RSbePunished = MsoNormalTableResList[1]      #  被处罚人或机构
                RSlawEnforcement = MsoNormalTableResList[2]  # 处罚机构
                RSprincipal = MsoNormalTableResList[3]       # 法人
                RSagency = MsoNormalTableResList[4]          # 处罚机构
                RSpunishedDate = MsoNormalTableResList[5]    # 处罚时间
                RScontent = MsoNormalTableResList[6]         # 全文
            else:
                raise RuntimeError('不知道，请查看下')
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
            address = '宁夏回族自治区'  # 省份  RSagency
            area = "包头市"  # 地区
            agency = RSagency  # 处罚机构
            if len(content) <= 100:
                grade = -1  # 级别
            elif 100 < len(content) <= 200:
                grade = 1  # 级别
            elif 200 < len(content) <= 1500:
                grade = 2  # 级别
            elif len(content) > 1500:
                grade = 0  # 级别
            showId = self.showId  # 系统ID

            #   看看是否有附件
            adjunct = re.findall(re.compile(r'<a.*?href="(.*?)".*?>(.*?)</a>', re.I | re.S),str(ConetentResponseSoupOld))
            # 假如存在数据，则保存数据道数据库
            if ConetentResponse:
                sql1 = " INSERT INTO  crawlData1(dataId,title,documentNum,bePunished,principal,lawEnforcement,punishedDate,content,uniqueSign,address,area,agency,grade,showId) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " % (
                dataId, title, documentNum, bePunished, principal, lawEnforcement, punishedDate, content, uniqueSign,
                address, area,
                agency, grade, showId)

                cur = 链接数据库.getConnect(sql1)

                conn = cur

                附件下载程序.DownloadData(adjunct, SavePath, baseUrl)
                self.OnlyID += 1
                self.showId += 1

            关闭链接= 链接数据库.breakConnect(conn=conn)
        print("下一页开始的id是" + str(self.OnlyID))
        print("这一夜爬取成功相关数据和文件，文件保存的目录在" + SavePath)

#######     执行    ########
if __name__ =="__main__":
    # 共计353页
    url ="http://www.cbrc.gov.cn/zhuanti/xzcf/getPcjgXZCFDocListDividePage/ningxia.html?current="
    baseUrl="http://www.cbrc.gov.cn"
    SavePath = "F:\行政处罚数据\宁夏\银监会新疆监管局"
    AdminiStrative =Utils()
    for i in range(1,6):
        AdminiStrative.parsePage(url,str(i),baseUrl=baseUrl,SavePath=SavePath)
        time.sleep(2)












