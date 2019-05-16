import re
import requests
from bs4 import BeautifulSoup
import time
import pymssql
import datetime

class Utils(object):
    def __init__(self):
        self.header = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
        self.OnlyID = 1

    def getPage(self, url=None):
        response = requests.get(url, headers=self.header)
        response = response.content.decode('utf-8')
        return response

    def parsePage(self,url,pageNo,baseUrl,baseUrl2,Savepath):

        if pageNo =="1":
            response = self.getPage(url+".shtml")
        else:
            response = self.getPage(url+str(int(pageNo)-1)+".shtml")
        print("+++++++++++++++++++这是第：" + pageNo + "页++++++++++++++++")

        homePageSoup = BeautifulSoup(response, 'lxml')
        homePageSoup = homePageSoup.findAll('div', attrs={'class': 'main_rt_list'})
        # print(homePageSoup)
        srcListFind = re.findall(re.compile(r'<span>(.*?)</span><a href="(.*?)".*?title="(.*?)">.*?</a>', re.S),
                                 str(homePageSoup))
        print(srcListFind)
        titleList = []
        timeList = []
        srcList = []
        for i in srcListFind:
            srcList.append(i[1])
            titleList.append(i[2])
            timeList.append(i[0])
        for src in srcList:

            print("这是第" + str(self.OnlyID) + "条数据")

            # print(src)
            srcIndex = srcList.index(src)
            print("+++++++++++++++++++这是第：" + pageNo + "页的" +str(srcIndex)+"条数据")
            if src.find("http") != -1:
                ContentSrc = src
            else:
                src = src.replace("../../../", '').replace("../../", '').replace("../", '').replace("./", '')
                ContentSrc = baseUrl + src
                print(ContentSrc)



            ConetentResponse =  self.getPage(ContentSrc)
            ConetentResponseSoup = BeautifulSoup(ConetentResponse, 'lxml')
            ConetentResponseSoupOld = ConetentResponseSoup.find('div', attrs={'id': 'ContentRegion'})

            if ConetentResponseSoupOld!=None:
               print("这div存在数据")
            else:
                NoFile = "这个div没有获取到数据"
                print("这个div没有获取到数据")
                with open("F:\记录数据.txt","wb") as  f:
                    f.write(NoFile)
                f.close()
if __name__ =="__main__":
    # 共计353页这是第
    url ="http://kjs.mee.gov.cn/hjbhbz/bzfb/index"
    baseUrl ="http://www.mee.gov.cn/"
    baseUrl2 =" "
    Savepath =" "

    AdminiStrative =Utils()
    for i in range(1,29):
        AdminiStrative.parsePage(url,str(i),baseUrl,baseUrl2,Savepath)
        time.sleep(2)
































