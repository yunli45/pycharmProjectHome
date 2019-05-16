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
        self.showId = 12300230

    def getPage(self,url=None):
        response = requests.get(url,headers = self.header)
        response = response.content.decode('UTF-8')
        return response

    def parsePage(self,url=None,pageNo=None,baseUrl="http://www.cbrc.gov.cn",path="F:\行政处罚数据\天津\滨海新区\/%s"):

        if pageNo=='1':
            response = self.getPage("http://www.cbrc.gov.cn/chinese/home/docViewPage/60240405&current=1")
        else:
            response = self.getPage(url+pageNo)
        print("+++++++++++++++++++这是第："+pageNo+"页++++++++++++++++")

        # print(response)

        soup = BeautifulSoup(response, 'lxml')
        soup = soup.find_all('div', attrs={'class': "xia3"})
        rsList = re.findall(re.compile(r'<a .*? href="(.*?)" target="_blank" title="(.*?)">.*?</td>.*?<td.*?>.*?(.*?)</td>',re.S|re.M),str(soup))
        srcList= []
        titleList = []
        timeList = []
        # print(len(rs))
        # print(rs)
        for i in rsList :
            srcList.append(i[0])
            titleList.append(i[1])
            timeList.append(i[2].replace('\r','').replace('\n','').replace('\t',''))
        for src in srcList:
            resTitle = titleList[srcList.index(src)]
            resTime = timeList[srcList.index(src)]

            if src.find("http") == -1:
                ContentSrc = baseUrl + src
            else:
                ContentSrc = src
            # print(ContentSrc)
            response2 = requests.get(ContentSrc,headers = self.header)
            response2 = response2.content.decode('UTF-8')
            soup2 = BeautifulSoup(response2,'lxml')
            rs2 = soup2.find('div',attrs={'class':'Section1'})
            print(rs2)
            rs2 = str(rs2)
            #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
            #
            # 提取文书号等信息
            #
            #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #

            rs3 = re.sub(r'<tr.*?>', '', str(rs2), flags=re.M | re.S).replace('</tr>', '')
            rs3 = re.sub(r'<td.*?>', '', str(rs3), flags=re.M | re.S).replace('</td>', '')
            rs3 = re.sub(r'<span.*?>', '', str(rs3), flags=re.M | re.S).replace('</span>', '')
            rs3 = re.sub(r'<table.*?>', '', str(rs3), flags=re.M | re.S).replace('</table>', '')
            rs3 = re.sub(r'<p.*?><o:p> </o:p></p>', '', str(rs3)).replace('<o:p></o:p>', '')
            rs3 = re.sub(r'<b .*?><o:p> </o:p></b>', '', str(rs3))
            rs3 = re.sub(r'<st1:.*?>', '', str(rs3)).replace('</st1:chsdate>', '').replace('<a name="TCSignYear"></a>','')
            rs3 = re.sub(r'<o:p>\xa0</o:p>', '', str(rs3))
            rs3 = re.sub(r'<p.*?class="MsoNormal".*?>', '<p class="MsoNormal">', str(rs3), flags=re.M | re.S)
            rs3 = rs3.replace("'", "''").replace('\u2002', ' ').replace('<b>', '').replace('</b>', '')
            print(rs3)

            MsoNormal = re.findall(re.compile(r'<p.*?class="MsoNormal".*?>(.*?)</p>', re.S), rs3)
            MsoNormal1=MsoNormal
            # 是一张表的形式
            if rs2.find("<table")!=-1:
                print("这是表格形式")
                if len(MsoNormal)<=21:
                    print("mmp1")
                    print(MsoNormal)
                    # 1 个人姓名  单\xa0 位名称  法定代表人（主要负责人）姓名  全部不在
                    if MsoNormal[6].find('单')!=-1 and MsoNormal[7].find("名称")!=-1 and MsoNormal[8].find("法定代表人")!=-1:
                        MsoNormal = MsoNormal1[0:6]+["无"]+[MsoNormal1[6]]+[MsoNormal1[7]]+["无"]+[MsoNormal1[8]]+["无"]+MsoNormal1[9:]

                    #  5 法定代表人（主要负责人）姓名  单\xa0 位  存在，  个人姓名 不在
                    elif MsoNormal[6].find("单") !=-1  and MsoNormal[9].find('法定代表人')!=-1 and MsoNormal[11].find("主要违法违规事实")!=-1:
                        print("mmp")
                        MsoNormal = MsoNormal1[0:6] + ["无"] + MsoNormal1[6:]

                    # 2 个人姓名 存在， 单\xa0 位名称  法定代表人（主要负责人） 全部不在
                    elif MsoNormal[9].find("法定代表人")!=- 1  and MsoNormal[10].find("主要违法违规事实")!=- 1:
                        MsoNormal = MsoNormal1[0:9]+['无']+[MsoNormal1[9]]+["无"]+MsoNormal1[10:]

                    # 3 个人姓名  单\xa0 位名称 存在，  法定代表人（主要负责人）姓名 不在
                    elif MsoNormal[11].find("主要违法违规事实")!=-1:
                        MsoNormal = MsoNormal1[0:11]+["无"]+MsoNormal1[11:]

                    # 4 个人姓名  法定代表人（主要负责人）姓名 存在，单\xa0 位名称 不在
                    elif MsoNormal[9].find("法定代表人")!=-1:
                        MsoNormal = MsoNormal1[0:9]+["无"]+MsoNormal1[9:]

                        # 最后的时间标签改变
                    elif len(MsoNormal)==21 and MsoNormal[20].find("作出处罚决定的日期")!=-1:
                        rsTimeP = re.findall(re.compile(r'<p class="CharChar".*?>(.*?)</p>',re.S|re.M),rs3)
                        MsoNormal = MsoNormal1[0:]+[rsTimeP[0]]
                    print(MsoNormal[5])
                    print(MsoNormal[10])
                    print(len(MsoNormal))
                    print(MsoNormal)
                else:
                    MsoNormal = MsoNormal
                    print(len(MsoNormal))
                print(MsoNormal)
                dataId = re.sub(r'.*/', '', src).replace(".html", '')
                documentNum = MsoNormal[3]  # 书文号
                bePunished = MsoNormal[6]  # 被处罚人或机构
                principal = MsoNormal[11]  # 法定代表人
                lawEnforcement = MsoNormal[9]  # 被处罚机构或单位
                if len(MsoNormal)<=21:
                    rsTmiePP = re.findall(re.compile(r'<p.*?>.*?(.*?年.*?月.*?日)</p>', re.S), rs3)
                    if rsTmiePP:
                        punishedDate = rsTmiePP[-1]  # 受处罚时间
                    else:
                        punishedDate = resTime
                else:
                    punishedDate = MsoNormal[21]
                content = MsoNormal[12] + ":" + MsoNormal[13] + "。" + MsoNormal[14] + ":" + MsoNormal[15] + "。" + \
                          MsoNormal[16] + ":" + MsoNormal[17]
                uniqueSign = ContentSrc  # url地址
                address = '天津'  # 省份
                area = '所有区县'  # 地区
                agency = MsoNormal[19]  # 处罚机构
                if len(content) <= 100:
                    grade = -1  # 级别
                elif 100 < len(content) <= 200:
                    grade = 1  # 级别
                elif 200 < len(content) <= 1500:
                    grade = 2  # 级别
                elif len(content) > 1500:
                    grade = 0  # 级别
                showId = self.showId  # 系统ID
                showAddress = None
                showArea = None

            else:
                RSdocumentNum = re.findall(re.compile(r'>(.*?津银.*?号).*?</p>'), rs3)  # 书文号
                RSlawEnforcement = re.findall(re.compile(r'机构名称(.*?)</p>', re.S), rs3)  # 被处罚机构或单位
                RSlawEnforcement1 = re.findall(re.compile(r'单位名称(.*?)</p>', re.S), rs3)  # 被处罚机构或单位
                RSpunishedDate = re.findall(re.compile(r'<p.*?>(.*?年.*?月.*?日)</p>'), rs3)
                if  RSdocumentNum:
                    documentNum = RSdocumentNum[0]
                else:
                    documentNum = ''
                if RSlawEnforcement:
                    lawEnforcement = RSlawEnforcement[0]
                elif RSlawEnforcement1:
                    lawEnforcement = RSlawEnforcement1[0]
                else:
                    lawEnforcement = ''
                if RSpunishedDate:
                    punishedDate = RSpunishedDate[-1]
                else:
                    punishedDate = resTime

                bePunished = ''  # 被处罚人或机构
                punishedDate= punishedDate   # 受处罚时间
                principal = ''  # 法定代表人
                dataId = re.sub(r'.*/', '', src).replace(".html", '')
                content = rs3
                uniqueSign = ContentSrc  # url地址
                address = '天津'  # 省份
                area = '所有区县'  # 地区
                agency = "中国银行业监督管理委员会天津监管局" # 处罚机构
                if len(content) <= 100:
                    grade = -1  # 级别
                elif 100 < len(content) <= 200:
                    grade = 1  # 级别
                elif 200 < len(content) <= 1500:
                    grade = 2  # 级别
                elif len(content) > 1500:
                    grade = 0  # 级别
                showId = self.showId  # 系统ID
                showAddress = None
                showArea = None


            #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
            #
            # 附件下载
            #
            #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
            adjunct = re.findall(re.compile(r'<a.*?href="(.*?)".*?>(.*?)</a>', re.I | re.S), rs2)

            if  MsoNormal:
                conn = pymssql.connect(host='(local)', user='sa', password='123456', database='AdministrativePun')
                # 打开游标
                cur = conn.cursor();
                if not cur:
                    raise Exception('数据库连接失败！')
                else:
                    print("数据库链接成功")
                sql1 = " INSERT INTO  crawlData2(dataId,title,documentNum,bePunished,principal,lawEnforcement,punishedDate,content,uniqueSign,address,area,agency,grade,showId,showAddress,showArea) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " % (  dataId, resTitle, documentNum, bePunished,principal,lawEnforcement,punishedDate,content,uniqueSign,address, area, agency,grade,showId,showAddress,showArea)


                print(sql1)
                if adjunct:
                    print("这条数据存在附件，可能会很大，请稍等，已经自动开始下载.....")
                    for xiaZai in adjunct:
                        rsDocuniqueSign = xiaZai[0]
                        rsDocName = xiaZai[1]
                        xiaZai = str(xiaZai)
                        rsDoc1 = re.findall(re.compile(r'.*?.doc', re.I), xiaZai)
                        rsPdF = re.findall(re.compile(r'.*?.pdf', re.I), xiaZai)
                        rsXlsx = re.findall(re.compile(r'.*?.xlsx|xls', re.I), xiaZai)
                        rsZip = re.findall(re.compile(r'.*?.zip', re.I), xiaZai)
                        rsRar = re.findall(re.compile(r'.*?.rar', re.I), xiaZai)
                        reJpg = re.findall(re.compile(r'.*?.jpg', re.I), xiaZai)
                        if rsDoc1:
                            rsDocName = rsDocName + ".doc"
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

    url ="http://www.cbrc.gov.cn/chinese/home/docViewPage/60240405&current="
    AdminiStrative =Utils()
    #cnblog.parsePage(url)
    for i in range(0,8):
        AdminiStrative.parsePage(url,str(i+1))
        time.sleep(3)



























