# -*- coding:utf-8 -*-
import requests
import re
import time
from bs4 import BeautifulSoup
import pymssql

class Utils(object):
    def __init__(self):
        self.header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
        self.OnlyID = 1
        self.showId =  12331800

    def getPage(self,url=None):
        response = requests.get(url, headers=self.header)
        response = response.content.decode('utf-8')
        return response

    def parsePage(self,url=None,pageNo=None,baseUrl="http://www.cbrc.gov.cn",path="F:\行政处罚数据\内蒙古\银监分局\%s"):
        if pageNo =="1":
            response = self.getPage(url+pageNo)
        else:
            response =  self.getPage(url+pageNo)

        print("+++++++++++++++++++这是第："+pageNo+"页++++++++++++++++")
        # print(response)
        response = response.replace("\n",'').replace("\r",'').replace("\t",'')
        # 注意这里数据提取出来不完整，只有src是完整的其他的信息去详细页面提取

        responseList = BeautifulSoup(response,'lxml')
        responseList = responseList.find_all('table',attrs={'id':'testUI'})
        # print(responseList)
        RSlist = re.findall(re.compile(r'<a.*?href="(.*?)".*?title=".*?">(.*?)</a></td><td.*?>(.*?)</td>',re.S|re.M),str(responseList))
        # print("这也是mmp")
        # print(RSlist)
        # print(len(RSlist))
        SrcList = []
        TitleList =[]
        TimeList = []
        for i in RSlist:
            SrcList.append(i[0])
            TitleList.append(i[1])
            TimeList.append(i[2])

        for src in SrcList:
            RSTitle = TitleList[SrcList.index(src)]
            RSTime = TimeList[SrcList.index(src)]
            RSdataId = re.sub(r'.*?/', '', src).replace('.html', '')

            if src.find("http")!=-1:
                ContentSrc = src
            else:
                src = src.replace('../../','/')
                ContentSrc = baseUrl+src
            print(ContentSrc)
            # print(ContentSrc)
            # 提取整个页面 在提取标题 时间   全文
            ConetentResponse = requests.get(ContentSrc, headers=self.header)
            ConetentResponse = ConetentResponse.content.decode('UTF-8')
            ConetentResponseSoup = BeautifulSoup(ConetentResponse, 'lxml')
            ConetentResponseSoupOld = ConetentResponseSoup.find('div', attrs={'class': ' f12c'})
            ConetentResponseSoupOld = re.sub("<strong.*?>", '', str(ConetentResponseSoupOld)).replace("</strong>", '')
            ConetentResponseSoupOld = re.sub("<u.*?>", '', ConetentResponseSoupOld, flags=re.S | re.M).replace("</u>",
                                                                                                               '')
            ConetentResponseSoupOld = re.sub("<b.*?>", '', ConetentResponseSoupOld, flags=re.S | re.M).replace("</b>",
                                                                                                               '')
            ConetentResponseSoupOld = re.sub('<span.*?>', '', ConetentResponseSoupOld, flags=re.S | re.M).replace(
                '</span>', '')
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
            ConetentResponse = re.sub('<col.*?>', '', ConetentResponseSoupOld)
            ConetentResponse = re.sub('<tr.*?>', '<p>', ConetentResponse).replace("</tr>","</p>")
            ConetentResponse = re.sub('<td.*?>', '<p>', ConetentResponse).replace("</td>","</p>")
            ConetentResponse = re.sub('<table.*?>', '', ConetentResponse).replace("</table>","")
            ConetentResponse = re.sub('<tbody.*?>', '', ConetentResponse).replace("</tbody>","")
            ConetentResponse = re.sub(r'<p.*?><o:p> </o:p></p>', '', str(ConetentResponse)).replace('<o:p></o:p>', '')
            ConetentResponse = re.sub(r'<st1:.*?>', '', str(ConetentResponse)).replace('</st1:chsdate>', '').replace(
                '<a name="TCSignYear"></a>', '')
            ConetentResponse = re.sub(r'<o:p>\xa0</o:p>', '', str(ConetentResponse))
            ConetentResponse = re.sub(r'<p.*?>', '<p>', str(ConetentResponse), flags=re.S | re.M)
            ConetentResponse = ConetentResponse.replace("'", "''").replace('<b>', '').replace('</b>', '').replace(
                "2312>'，", '')

            # print("修改后i的全文")
            # print(ConetentResponse)

            # 含有行政处罚信息公开表MsoNormalTable
            if ConetentResponseSoupOld.find("行政处罚信息公开表")!=-1:
                MsoNormalTable = BeautifulSoup(ConetentResponseSoupOld,'lxml')
                MsoNormalTable1 =  MsoNormalTable.findAll('table',attrs={'class':'MsoNormalTable'})
                MsoNormalTable2 =  MsoNormalTable.findAll('table',attrs={'class':'MsoTableGrid'})

                if MsoNormalTable1 !=[]:
                    MsoNormalTable = MsoNormalTable1
                elif MsoNormalTable2 !=[]:
                    MsoNormalTable = MsoNormalTable2
                else:
                    print("有问题")
                    break

                MsoNormalTable = re.sub(r'<table.*?>','',str(MsoNormalTable),flags=re.M|re.S)
                MsoNormalTable = re.sub('<tr.*?>', '<tr>',str(MsoNormalTable),flags=re.M|re.S)
                MsoNormalTable = re.sub('<td.*?>', '<td>',str(MsoNormalTable),flags=re.M|re.S)
                MsoNormalTable = re.sub('<col.*?>', '',str(MsoNormalTable),flags=re.M|re.S)
                MsoNormalTable = re.sub('<div.*?>', '',str(MsoNormalTable),flags=re.M|re.S).replace("</div>",'')
                MsoNormalTable = re.sub('<st1.*?>', '',str(MsoNormalTable),flags=re.M|re.S).replace("</st1:chsdate>",'').replace("\n",'').replace("\t",'')
                MsoNormalTable = re.sub('<p.*?>', '',str(MsoNormalTable),flags=re.M|re.S).replace('</p>','').replace('<o:p>','').replace('</o:p>','')
                # print("行政处罚信息公开表")
                # print(MsoNormalTable)
                MsoNormalTable = BeautifulSoup(MsoNormalTable, 'lxml')
                TrList = []
                TDList = []
                for ids,tr in enumerate(MsoNormalTable.findAll('tr')):
                    TrList.append(tr)
                    if ids!=-1:
                        tds = tr.find_all('td')
                        TDList.append(tds)
                print("表格LIst")
                print(TDList)
                if TDList !=[]:
                    RSdocumentNum = TDList[0][-1].text.strip()  # s书文号
                    RSbePunished = TDList[1][-1].text.strip()  # 被处罚人或机构
                    RSlawEnforcement = TDList[2][-1].text.strip()  # 被处罚机构
                    RSprincipal = TDList[3][-1].text.strip()  # 法人
                    RSagency = TDList[-2][-1].text.strip()  # 做出处罚机构
                    RSpunishedDate = TDList[-1][-1].text.strip()  # 处罚时间
                    RScontent ="主要违法违规事实（案由）:"+TDList[4][-1].text.strip()+"\n 行政处罚依据:"+TDList[5][-1].text.strip()+"\n 行政处罚决定:"+TDList[6][-1].text.strip()

            else:
                MsoNormalContent  = BeautifulSoup(ConetentResponseSoupOld, 'lxml')
                MsoNormalContent  = MsoNormalContent.findAll('div', attrs={'class': 'Section1'})
                MsoNormalContent = re.sub('<span.*?>','',str(MsoNormalContent),flags=re.S|re.M).replace("</span>",'')
                MsoNormalContent = re.sub('<p.*?>','<p>',str(MsoNormalContent),flags=re.S|re.M)
                MsoNormalContent = re.sub('<font.*?>','',str(MsoNormalContent),flags=re.S|re.M)
                MsoNormalContent = re.sub('<st1:chsdate.*?>','',str(MsoNormalContent),flags=re.S|re.M).replace("</st1:chsdate>",'').replace("<o:p>",'')
                MsoNormalContentNew = MsoNormalContent.replace("</o:p>",'').replace("\n",'').replace("\t",'')
                MsoNormalContent = BeautifulSoup(MsoNormalContentNew,'lxml')
                MsoNormalContentP = MsoNormalContent.find_all('p')
                RSdocNumFind = re.findall(re.compile("<p>.*?银监罚字.*\d号</p>"),MsoNormalContentNew)
                RSagencyFind = re.findall(re.compile("<p>.*?银监分局</p>"),MsoNormalContentNew)
                PList = []
                for p in MsoNormalContentP:
                    PList.append(p)
                print(PList)
                # print(PList[0])
                if PList[3].text.strip() !=''or " " and len(PList[3].text.strip())>11 :
                    RSbePunished = PList[3].text.strip() # 被处罚人或单位
                else:
                    RSbePunished = ''

                if RSdocNumFind !=[]:
                    RSdocNumFind = RSdocNumFind[0]
                    RSdocumentNum = PList[PList.index(RSdocNumFind)].text.strip()
                else:
                    RSdocumentNum = ""

                if PList[-2].text.strip()!=''or " "  and len(PList[-2].text.strip())<20  and PList[-2].text.strip().find("银监分局")!=-1:
                    RSagency = PList[-2].text.strip() # 处罚机构
                    RSlawEnforcement = RSagency  # 被处罚单位
                elif PList[-3].text.strip()!=''or " "  and len(PList[-3].text.strip())<20  and PList[-3].text.strip().find("银监分局")!=-1:
                    RSagency = PList[-3].text.strip()  # 处罚机构
                    RSlawEnforcement = RSagency  # 被处罚单位
                else:
                    RSagency =""
                    RSlawEnforcement =""

                if PList[-2].text.strip()!=''or " "  and len(PList[-2].text.strip())<20 and PList[-2].text.strip().find("年") !=-1 and  PList[-2].text.strip().find("月")!=-1  and PList[-2].text.strip().find("日")!=-1:
                    RSpunishedDate = PList[-2].text.strip()
                elif PList[-3].text.strip()!=''or " "  and len(PList[-3].text.strip())<20 and PList[-3].text.strip().find("年")!=-1 and  PList[-3].text.strip().find("月")!=-1  and PList[-3].text.strip().find("日")!=-1:
                    RSpunishedDate = PList[-3].text.strip()
                elif PList[-1].text.strip() != '' or " " and len(PList[-1].text.strip()) < 20 and PList[-1].text.strip().find("年")!=-1 and PList[-1].text.strip().find("月")!=-1 and PList[-1].text.strip().find("日")!=-1:
                    RSpunishedDate = PList[-1].text.strip()
                elif PList[-4].text.strip() != '' or " " and len(PList[41].text.strip()) < 20 and PList[
                        -4].text.strip().find("年")!=-1 and PList[-4].text.strip().find("月")!=-1 and PList[-4].text.strip().find(
                        "日")!=-1:
                    RSpunishedDate = PList[-4].text.strip()
                else:
                    RSpunishedDate =""
                RSprincipal =""
                RScontent = ConetentResponse

                    # RScontent = "行政处罚决定书文号:"+RSdocumentNum +"处罚类别:"+ listTd[1][-1].text.strip()# 全文


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
            address = '内蒙古自治区'  # 省份  RSagency
            area = "包头市"  # 地区
            agency = RSagency   # 处罚机构
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
            adjunct = re.findall(re.compile(r'<a.*?href="(.*?)".*?>(.*?)</a>', re.I | re.S), str(ConetentResponseSoupOld))

            if ConetentResponse:
                conn = pymssql.connect(host='(local)', user='sa', password='123456', database='AdministrativePunNeiM')
                # 打开游标
                cur = conn.cursor();
                if not cur:
                    raise Exception('数据库连接失败！')
                else:
                    print("数据库链接成功")
                sql1 = " INSERT INTO  crawlDataNeiM11(dataId,title,documentNum,bePunished,principal,lawEnforcement,punishedDate,content,uniqueSign,address,area,agency,grade,showId) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " % (dataId, title, documentNum, bePunished,principal,lawEnforcement,punishedDate,content,uniqueSign,address, area, agency,grade,showId)


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
                            r = requests.get(rsDocuniqueSign, headers=self.header, timeout=30)
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
    url ="http://www.cbrc.gov.cn/chinese/home/docViewPage/60270407&current="
    AdminiStrative =Utils()
    for i in range(1,10):
        AdminiStrative.parsePage(url,str(i))
        time.sleep(2)



























