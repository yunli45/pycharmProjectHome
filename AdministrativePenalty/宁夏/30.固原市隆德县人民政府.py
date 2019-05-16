# -*- coding:utf-8 -*-
import requests
import re
import time
from bs4 import BeautifulSoup
from 宁夏.工具包 import 链接数据库, 替换标签, 附件下载程序, _30附件下载处理


class Utils(object):

    def __init__(self):
        self.header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
        self.OnlyID = 1
        self.showId =12378700

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
            response = self.getPage(url+".html")
        else:
            response = self.getPage(url+"_"+str(int(pageNo)-1)+".html")

        print("+++++++++++++++++++这是第：" + pageNo + "页++++++++++++++++")
        # print(response)
        response = response.replace("\n", '').replace("\r", '').replace("\t", '')
        # print(response)
        # 每页包含的每条数据的div
        responseList = BeautifulSoup(response, 'lxml')
        responseList = responseList.find_all('div',attrs={'class':'xxgk_wrap'})
        print(responseList)
        RSlist = re.findall(re.compile(r'<ul>.*?<li.*?><span>(.*?)</span></li>.*?<li.*?><a.*?href="(.*?)".*?title="(.*?)".*?>.*?</a></li>.*?<li.*?><span.*?>(.*?)</span></li>.*?<li.*?><span>(.*?)</span></li>.*? </ul>', re.S | re.M),str(response))
        RSdocument = re.findall(re.compile(r'.*?<p>文.*?号：<span>(.*?)</span></p>', re.S | re.M),str(response))
        print(RSdocument)
        print(RSlist)
        print(len(RSlist))
        SrcList = []
        TitleList = []
        TimeList = []
        RSdataIdList = []# 以索引号为唯一id
        RSlawEnforcementList = []

        for i in RSlist:
            RSdataIdList.append(i[0])
            SrcList.append(i[1])
            TitleList.append(i[2])
            RSlawEnforcementList.append(i[3])
            TimeList.append(i[4])

        for src in SrcList:
            RSTitle = TitleList[SrcList.index(src)]
            RSTime = TimeList[SrcList.index(src)]
            RSdataId =  RSdataIdList[SrcList.index(src)]
            RSlawEnforcement = RSlawEnforcementList[SrcList.index(src)]
            srcIndex = SrcList.index(src)
            RSdocumentNum= RSdocument[srcIndex]
            if src.find("http") != -1:
                ContentSrc = src
            else:
                src = src.replace('../../', '/').replace('./','/')
                ContentSrc = baseUrl + src

            print(ContentSrc)
            ConetentResponse = self.getPage(ContentSrc)
            ConetentResponseSoup = BeautifulSoup(ConetentResponse, 'lxml')
            ConetentResponseSoupOld = ConetentResponseSoup.find('div', attrs={'class': 'zz-xl-ct'})
            # 返回去除掉部分标签的全文、返回去掉标签前原来的tr 和td的个数 、返回去掉表格前后p标签的个数
            returnData = 替换标签.replaceLable(ConetentResponseSoupOld)
            ConetentResponseSoupOld = returnData[0]
            ContentTrNum = returnData[1]
            ContentTdNum = returnData[2]
            ContentPNum = returnData[3]
            ContentPNum1 = returnData[4]

            OnlyID = self.OnlyID
            header = self.header
            fields =_30附件下载处理.getNeed(ConetentResponseSoupOld, ConetentResponse, ContentPNum, ContentPNum1, ContentTrNum, ContentTdNum,
                   RSTime,RSTitle,SavePath,header,ContentSrc,RSlawEnforcement,RSdocumentNum,RSdataId)
            """"
            表中的字段 公共部分插入到数据库
            """
            # RSdocumentNumList, RSbePunishedList, RSprincipalList, RSlawEnforcementList, RSpunishedDateList, RScontentList, RSagencyList,RSTitleList,RSdataIdList

            RSdocumentNumList = fields[0] # 书文号
            RSbePunishedList = fields[1]  # 被处罚人或者单位
            RSprincipalList = fields[2]  # 法人
            RSlawEnforcementList1 = fields[3]  # 处罚机构
            RSpunishedDateList = fields[4]  # 处罚时间
            RScontentList = fields[5]  # 全文
            RSagencyList = fields[6]  # 处罚机构
            RSTitleList = fields[7]
            RSdataIdList1 = fields[8]
            #   看看是否有附件
            adjunct = re.findall(re.compile(r'<a.*?href="(.*?)".*?>(.*?)</a>', re.I | re.S),
                                 str(ConetentResponseSoupOld))
            for indes in  RSdocumentNumList:
                RSdocumentNum = RSdocumentNumList[RSdocumentNumList.index(indes)]
                RSbePunished = RSbePunishedList[RSdocumentNumList.index(indes)]
                RSprincipal =RSprincipalList[RSdocumentNumList.index(indes)]
                RSlawEnforcement =RSlawEnforcementList1[RSdocumentNumList.index(indes)]
                RSpunishedDate = RSpunishedDateList[RSdocumentNumList.index(indes)]
                RScontent = RScontentList[RSdocumentNumList.index(indes)]
                RsuniqueSign= ContentSrc
                RSagency = RSagencyList[RSdocumentNumList.index(indes)]
                RSTitle = RSTitleList[RSdocumentNumList.index(indes)]
                RSdataId = RSdataIdList1[RSdocumentNumList.index(indes)]
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
                    sql1 = " INSERT INTO  AdministrativePunNingXia.dbo.crawlData25(dataId,title,documentNum,bePunished,principal,lawEnforcement,punishedDate,content,uniqueSign,address,area,agency,grade,showId,FalseHeadlines,Page,sourceUrl) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " % (
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
    url ="http://www.nxld.gov.cn/xxgk/xzcf/list"
    baseUrl="http://www.nxld.gov.cn/xxgk/xzcf/"
    SavePath = "F:\行政处罚数据\宁夏\固原市隆德县人民政府\%s"
    RSaddress ="宁夏回族自治区"
    RSarea ="固原市隆德县人民政府" # 在全文的地址栏去匹配
    RSFalseHeadlines ="宁夏回族自治区固原市隆德县人民政府的数据"

    AdminiStrative =Utils()
    for i in range(1,5):
        AdminiStrative.parsePage(url,str(i),baseUrl,SavePath,RSaddress,RSarea,RSFalseHeadlines)
        time.sleep(2)

