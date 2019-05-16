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
        self.showId =  12330000

    def getPage(self,url=None):
        response = requests.get(url, headers=self.header)
        response = response.content.decode('utf-8')
        return response

    def parsePage(self,url=None,pageNo=None,baseUrl="http://www.nmgslw.gov.cn",path="F:\行政处罚数据\内蒙古\银监会\%s"):

        response = self.getPage("http://www.nmgslw.gov.cn/col/col510/index.html")

        print("+++++++++++++++++++这是第："+pageNo+"页++++++++++++++++")
        # print(response)

        # 注意这里数据提取出来不完整，只有src是完整的其他的信息去详细页面提取
        srcList= re.findall(re.compile(r"urls\[i\]='(.*?)';"),str(response))
        # print("这也是mmp")

        for src in srcList:
            print(src)
            RSdataId = re.sub(r'.*?/', '', src).replace('.html', '')

            if src.find("http")!=-1:
                ContentSrc = src
            else:
                src = src.replace('../../','/')
                ContentSrc = baseUrl+src
            print(ContentSrc)
            # print(ContentSrc)
            ConetentResponse = requests.get(ContentSrc,headers = self.header)
            ConetentResponse = ConetentResponse.content.decode('UTF-8')
            # 提取整个页面 在提取标题 时间   全文
            ConetentResponseSoup = BeautifulSoup(ConetentResponse, 'lxml')
            ConetentResponseSoupOld = ConetentResponseSoup.find('table', attrs={'id': 'article'})
            ConetentResponseSoupOld = re.sub("<strong.*?>",'',str(ConetentResponseSoupOld)).replace("</strong>",'')
            ConetentResponseSoupOld = re.sub("<u.*?>",'',ConetentResponseSoupOld, flags=re.S | re.M).replace("</u>",'')
            ConetentResponseSoupOld = re.sub("<b.*?>",'',ConetentResponseSoupOld, flags=re.S | re.M).replace("</b>",'')
            ConetentResponseSoupOld = re.sub('<span.*?>','',ConetentResponseSoupOld, flags=re.S | re.M).replace('</span>','')
            ConetentResponseSoupOld = str(ConetentResponseSoupOld)

            #   #  #  #  #  #  #  #  #  #  #  #  #  #  #
            #
            #           替换掉表格的所有的格式为p标签
            #
            #  #  #  #  #  #  #  #  #  #  #  #  #  #  #




            #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
            #
            # 提取文书号等信息
            #
            #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #

            RSTitle = re.findall(re.compile(r'<td.*?class="title".*?>(.*?)</td>'),ConetentResponseSoupOld)
            RSTime = re.findall(re.compile(r'.*?>.*?发布日期:(.*?)<'),ConetentResponseSoupOld)
            ConetentRS = BeautifulSoup(ConetentResponseSoupOld,'lxml')
            ConetentRS = ConetentRS.find_all('table',attrs={'id':'data'})

            ConetentRS = re.sub('<span.*?>', '', str(ConetentRS), flags=re.S | re.M).replace(
                '</span>', '')
            ConetentRS = re.sub('<col.*?>', '', ConetentRS)
            ConetentRS = re.sub('<tr.*?>', '', ConetentRS)
            ConetentRS = re.sub('<td.*?>', '', ConetentRS)
            ConetentRS = re.sub('<table.*?>', '', ConetentRS).replace('<td>', '<p><p>').replace('</td>',
                                                                                                            '</p><p>').replace(
                'tr', 'p').replace('tbody', 'p').replace('table', '').replace('</p><p></p>', '</p><p>')

            ConetentRS = re.sub(r'<p.*?><o:p> </o:p></p>', '', str(ConetentRS)).replace('<o:p></o:p>', '')
            ConetentRS = re.sub(r'<st1:.*?>', '', str(ConetentRS)).replace('</st1:chsdate>', '').replace(
                '<a name="TCSignYear"></a>', '')
            ConetentRS = re.sub(r'<o:p>\xa0</o:p>', '', str(ConetentRS))
            ConetentRS = re.sub(r'</p></p><p><p', '</p><p', str(ConetentRS)).replace('</p></p>', '</p>')
            ConetentRS = re.sub(r'<font.*?>', '', str(ConetentRS)).replace('</font>', '')
            ConetentRS = re.sub(r'<p.*?>', '<p>', str(ConetentRS), flags=re.S | re.M)
            ConetentRS = ConetentRS.replace("'", "''").replace('<b>', '').replace('</b>', '').replace(
                "2312>'，", '')

            print("修改后i的全文")
            print(ConetentRS)
            权力名称 = re.findall(re.compile(r'.*?权力名称.*?</p><p>(.*?)</p>',flags=re.M|re.S),ConetentRS)
            权力类别 = re.findall(re.compile(r'.*?权力类别.*?</p><p>(.*?)</p>',flags=re.M|re.S),ConetentRS)
            责任主体 = re.findall(re.compile(r'.*?责任主体.*?</p><p>(.*?)</p>',flags=re.M|re.S),ConetentRS)
            设定依据 = re.findall(re.compile(r'.*?设定依据.*?</p><p>(.*?)</p>',flags=re.M|re.S),ConetentRS)
            责任事项 = re.findall(re.compile(r'.*?责任事项.*?</p><p>(.*?)</p>',flags=re.M|re.S),ConetentRS)
            追责情形及追责依据 = re.findall(re.compile(r'.*?追责情形及追责依据.*?</p><p>(.*?)</p>',flags=re.M|re.S),ConetentRS)

            print(责任事项)
            RSdocumentNum = '无'
            RSTitle =  权力名称[0].replace(" ",'').replace("\n",'')
            RSbePunished = 责任主体[0].replace(" ",'').replace("\n",'')
            RSprincipal = ''
            RSlawEnforcement = 责任主体[0].replace(" ",'').replace("\n",'')
            RSpunishedDate = RSTime[0].replace(" ",'').replace("\n",'')
            RScontent = "权力类别："+权力类别[0].replace(" ",'').replace("\n",'')+"\n 责任主体："+责任主体[0].replace(" ",'').replace("\n",'')+"\n 设定依据："+设定依据[0].replace(" ",'').replace("\n",'')+"\n 责任事项："+责任事项[0].replace(" ",'').replace("\n",'')+"\n 追责情形及追责依据："+追责情形及追责依据[0].replace(" ",'').replace("\n",'')


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
            area = "内蒙古自治区"  # 地区
            agency =  "内蒙古自治区水利厅"   # 处罚机构
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
                conn = pymssql.connect(host='(local)', user='sa', password='123456', database='AdministrativePunNeiM')
                # 打开游标
                cur = conn.cursor();
                if not cur:
                    raise Exception('数据库连接失败！')
                else:
                    print("数据库链接成功")
                sql1 = " INSERT INTO  crawlDataNeiM7(dataId,title,documentNum,bePunished,principal,lawEnforcement,punishedDate,content,uniqueSign,address,area,agency,grade,showId) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " % (dataId, title, documentNum, bePunished,principal,lawEnforcement,punishedDate,content,uniqueSign,address, area, agency,grade,showId)


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
    url ="http://www.nmgslw.gov.cn/col/col510/index.html"
    AdminiStrative =Utils()
    for i in range(1,2):
        AdminiStrative.parsePage(url,str(i))
        time.sleep(5)



























