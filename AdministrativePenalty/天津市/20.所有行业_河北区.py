# -*- coding: UTF-8 -*-
import requests
import re
import time
from bs4 import BeautifulSoup
import pymssql

class Utils(object):
    def __init__(self):
        self.header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
        self.OnlyID = 1
        self.showId = 12309500

    def getPage(self,url=None,data=None):
        response = requests.post(url,data=data)
        response = response.content.decode('UTF-8')
        return response

    def parsePage(self,url=None,pageNo=None,baseUrl=" ",path="F:\行政处罚数据\天津\河北区\%s"):

        response = self.getPage("http://www.tjhbq.gov.cn:7001/xxgk/www/info/loadInfoDataForUser",data)

        print("+++++++++++++++++++这是第："+pageNo+"页++++++++++++++++")
        # print(response)

        homePageSoup = BeautifulSoup(response,'lxml')
        homePageSoup = homePageSoup.findAll('tr')
        # print("这也是mmp")
        # print(homePageSoup)
        srcListFind = re.findall(re.compile(r'<span>.*?<input name="infoId" type="hidden" value="(.*?)"/>.*?<input name="suoyinhao" type="hidden" value="(.*?)"/>.*?<input name="fujiama" type="hidden" value="(.*?)"/>.*?<input name="fabujigou" type="hidden" value="(.*?)"/>.*?<input name="fawenriqi" type="hidden" value="(.*?)"/>.*?<input name="wenhao" type="hidden" value="(.*?)"/>.*?<input name="zhutici" type="hidden" value="(.*?)"/>.*?<input name="mingcheng" type="hidden" value="(.*?)"/>.*?<input name="deptId" type="hidden" value="(.*?)"/>.*?<input name="zhutifenlei" type="hidden" value="(.*?)"/>.*?<input name="categoryId" type="hidden" value="(.*?)"/>', re.S),str(homePageSoup))

        srcList =[]
        suoyinhaoList =[]
        fujiamaList = []
        fabujigouList = []
        fawenriqiList = []
        wenhaoList = []
        zhuticiList = []
        mingchengList = []
        deptIdList =[]  # 部门编号
        zhutifenleiList = []  # 主题分类
        categoryIdList = [] # 类别ID


        for i in srcListFind:
            srcList.append(i[0])
            fabujigouList.append(i[3])
            fawenriqiList.append(i[4])
            wenhaoList.append(i[5])
            mingchengList.append(i[7])

        # print("wenshuhao ")
        # print(wenhaoList)

        for src in srcList:

            RSTitle = mingchengList[srcList.index(src)] # 标题
            RSTime = fawenriqiList[srcList.index(src)] # 时间
            RSdocumentNum = wenhaoList[srcList.index(src)].replace(" ",'')
            # print("西藏")
            # print(RSdocumentNum)
            RSdataId = re.sub(r'.*?/', '', src).replace('.html', '')
            RSagency = fabujigouList[srcList.index(src)]
            if src.find("http")!=-1:
                ContentSrc = src
            else:
                ContentSrc = "http://www.tjhbq.gov.cn:7001/xxgk/www/info/show/"+src
            print(ContentSrc)
            # print(ContentSrc)
            ConetentResponse = requests.get(ContentSrc,headers = self.header)
            ConetentResponse = ConetentResponse.content.decode('UTF-8')
            ConetentResponseSoup = BeautifulSoup(ConetentResponse, 'lxml')

            overviewConetent = ConetentResponseSoup.findAll('div', attrs={'class': 'div_center'})  # 1:内容概述 2:内容全文
            overviewConetentFindAll = ConetentResponseSoup.findAll('div', attrs={'class': 'textIndent'})  #  1：内容概述  2：全文内容
            fujian = ConetentResponseSoup.find('div', attrs={'class': 'fujian'})  #  附件


            CONET1 = overviewConetent[0]
            CONET1All = overviewConetentFindAll[0]
            CONET2 = overviewConetent[1]
            CONET2All =overviewConetentFindAll[1]

            RScontent = str(CONET1) + str(CONET1All)+ str(CONET2) + str(CONET2All)






            #   #  #  #  #  #  #  #  #  #  #  #  #  #  #
            #
            #           替换掉表格的所有的格式为p标签
            #
            #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
            ConetentResponse = re.sub('<span.*?>', '', str(RScontent), flags=re.S | re.M).replace('</span>', '')
            ConetentResponse = re.sub('<col.*?>', '', ConetentResponse)
            ConetentResponse = re.sub('<tr.*?>', '', ConetentResponse)
            ConetentResponse = re.sub('<td.*?>', '', ConetentResponse)
            ConetentResponse = re.sub('<table.*?>', '', ConetentResponse).replace('<td>', '<p><p>').replace('</td>', '</p><p>').replace('tr',  'p').replace( 'tbody', 'p').replace('table', '').replace('</p><p></p>', '</p><p>')
            ConetentResponse = re.sub(r'<p.*?><o:p> </o:p></p>', '', str(ConetentResponse)).replace('<o:p></o:p>', '')
            ConetentResponse = re.sub(r'<st1:.*?>', '', str(ConetentResponse)).replace('</st1:chsdate>', '').replace('<a name="TCSignYear"></a>','')
            ConetentResponse=re.sub( r'<o:p>\xa0</o:p>','', str(ConetentResponse))
            ConetentResponse = re.sub(r'</p></p><p><p','</p><p',str(ConetentResponse)).replace('</p></p>','</p>')
            ConetentResponse = re.sub(r'<font.*?>', '', str(ConetentResponse)).replace('</font>', '')
            RScontent = ConetentResponse.replace("'", "''").replace('\u2002', ' ').replace('<b>', '').replace('</b>', '')



            #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
            #
            # 提取文书号等信息
            #
            #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #

            """"
            表中的字段 公共部分插入到数据库
            """

            #  来源处的id，没有就以src最后的数字为准
            dataId = RSdataId
            title = RSTitle
            if  RSdocumentNum != '':
                # print("RSdocumentNum"+ str("mmp"))
                documentNum = RSdocumentNum  # 书文号
                # print("documentNum"+documentNum)
            else:
                # print("书文号列表没有")
                if RSTitle.find("号") != -1:
                    # print("标题中含有")
                    documentNum = RSTitle
                else:
                    documentNum = ''

            if RSTitle.find("行政处罚决定书") ==-1:
                bePunished = ''  # 被处罚人或机构
            else:
                RsbePunished = re.sub(r'.*书','',RSTitle).replace("（",'').replace("）",'')
                bePunished = RsbePunished

            principal = ''  # 法定代表人

            lawEnforcement = bePunished  # 被处罚单位
            punishedDate = RSTime  # 受处罚时间
            content = RScontent  # 全文RScontent
            uniqueSign = ContentSrc  # url地址
            address = '天津'  # 省份
            area = '和平区'  # 地区
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
            adjunct = re.findall(re.compile(r'<a.*?href="(.*?)".*?>(.*?)</a>', re.I | re.S), str(fujian))

            if ConetentResponse:
                conn = pymssql.connect(host='(local)', user='sa', password='123456', database='AdministrativePun')
                # 打开游标
                cur = conn.cursor();
                if not cur:
                    raise Exception('数据库连接失败！')
                else:
                    print("数据库链接成功")
                sql1 = " INSERT INTO  crawlData20(dataId,title,documentNum,bePunished,principal,lawEnforcement,punishedDate,content,uniqueSign,address,area,agency,grade,showId) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " % (dataId, title, documentNum, bePunished,principal,lawEnforcement,punishedDate,content,uniqueSign,address, area, agency,grade,showId)


                # print(sql1)
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
    url ="http://scjg.tj.gov.cn/heping/zwgk/xzcfxx/index"

    AdminiStrative =Utils()
    for i in range(1,3):
        data = {
            'bar': 'true',
            'categoryId': '18003000000000000',
            'pageNo': '%s'%(i),
            'pageSize': '15',
            'words': '40',
            'year': '0'
        }
        AdminiStrative.parsePage(url,str(i),data)
        time.sleep(2)



























