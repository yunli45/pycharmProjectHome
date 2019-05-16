import re
import requests
from bs4 import BeautifulSoup
import time
import pymssql
import datetime

#  该网址只需要抓取政策法规就好了 http://www.zhb.gov.cn/gzfw_13107/zcfg/zcfgjd/

class Utils(object):
    def __init__(self):
        self.header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
        self.OnlyID = 82
        self.showId =  12355208
        # 第96页跑完 ：12353000 - 12355207，从第97页开始：12355208


    def getPage(self,url=None):
        response = requests.get(url, headers=self.header)
        response = response.content.decode('utf-8')
        return response
    def parsePage(self,url,pageNo,baseUrl1,baseUrl2,Savepath):

        if pageNo =="1":
            response = self.getPage(url)
        else:
            response = self.getPage(url+"index_"+str(int(pageNo)-1)+".shtml")
        print("+++++++++++++++++++这是第：" + pageNo + "页++++++++++++++++")

        if int(pageNo)<6:
            baseUrl = baseUrl1
        else:
            baseUrl = baseUrl2

        homePageSoup = BeautifulSoup(response, 'lxml')
        homePageSoup = homePageSoup.findAll('div', attrs={'class': 'main_rt_list'})
        # print(homePageSoup)
        srcListFind = re.findall(re.compile(r'<span>(.*?)</span><a href="(.*?)".*?title="(.*?)">.*?</a>', re.S),
                                 str(homePageSoup))
        # print("这是mmp")
        print(srcListFind)
        titleList = []
        timeList = []
        srcList = []
        for i in srcListFind:
            srcList.append(i[1])
            titleList.append(i[2])
            timeList.append(i[0])
        for src in srcList:

            print("这是第"+str(self.OnlyID )+"条数据")
            # print(src)
            srcIndex = srcList.index(src)
            if src.find("http") != -1:
                ContentSrc = src
            else:
                src =   src.replace("../../../",'').replace("../../",'').replace("../",'').replace("./",'')
                # print(src)
                ContentSrc = baseUrl + src
                print(ContentSrc)

                ConetentResponse = requests.get(ContentSrc, headers=self.header)
                ConetentResponse = ConetentResponse.content.decode('UTF-8')
                ConetentResponseSoup = BeautifulSoup(ConetentResponse, 'lxml')
                ConetentResponseSoupOld1 = ConetentResponseSoup.find('div', attrs={'id': 'ContentRegion'})
                ConetentResponseSoupOld2 = ConetentResponseSoup.find('div', attrs={'class': 'TRS_Editor'})
                ConetentResponseSoupOld3 = ConetentResponseSoup.find('div', attrs={'class': 'wzxq_neirong2'})

                if ConetentResponseSoupOld1:
                    print("第一种")
                    ConetentResponseSoupOld =ConetentResponseSoupOld1
                elif ConetentResponseSoupOld2:
                    print("第二张")
                    ConetentResponseSoupOld =ConetentResponseSoupOld2
                elif ConetentResponseSoupOld3:
                    print("第三中")
                    ConetentResponseSoupOld = ConetentResponseSoupOld3

                # 去除分享链接
                ConetentResponseSoupOld = str(ConetentResponseSoupOld)
                ConetentResponseSoupOld = ConetentResponseSoupOld[0:ConetentResponseSoupOld.find('<span class="wzxq2_lianjie">【字体')]

                ConetentResponseSoupOld = re.sub("<u.*?>", '', str(ConetentResponseSoupOld), flags=re.S | re.M).replace(
                    "</u>", '')
                ConetentResponseSoupOld = re.sub("<b.*?>", '', ConetentResponseSoupOld, flags=re.S | re.M).replace(
                    "</b>", '')
                # ConetentResponseSoupOld = re.sub('<a.*?">', '',ConetentResponseSoupOld).replace("</a>", '')

                ConetentResponseSoupOld = re.sub('<span.*?>', '', ConetentResponseSoupOld, flags=re.S | re.M).replace(
                    '</span>', '')
                ConetentResponseSoupOld = re.sub("<div.*?>",'',ConetentResponseSoupOld).replace("</div>",'')
                ConetentResponseSoupOld = re.sub(r'\xa0', '', ConetentResponseSoupOld)
                ConetentResponseSoupOld = str(ConetentResponseSoupOld).replace(r"2312'>", '').replace("</ul>",'')

                # 去除下部的分享链接
                tableStratIndx = ConetentResponseSoupOld.find("<table")
                tableEndIndx = ConetentResponseSoupOld.find("</table>")+8
                # table =ConetentResponseSoupOld[tableStratIndx:tableEndIndx]
                ConetentResponseSoupOld = ConetentResponseSoupOld[0:tableStratIndx]

                # 附件下载
                adjunct = re.findall(re.compile(r'<a.*?href="(.*?)".*?>(.*?)</a>', re.I | re.S), ConetentResponseSoupOld)

                # print(ConetentResponseSoupOld)
                RSid =self.OnlyID
                RStitle = titleList[srcIndex] # 标题
                RStime = timeList[srcIndex]  # 时间
                RSsourceUrl = ContentSrc  # 来源的url地址
                RSsourceId = re.sub(r'.*?/', '', src).replace('.html', '')  # 来源网址中的唯一id
                RSsourcePage = "来自于"+str(pageNo)+"页的"+str(srcIndex) +"条" # 来源地址中属于那一页那一条
                now_time = datetime.datetime.now()
                RSinsertTime = str(now_time)  # 插入这条数据的时间

                RScontent =ConetentResponseSoupOld  # 全文内容
                if RScontent ==None:
                    RScontent ="全文可能是附件的形式"
                else:
                    RScontent=RScontent

                RSsourceModel = "来源于政策法规下面的政策法规解读模块"  # 来源网址的那个模块

                if RScontent:
                    conn = pymssql.connect(host='(local)', user='sa', password='123456', database='9.1EnvironmentData')
                    # 打开游标
                    cur = conn.cursor();
                    if not cur:
                        raise Exception('数据库连接失败！')
                    else:
                        print("数据库链接成功")
                    sql1 = " INSERT INTO  policiesAndFegulations(id,title,time,sourceUrl,sourceId,sourcePage,insertTime,content,sourceModel) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s') " % (RSid,RStitle,RStime,RSsourceUrl,RSsourceId,RSsourcePage,RSinsertTime,RScontent,RSsourceModel)
                    print(sql1)
                    if adjunct:
                        print("这条数据存在附件，可能会很大，请稍等，已经自动开始下载.....")
                        for xiaZai in adjunct:
                            print(xiaZai)

                            rsDocuniqueSign = xiaZai[0]
                            if rsDocuniqueSign .find("http")!=-1:
                                rsDocuniqueSign  =rsDocuniqueSign
                            else:

                                rsDocuniqueSign =rsDocuniqueSign.replace("./",'')
                                rsDocuniqueSign =   ContentSrc[0:ContentSrc.rfind("/")+1]+rsDocuniqueSign
                            print("附件下载地址"+rsDocuniqueSign)

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

                                Savepath1 = Savepath % (rsDocName)

                                if rsDocuniqueSign.find("http") == -1:
                                    rsDocuniqueSign = "%s" % (baseUrl) + rsDocuniqueSign
                                else:
                                    rsDocuniqueSign = rsDocuniqueSign
                                # print(rsDocuniqueSign)
                                r = requests.get(rsDocuniqueSign, headers=self.header, timeout=30)
                                with open(Savepath1, "wb") as f:
                                    f.write(r.content)
                                f.close()
                            elif rsPdF:
                                rsDocName = rsDocName + ".PDF"
                                rsDocName = rsDocName.replace("/", '_')
                                Savepath1 = Savepath % (rsDocName)

                                if rsDocuniqueSign.find("http") == -1:
                                    rsDocuniqueSign = baseUrl + rsDocuniqueSign
                                else:
                                    rsDocuniqueSign = rsDocuniqueSign
                                # print(rsDocuniqueSign)
                                r = requests.get(rsDocuniqueSign, headers=self.header)
                                with open(Savepath1, "wb") as f:
                                    f.write(r.content)
                                f.close()
                            elif rsXlsx:
                                rsDocName = rsDocName + ".xlsx"
                                rsDocName = rsDocName.replace("/", '_')
                                Savepath1 = Savepath % (rsDocName)

                                if rsDocuniqueSign.find("http") == -1:
                                    rsDocuniqueSign = baseUrl + rsDocuniqueSign
                                else:
                                    rsDocuniqueSign = rsDocuniqueSign

                                # print(rsDocuniqueSign)
                                r = requests.get(rsDocuniqueSign, headers=self.header)
                                with open(Savepath1, "wb") as f:
                                    f.write(r.content)
                                f.close()
                            elif rsZip:
                                rsDocName = rsDocName + ".zip"
                                rsDocName = rsDocName.replace("/", '_')
                                Savepath1 = Savepath % (rsDocName)

                                if rsDocuniqueSign.find("http") == -1:
                                    rsDocuniqueSign = baseUrl + rsDocuniqueSign
                                else:
                                    rsDocuniqueSign = rsDocuniqueSign

                                # print(rsDocuniqueSign)
                                r = requests.get(rsDocuniqueSign, headers=self.header)
                                with open(Savepath1, "wb") as f:
                                    f.write(r.content)
                                f.close()
                            elif rsRar:
                                rsDocName = rsDocName + ".rar"
                                rsDocName = rsDocName.replace("/", '_')
                                Savepath1 = Savepath % (rsDocName)

                                if rsDocuniqueSign.find("http") == -1:
                                    rsDocuniqueSign = baseUrl + rsDocuniqueSign
                                else:
                                    rsDocuniqueSign = rsDocuniqueSign

                                # print(rsDocuniqueSign)
                                r = requests.get(rsDocuniqueSign, headers=self.header)
                                with open(Savepath1, "wb") as f:
                                    f.write(r.content)
                                f.close()
                            elif reJpg:
                                rsDocName = rsDocName + ".jpg"
                                rsDocName = rsDocName.replace("/", '_')
                                Savepath1 = Savepath % (rsDocName)

                                if rsDocuniqueSign.find("http") == -1:
                                    rsDocuniqueSign = "%s" % (baseUrl) + rsDocuniqueSign
                                else:
                                    rsDocuniqueSign = rsDocuniqueSign
                                # print(rsDocuniqueSign)
                                r = requests.get(rsDocuniqueSign, headers=self.header, timeout=30)
                                with open(Savepath1, "wb") as f:
                                    f.write(r.content)
                                f.close()
                cur.execute(sql1)
                self.OnlyID += 1
                self.showId += 1
            conn.commit()
            conn.close()
        print("下一页开始的id是" + str(self.OnlyID))









#######     执行    ########
if __name__ =="__main__":
    # 共计353页
    url ="http://www.mee.gov.cn/gzfw_13107/zcfg/zcfgjd/"
    baseUrl1 ="http://www.mee.gov.cn/"
    baseUrl2 ="http://www.mee.gov.cn/gzfw_13107/zcfg/zcfgjd/"
    Savepath ="F:\9.1环境生态部\%s"

    AdminiStrative =Utils()
    for i in range(6,9):
        AdminiStrative.parsePage(url,str(i),baseUrl1,baseUrl2,Savepath)
        time.sleep(2)











