import requests
import re
from bs4 import BeautifulSoup
import time
import pymssql

########################################################
#
#              抓取中国司法部--通知类文件--分页自动全部下载
#       唯一注意的是需要手动给出最大的页数
#
#
########################################################

class  Utils(object):
    def __init__(self):
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
        # # # # # # # # # # # # # # # # # # # # # # #
        #  注意：如果是一次性全部抓取，并给出最大的页数hsID 就为1 ，如果分批次抓取就得注意每次ID的变化
        # # # # # # # # # # # # # # # # #
        self.hsID=1

    def getPage(self,url=None):
        response=requests.get(url,headers=self.header)
        response = response.content.decode('UTF-8')
        return response

    """
    注意：baseUrL 和path(附件存储地址)需要提前给出不能为空
    """
    def parsePage(self,url=None,pageNo=None,baseUrL="http://www.moj.gov.cn",path="F:\%s"):
        if pageNo == '1':
            print(10)
            response = self.getPage("http://www.moj.gov.cn/government_public/node_tzwj.html")
        else:
            response=self.getPage(url+pageNo+".html")

        print("+++++++++++++++++++++++++++第", pageNo, "页++++++++++++++++++++++++++++")
        rsTiTSrc = re.findall(re.compile(
            r'<li>.*?<dt>.*?<a href="(.*?)" target="_blank">(.*?)</a>.*?</dt>.*? <dd class="font_gray_12">(.*?)</dd>.*?</li> ',
            re.M | re.S), response)
        srcList = []
        titleList = []
        timeList = []
        for i in rsTiTSrc:
            srcList.append(i[0])
            titleList.append(i[1])
            timeList.append(i[2].replace('\n', '').replace(' ', '').replace('\r', ''))
        # print(srcList)
        for src in srcList:
            # print(type(baseUrL))
            rsTime1 = timeList[srcList.index(src)]
            dataId = src
            title = titleList[srcList.index(src)]
            if src.find("http") == -1:
                ContentSrc = baseUrL + src
            else:
                ContentSrc = src
            text2 = requests.get(ContentSrc, headers=self.header)
            text2 = text2.content.decode('UTF-8')
            soup = BeautifulSoup(text2, 'lxml')
            content = soup.find('div', id="content")
            content = str(content).replace("\r", '<br>').replace("'", "''").replace('\u2002', ' ')
            bookcont = soup.find('div', id="content")
            bookcont = str(bookcont)
            rsDoc = re.findall(re.compile(r'<a.*?href="(.*?)".*?>(.*?)</a>', re.I | re.S), bookcont)
            # rsDoc = re.findall(re.compile('<a title="(.*?).*?href="(.*?)".*?>.*?</a>',re.I|re.S),content1)

            # print(hsID)
            # print(rsDoc)
            # print("这条数据有"+str(len(rsDoc))+"个附件")
            if content:
                conn = pymssql.connect(host='(local)', user='sa', password='123456', database='faqi')
                # 打开游标
                cur = conn.cursor();
                if not cur:
                    raise Exception('数据库连接失败！')
                else:
                    print("数据库链接成功")
                sql1 = "INSERT INTO  ZGSFBTongZhiLeiWenJian1(ID,title,content,uniqueSign,address,punisheDate,dataId) values ('%s','%s','%s','%s','%s','%s','%s')" % (
                self.hsID, title, content, ContentSrc, '深圳', rsTime1, dataId)

                # print(sql1)
                if rsDoc:
                    print("这条数据存在附件，可能会很大，请稍等，已经自动开始下载.....")
                    for xiaZai in rsDoc:
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
                                rsDocuniqueSign = "%s" % (baseUrL) + rsDocuniqueSign
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
                                rsDocuniqueSign = baseUrL + rsDocuniqueSign
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
                                rsDocuniqueSign = baseUrL + rsDocuniqueSign
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
                                rsDocuniqueSign = baseUrL + rsDocuniqueSign
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
                                rsDocuniqueSign = baseUrL + rsDocuniqueSign
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
                                rsDocuniqueSign = "%s" % (baseUrL) + rsDocuniqueSign
                            else:
                                rsDocuniqueSign = rsDocuniqueSign
                            # print(rsDocuniqueSign)
                            r = requests.get(rsDocuniqueSign, headers=self.header, timeout=300)
                            with open(path1, "wb") as f:
                                f.write(r.content)
                            f.close()
                cur.execute(sql1)
                self.hsID += 1
            conn.commit()
            conn.close()
            print("下一页开始的id是" + str(self.hsID))
            print("这一夜爬取成功相关数据和文件，文件保存的目录在" + path)

#######     执行    ########
if __name__ =="__main__":

    url = "http://www.moj.gov.cn/government_public/node_tzwj_"
    cnblog=Utils()
    #cnblog.parsePage(url)
    for i in range(0,4):
        cnblog.parsePage(url,str(i+1))
        time.sleep(3)
