import requests
from bs4 import BeautifulSoup
import re


ZCJDSavePath = "F:\知识产权局相关附件\政策解读\%s"
ZSCQGZSavePath = "F:\知识产权局相关附件\知识产权工作\%s"



ZCJDurl = "http://www.sipo.gov.cn/zcfg/zcjd/index.htm"
政策解读上一次抓取的最后的标题的url = "1124218.htm"



def getPage( url):
    header = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    response = requests.get(url, headers= header)
    print(response.url)
    if response.status_code == 404:
        pass
    else:
        response = response.content.decode('utf-8', errors='ignore')
    # print(response)
    return response
def getEveryPage( url, pageNo):
    header = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    if pageNo == "1":
        url = url
    else:
        url = url + str(int(pageNo) - 1) + ".htm"
    response = requests.get(url, headers=header)
    print(response.url)
    if response.status_code == 404:
        pass
    else:
        response = response.content.decode('utf-8', errors='ignore')
    # print(response)
    return response
def pageDate( response):
    response = BeautifulSoup(response, 'lxml')

    pagelable = "div"
    pagelableSelector = "class"
    pageNumS = "index_page01"  # 总页数的div名字
    pageTableName = "index_articl_list"  # 每条数据的div名字
    compilePageTable = '<li.*?><a.*?href="(.*?)".*?title="(.*?)".*?>.*?</a> <span>(.*?)</span></li>'  # 每条数据的匹配规则：标题、时间
    # 总记录数
    pageSoup = response.find_all(pagelable, attrs={pagelableSelector: pageNumS})
    pageS = re.findall(re.compile("<font.*?>共(.*?)页"),str(pageSoup))
    pageS1 =pageS[0]
    # 每条数据
    pageSoup1 = response.find_all(pagelable, attrs={pagelableSelector: pageTableName})
    RSList = re.findall(re.compile(compilePageTable), str(pageSoup1))
    print("这一页一共有："+str(len(RSList))+"条数据")
    return pageS1,RSList

ZCJDresponse = getPage(ZCJDurl)
# print(ZCJDresponse)
ZCJDdate = pageDate(ZCJDresponse)
ZCJDpageS = int(ZCJDdate[0])# 总页数
# print(ZCJDpageS)
# print(type(ZCJDpageS))
ZCJDRList =[]

def dg(pageNo):
    if ZCJDpageNo == 1:
        for x in ZCJDdate[1]:
            ZCJDRList.append(x)

for ZCJDpageNo in range(1,ZCJDpageS):
    if ZCJDpageNo ==1:
        for x in ZCJDdate[1]:
            ZCJDRList.append(x)
        print("现在已经将--政策解读--下第一页的src title time 集中到一个集合中了，只需要遍历该集合，找到与上一次结束url一致的时候停止")
        for ZCJDlst  in ZCJDRList:
            if  政策解读上一次抓取的最后的标题的url ==ZCJDlst[0]:
                break
            else:
                print("hahah")
                zcjdUrl = ZCJDurl[:ZCJDurl.rfind(".")]
                ZCJDresponse1 = getEveryPage(zcjdUrl,str(ZCJDpageNo))
                ZCJDdate1 = pageDate(ZCJDresponse1)[1]
                for y in ZCJDdate1:
                    ZCJDRList.append(y)