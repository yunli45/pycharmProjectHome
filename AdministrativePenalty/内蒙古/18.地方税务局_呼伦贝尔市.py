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
        self.showId = 12334180

    def getPage(self,url=None):
        response = requests.get(url, headers=self.header)
        response = response.content.decode('utf-8')
        return response

    def parsePage(self,url=None,pageNo=None,baseUrl="http://www.btgaj.gov.cn",path="F:\行政处罚数据\内蒙古\呼伦贝尔_地方税务局\%s"):
        if pageNo =="1":
            response = self.getPage(url+".html")
        else:
            response =  self.getPage(url+"_"+str(int(pageNo)-1)+".html")
            print(url+"_"+str(int(pageNo)-1)+".html")

        print("+++++++++++++++++++这是第："+pageNo+"页++++++++++++++++")
        # print(response)
        response = response.replace("\n",'').replace("\r",'').replace("\t",'')
        # 注意这里数据提取出来不完整，只有src是完整的其他的信息去详细页面提取

        responseList = BeautifulSoup(response,'lxml')
        responseList = responseList.find_all('div',attrs={'class':'gailan_R'})
        # print(responseList)
        RSlist = re.findall(re.compile(r'<a href="(.*?)" target="_blank">(.*?)</a><span.*?>(.*?)</span>',re.S|re.M),str(responseList))
        # print("这也是mmp")
        print(RSlist)
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
            ConetentResponseSoupOld = ConetentResponseSoup.find('table', attrs={'class': 'xl_hei14'})
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
            print("还没修改完全的全文+" + ConetentResponseSoupOld)
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

            # 含有表格
            if ConetentResponseSoupOld.find("<table")!=-1:
                ConetentResponseTable = re.sub('<span.*?>', '', str(ConetentResponseSoupOld)).replace('</span>', '')
                ConetentResponseTable = re.sub('<p.*?>', '', str(ConetentResponseTable)).replace('</p>', '')
                ConetentResponseTable = re.sub('<font.*?>', '', str(ConetentResponseTable)).replace('</font>', '')

                # 替换标签
                ConetentResponseTable = re.sub('<col.*?>', '', ConetentResponseTable).replace('</colgroup>', '')
                ConetentResponseTable = re.sub('<td.*?>', '<td>', ConetentResponseTable)
                ConetentResponseTable = re.sub('<tr.*?>', '<tr>', ConetentResponseTable).replace("<td><td>", "<td>")
                # print("表格的内容" + ConetentResponseTable)
                TableSoup = BeautifulSoup(ConetentResponseTable, 'lxml')
                # listTr = []
                listTd= []
                for ids ,tr in enumerate( TableSoup.find_all('tr')):
                    # listTr.append(tr)
                    tds = tr.find_all('td')
                    listTd.append(tds)
                print("TD集合")
                print(listTd)
                if listTd!=[]:
                    # print(listTd[-3][-1])
                    RSdocumentNum =  listTd[1][1].text.strip() # s书文号
                    RSagency =  listTd[2][1].text.strip() # 做出处罚机构
                    RSbePunished =  listTd[3][3].text.strip() #被处罚人或机构
                    RSlawEnforcement = listTd[3][3].text.strip() #被处罚机构
                    RSprincipal =listTd[-3][-1].text.strip() # 法人
                    RSpunishedDate = listTd[4][1].text.strip() # 处罚时间
                    行政处罚决定书文号 = RSdocumentNum
                    RScontent = ConetentResponse

                    # RScontent = "行政处罚决定书文号:"+RSdocumentNum +"处罚类别:"+ listTd[1][-1].text.strip()# 全文

            #  文中可能含有图片，进行下载
            JpgContent = re.findall(re.compile(r'<img src="(.*?)".*?>'),str(ConetentResponseSoupOld))
            print("tupianList"+str(JpgContent))
            if JpgContent!=[]:
                for num in JpgContent:
                    print("tup地址"+num)
                    rsJpgName =  RSTitle+ str(JpgContent.index(num))+".jpg"
                    print(rsJpgName)
                    if num.find("http")== -1:
                        rsJpgSrc =  baseUrl+num
                    else:
                        rsJpgSrc =num

                    print("图片地址"+rsJpgSrc)
                    path1 = path % (rsJpgName)
                    r = requests.get(rsJpgSrc, headers=self.header, timeout=1)
                    with open(path1, "wb") as f:
                        f.write(r.content)
                    f.close()


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
            area = "包头市地方税务局"  # 地区
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
                sql1 = " INSERT INTO  crawlDataNeiM21(dataId,title,documentNum,bePunished,principal,lawEnforcement,punishedDate,content,uniqueSign,address,area,agency,grade,showId) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " % (dataId, title, documentNum, bePunished,principal,lawEnforcement,punishedDate,content,uniqueSign,address, area, agency,grade,showId)


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
    url ="http://hlbe.nmds.gov.cn/xxgk/yfxz/xzcfgs/index"
    AdminiStrative =Utils()
    for i in range(1,2):
        AdminiStrative.parsePage(url,str(i))
        time.sleep(5)



























