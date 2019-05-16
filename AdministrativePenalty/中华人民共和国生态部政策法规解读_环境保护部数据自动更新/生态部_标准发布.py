# coding:utf-8
import requests
from bs4 import BeautifulSoup
import time
import re
import datetime
import os
from 中华人民共和国生态部政策法规解读_环境保护部数据自动更新.工具包  import 链接数据库,附件下载程序
import sys

sys.path.append(r"F:\知识产权局相关附件\程序脚本")
# import 链接数据库
# import 附件下载程序


class Utils(object):
    # 一些共用的初始化参数
    def __init__(self):
        self.header = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
        self.OnlyID = 1
        # 因为每页记录数据标签一般不会发生改变，就直接些成位置参数，不用写成形参
        # 因为这两个网址每页记录数据标签参数是一样的就是用同一组标签
        self.pagelable = "div"
        self.pagelableSelector = "class"
        self.pageNumS = "page"  # 总页数的div名字，总页数在尾页这个超链接中取在加上1（<a href="index_28.shtml" target="_self">尾页</a> ==》 28+1=29）
        self.pageTableName = "main_rt"  # 每条数据的div名字
        self.compilePageTable = '<li><span>(.*?)</span><a.*?href="(.*?)".*?title="(.*?)">.*?</a></li>'  # 每条数据的匹配规则：标题、时间
        self.SavePath = "F:\各种自动爬取更新数据程序\中华人民共和国生态部-政策解读"

    # 用于匹配--政策解读、知识产权工作--首页的总页数 、 每页的记录数的,返回总页数和每页数据的集合（url、标题、时间）
    def pageDate(self, response):
        response = BeautifulSoup(response, 'lxml')
        # 总记录数
        pageSoup = response.find_all(self.pagelable, attrs={self.pagelableSelector: self.pageNumS})
        pageS = re.findall(re.compile(r'var countPage=(.*)'),str(pageSoup))
        pageS1 = pageS[0]
        print("总页数："+ str(pageS))
        # 每条数据
        pageSoup1 = response.find_all(self.pagelable, attrs={self.pagelableSelector: self.pageTableName})
        RSList = re.findall(re.compile(self.compilePageTable), str(pageSoup1))
        print("这一页一共有：" + str(len(RSList)) + "条数据")
        return pageS1, RSList

    # 用于的访问--政策解读、动作来源--页面的数据
    def getPage(self, url):
        response = requests.get(url, headers=self.header)
        print(response.url)
        if response.status_code == 404:
            pass
        else:
            response = response.content.decode('utf-8', errors='ignore')
        # print(response)
        return response

    # 用于的访问首页，返回每页的数据
    def getEveryPage(self, url, pageNo):
        if pageNo == "1":
            url = url
        else:
            url = url +"_"+ str(int(pageNo) - 1) + ".shtml"
        response = requests.get(url, headers=self.header)
        print(response.url)
        if response.status_code == 404:
            pass
        else:
            response = response.content.decode('utf-8', errors='ignore')
        # print(response)
        return response

    # 用于解析具体的页面：判断初始的src是否有跳转、是否是附件、以及具体页面数据的提取
    def parePage(self, src, baseUrl, title, imgBaseUrl, SavePath):
        Rs = re.findall(re.compile(r'.*?.pdf|PDF|doc|DOC|docx|DOCX|xlsx|XLSX|xls|XLS'), src)
        # 说明这条数据--存在--跳转或附件的形式
        if src.find("http://") != -1 or Rs != []:
            # 网址是一个http形式的
            if src.find("http://") != -1:
                Rs1 = re.findall(re.compile(r'.*?(pdf|PDF|doc|DOC|docx|DOCX|xlsx|XLSX|xls|XLS)'), src)
                # 先判断这条数据完整的网址是否是附件
                # 这条数据是一个附件
                if Rs1 != []:
                    suffix = "." + Rs1[0]
                    附件下载程序.DownloadData(src, imgBaseUrl, title, SavePath)
                    Content = '<a href="/photo/img/%s%s">%s</a>' % (title, suffix, title)
                    来源处唯一标志_url = src
                    来源处完整的url = src
                # 这条数据存在跳转，跳转后怎么取标签
                else:
                    pass
            # 网址是一个附件，并且需要进行拼接网址
            else:
                Rs2 = re.findall(re.compile(r'.*?(pdf|PDF|doc|DOC|docx|DOCX|xlsx|XLSX|xls|XLS)'), src)
                suffix = "." + Rs2[0]
                附件下载程序.DownloadData(src, imgBaseUrl, title, SavePath)
                Content = '<a href="/photo/img/%s%s">%s</a>' % (title, suffix, title)
                来源处唯一标志_url = src
                来源处完整的url = baseUrl + (src.replace("../", '').replace('./', ''))
        # 说明这条数据--不存在--跳转或附件的形式,并且需要拼接该地址
        else:
            contSrc = baseUrl + src
            ContResponse = self.getPage(contSrc)
            ContentResponse = BeautifulSoup(ContResponse, 'lxml')
            ContentResponse = ContentResponse.find_all("div", attrs={'class', 'index_art_con'})
            Content = str(ContentResponse[0])
            imgList = re.findall(re.compile(r'<img.*?src="(.*?)".*?>'), Content)
            imgList1 = re.findall(re.compile(r'<img.*?src=".*?".*?>'), Content)
            if imgList != []:
                # 如果存在图片就以图片的src最后一个 / 以后的数字或者文字为本地的名字
                for imgSrc in imgList:
                    imgSrc = imgSrc.replace("../", '').replace("./", '')
                    imgName = imgSrc[imgSrc.rfind("/") + 1:]
                    imgUrl = imgBaseUrl + imgSrc
                    附件下载程序.imgDownLoad(imgUrl, imgName, SavePath)
                    for img in imgList1:
                        SavePath1 = SavePath % (imgName)
                        Content = re.sub("<style.*?>.*?</style>", '', Content)
                        Content = Content.replace(img, '<img src="/photo/img/%s">' % (imgName))

                print("图片下载完成,文中的图片地址也已经转换为本地的地址了")
            来源处唯一标志_url = src
            来源处完整的url = contSrc

        return 来源处唯一标志_url, 来源处完整的url, Content

    # 核心：比较--政策解读、--知识产权工作的本次访问，如果有更新就进行爬取，没有再次写入上次的数据
    def compareAndDown(self, ZCJDurl, ZCJDbaseUrl, ZCJDSavePath, ZSCQGZurl, ZSCQGZbaseUrl, ZSCQGZSavePath, DownBaseUrl):
        readTableRecord = self.readTableRecord()
        print(readTableRecord)
        ZCJD上一次抓取的第一条数据标题 = readTableRecord[0]
        ZCJD上一次抓取的第一条数据发布时间 = readTableRecord[1]
        ZCJD上一次抓取的第一条数据的唯一标识 = readTableRecord[2]
        ZCJD上一次抓取的第一条数据url = readTableRecord[3]
        ZCJD上一次抓取的第一条数据完整的url = readTableRecord[4]
        packid = readTableRecord[11]
        上一次整个抓取后的最大唯一标识 = readTableRecord[10]
        本次更新时间 = datetime.datetime.now().strftime('%Y-%m-%d')
        ZCJDresponse = self.getPage(ZCJDurl)
        # print(ZCJDresponse)
        ZCJDdate = self.pageDate(ZCJDresponse)
        ZCJDpageS = int(ZCJDdate[0])  # 总页数
        # print(ZCJDpageS)
        # print(type(ZCJDpageS))
        ZCJDRList = []
        for ZCJDpageNo in range(1, ZCJDpageS):
            if ZCJDpageNo == 1:
                for x in ZCJDdate[1]:
                    ZCJDRList.append(x)
            else:
                zcjdUrl = ZCJDurl[:ZCJDurl.rfind(".")]
                ZCJDresponse1 = self.getEveryPage(zcjdUrl, str(ZCJDpageNo))
                ZCJDdate1 = self.pageDate(ZCJDresponse1)[1]
                for y in ZCJDdate1:
                    ZCJDRList.append(y)
        # print(ZCJDRList)
        if ZCJDRList != []:
            # 移除网页跳转的情况，不包括附件
            for s, http in enumerate(ZCJDRList):
                rss = re.findall(re.compile(r'http://www.*?.htm'), http[0])
                if rss:
                    ZCJDRList.remove(ZCJDRList[s])
            print("现在已经将--政策解读--下每页的src title time 集中到一个集合中了，只需要遍历该集合，找到与上一次结束url一致的时候停止")
            ZCJDsrcList, ZCJDtitleList, ZCJDtimeList = [], [], []
            for ZCJDsrc in ZCJDRList:
                ZCJDsrcList.append(ZCJDsrc[0]), ZCJDtitleList.append(ZCJDsrc[1]), ZCJDtimeList.append(ZCJDsrc[2])
            # 判断本次政策解读是否有更新
            if ZCJDsrcList[0] == ZCJD上一次抓取的第一条数据url:
                政策解读本次是否有更新 = "没有"
                政策解读本次抓取的第一条的标题 = ZCJD上一次抓取的第一条数据标题
                政策解读本次抓取的最后一条的标题 = ZCJD上一次抓取的第一条数据标题
                政策解读本次抓取的第一条的标题的发布时间 = ZCJD上一次抓取的第一条数据发布时间
                政策解读本次抓取的最后一条的标题的发布时间 = ZCJD上一次抓取的第一条数据发布时间
                政策解读本次抓取的第一条的标题的url = ZCJD上一次抓取的第一条数据url
                政策解读本次抓取的最后一条的标题的url = ZCJD上一次抓取的第一条数据url
                政策解读本次抓取的第一条的标题的完整的url = ZCJD上一次抓取的第一条数据完整的url
                政策解读本次抓取的最后一条的标题的完整的url = ZCJD上一次抓取的第一条数据完整的url
                政策解读本次抓取的第一条的标题的唯一标志ID = ZCJD上一次抓取的第一条数据的唯一标识
                政策解读本次抓取的最一条的标题的唯一标志ID = ZCJD上一次抓取的第一条数据的唯一标识
                政策解读本次整个抓取后的最大唯一标识 = 政策解读本次抓取的最一条的标题的唯一标志ID

            else:
                print("政策解读本次是否有更新:有，正在进行数据爬取")
                packid1 = packid + 1
                for ZCJDids, ZCJDsrc1 in enumerate(ZCJDsrcList):
                    print("遍历src集合与政策解读上一次抓取的最后的标题的url进行比较中")
                    if ZCJDsrc1 != ZCJD上一次抓取的第一条数据url:
                        print("这条数据与政策解读上一次抓取的最后的标题的url不一致，正在进行抓取该数据")
                        ZCJDsrc1, ZCJDtitle, ZCJDtime = ZCJDsrc1, ZCJDtitleList[ZCJDids], ZCJDtimeList[ZCJDids]
                        ZCJD来源处唯一标志_url, ZCJD来源处完整的url, ZCJDContent = self.parePage(ZCJDsrc1, ZCJDbaseUrl, ZCJDtitle,
                                                                                    DownBaseUrl, ZCJDSavePath)
                        print(ZCJDsrc1)
                        ZCJDdate = "发布时间：" + str(ZCJDtime)
                        ZCJDtypeName, ZCJDtype = "政策解读", 2
                        上一次整个抓取后的最大唯一标识 += 1
                        sql = "insert into [cnlaw2.0].[dbo].[知识产权-科新局](title,date,content,typeName,type,packid,插入时间,来源处的唯一标志_url,来源处完整的url) values('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                        ZCJDtitle, ZCJDdate, ZCJDContent, ZCJDtypeName, int(ZCJDtype), int(packid1), 本次更新时间,
                        ZCJD来源处唯一标志_url, ZCJD来源处完整的url)
                        print(sql)
                        self.writeTableRecod(sql)
                    else:
                        break
                政策解读本次是否有更新 = "有"
                政策解读本次抓取的第一条的标题 = ZCJDtitleList[0]
                政策解读本次抓取的最后一条的标题 = ZCJDtitleList[ZCJDids - 1]
                政策解读本次抓取的第一条的标题的发布时间 = "发布时间：" + str(ZCJDtimeList[0])
                政策解读本次抓取的最后一条的标题的发布时间 = "发布时间：" + str(ZCJDtimeList[ZCJDids - 1])
                政策解读本次抓取的第一条的标题的url = self.parePage(ZCJDsrcList[0], ZCJDbaseUrl, ZCJDtitle, DownBaseUrl, ZCJDSavePath)[
                    0]
                政策解读本次抓取的第一条的标题的完整的url = \
                self.parePage(ZCJDsrcList[0], ZCJDbaseUrl, ZCJDtitle, DownBaseUrl, ZCJDSavePath)[1]
                政策解读本次抓取的最后一条的标题的url = \
                self.parePage(ZCJDsrcList[ZCJDids - 1], ZCJDbaseUrl, ZCJDtitle, DownBaseUrl, ZCJDSavePath)[0]
                政策解读本次抓取的最后一条的标题的完整的url = \
                self.parePage(ZCJDsrcList[ZCJDids - 1], ZCJDbaseUrl, ZCJDtitle, DownBaseUrl, ZCJDSavePath)[1]
                政策解读本次抓取的第一条的标题的唯一标志ID = 上一次整个抓取后的最大唯一标识
                政策解读本次抓取的最一条的标题的唯一标志ID = 上一次整个抓取后的最大唯一标识 + ZCJDids - 1
                政策解读本次整个抓取后的最大唯一标识 = 政策解读本次抓取的最一条的标题的唯一标志ID

        政策解读本次整个抓取后的最大唯一标识1 = 政策解读本次整个抓取后的最大唯一标识
        ZSCQGZ上一次抓取的第一条数据标题 = readTableRecord[5]
        ZSCQGZ上一次抓取的第一条数据发布时间 = readTableRecord[6]
        ZSCQGZ上一次抓取的第一条数据唯一标识 = readTableRecord[7]
        ZSCQGZ上一次抓取的第一条数据url = readTableRecord[8]
        ZSCQGZ上一次抓取的第一条数据完整的url = readTableRecord[9]

        ZSCQGZresponse = self.getPage(ZSCQGZurl)
        ZSCQGZdate = self.pageDate(ZSCQGZresponse)
        ZSCQGZpageS = int(ZSCQGZdate[0])  # 总页数
        ZSCQGZList = []
        for ZSCQGZpageNo in range(1, ZSCQGZpageS // 3):
            if ZSCQGZpageNo == 1:
                for z in ZSCQGZdate[1]:
                    ZSCQGZList.append(z)
            else:
                zsqcgzUrl = ZSCQGZurl[:ZSCQGZurl.rfind(".")]
                ZCJDresponse1 = self.getEveryPage(zsqcgzUrl, str(ZSCQGZpageNo))
                ZCJDdate1 = self.pageDate(ZCJDresponse1)[1]
                for w in ZCJDdate1:
                    ZSCQGZList.append(w)
        print(ZSCQGZList)
        if ZSCQGZList != []:
            # 移除网页跳转的情况，不包括附件
            for s1, http1 in enumerate(ZSCQGZList):
                print(http1[0])
                rss = re.findall(re.compile(r'http://www.*?.htm'), http1[0])
                if rss:
                    print(rss)
                    ZSCQGZList.remove(ZSCQGZList[s1])
            print("现在已经将--知识产权工作--下每页的src title time 集中到一个集合中了，只需要遍历该集合，找到与上一次结束url一致的时候停止")
            ZSCQGZsrcList, ZSCQGZtitleList, ZSCQGZtimeList = [], [], []
            for ZSCQGZsrc in ZSCQGZList:
                ZSCQGZsrcList.append(ZSCQGZsrc[0]), ZSCQGZtitleList.append(ZSCQGZsrc[1]), ZSCQGZtimeList.append(
                    ZSCQGZsrc[2])
            # 判断本次知识产权工作是否有更新
            if ZSCQGZsrcList[0] == ZSCQGZ上一次抓取的第一条数据url:
                print("知识产权工作本次是否有更新:没有")
                知识产权工作本次是否有更新 = "没有"
                知识产权工作本次抓取的第一条的标题 = ZSCQGZ上一次抓取的第一条数据标题
                知识产权工作本次抓取的最后一条的标题 = ZSCQGZ上一次抓取的第一条数据标题
                知识产权工作本次抓取的第一条的标题的发布时间 = ZSCQGZ上一次抓取的第一条数据发布时间
                知识产权工作本次抓取的最后一条的标题的发布时间 = ZSCQGZ上一次抓取的第一条数据发布时间
                知识产权工作本次抓取的第一条的标题的url = ZSCQGZ上一次抓取的第一条数据url
                知识产权工作本次抓取的最后一条的标题的url = ZSCQGZ上一次抓取的第一条数据url
                知识产权工作本次抓取的第一条的标题的完整的url = ZSCQGZ上一次抓取的第一条数据完整的url
                知识产权工作本次抓取的最后一条的标题的完整的url = ZSCQGZ上一次抓取的第一条数据完整的url
                知识产权工作本次抓取的第一条的标题的唯一标志ID = ZSCQGZ上一次抓取的第一条数据唯一标识
                知识产权工作本次抓取的最一条的标题的唯一标志ID = ZSCQGZ上一次抓取的第一条数据唯一标识
                知识产权工作本次整个抓取后的最大唯一标识 = 知识产权工作本次抓取的最一条的标题的唯一标志ID

            else:
                print("知识产权工作本次是否有更新:有，正在进行数据爬取")
                for ZSCQGZids, ZSCQGZsrc1 in enumerate(ZSCQGZsrcList):
                    print("1  :" + str(ZSCQGZsrc1))
                    print("遍历src集合与知识产权工作上一次抓取的最后的标题的url进行比较中")
                    if ZSCQGZsrc1 != ZSCQGZ上一次抓取的第一条数据url:
                        print("这条数据与知识产权工作上一次抓取的最后的标题的url不一致，正在进行抓取该数据")
                        ZSCQGZsrc1, ZSCQGZtitle, ZSCQGZtime = ZSCQGZsrc1, ZSCQGZtitleList[ZSCQGZids], ZSCQGZtimeList[
                            ZSCQGZids]
                        print("2  :")
                        print(str(ZSCQGZsrc1))
                        print(str(ZSCQGZtitle))
                        ZSCQGZ来源处唯一标志_url, ZSCQGZ来源处完整的url, ZSCQGZContent = self.parePage(ZSCQGZsrc1, ZSCQGZbaseUrl,
                                                                                          ZSCQGZtitle, DownBaseUrl,
                                                                                          ZSCQGZSavePath)
                        print(ZSCQGZ来源处唯一标志_url)

                        ZSCQGZdate = "发布时间：" + str(ZSCQGZtime)
                        ZSCQGZtypeName, ZSCQGZtype = "科信", 1
                        政策解读本次整个抓取后的最大唯一标识1 += 1

                        sql = "insert into [cnlaw2.0].[dbo].[知识产权-科新局](title,date,content,typeName,type,packid,插入时间,来源处的唯一标志_url,来源处完整的url) values('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                            ZSCQGZtitle, ZSCQGZdate, ZSCQGZContent, ZSCQGZtypeName, int(ZSCQGZtype), int(packid1),
                            本次更新时间, ZSCQGZ来源处唯一标志_url, ZSCQGZ来源处完整的url)
                        print(sql)
                        self.writeTableRecod(sql)

                    else:
                        break
                知识产权工作本次是否有更新 = "有"
                知识产权工作本次抓取的第一条的标题 = ZSCQGZtitleList[0]
                知识产权工作本次抓取的最后一条的标题 = ZSCQGZtitleList[ZSCQGZids - 1]
                知识产权工作本次抓取的第一条的标题的发布时间 = "发布时间：" + str(ZSCQGZtimeList[0])
                知识产权工作本次抓取的最后一条的标题的发布时间 = "发布时间：" + str(ZSCQGZtimeList[ZSCQGZids - 1])
                知识产权工作本次抓取的第一条的标题的url = \
                self.parePage(ZSCQGZsrcList[0], ZSCQGZbaseUrl, ZSCQGZtitle, DownBaseUrl, ZSCQGZSavePath)[0]
                知识产权工作本次抓取的第一条的标题的完整的url = \
                self.parePage(ZSCQGZsrcList[0], ZSCQGZbaseUrl, ZSCQGZtitle, DownBaseUrl, ZSCQGZSavePath)[1]
                知识产权工作本次抓取的最后一条的标题的url = \
                self.parePage(ZSCQGZsrcList[ZSCQGZids - 1], ZSCQGZbaseUrl, ZSCQGZtitle, DownBaseUrl, ZSCQGZSavePath)[0]
                知识产权工作本次抓取的最后一条的标题的完整的url = \
                self.parePage(ZSCQGZsrcList[ZSCQGZids - 1], ZSCQGZbaseUrl, ZSCQGZtitle, DownBaseUrl, ZSCQGZSavePath)[1]
                知识产权工作本次抓取的第一条的标题的唯一标志ID = 政策解读本次整个抓取后的最大唯一标识 + 1
                知识产权工作本次抓取的最一条的标题的唯一标志ID = 政策解读本次整个抓取后的最大唯一标识 + ZSCQGZids - 1
                本次整个抓取后的最大唯一标志 = 知识产权工作本次抓取的最一条的标题的唯一标志ID + 1
                print("print(本次整个抓取后的最大唯一标志)" + str(本次整个抓取后的最大唯一标志))
        if 知识产权工作本次是否有更新 == "没有":
            if 知识产权工作本次是否有更新 == "没有":
                本次整个抓取后的最大唯一标志 = 上一次整个抓取后的最大唯一标识
            else:
                本次整个抓取后的最大唯一标志 = 知识产权工作本次抓取的最一条的标题的唯一标志ID
        else:
            if 知识产权工作本次是否有更新 == "没有":
                本次整个抓取后的最大唯一标志 = 政策解读本次整个抓取后的最大唯一标识
            else:
                本次整个抓取后的最大唯一标志 = 知识产权工作本次抓取的最一条的标题的唯一标志ID + 1

        sql = "insert into [cnlaw2.0].[dbo].[知识产权局更新记录表](政策解读上一次抓取的第一条的标题,政策解读上一次抓取的第一条标题的发布时间,政策解读上一次抓取的第一条的标题的url,政策解读上一次抓取的第一条的标题的完整的url,政策解读上一次抓取的第一条的标题的唯一标志ID,知识产权工作上一次抓取的第一条的标题,知识产权工作上一次抓取的第一条的标题的发布时间,知识产权工作上一次抓取的第一条的标题的url,知识产权工作上一次抓取的第一条的标题的完整的url,知识产权工作上一次抓取的第一条的标题的唯一标志ID,packid,上一次整个抓取后的最大的唯一标志ID,政策解读本次是否有更新,知识产权工作本次是否有更新,本次更新时间) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
        政策解读本次抓取的第一条的标题, 政策解读本次抓取的第一条的标题的发布时间, 政策解读本次抓取的第一条的标题的url, 政策解读本次抓取的第一条的标题的完整的url, int(政策解读本次抓取的第一条的标题的唯一标志ID),
        知识产权工作本次抓取的第一条的标题, 知识产权工作本次抓取的第一条的标题的发布时间, 知识产权工作本次抓取的第一条的标题的url, 知识产权工作本次抓取的第一条的标题的完整的url,
        int(知识产权工作本次抓取的第一条的标题的唯一标志ID), int(packid + 1), int(本次整个抓取后的最大唯一标志), 政策解读本次是否有更新, 知识产权工作本次是否有更新, 本次更新时间)
        print(sql)
        self.writeTableRecod(sql)

    # 每次在更新的时候去查询数据表（中华人民共和国环境生态部）中的上一次抓取--标准发布--结束后的结束id和最后一条数据的标题、时间、url、完整的url、以及上一次结束时的最大唯一标识ID
    def readTableRecord(self):
        # 查询--标准发布--上一次抓取的第一条数据的 标题 、发布时间、 唯一标识、src 、完整的url(以最大的发布时间为基础来查)
        sql1 = """
        select  * from 中华人民共和国环境生态部 where 唯一标志 = (select min(唯一标志) from 中华人民共和国环境生态部 where  time=(select max(time) from 中华人民共和国环境生态部 where 模块 like '%标准发布'))
        """

        # 查询上一次抓取后的最大唯一标识，插入数据的时候不需要插入，因为它是自增的，用于备份表记录
        sql2 = """
          select max(唯一标志) from 中华人民共和国环境生态部
        """
        sql3 = """
            select max(packid) from 中华人民共和国环境生态部 where  模块 like '%标准发布'
        """
        sql = [sql1, sql2, sql3]
        rs = []
        for i in sql:
            con = 链接数据库.getConnect(i)
            conn = con[0]
            cursor = con[1]
            row = cursor.fetchone()
            rs.append(row)
        print(rs)
        上一次抓取的第一条数据的标题 = rs[0][1].replace("\r", '').replace(" ", '').replace("\n", '')
        上一次抓取的第一条数据的发布时间 = rs[0][2].replace("\r", '').replace(" ", '').replace("\n", '')
        上一次抓取的第一条数据的模块 = rs[0][3]
        上一次抓取的第一条数据的库 = rs[0][3].replace("\r", '').replace(" ", '').replace("\n", '')
        上一次抓取的第一条数据的url = rs[0][4].replace("\r", '').replace(" ", '').replace("\n", '')
        上一次抓取的第一条数据的完整请求url = rs[0][4].replace("\r", '').replace(" ", '').replace("\n", '')
        上一次抓取的第一条数据的唯一标志ID = rs[0][4].replace("\r", '').replace(" ", '').replace("\n", '')
        上一次抓取后的最大唯一标识 = rs[2][0]
        上一次抓取后的packid = rs[3][0]
        链接数据库.breakConnect(conn)
        # return 上一次抓取的第一条标题, 上一次抓取的第一条发布时间, 上一次抓取的第一条唯一标识, 上一次抓取的第一条url, 上一次抓取的第一条完整的url,上一次抓取后的最大唯一标识, 上一次抓取后的packid

    # 写入本次插入数据的记录(保存爬取记录的--知识产权局更新记录表)
    def writeTableRecod(self, sql):
        con = 链接数据库.getConnect(sql)
        conn = con[0]
        链接数据库.breakConnect(conn)


if __name__ == "__main__":
    # 数据库:
    # 实例：192.168.31.124\SQLEXPRESS  账户：sa  密码： 123qwe!@#    数据库：cnlaw2.0 表： 中华人民共和国环境生态部
   # 在该表中以“模块”字段来区分不同数据
    AdminiStrative = Utils()
    # 政策解读相关参数
    indexUrl = "http://kjs.mee.gov.cn/hjbhbz/bzfb/index.shtml"
    baseUrl = ""
    ZCJDSavePath = "F:\各种自动爬取更新数据程序\中华人民共和国生态部-政策解读\%s"
    # 文章中图片下载的基础地址
    DownBaseUrl = ""
    # AdminiStrative.compareAndDown(indexUrl, baseUrl, ZCJDSavePath)
    AdminiStrative.readTableRecord()
    # reww  = AdminiStrative.getPage(indexUrl)
    # AdminiStrative.pageDate(reww)




