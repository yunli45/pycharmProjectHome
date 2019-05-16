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
    def parsePage(self,url=None,pageNo=None,baseUrl="http://www.cbrc.gov.cn",path="F:\行政处罚数据\天津\滨海新区\/%s"):

        if pageNo=='1':
            response = self.getPage("http://www.cbrc.gov.cn/zhuanti/xzcf/get2and3LevelXZCFDocListDividePage/tianjin/2.html")
        else:
            response = self.getPage(url+pageNo+'')
        print("+++++++++++++++++++这是第："+pageNo+"页++++++++++++++++")

        soup = BeautifulSoup(response, 'lxml')
        soup = soup.find_all('div', attrs={'class': "xia3"})
        rs = re.findall(re.compile(r'<a .*? href="(.*?)" target="_blank" title="(.*?)">'), str(soup))
        rsTime = re.findall(re.compile(r'<td style="width: 70px; color: #c5c5c5;">(.*?)</td>'), str(soup))
        srcList= []
        titleList = []
        # print(len(rs))
        # print(rs)
        for i in rs :
            srcList.append(i[0])
            titleList.append(i[1])

        for src in srcList:
            resTitle = titleList[srcList.index(src)]
            # resTime = rsTime[srcList.index(src)]

            if src.find("http") == -1:
                ContentSrc = baseUrl + src
            else:
                ContentSrc = src

            response2 = requests.get(ContentSrc,headers =self.header)
            response2 = response2.content.decode('UTF-8')
            soup2 = BeautifulSoup(response2,'lxml')
            rs2 = soup2.find('div',attrs={'class':'Section1'})

            #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
            #
            # 提取文书号等信息
            #
            #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #

            rs2 = str(rs2)
            rs3 = re.sub(r'<span.*?>', '', rs2, flags=re.S).replace('</span>', '').replace('<p class="MsoNormal"><o:p>\xa0</o:p></p>', '').replace('<o:p></o:p>', '')
            rs3 = re.sub(r'<p.*?class="MsoNormal".*?><o:p>\xa0</o:p></p>','',rs3, flags=re.S)
            rs3 = re.sub(r'<st1:chsdate.*?>','',rs3,flags=re.S).replace('</st1:chsdate>','')
            rs3 = rs3.replace("'", "''").replace('\u2002', ' ').replace('<b>','').replace('</b>','')

            MsoNormal = re.findall(re.compile(r'<p.*?class="MsoNormal".*?>(.*?)</p>', re.S), rs3)

            print(MsoNormal)
            id = self.OnlyID
            dataId = re.sub(r'.*/','',src).replace(".html",'')
            documentNum = MsoNormal[2]  # 书文号
            bePunished  = MsoNormal[5] # 被处罚人或机构
            principal = MsoNormal[10] # 法定代表人
            lawEnforcement= MsoNormal[8]  # 被处罚机构或单位
            punishedDate = MsoNormal[20] # 受处罚时间
            content = MsoNormal[11]+":"+MsoNormal[12]+"。"+MsoNormal[13]+":"+MsoNormal[14]+"。"+MsoNormal[15]+":"+MsoNormal[16]
            uniqueSign = ContentSrc # url地址
            address =  '天津'# 省份
            area  =  '滨海新区'# 地区
            agency = MsoNormal[18]  # 处罚机构
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

            if  MsoNormal:
                conn = pymssql.connect(host='(local)', user='sa', password='123456', database='AdministrativePun')
                # 打开游标
                cur = conn.cursor();
                if not cur:
                    raise Exception('数据库连接失败！')
                else:
                    print("数据库链接成功")
                sql1 = " INSERT INTO  crawlData3(dataId,title,documentNum,bePunished,principal,lawEnforcement,punishedDate,content,uniqueSign,address,area,agency,grade,showId,showAddress,showArea) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " % (  dataId, resTitle, documentNum, bePunished,principal,lawEnforcement,punishedDate,content,uniqueSign,address, area, agency,grade,showId,showAddress,showArea)


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
            #
            cur.execute(sql1)
            self.OnlyID += 1
            self.showId += 1
            conn.commit()
            conn.close()
            print("下一页开始的id是" + str(self.OnlyID))
            print("这一夜爬取成功相关数据和文件，文件保存的目录在" + path)

#######     执行    ########
if __name__ =="__main__":

    url = " "
    AdminiStrative =Utils()
    #cnblog.parsePage(url)
    for i in range(0,1):
        AdminiStrative.parsePage(url,str(i+1))
        time.sleep(3)



























