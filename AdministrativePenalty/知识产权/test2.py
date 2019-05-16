# coding :utf-8
import requests
import re
from bs4 import BeautifulSoup


def main(url,pageNo):
    header = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    pagelable = "div"
    pagelableSelector = "class"
    pageNumS = "index_page01"
    pageTableName = "index_articl_list"

    ZSCQGZcompilePageTable = '<li.*?><a.*?href="(.*?)".*?title="(.*?)".*?>.*?</a> <span>(.*?)</span></li>'
    response = requests.get(url,headers = header)

    print(response.url)
    if response.status_code == 404:
        pass
    else:
        response = response.content.decode('utf-8', errors='ignore')
    # print(response)
    response = BeautifulSoup(response, 'lxml')
    # pageSoup = response.find_all(pagelable , attrs={pagelableSelector : pageNumS})
    # pageS = re.findall(re.compile("<font.*?>共(.*?)页"), str(pageSoup))
    # print(pageS)
    pageSoup = response.find_all(pagelable , attrs={pagelableSelector : pageTableName})
    pageS = re.findall(re.compile(ZSCQGZcompilePageTable), str(pageSoup))
    # print(pageS)
    pa = []
    for src in pageS:
        pa.append([src[0]])
    print(pa)
    # print(len(pageS))
    for i in pageS:
        src = i[0]
        rs = re.findall(re.compile(r'(.*?).(pdf|PDF|doc|DOC|docx|DOCX|xlsx|XLSX|xls|XLS)'), src)
        if rs :
            print(i,pageNo)
        rs2 = re.findall(re.compile(r'http://.*?'),src)
        if rs2!=[]:
            print(i,pageNo)


url = "http://www.sipo.gov.cn/zscqgz/index.htm"  # 知识产权工作
# url = "http://www.sipo.gov.cn/zcfg/zcjd/index.htm" # 政策解读

for pageNo in range(1,20):
    if pageNo==1:
        url1 =url
        main(url1,1)
    else:
        url1 = url[:url.rfind(".")]+str(pageNo-1)+".htm"
        main(url1,pageNo)
