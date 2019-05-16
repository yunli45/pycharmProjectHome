import requests
import re
import time
from bs4 import BeautifulSoup
import pymssql

# # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#    抓取天津市滨海新区 —银监分局数据
#
# # # # # # # # # # # # # # # # # # # # # # # # # # #


class Utils(object):
    def __init__(self):
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
        self.OnlyID = 1
        self.showId = 12300000
    def getPage(self,url=None):
        response = requests.get(url,headers = self.header)
        response = response.content.decode('UTF-8')
        return response
    def parsePage(self,url=None,pageNo=None,baseUrl="http://ningxia.circ.gov.cn",path="F:\行政处罚数据\天津\/%s"):

        if pageNo=='1':
            response = self.getPage("http://ningxia.circ.gov.cn/web/site35/tab3385/module8892/page1.htm")
        else:
            response = self.getPage(url+pageNo+'.htm')
        print("+++++++++++++++++++这是第："+pageNo+"页++++++++++++++++")

        soup = BeautifulSoup(response, 'lxml')
        soup = soup.find_all('div', attrs={'id': "ess_ctr8892_contentpane"})
        # print(soup)
        rs = re.findall(re.compile(r'<a.*?href="(.*?)".*?title="(.*?)">'), str(soup))
        RsdataID = re.findall(re.compile(r'<a.*?href=".*?" id="(.*?)".*?>'), str(soup))
        rsTimeList = re.findall(re.compile(r'<td style="width: 70px; color: #c5c5c5;">(.*?)</td>'), str(soup))
        # print(rs)
        # print(rsTimeList)
        # print(RsdataID)
        srcList= []
        titleList = []
        # print(len(rs))
        # print(rs)
        for i in rs :
            srcList.append(i[0])
            titleList.append(i[1])

        for src in srcList:
            resTitle =titleList[srcList.index(src)]
            resTime ='20'+ rsTimeList[srcList.index(src)].replace('(','').replace(')','')
            dataId = RsdataID[srcList.index(src)]

            if src.find("http") == -1:
                ContentSrc = baseUrl + src
            else:
                ContentSrc = src

            response2 = requests.get(ContentSrc,headers =self.header)
            response2 = response2.content.decode('UTF-8')
            soup2 = BeautifulSoup(response2,'lxml')
            rs2 = soup2.find('span',attrs={'id':'zoom'})

            #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
            #
            # 提取文书号等信息
            #
            #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #

            rs2 = str(rs2).replace('\xa0','').replace('\u3000','').replace("'","''")
            rs2 = re.sub('<span.*?>','',rs2).replace('</span>','')
            # print(rs2)
            id = self.OnlyID

            dataId = dataId
            documentNum = re.sub(r'.*?处罚决定书','',resTitle).replace("(",'') .replace(")",'')     # 书文号
            # print(rs2)
            RsbePunished =re.findall(re.compile(r'当事人.*?</p>',re.M|re.S), rs2)

            if  RsbePunished:
                bePunished  =  RsbePunished[0].replace("\n",'').replace("</p>",'')  # 被处罚人或机构   # 被处罚机构或单位
            else:
                bePunished = ''
            print(bePunished)
            Rsprincipal =  re.findall(re.compile(r'法定代表人.*?</p>',re.M|re.S),rs2)
            Rsprincipa2 = re.findall(re.compile(r'主要负责人.*?</p>',re.M|re.S), rs2)  # 法定代表人 # 法定代表人
            if Rsprincipal:
                principal = Rsprincipal[0].replace("\n",'').replace("</p>",'') # 法定代表人
            elif Rsprincipa2:
                principal = Rsprincipa2[0].replace("\n",'').replace("</p>",'')
            else:
                principal=''

            RslawEnforcement= re.findall(re.compile(r'当事人.*?：(.*?)</p>',re.M|re.S),rs2)  # 被处罚机构或单位
            if RslawEnforcement:
                lawEnforcement= RslawEnforcement[0].replace("\n",'').replace("</p>",'')
            else:
                lawEnforcement=''
            print(lawEnforcement)

            RspunishedDate = re.findall(re.compile(r'<p.*?>.*?(.*?年.*?月.*?日.*?).*?</p>'), rs2)  # s时间
            if RspunishedDate and len(RspunishedDate[-1])<= 30:
                punishedDate = RspunishedDate[-1]   # 受处罚时间
            else:
                punishedDate = resTime
            print(punishedDate)
            content = rs2
            uniqueSign = ContentSrc # url地址
            address =  '天津'# 省份
            area  =  '所有区县'# 地区
            agency = '中国保监会天津监管局'  # 处罚机构

            if len(content) <= 100:
                grade = -1 # 级别
            elif 100 < len(content)<= 200:
                grade = 1  # 级别
            elif 200< len(content)<= 1500:
                grade = 2  # 级别
            elif len(content)>1500:
                grade = 0  # 级别
            showId = self.showId # 系统ID
            showAddress = None
            showArea = None

            #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
            #
            # 附件下载
            #
            #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
            adjunct = re.findall(re.compile(r'<a.*?href="(.*?)".*?>(.*?)</a>', re.I | re.S), rs2)

            if  rs2:
                conn = pymssql.connect(host='(local)', user='sa', password='123456', database='AdministrativePun')
                # 打开游标
                cur = conn.cursor();
                if not cur:
                    raise Exception('数据库连接失败！')
                else:
                    print("数据库链接成功")
                sql1 = " INSERT INTO  TJbhxqCBRC(dataId,title,documentNum,bePunished,principal,lawEnforcement,punishedDate,content,uniqueSign,address,area,agency,grade,showId,showAddress,showArea) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " % (dataId, resTitle, documentNum, bePunished,principal,lawEnforcement,punishedDate,content,uniqueSign,address, area, agency,grade,showId,showAddress,showArea)


                # print(sql1)
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

    url = "http://ningxia.circ.gov.cn/web/site35/tab3385/module8892/page"
    AdminiStrative =Utils()
    # parsePage(url)
    for i in range(0,12):
        AdminiStrative.parsePage(url,str(i+1))
        time.sleep(3)



























