# -*- coding:utf-8 -*-
import requests
import re
import time
from bs4 import BeautifulSoup
from 宁夏.工具包 import 链接数据库, 替换标签, 附件下载程序,_31

class Utils(object):

    def __init__(self):
        self.header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
        self.OnlyID = 1
        self.showId =12378800

    def getPage(self, url):
        response = requests.get(url, headers=self.header)
        # print(response.url)
        if response.status_code == 404:
            pass
        else:
            response = response.content.decode('utf-8',errors = 'ignore')
        return response

    def parsePage(self, url=None, pageNo=None, baseUrl=None, SavePath=None,RSaddress=None,RSarea=None,RSFalseHeadlines=None):
        if pageNo == "1":
            response = self.getPage(url)
        url = url
        print("+++++++++++++++++++这是第：" + pageNo + "页++++++++++++++++")
        # print(response)
        response = response.replace("\n", '').replace("\r", '').replace("\t", '')
        # print(response)
        # 每页包含的每条数据的div
        responseList = BeautifulSoup(response, 'lxml')
        responseList = responseList.find_all('ul',attrs={'class':'list2'})
        print(responseList)
        RSlist = re.findall(re.compile(r'<li><span>(.*?)</span><a.*?href="(.*?)".*?>(.*?)</a></li>', re.S | re.M),str(response))
        print(RSlist)
        print(len(RSlist))
        SrcList = []
        TitleList = []
        TimeList = []
        for i in RSlist:
            SrcList.append(i[1])
            TitleList.append(i[2])
            TimeList.append(i[0])

        for src in SrcList:
            RSTitle = TitleList[SrcList.index(src)]
            RSTime = TimeList[SrcList.index(src)]
            RSdataId =  re.sub(r'.*?/', '', src).replace('.html', '').replace(".htm",'').replace(".shtml",'')
            srcIndex = SrcList.index(src)
            if src.find("http") != -1:
                ContentSrc = src
            else:
                src = src.replace('../../', '/').replace('./','/')
                ContentSrc = baseUrl + src

            print(ContentSrc)
            ConetentResponse = self.getPage(ContentSrc)
            ConetentResponseSoup = BeautifulSoup(ConetentResponse, 'lxml')
            ConetentResponseSoupOld = ConetentResponseSoup.find('div', attrs={'class': 'TRS_Editor'})
            # 返回去除掉部分标签的全文、返回去掉标签前原来的tr 和td的个数 、返回去掉表格前后p标签的个数
            returnData = 替换标签.replaceLable(ConetentResponseSoupOld)
            ConetentResponseSoupOld = returnData[0]
            ContentTrNum = returnData[1]
            ContentTdNum = returnData[2]
            ContentPNum = returnData[3]
            ContentPNum1 = returnData[4]

            OnlyID = self.OnlyID
            header = self.header

            fields =_31.getNeed(ConetentResponseSoupOld,RSTime,RSTitle)
            """"
            表中的字段 公共部分插入到数据库
            """
            # RSdocumentNum, RSbePunished, RSprincipal, RSlawEnforcement, RSpunishedDate, RScontent, RSagency

            RSdocumentNum = fields[0] # 书文号
            RSbePunished = fields[1]  # 被处罚人或者单位
            RSprincipal = fields[2]  # 法人
            RSlawEnforcement = fields[3]  # 处罚机构
            RSpunishedDate = fields[4]  # 处罚时间
            RScontent = fields[5]  # 全文
            RSagency = fields[6]  # 处罚机构
            RSTitle =  RSTitle
            RSdataId = RSdataId
            #   看看是否有附件
            adjunct = re.findall(re.compile(r'<a.*?href="(.*?)".*?>(.*?)</a>', re.I | re.S),
                                 str(ConetentResponseSoupOld))

            RsuniqueSign= ContentSrc

            RSarea = RSarea  # 区域
            RSaddress =RSaddress# 省份

            if len(RScontent) <= 100:
                RSgrade = -1  # 级别
            elif 100 < len(RScontent) <= 200:
                RSgrade = 1  # 级别
            elif 200 < len(RScontent) <= 1500:
                RSgrade = 2  # 级别
            elif len(RScontent) > 1500:
                RSgrade = 0  # 级别
            RSshowId = self.showId  # 系统ID
            RSFalseHeadlines= RSFalseHeadlines
            RSPage = "这是第"+str(pageNo)+"页的第"+str(srcIndex)+"条数据"
            RSsourceUrl = url
            # 假如存在数据，则保存数据道数据库
            if ConetentResponse:
                sql1 = " INSERT INTO  AdministrativePunNingXia.dbo.crawlData26(dataId,title,documentNum,bePunished,principal,lawEnforcement,punishedDate,content,uniqueSign,address,area,agency,grade,showId,FalseHeadlines,Page,sourceUrl) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " % (
                    RSdataId, RSTitle, RSdocumentNum, RSbePunished, RSprincipal, RSlawEnforcement, RSpunishedDate, RScontent, RsuniqueSign,
                    RSaddress, RSarea,
                    RSagency, RSgrade, RSshowId,RSFalseHeadlines,RSPage,RSsourceUrl)
                print(sql1)
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
    # 共计1页数据
    url ="http://www.ycjinfeng.gov.cn/xxgk/xzqlyx/xzcfjggk/"
    baseUrl="http://www.ycjinfeng.gov.cn/xxgk/xzqlyx/xzcfjggk"
    SavePath = ""
    RSaddress ="宁夏回族自治区"
    RSarea ="银川市金凤区" # 在全文的地址栏去匹配
    RSFalseHeadlines ="宁夏回族自治区银川市金凤区的数据"

    AdminiStrative =Utils()
    for i in range(1,3):
        AdminiStrative.parsePage(url,str(i),baseUrl,SavePath,RSaddress,RSarea,RSFalseHeadlines)
        time.sleep(2)

