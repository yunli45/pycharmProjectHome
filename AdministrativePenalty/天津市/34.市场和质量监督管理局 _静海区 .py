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
        self.showId = 12318222

    def getPage(self,url=None):
        response = requests.get(url, headers=self.header)
        response = response.content.decode('utf-8')
        return response

    def parsePage(self,url=None,pageNo=None,baseUrl="http://scjg.tj.gov.cn/jinghai/zwgk/xzcfxx/",path="F:\行政处罚数据\天津\市市场和质量监督管理局 _静海区\%s"):
        if pageNo =="1":
            response = self.getPage(url+".html")
            print(url+".html")
        else:
            response = self.getPage(url+"_"+str(int(pageNo)-1)+".html")

        print("+++++++++++++++++++这是第："+pageNo+"页++++++++++++++++")
        # print(response)

        homePageSoup = BeautifulSoup(response,'lxml')
        homePageSoup = homePageSoup.findAll('div',attrs={'class':'content'})
        # print("这也是mmp")
        print(homePageSoup)
        srcListFind = re.findall(re.compile(r'<a href="(.*?)".*?title="(.*?)">.*?</a>.*?<span.*?>(.*?)</span>', re.S),str(homePageSoup))
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
                src = src.replace('../../','/')
                ContentSrc = "http://scjg.tj.gov.cn/jinghai/zwgk/xzcfxx"+src
            print(ContentSrc)
            # print(ContentSrc)
            ConetentResponse = requests.get(ContentSrc,headers = self.header)
            ConetentResponse = ConetentResponse.content.decode('UTF-8')
            ConetentResponseSoup = BeautifulSoup(ConetentResponse, 'lxml')
            ConetentResponseSoupOld = ConetentResponseSoup.find('div', attrs={'class': 'news_content'})
            ConetentResponseSoupOld = re.sub("<strong.*?>",'',str(ConetentResponseSoupOld)).replace("</strong>",'')
            ConetentResponseSoupOld = re.sub("<u.*?>",'',ConetentResponseSoupOld, flags=re.S | re.M).replace("</u>",'')
            ConetentResponseSoupOld = re.sub("<b.*?>",'',ConetentResponseSoupOld, flags=re.S | re.M).replace("</b>",'')
            ConetentResponseSoupOld = re.sub('<span.*?>','',ConetentResponseSoupOld, flags=re.S | re.M).replace('</span>','')
            ConetentResponseSoupOld = str(ConetentResponseSoupOld)

            ContentNum = BeautifulSoup(str(ConetentResponseSoupOld), 'lxml')
            ContentTrNum =len( ContentNum.findAll('tr'))
            print("这条数据一共有："+str(ContentTrNum)+"个tr")
            ContentPNum = len(ContentNum.findAll('p'))
            print("这条数据有：" + str(ContentPNum) + "个P")
            print("还没修改完全的全文+"+ConetentResponseSoupOld)
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
            ConetentResponse = re.sub(r'<p.*?>', '<p>', str(ConetentResponse), flags=re.S | re.M)
            ConetentResponse = ConetentResponse.replace("'","''").replace('<b>','').replace('</b>','')
            print("修改后i的全文")
            print(ConetentResponse)



            #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
            #
            # 提取文书号等信息
            #
            #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #

            # 全文已经所需的部分后，如果找到table，,并且找到的tr的个数为3 或者4个     进行以下处理
             # 全文是一个大表的形式 一共有1-4个tr标签，我们想要的结果都在一般在最后一行，所以先找tr --》在找td-->再找书文号--》一以书文号所在哪一行为基准进行取值
            if str(ConetentResponseSoupOld).find("<table") != -1 and  1 <= ContentTrNum <= 13 and ContentPNum < 60 and str(ConetentResponseSoupOld).find("行政处罚信息摘要")==-1:
                # 先去除多余的标签

                ConetentResponseTable = re.sub('<span.*?>', '', str(ConetentResponseSoupOld)).replace('</span>', '')
                ConetentResponseTable = re.sub('<p.*?>', '', str(ConetentResponseTable)).replace('</p>', '')
                ConetentResponseTable = re.sub('<font.*?>', '', str(ConetentResponseTable)).replace('</font>', '')

                # 替换标签
                ConetentResponseTable = re.sub('<col.*?>', '', ConetentResponseTable).replace('</colgroup>', '')
                ConetentResponseTable = re.sub('<td.*?>', '<td>', ConetentResponseTable)
                ConetentResponseTable = re.sub('<tr.*?>', '<tr>', ConetentResponseTable).replace("<td><td>", "<td>")
                print("表格的内容"+ConetentResponseTable)
                TableSoup = BeautifulSoup(ConetentResponseTable, 'lxml')
                listTr1 = []
                for ids, tr in enumerate(TableSoup.find_all('tr')):
                    listTr1.append(ids)
                    TrDocNUM = re.findall(re.compile(r'<td>津.*?[工 商 市 场 罚].*?\d.*?号.*?</td>'), str(tr))
                    print("表格中书文号："+str(TrDocNUM))
                    print("这里是表格形式的")
                    if TrDocNUM!=[]:
                        TrNUM = ids
                        # 以书文号一行为基准找数据
                        if listTr1[TrNUM]:
                            print("找到书文号啦"+str(listTr1[TrNUM]))
                            tds = tr.find_all('td')
                            if len(tds) > 10:
                                print("这是大于10的表格")
                                RSbePunished = tds[1].text.strip()  # 被处罚人或机构
                                RSlawEnforcement = tds[1].text.strip()  # 被处罚单位
                                RSprincipal = tds[4].text.strip()  # 法定代表人
                                RSdocumentNum = tds[5].text.strip()  # 书文号
                                RSagency = tds[10].text.strip()  # 作出行政处罚决定机关名称
                                RSpunishedDate = tds[11].text.strip()  # 受处罚时间
                                RScontent = "主要违法事实:" + tds[6].text.strip() + "\n 处罚种类:" + tds[
                                    7].text.strip() + "\n 处罚依据:"+ tds[8].text.strip() + "\n 行政处罚的履行方式和期限:" + tds[
                                                    9].text.strip()
                            # 特殊情况
                            elif len(tds)==10:
                                print("这是等于10的 表格")
                                RSbePunished = tds[1].text.strip()  # 被处罚人或机构
                                RSlawEnforcement = tds[1].text.strip()  # 被处罚单位
                                RSprincipal = ''  # 法定代表人
                                RSdocumentNum = tds[3].text.strip()  # 书文号
                                RSagency = tds[8].text.strip()  # 作出行政处罚决定机关名称
                                RSpunishedDate = tds[9].text.strip()  # 受处罚时间
                                RScontent = "违法行为:" + tds[4].text.strip() + "\n 处罚种类:" + tds[
                                    5].text.strip() + "\n 罚款金额，单位：万元:" + tds[6].text.strip()
                            elif len(tds) == 9:
                                print("这是等于9的 表格")
                                RSbePunished = tds[0].text.strip()  # 被处罚人或机构
                                RSlawEnforcement = tds[0].text.strip()  # 被处罚单位
                                RSprincipal = ''  # 法定代表人
                                RSdocumentNum = tds[2].text.strip()  # 书文号
                                RSagency = tds[7].text.strip()  # 作出行政处罚决定机关名称
                                RSpunishedDate = tds[8].text.strip()  # 受处罚时间
                                RScontent = "违法行为:" + tds[3].text.strip() + "\n 处罚种类:" + tds[
                                    4].text.strip() + "\n 罚款金额，单位：万元:" + tds[5].text.strip()




                        else:
                            RSbePunished = '特殊情况1，查看你下'  # 被处罚人或机构
                            RSlawEnforcement = '特殊情况1，查看你下'  # 被处罚单位
                            RSprincipal = '特殊情况1，查看你下' # 法定代表人
                            RSdocumentNum = '特殊情况1，查看你下'  # 书文号
                            RSagency = '特殊情况1，查看你下'  # 作出行政处罚决定机关名称
                            RSpunishedDate = '特殊情况1，查看你下'  # 受处罚时间
                            RScontent = ConetentResponse

            # 全文以“行政处罚信息摘要”的表格为开头
            elif  str(ConetentResponseSoupOld).find("<table") != -1 and str(ConetentResponseSoupOld).find("行政处罚信息摘要")!=-1:
                print("全文含有表格")
                # 先处理标签问题，先简化  只剩td tr标签
                ConetentResponseAndTabe = re.sub('<span.*?>', '', str(ConetentResponseSoupOld),
                                                 flags=re.S | re.M).replace('</span>', '')
                ConetentResponseAndTabe = re.sub(r'<p.*?>', '', str(ConetentResponseAndTabe)).replace('</p>', '')
                ConetentResponseTable = re.sub('<col.*?>', '', ConetentResponseAndTabe).replace('</colgroup>', '')
                ConetentResponseTable = re.sub('<td.*?>', '<td>', ConetentResponseTable)
                ConetentResponseTable = re.sub('<tr.*?>', '<tr>', ConetentResponseTable).replace("<td><td>", "<td>").replace("'","''")

                ConetentResponseAndTabe = BeautifulSoup(ConetentResponseTable, 'lxml')

                # 全文是表格的形式，且不止4个tr
                tdlist = []
                for idx, tr in enumerate(ConetentResponseAndTabe.findAll('tr')):
                    # print(idx)
                    # print(tr)
                    if tr.find("行政处罚信息摘要") != -1:
                        tds = tr.find_all('td')
                        tdlist.append(tds)
                    else:
                         pass

                RSdocumentNum = tdlist[0][1].text.strip()
                RSbePunished = tdlist[1][3].text.strip() # 被处罚人或机构
                RSprincipal = tdlist[5][1].text.strip() # 法定代表人
                RSlawEnforcement = tdlist[3][2].text.strip()# 被处罚单位
                RSpunishedDate = tdlist[9][1].text.strip() # 受处罚时间
                RSagency = tdlist[8][1].text.strip() # 处罚机构
                RScontent = ConetentResponse # 全文
            #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
            #      不含有表格 ：全文可能是纯文字的也可能是一张图片
            #      注意：有一个坑是全文是文字，图片是一个线段< img src:"..">
            #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
            else:
                # 处理掉空格
                print("这里是不含有表格的,只有文章内容")
                ConetentNoTable  = ConetentResponse.replace(' ','').replace("当事人名称或姓名：",'').replace("法定代表人（负责人）：",'').replace("法定代表人：",'').replace("当事人姓名或者单位名称:",'').replace("法定代表人（负责人）:",'').replace("负责人:",'')
                # 全文还可能是一个图片的形式
                RSimgFind = re.findall(re.compile(r'<img.*?src="(.*?)".*?>'), ConetentResponse)

                print(ConetentNoTable)
                ConetentNOW = BeautifulSoup(ConetentNoTable, 'lxml')
                ConetentNOWp = ConetentNOW.find_all('p')
                print(ConetentNOWp)
                for p in ConetentNOWp:
                    RSdocumentNumFind = re.findall(re.compile(r'津.*?[市 场 监].*?号'), str(p))
                    AdressNumFind = re.findall(re.compile(r'.*?地址|住址.*?'), str(p))

                    if RSdocumentNumFind!=[]:
                        RSdocumentNum = RSdocumentNumFind[0]  # 书文号
                        documentPNum =  ConetentNOWp.index(p)
                        0
                    if AdressNumFind != []:
                        print(p)
                        AdressNum =  ConetentNOWp.index(p)
                        print("hajhahah ")
                        print(AdressNum)
                        RSbePunished = ConetentNOWp[AdressNum-2].text.strip() # 被处罚人或者单位
                        RSlawEnforcement = ConetentNOWp[AdressNum-2].text.strip()# 被处罚单位
                        RSprincipal = ConetentNOWp[AdressNum+1].text.strip()   # 法人
                        print(RSbePunished)
                        print(RSlawEnforcement)
                        print(RSprincipal)
                        break
                    elif AdressNumFind ==[]:
                        print("mmmpppp")
                        RSbePunished = "地址没有的情况"
                        RSlawEnforcement= "地址没有的情况"
                        RSprincipal ="地址没有的情况"

                    if  ConetentNOWp[-1].text.strip() != ''or ' ':
                        RSpunishedDate = ConetentNOWp[-1].text.strip()  # 受处罚时间
                    else:
                        RSpunishedDate = ConetentNOWp[-2].text.strip()  # 受处罚时间
                if RSimgFind:
                    print(RSTitle)
                    print(RSimgFind)
                    print(ConetentResponse)
                    ConetentResponse = "这可能是一个图片形式的，请查看本地是否有相应的标题图片"+ ConetentResponse
                    RSdocumentNum = ''  # 书文号
                    imgSrc = RSimgFind[0]
                    RSbePunished = ''  # 被处罚人或者单位
                    RSlawEnforcement = ''  # 被处罚单位
                    RSprincipal = ''  # 法人
                    RSpunishedDate = ''  # 受处罚时间

                    try :
                        imgSrc =   imgSrc
                        for TitleNum in enumerate(RSimgFind):
                            imgTitle = RSTitle + str(TitleNum[0])+".jpg"
                            path1 = path  % (imgTitle)
                            r = requests.get(imgSrc, headers=self.header, timeout=3)
                            with open(path1, "wb") as f:
                                f.write(r.content)
                            f.close()
                    except :
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
            area = '静海区'  # 地区
            agency =  '天津市静海区市场和质量监督管理局'  # 处罚机构
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
                sql1 = " INSERT INTO  crawlData34(dataId,title,documentNum,bePunished,principal,lawEnforcement,punishedDate,content,uniqueSign,address,area,agency,grade,showId) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " % (dataId, title, documentNum, bePunished,principal,lawEnforcement,punishedDate,content,uniqueSign,address, area, agency,grade,showId)
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
    # 共计353页
    url ="http://scjg.tj.gov.cn/jinghai/zwgk/xzcfxx/index"
    AdminiStrative =Utils()
    for i in range(15,16):
        AdminiStrative.parsePage(url,str(i))
        time.sleep(2)



























