import re
import requests
from bs4 import BeautifulSoup
import time
from 工具包 import 判断url前面的点返回完整的请求地址
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

    def parsePage(self, url, pageNo, baseUrl):
        index_url = url
        if pageNo == 1:
            url_1 = url
            response = self.getPage(url_1)
        else:
            url_1 = url[:url.rfind("=") + 1] + str(int(pageNo))
            response = self.getPage(url_1)

        print("+++++++++++++++++++这是第：" + str(pageNo) + "页++++++++++++++++")
        print(url_1)

        # print(homePageSoup)
        rs_soup = BeautifulSoup(response, 'lxml')
        rs_soup = rs_soup.find_all('div', attrs={'class': 'pcjg_fffbg'})
        rs_soup = str(rs_soup[0]).replace("\n", '').replace("\r", '').replace("\t"
                                                                              "", '')
        srcListFind = re.findall(re.compile(r'<a.*?href="(.*?)".*?title="(.*?)">.*?</a></div><div.*?>(.*?)</div>', re.S),
                                 str(rs_soup))
        print(srcListFind)
        titleList = []
        timeList = []
        srcList = []
        for i in srcListFind:
            srcList.append(i[0])
            titleList.append(i[1])
            timeList.append(i[2])
        print(srcList)
        for ids, src in enumerate(srcList):

            print("这是第" + str(ids+1) + "条数据")

            # print(src)
            srcIndex = srcList.index(src)
            content_src = 判断url前面的点返回完整的请求地址.returnSRC().returnSrc(url, src, '')
            print("content_src   :  "+str(content_src))

            cont_response = self.getPage(content_src)
            cont_response_soup = BeautifulSoup(cont_response, 'lxml')
            # print(cont_response)

            # content_body_box == 》Custom_UnionStyle
            cont_response_soup_1 = cont_response_soup.find_all("table", attrs={'class', 'MsoNormalTable'})
            cont_response_soup_2 = cont_response_soup.find_all("div", attrs={'class', 'Custom_UnionStyle'})

            if cont_response_soup_1 :
                if cont_response_soup_1 and len(str(cont_response_soup_1[0])) > 50:
                    cont_response_soup_1 = str(cont_response_soup_1[0]).replace("\n", '').replace("\r", '').replace("\t"
                                                                              "", '')
                    print(cont_response_soup_1)
                    pass
            else:
                raise Exception("NO")


# if __name__ == "__main__":
    # # 共计353页这是第
    # index_url ="http://www.cbrc.gov.cn/zhuanti/xzcf/getPcjgXZCFDocListDividePage/hebei.html?current=1"
    # baseUrl ="http://www.mee.gov.cn/"
    # baseUrl2 =" "
    # Savepath =" "
    #
    # AdminiStrative =Utils()
    # for i in range(1, 13):
    #     AdminiStrative.parsePage(index_url, i, baseUrl)
        # time.sleep(2)