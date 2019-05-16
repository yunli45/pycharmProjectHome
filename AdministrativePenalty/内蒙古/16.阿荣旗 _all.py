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
        self.showId =  12332700

    def getPage(self,url=None):
        response = requests.get(url, headers=self.header)
        response = response.text.encode('UTF-8').decode('utf-8')
        return response

    def parsePage(self,url=None,pageNo=None,baseUrl="http://www.arq.gov.cn",path="F:\行政处罚数据\内蒙古\阿荣旗\%s"):
        if pageNo=="1":
            response = self.getPage(url+".aspx")
        else:
            response = self.getPage(url +"_"+str(int(pageNo)-1)+".aspx")
        print("+++++++++++++++++++这是第："+pageNo+"页++++++++++++++++")
        print("全文返回数据")
        # print(response)
        response = response.replace("\n",'').replace("\r",'').replace("\t",'')
        # 注意这里数据提取出来不完整，只有src是完整的其他的信息去详细页面提取
        RS = re.findall(re.compile(r'<ul class="newsList">(.*?)</ul>'),str(response))
        # print("首页找到得集合")
        # print(RS)
        RSlist = re.findall(re.compile(r'<span class="date">(.*?)</span><a.*?href="(.*?)".*?title="标题：(.*?)&#xD.*?&#xD.*?">',re.S|re.M),str(RS))
        # print("这也是mmp")
        # print(RSlist)
        print(len(RSlist))
        SrcList = []
        TitleList =[]
        TimeList = []
        for i in RSlist:
            SrcList.append(i[1])
            TitleList.append(i[2])
            TimeList.append(i[0])
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
            ConetentResponse = ConetentResponse.content.decode('utf-8')
            ConetentResponseSoup = BeautifulSoup(ConetentResponse, 'lxml')
            ConetentResponseSoupOld = ConetentResponseSoup.find('div', attrs={'id': 'fontzoom'})
            ConetentResponseSoupOld = re.sub("<strong.*?>", '', str(ConetentResponseSoupOld)).replace("</strong>", '')
            ConetentResponseSoupOld = re.sub("<u.*?>", '', ConetentResponseSoupOld, flags=re.S | re.M).replace("</u>",
                                                                                                               '')
            ConetentResponseSoupOld = re.sub("<b.*?>", '', ConetentResponseSoupOld, flags=re.S | re.M).replace("</b>",
                                                                                                               '')
            ConetentResponseSoupOld = re.sub('<span.*?>', '', ConetentResponseSoupOld, flags=re.S | re.M).replace(
                '</span>', '')
            ConetentResponseSoupOld = re.sub('<font.*?>', '', ConetentResponseSoupOld, flags=re.S | re.M).replace(
                '</font>', '')
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
            ConetentResponse = re.sub(r'<font.*?>', '', str(ConetentResponse), flags=re.S | re.M).replace("</font>",'')
            ConetentResponse = ConetentResponse.replace("'", "''").replace('<b>', '').replace('</b>', '').replace(
                "2312>'，", '')

            ConetentSoup = BeautifulSoup(ConetentResponse,'lxml')
            ConetentSoupP = ConetentSoup.find_all('p')
            RSbePunishedFind1 = re.findall(re.compile(r'<p.*?>当事人[: ：](.*?)[$;|；|,|，]'),str(ConetentResponse))
            RSbePunishedFind2 = re.findall(re.compile(r'<p.*?>违法行为人[: ：](.*?)身份证号'),str(ConetentResponse))
            if RSbePunishedFind1!=[]:
                RSbePunishedFind = RSbePunishedFind1
            elif RSbePunishedFind2 !=[]:
                RSbePunishedFind =RSbePunishedFind2

            RSprincipalFind =  re.findall(r'经营者|法.*?代表.*?[: ：](.*?)[$;|；|,|，]',str(ConetentResponse))
            RSRSagencyFind = re.findall(re.compile(r'阿荣旗.*?局'),str(ConetentResponse))
            for p in ConetentSoupP:
                RSdocumentNumFind1 = re.findall(re.compile(r'<p>当事人.*?</p>'),str(p))
                RSdocumentNumFind2 = re.findall(re.compile(r'<p>违法行为人.*?</p>'),str(p))
                if RSdocumentNumFind1:
                    Pnum = ConetentSoupP.index(p)
                    break
                elif RSdocumentNumFind2:
                    Pnum = ConetentSoupP.index(p)
                    break
                elif RSdocumentNumFind1==[] and RSdocumentNumFind2 ==[]:
                    Pnum = 3
            # 书文号
            try:
                if ConetentSoupP[Pnum-1].text.strip()!=""or " ":
                    RSdocumentNum = ConetentSoupP[Pnum-1].text.strip()
                else:
                    RSdocumentNum = ConetentSoupP[Pnum - 2].text.strip()
            except:

                RSdocumentNum = ""

            # 被处罚人或机构  #被处罚单位
            try :
                if RSbePunishedFind!=[]:
                    RSbePunished = RSbePunishedFind[0]
                    RSlawEnforcement = RSbePunishedFind[0]
                else:
                    RSbePunished =''
                    RSlawEnforcement =""
            except:

                RSbePunished = ''
                RSlawEnforcement = ""


            # 法人
            try:
                if RSprincipalFind!=[]:
                    RSprincipal = RSprincipalFind[0]
                else:
                    RSprincipal = "无"
            except:

                RSprincipal = ''
            try:
                if ConetentSoupP[-1].text.strip()!="" and len(ConetentSoupP[-1].text.strip())<30 and  ConetentSoupP[-1].text.strip().find("年")!=-1 and ConetentSoupP[-1].text.strip().find("月")!=-1 and ConetentSoupP[-1].text.strip().find("日")!=-1 :
                    RSpunishedDate =ConetentSoupP[-1].text.strip()
                elif ConetentSoupP[-2].text.strip()!="" and len(ConetentSoupP[-2].text.strip())<30 and  ConetentSoupP[-2].text.strip().find("年")!=-1 and ConetentSoupP[-2].text.strip().find("月")!=-1 and ConetentSoupP[-2].text.strip().find("日")!=-1 :
                    RSpunishedDate = ConetentSoupP[-2].text.strip()
                elif ConetentSoupP[-3].text.strip()!="" and len(ConetentSoupP[-3].text.strip())<30 and  ConetentSoupP[-3].text.strip().find("年")!=-1 and ConetentSoupP[-3].text.strip().find("月")!=-1 and ConetentSoupP[-3].text.strip().find("日")!=-1 :
                    RSpunishedDate = ConetentSoupP[-3].text.strip()
                else:
                    RSpunishedDate =" "
            except:
                RSpunishedDate =" "
            if RSRSagencyFind !=[]:
                RSagency = RSRSagencyFind[0]
            else:
                RSagency = " "

            #表中的字段 公共部分插入到数据库
            dataId = RSdataId
            title = RSTitle
            documentNum = RSdocumentNum # 书文号
            bePunished = RSbePunished  # 被处罚人或机构
            principal = RSprincipal  # 法定代表人
            lawEnforcement = RSlawEnforcement  # 被处罚单位
            punishedDate = RSpunishedDate   # 受处罚时间
            content = ConetentResponse  # 全文RScontent
            uniqueSign = ContentSrc  # url地址
            address = '内蒙古自治区'  # 省份  RSagency
            area = " 阿荣旗"  # 地区
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
                sql1 = " INSERT INTO  crawlDataNeiM16(dataId,title,documentNum,bePunished,principal,lawEnforcement,punishedDate,content,uniqueSign,address,area,agency,grade,showId) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " % (dataId, title, documentNum, bePunished,principal,lawEnforcement,punishedDate,content,uniqueSign,address, area, agency,grade,showId)


                print(sql1)
                if adjunct:
                    print("这条数据存在附件，可能会很大，请稍等，已经自动开始下载.....")
                    for xiaZai in adjunct:
                        print(xiaZai)
                        rsDocuniqueSign = xiaZai[0]
                        rsDocName =  RSTitle
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
    url ="http://www.arq.gov.cn/Category_791/Index"
    AdminiStrative =Utils()
    for i in range(1,18):
        AdminiStrative.parsePage(url,str(i))
        time.sleep(2)



























