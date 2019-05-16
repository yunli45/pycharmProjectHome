# -*- coding: UTF-8 -*-
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
        self.showId = 12301635

    def getPage(self,url=None,params=None):
        response = requests.get(url,headers = self.header,params=params)
        response = response.content.decode('UTF-8')
        return response

    def parsePage(self,url=None,pageNo=None,params=None,baseUrl="http://xxgk.tj.spb.gov.cn",path="F:\行政处罚数据\天津\滨海新区\/%s"):
        response = self.getPage(url,params)

        print("+++++++++++++++++++这是第："+pageNo+"页++++++++++++++++")
        print(response)

        timeList = re.findall(re.compile(r'"pub_date":"(.*?)"'), response)
        timeList = re.findall(re.compile(r'"generate_date":"(.*?)"'), response)
        srcList = re.findall(re.compile(r'"yc_id":"(.*?)"'), response)
        doc_numList = re.findall(re.compile(r'"doc_number":"(.*?)"'), response)
        titleList = re.findall(re.compile(r'"info_name":"(.*?)"'), response)


        for src in srcList:
            resTitle = titleList[srcList.index(src)] # 标题
            resTime = timeList[srcList.index(src)] # 时间
            resdocumentNum = doc_numList[srcList.index(src)]  # s书文号

            ContentSrc = "http://xxgk.tj.spb.gov.cn/extranet/detail.html?yc_id="+src
            # print(ContentSrc)
            # print(ContentSrc)
            response2 = requests.get(ContentSrc,headers = self.header)
            response2 = response2.content.decode('UTF-8')
            response2 = str(response2)
            # print(response2)
            # print("发布")
            lawEnforcement = re.findall(re.compile(r'<li class="pull-left">发布机构(.*?)</li>'),str(response2))  # 发布机构
            # print(lawEnforcement)
            soup2 = BeautifulSoup(response2,'lxml')

            rs2 = soup2.find('div',attrs={'class':'content'})
            # print(rs2)
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
            rs3 = re.sub(r'<font.*?>', '', str(rs3)).replace('</font>','')
            # rs3 = re.sub(r'<p.*?class="MsoNormal".*?>', '<p class="MsoNormal">', str(rs3), flags=re.M | re.S)
            rs3 = rs3.replace("'", "''").replace('\u2002', ' ').replace('<b>', '').replace('</b>', '')
            # print(rs3)

            documentNum = resdocumentNum
            lawEnforcement = lawEnforcement[0]
            bePunished = ''  # 被处罚人或机构
            punishedDate=  resTime  # 受处罚时间
            principal = ''  # 法定代表人
            dataId =  src
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
            adjunct = re.findall(re.compile(r'<a.*?href="(.*?)".*?>(.*?)</a>', re.I | re.S), rs3)

            if rs3:
                # conn = pymssql.connect(host='(local)', user='sa', password='123456', database='AdministrativePun')
                # # 打开游标
                # cur = conn.cursor();
                # if not cur:
                #     raise Exception('数据库连接失败！')
                # else:
                #     print("数据库链接成功")
                # sql1 = " INSERT INTO  crawlData6(dataId,title,documentNum,bePunished,principal,lawEnforcement,punishedDate,content,uniqueSign,address,area,agency,grade,showId,showAddress,showArea) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " % (  dataId, resTitle, documentNum, bePunished,principal,lawEnforcement,punishedDate,content,uniqueSign,address, area, agency,grade,showId,showAddress,showArea)
                # sql1 = " INSERT INTO  crawlData5(dataId,title,documentNum,bePunished,uniqueSign,principal,lawEnforcement) values ('%s','%s','%s','%s','%s','%s','%s') " % (  dataId, resTitle, documentNum,bePunished,principal,lawEnforcement,uniqueSign)

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

                # cur.execute(sql1)
                self.OnlyID += 1
                self.showId += 1
            # conn.commit()
            # conn.close()
        print("下一页开始的id是" + str(self.OnlyID))
        print("这一夜爬取成功相关数据和文件，文件保存的目录在" + path)

#######     执行    ########
if __name__ =="__main__":

    url ="http://xxgk.tj.spb.gov.cn/extranet/getContent.jsp"

    AdminiStrative =Utils()
    #cnblog.parsePage(url)
    for i in range(1,31):
        params = {
            'doObj': '{"lx":1,"id":100000,"name":"信息公开目录","pagenum":"%s","host":"xxgk.tj.spb.gov.cn","sousouVal":""}'%(i)
        }

        AdminiStrative.parsePage(url,str(i),params)
        time.sleep(3)



























