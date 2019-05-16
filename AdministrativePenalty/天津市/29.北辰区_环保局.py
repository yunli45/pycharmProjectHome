# -*- coding: UTF-8 -*-
import requests
import re
import time
from bs4 import BeautifulSoup
import pymssql
import chardet
class Utils(object):
    def __init__(self):
        self.header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
        self.OnlyID = 1
        self.showId = 12311810

    def getPage(self,url=None):
        response = requests.get(url, headers=self.header)
        # print(response.encoding)
        response = response.content.decode('GB2312')
        return response

    def parsePage(self,url=None,pageNo=None,baseUrl=" ",path="F:\行政处罚数据\天津\环保局--红桥区\%s"):
        if pageNo =="1":
            response = self.getPage("http://www.tjbc.gov.cn/hbj/hjjc/")
            # print(url+".html")
        else:
            if int(pageNo)< 9:
                response = self.getPage(url + str(19 - int(pageNo)) + ".shtml")
            else:
                response = self.getPage(url + "0" + str(19 - int(pageNo)) + ".shtml")


        print("+++++++++++++++++++这是第："+pageNo+"页++++++++++++++++")
        # print(response)

        homePageSoup = BeautifulSoup(response,'lxml')
        homePageSoup = homePageSoup.findAll('td',attrs={'class':'zi14 hanggao30'})
        # print("这也是mmp")
        print(homePageSoup)
        srcListFind = re.findall(re.compile(r'<a href="(.*?)"></a><a href=".*?">(.*?)</a></div></td>.*?<td.*?"><div.*?">(.*?)</div></td>', re.S),str(homePageSoup))
        # print("这是mmp")
        print(srcListFind)
        print(len(srcListFind))
        print("\n\n")
        titleList=[]
        timeList=[]
        srcList =[]
        for i in srcListFind:

            srcList.append(  re.sub('.*?"','',i[0]))
            titleList.append(i[1])
            timeList.append(i[2])
        # print(srcList)
        for src in srcList:
            # print(src)
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
            ConetentResponse = ConetentResponse.content.decode('GB18030')
            ConetentResponseSoup = BeautifulSoup(ConetentResponse, 'lxml')
            ConetentResponseSoupOld = ConetentResponseSoup.find('td', attrs={'class': 'zi14 hanggao30'})
            ConetentResponseSoupOld = re.sub("<strong.*?>",'',str(ConetentResponseSoupOld)).replace("</strong>",'')
            ConetentResponseSoupOld = re.sub("<a.*?>",'',ConetentResponseSoupOld).replace("</a>",'')
            ConetentResponseSoupOld = str(ConetentResponseSoupOld)


            ContentNum = BeautifulSoup(str(ConetentResponseSoupOld), 'lxml')
            ContentTrNum =len( ContentNum.findAll('tr'))
            print("这条数据一共有："+str(ContentTrNum)+"个tr")
            ContentPNum = len(ContentNum.findAll('p'))
            print("这条数据有：" + str(ContentPNum) + "个P")

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
            ConetentResponse = re.sub(r'<p.*?>', '<p>', ConetentResponse)
            ConetentResponse = ConetentResponse.replace("'", "''").replace('\u2002', ' ').replace('<b>', '').replace('</b>', '')

            #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
            #
            # 提取文书号等信息
            #
            #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #

            # 全文已经所需的部分后，如果找到table，,并且找到的tr的个数为3 或者4个     进行以下处理
             # 全文是一个大表的形式 一共有1-4个tr标签
            if  re.findall(re.compile(r'天津市北辰区环境保护局(.*?)决定书'),RSTitle) !=[]:
                # print(re.findall(re.compile(r'天津市北辰区环境保护局(.*?)决定书'),RSTitle))
                print("天津市北辰区环境保护局(.*?)决定书")
                ConetentResponse = ConetentResponse.replace("\u3000",'').replace(' ','')
                ConetentNOW = BeautifulSoup(ConetentResponse.replace(' ',''),'lxml')
                ConetentNOWp = ConetentNOW.find_all('p')
                print(ConetentNOWp)
                for p in ConetentNOWp:
                    print(p)
                    rs = re.findall(re.compile(r'津辰环.*?号</p>'),str(p))
                    rs1 = re.findall(re.compile(r'<p>法定代表人(.*?)</p>',re.S|re.M),str(p))
                    print("找到书问号")
                    print(rs)
                    print("找到法定代表人")
                    print(rs1)
                    if rs !=[]:
                        num = ConetentNOWp.index(p)
                        print(num)
                        print("书问号xxx")
                        print(ConetentNOWp[num])
                        RSdocumentNum = ConetentNOWp[num].text.strip()  # 书文号
                        RSbePunished = ConetentNOWp[num + 1].text.strip()  # 被处罚人或机构
                        RSlawEnforcement = ConetentNOWp[num + 1].text.strip()  # 被处罚单位
                        if ConetentNOWp[-1].text.strip() =="" or ' ':
                            RSpunishedDate = ConetentNOWp[-2].text.strip()  # 受处罚时间
                        else:
                            RSpunishedDate = ConetentNOWp[-1].text.strip()  # 受处罚时间
                    if rs1!=[]:
                        print("法定jjjjj")
                        num1 = ConetentNOWp.index(p)
                        print(num1)
                        RSprincipal = ConetentNOWp[num1].text.strip()  # 法定代表人
                        print("fa")
                        print(RSprincipal)
                        print(ConetentNOWp[num1])

                    RSagency = '天津市北辰区环境保护局'  # 作出行政处罚决定机关名称
                    RScontent = ConetentResponse


            elif RSTitle.find("处罚信息公开") != -1:
                print("处罚信息公开")
                RSbePunished = ''  # 被处罚人或机构
                RSlawEnforcement = '' # 被处罚单位
                RSprincipal = ''  # 法定代表人
                RSdocumentNum = ''  # 书文号
                RSagency = '天津市北辰区环境保护局'  # 作出行政处罚决定机关名称
                RSpunishedDate = ''  # 受处罚时间
                RScontent = "这是一个附件，查查看相应的文件"+ConetentResponse

            else:
                print("这里是不含有表格的")
                ConetentNoTable  = ConetentResponse.replace(' ','')
                print(ConetentNoTable)
                RSdocumentNumFind = re.findall(re.compile(r'>(.*?津.*?[罚 处].*?号)<'), ConetentNoTable)
                RSbePunishedFind = re.findall(re.compile(r'当事人姓名或者单位名称(.*?)<'),ConetentNoTable)  # 当事人
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
                elif ConetentResponse.find("撤销环保“黄牌”警示通知书"):
                    ConetentNOW = BeautifulSoup(ConetentResponse.replace(' ', ''), 'lxml')
                    ConetentNOWp = ConetentNOW.find_all('p')
                    # print(ConetentNOWp)
                    for p in ConetentNOWp:
                        # print(p)/
                        rs = re.findall(re.compile(r'撤销环保“黄牌”警示通知书'), str(p))
                        if rs !=-1:
                            num = ConetentNOWp.index(p)
                            RSbePunished = ConetentNOWp[num].text.strip()
                            RSlawEnforcement = ConetentNOWp[num].text.strip()
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
                        r = requests.get(imgSrc, headers=self.header)
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
            area = '北辰区'  # 地区
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
                sql1 = " INSERT INTO  crawlData29(dataId,title,documentNum,bePunished,principal,lawEnforcement,punishedDate,content,uniqueSign,address,area,agency,grade,showId) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " % (dataId, title, documentNum, bePunished,principal,lawEnforcement,punishedDate,content,uniqueSign,address, area, agency,grade,showId)
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
    # 共计19页
    url ="http://www.tjbc.gov.cn/hbj/system/more/2512000000000000/0000/2512000000000000_000000"
    AdminiStrative =Utils()
    for i in range(1,19):
        AdminiStrative.parsePage(url,str(i))
        time.sleep(2)



























