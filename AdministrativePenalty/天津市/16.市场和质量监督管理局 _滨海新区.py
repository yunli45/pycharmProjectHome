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
        self.showId =  12308200

    def getPage(self,url=None):
        response = requests.get(url,headers = self.header)
        response = response.content.decode('UTF-8')
        return response

    def parsePage(self,url=None,pageNo=None,baseUrl="http://scjg.tj.gov.cn",path="F:\行政处罚数据\天津\市场和质量监督管理局\/%s"):

        if pageNo =="1":
            response = self.getPage(url+".html")
        else:
            response = self.getPage(url+"_"+str(int(pageNo)-1)+".html")
        print("+++++++++++++++++++这是第："+pageNo+"页++++++++++++++++")
        # print(response)

        homePageSoup = BeautifulSoup(response,'lxml')
        homePageSoup = homePageSoup.findAll('ul',attrs={'class':'info_list'})
        # print("这也是mmp")
        # print(homePageSoup)
        srcListFind = re.findall(re.compile(r'<a href="(.*?)".*?title="(.*?)">.*?</a>.*?<span>(.*?)</span>', re.S),str(homePageSoup))

        # print("这是mmp")
        print(srcListFind)
        titleList=[]
        timeList=[]
        srcList =[]
        for i in srcListFind:
            srcList.append(i[0])
            titleList.append(i[1])
            timeList.append(i[2])

        for src in srcList:
            print(src)
            RSTitle = titleList[srcList.index(src)] # 标题
            RSTime = timeList[srcList.index(src)] # 时间
            RSdataId = re.sub(r'.*?/', '', src).replace('.html', '')

            if src.find("http")!=-1:
                ContentSrc = src
            else:
                ContentSrc = "http://scjg.tj.gov.cn"+src
            print(ContentSrc)
            # print(ContentSrc)
            ConetentResponse = requests.get(ContentSrc,headers = self.header)
            ConetentResponse = ConetentResponse.content.decode('UTF-8')
            ConetentResponseSoup = BeautifulSoup(ConetentResponse, 'lxml')
            ConetentResponseSoupOld = ConetentResponseSoup.find('div', attrs={'class': 'news_content'})
            ConetentResponseSoupOld = str(ConetentResponseSoupOld)

            ContentTrNum = BeautifulSoup(str(ConetentResponseSoupOld), 'lxml')
            ContentTrNum =len( ContentTrNum.findAll('tr'))
            print(ContentTrNum)

            #   #  #  #  #  #  #  #  #  #  #  #  #  #  #
            #
            #           替换掉表格的所有的格式为p标签
            #
            #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
            ConetentResponse = re.sub('<span.*?>', '', str(ConetentResponseSoupOld), flags=re.S | re.M).replace('</span>', '')
            ConetentResponse = re.sub('<col.*?>', '', ConetentResponse)
            ConetentResponse = re.sub('<tr.*?>', '', ConetentResponse)
            ConetentResponse = re.sub('<td.*?>', '', ConetentResponse)
            ConetentResponse = re.sub('<table.*?>', '', ConetentResponse).replace('<td>', '<p><p>').replace('</td>', '</p><p>').replace('tr',  'p').replace( 'tbody', 'p').replace('table', '').replace('</p><p></p>', '</p><p>')
            ConetentResponse = re.sub(r'<p.*?><o:p> </o:p></p>', '', str(ConetentResponse)).replace('<o:p></o:p>', '')
            ConetentResponse = re.sub(r'<st1:.*?>', '', str(ConetentResponse)).replace('</st1:chsdate>', '').replace('<a name="TCSignYear"></a>','')
            ConetentResponse=re.sub( r'<o:p>\xa0</o:p>','', str(ConetentResponse))
            ConetentResponse = re.sub(r'</p></p><p><p','</p><p',str(ConetentResponse)).replace('</p></p>','</p>')
            ConetentResponse = re.sub(r'<font.*?>', '', str(ConetentResponse)).replace('</font>', '')

            ConetentResponse = ConetentResponse.replace("'", "''").replace('\u2002', ' ').replace('<b>', '').replace('</b>', '')

            #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
            #
            # 提取文书号等信息
            #
            #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #

            # 全文已经所需的部分后，如果找到table，,并且找到的tr的个数为3 或者4个     进行以下处理
             # 全文是一个大表的形式
            if str(ConetentResponseSoupOld).find("<table") != -1 and ContentTrNum == 2:
                # 先去除多余的标签
                print("这是大表 有2个tr")
                ConetentResponseTable = re.sub('<span.*?>', '', str(ConetentResponseSoupOld)).replace('</span>', '')
                ConetentResponseTable = re.sub('<p.*?>', '', str(ConetentResponseTable)).replace('</p>', '')
                ConetentResponseTable = re.sub('<font.*?>', '', str(ConetentResponseTable)).replace('</font>', '')

                TableSoup = BeautifulSoup(ConetentResponseTable, 'lxml')

                for idx, tr in enumerate(TableSoup.find_all('tr')):
                    if idx != 0:  # 不等于0就会去表格的最后一行tr，方便取值
                        tds = tr.find_all('td')
                        RSdocumentNum = tds[5].text.strip()  # 书文号
                        RSbePunished = tds[1].text.strip()  # 被处罚人或机构
                        RSprincipal = tds[4].text.strip()  # 法定代表人
                        RSlawEnforcement = tds[1].text.strip()  # 被处罚单位
                        RSpunishedDate = tds[11].text.strip()  # 受处罚时间
                        RScontent = "主要违法事实：" + tds[6].text.strip() + "。\n 处罚种类:" + tds[7].text.strip() + "。\n 处罚依据：" + \
                                    tds[8].text.strip() + "。\n 行政处罚的履行方式和期限:" + tds[9].text.strip()
                        RSagency = tds[10].text.strip()
            elif str(ConetentResponseSoupOld).find("<table") !=-1 and  ContentTrNum ==3 :
                # 先去除多余的标签
                print("这是大表 有3个tr")
                ConetentResponseTable = re.sub('<span.*?>','',str(ConetentResponseSoupOld)).replace('</span>','')
                ConetentResponseTable = re.sub('<p.*?>','',str(ConetentResponseTable)).replace('</p>','')
                ConetentResponseTable = re.sub('<font.*?>','',str(ConetentResponseTable)).replace('</font>','')

                TableSoup = BeautifulSoup(ConetentResponseTable,'lxml')

                for idx, tr in enumerate(TableSoup.find_all('tr')):
                    try:
                        if idx != 0:  # 不等于0就会去表格的最后一行tr，方便取值
                            tds = tr.find_all('td')
                            RSdocumentNum = tds[5].text.strip() # 书文号
                            RSbePunished = tds[1].text.strip()  # 被处罚人或机构
                            RSprincipal = tds[4].text.strip()  # 法定代表人
                            RSlawEnforcement = tds[1].text.strip() # 被处罚单位
                            RSpunishedDate = tds[11].text.strip() # 受处罚时间
                            RScontent = "主要违法事实：" + tds[6].text.strip() + "。\n 处罚种类:" + tds[7].text.strip() + "。\n 处罚依据：" + \
                                 tds[8].text.strip() + "。\n 行政处罚的履行方式和期限:" + tds[9].text.strip()
                            RSagency = tds[10].text.strip()
                    except IndexError as e:
                        pass
            elif  str(ConetentResponseSoupOld).find("<table") !=-1 and  ContentTrNum ==4 :
                # 先去除多余的标签
                print("这是大表 有4个tr")
                ConetentResponseTable = re.sub('<span.*?>','',str(ConetentResponseSoupOld)).replace('</span>','')
                ConetentResponseTable = re.sub('<p.*?>','',str(ConetentResponseTable)).replace('</p>','')
                ConetentResponseTable = re.sub('<font.*?>','',str(ConetentResponseTable)).replace('</font>','')

                TableSoup = BeautifulSoup(ConetentResponseTable,'lxml')

                for idx, tr in enumerate(TableSoup.find_all('tr')):
                    try:
                        if idx != 0:  # 不等于0就会去表格的最后一行tr，方便取值
                            tds = tr.find_all('td')
                            RSdocumentNum = tds[5].text.strip() # 书文号
                            RSbePunished = tds[1].text.strip()  # 被处罚人或机构
                            RSprincipal = tds[4].text.strip()  # 法定代表人
                            RSlawEnforcement = tds[1].text.strip() # 被处罚单位
                            RSpunishedDate = tds[11].text.strip() # 受处罚时间
                            RScontent = "主要违法事实：" + tds[6].text.strip() + "。\n 处罚种类:" + tds[7].text.strip() + "。\n 处罚依据：" + \
                                 tds[8].text.strip() + "。\n 行政处罚的履行方式和期限:" + tds[9].text.strip()
                            RSagency = tds[10].text.strip()
                    except IndexError as e:
                        pass
            # 全文可能包含表格，也可能不包含
            elif  str(ConetentResponseSoupOld).find("<table") !=-1  and  ContentTrNum >4 :
                print("全文含有表格")
                # 先处理标签问题，先简化  只剩td tr标签
                ConetentResponseAndTabe = re.sub('<span.*?>', '', str(ConetentResponseSoupOld), flags=re.S | re.M).replace('</span>', '')
                ConetentResponseAndTabe = re.sub(r'</p></p><p><p', '</p><p', ConetentResponseAndTabe).replace('</p></p>', '</p>')
                ConetentResponseAndTabe = re.sub(r'<p.*?>', '', str(ConetentResponseAndTabe)).replace('</p>', '')
                ConetentResponseAndTabe = BeautifulSoup(ConetentResponseAndTabe, 'lxml')
                for ids, tr in enumerate(ConetentResponseAndTabe.find_all('tr')):
                    tds = tr.find_all('td')
                    try:
                        if ids == 0:
                            RSdocumentNum = tds[-1].text.strip()  #  s书文号
                            # print(RSdocumentNum)
                        if ids == 1:
                            RSbePunished = tds[-1].text.strip() # 被处罚人或机构
                            print(RSbePunished)
                        if ids == 2:
                            print(tds[-1])
                        if ids == 3:
                            RSlawEnforcement = tds[-1].text.strip()  # 被处罚单位
                            print(RSbePunished)
                        if ids == 5:
                            RSprincipal = tds[-1].text.strip() # 法定代表人
                            print()
                        if ids == 6:
                            content1 = tds[-1].text.strip()  #违法行为类型
                        if ids == 7:
                            content2 = tds[-1].text.strip()  #行政处罚内容
                        if ids == 8:
                            RSagency = tds[-1].text.strip()  #作出行政处罚决定机关名称
                        if ids == 9:
                            RSpunishedDate = tds[-1].text.strip()  # 受处罚时间
                            print()
                        if ids == 10:
                            print(tds[-1].text.strip())
                        RScontent = ConetentResponse
                    except IndexError as e:
                        pass
            # 不含有表格
            else:
                # 处理掉空格
                print("这里是不含有表格的")
                ConetentNoTable  = ConetentResponse.replace(' ','')
                print(ConetentNoTable)
                RSdocumentNumFind = re.findall(re.compile(r'>(.*?津.*?号)<'), ConetentNoTable)
                RSbePunishedFind = re.findall(re.compile(r'当事人姓名或者单位名称(.*?)<'),ConetentNoTable)
                RSprincipalFind = re.findall(re.compile(r'法定代表人[（负责人）|（负 责 人）](.*?)<'),ConetentNoTable)
                RSagencyFind = re.findall(re.compile(r'>(.*?[天]津市.*?局)'), ConetentNoTable)
                RSpunishedDateFind = re.findall(re.compile(r'>(.*?年.*?月.*?日)'),ConetentNoTable)

                # 全文还可能是一个图片的形式
                RSimgFind = re.findall(re.compile(r'<img src="(.*?)".*? title="(.*?)".*>'),ConetentResponse)

                if RSdocumentNumFind:
                    RSdocumentNumFind = re.sub('.*?>','',str(RSdocumentNumFind[0]))
                    RSdocumentNum = RSdocumentNumFind
                else:
                    RSdocumentNum = ''
                if RSbePunishedFind:
                    RSbePunished = RSbePunishedFind[0].replace(":",'')
                    RSlawEnforcement = RSbePunishedFind[0].replace(":",'')
                else:
                    RSbePunished = ''
                    RSlawEnforcement = ''
                if RSprincipalFind:
                    RSprincipalFind = re.sub(r'.*?）:','',str(RSprincipalFind[0]))
                    RSprincipal = RSprincipalFind
                else:
                    RSprincipal = ''
                if RSagencyFind:
                    RSagencyFind =  re.sub('.*?>','',str(RSagencyFind[0]))
                    RSagency = RSagencyFind[0]
                else:
                    RSagency = ''
                if RSpunishedDateFind:
                    RSpunishedDateFind = re.sub('.*?>','',str(RSpunishedDateFind[-1]))
                    RSpunishedDate=RSpunishedDateFind
                else:
                    RSpunishedDate = RSTime
                if RSimgFind:
                    ConetentResponse = "这可能是一个图片形式的，请查看本地是否有相应的标题图片"+ ConetentResponse
                    imgSrc = RSimgFind[0]
                    imgTitle = RSimgFind[1]
                    try :
                        imgSrc =   imgSrc
                        path1 = path  % (imgTitle)
                        r = requests.get(imgSrc, headers=self.header, timeout=30)
                        with open(path1, "wb") as f:
                            f.write(r.content)
                        f.close()
                    except   requests.URLRequired :
                        print("这条数据的网址出错了")
                        print("id是"+str(self.OnlyID))
                        pass
                else:
                    ConetentResponse = ConetentResponse

                RScontent = ConetentResponse



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
            agency =  RSagency  # 处罚机构
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
            adjunct = re.findall(re.compile(r'<a.*?href="(.*?)".*?>(.*?)</a>', re.I | re.S), ConetentResponse)

            if ConetentResponse:
                conn = pymssql.connect(host='(local)', user='sa', password='123456', database='AdministrativePun')
                # 打开游标
                cur = conn.cursor();
                if not cur:
                    raise Exception('数据库连接失败！')
                else:
                    print("数据库链接成功")
                sql1 = " INSERT INTO  crawlData16(dataId,title,documentNum,bePunished,principal,lawEnforcement,punishedDate,content,uniqueSign,address,area,agency,grade,showId) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " % (dataId, title, documentNum, bePunished,principal,lawEnforcement,punishedDate,content,uniqueSign,address, area, agency,grade,showId)
                # sql1 = " INSERT INTO  crawlData5(dataId,title,documentNum,bePunished,uniqueSign,principal,lawEnforcement) values ('%s','%s','%s','%s','%s','%s','%s') " % (  dataId, resTitle, documentNum,bePunished,principal,lawEnforcement,uniqueSign)

                print(sql1)
                if adjunct:
                    print("这条数据存在附件，可能会很大，请稍等，已经自动开始下载.....")
                    for xiaZai in adjunct:
                        print(xiaZai)
                        rsDocuniqueSign = xiaZai[0]
                        rsDocName = xiaZai[1]
                        xiaZai = str(xiaZai)
                        rsDoc1 = re.findall(re.compile(r'.*?.doc', re.I), xiaZai)
                        rsDoc2 = re.findall(re.compile(r'.*?.docx', re.I), xiaZai)
                        rsPdF = re.findall(re.compile(r'.*?.pdf', re.I), xiaZai)
                        rsXlsx = re.findall(re.compile(r'.*?.xlsx|xls', re.I), xiaZai)
                        rsZip = re.findall(re.compile(r'.*?.zip', re.I), xiaZai)
                        rsRar = re.findall(re.compile(r'.*?.rar', re.I), xiaZai)
                        reJpg = re.findall(re.compile(r'.*?.jpg', re.I), xiaZai)
                        if rsDoc1 or rsDoc2:
                            rsDocName = rsDocName + ".doc"
                            rsDocName = rsDocName.replace("/", '_')

                            path1 = path % (rsDocName)

                            if rsDocuniqueSign.find("http") == -1:
                                rsDocuniqueSign = "%s" % (baseUrl) + rsDocuniqueSign
                            else:
                                rsDocuniqueSign = rsDocuniqueSign
                            # print(rsDocuniqueSign)
                            r = requests.get(rsDocuniqueSign, headers=self.header, timeout=30)
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

    # 共计353页
    url ="http://scjg.tj.gov.cn/binhaixinqu/zwgk/xzcfxx/index"
    # url ="http://scjg.tj.gov.cn/jgdt/xzcfxxgs/index_1.html"
    AdminiStrative =Utils()
    for i in range(1,18):
        AdminiStrative.parsePage(url,str(i))
        time.sleep(2)



























