# -*- coding:utf-8 -*-
import re,requests
from 宁夏.工具包 import 链接数据库, 替换标签, 附件下载程序, 只有行政处罚信息公开表,判断全文的类型返回表中需要的字段,表格加全文的形式8行19格10行23格

from  bs4 import BeautifulSoup

for i in range(1,2):
    url = "http://www.nxld.gov.cn/xxgk/xzcf/list.html"
    header = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    response = requests.get(url, headers=header)
    print(type(response.status_code))
    if response.status_code==200:
        print("yes")
    else:
        print("No")
    response = response.content.decode('utf-8',errors = 'ignore')
    response = response.replace("\n", '').replace("\r", '').replace("\t", '')

    soup = BeautifulSoup(response,'lxml')
    responseList = soup.find_all('table', attrs={'class': 'table_normal'})
    print(soup)

    RSlist = re.findall(re.compile(
        r'<ul>.*?<li.*?><span>(.*?)</span></li>.*?<li.*?><a.*?href="(.*?)".*?title="(.*?)".*?>.*?</a></li>.*?<li.*?><span.*?>(.*?)</span></li>.*?<li.*?><span>(.*?)</span></li>.*? </ul>',
        re.S | re.M), str(response))
    print(RSlist)
    print(len(RSlist))
    SrcList = []
    TitleList = []
    TimeList = []
    for i in RSlist:
        SrcList.append(i[1])
    for src in SrcList:
        url = "http://www.nxld.gov.cn/xxgk/xzcf/"+src
        print(url)
        ConetentResponse = requests.get(url, headers=header)
        ConetentResponse = ConetentResponse.content.decode('utf-8')
        ConetentResponseSoup = BeautifulSoup(ConetentResponse, 'lxml')
        ConetentResponseSoupOld = ConetentResponseSoup.find_all('div', attrs={'class': 'zz-xl-ct'})

        # ConetentResponseSoup = BeautifulSoup(str(ConetentResponseSoup), 'lxml')
        # ConetentResponseSoupOld = ConetentResponseSoup.find('table')

        returnData = 替换标签.replaceLable(ConetentResponseSoupOld)
        ConetentResponseSoupOld = returnData[0]
        ContentTrNum = returnData[1]
        ContentTdNum = returnData[2]
        ContentPNum = returnData[3]
        ContentPNum1 = returnData[4]
        ConetentResponse = 替换标签.replaceLableNow(ConetentResponseSoupOld)

        if ConetentResponseSoupOld.find(".xls")!=-1:
            print("这是xls文件")
        if ConetentResponseSoupOld.find(".xlsx")!=-1:
            print("这是xlsx文件")
        if ConetentResponseSoupOld.find(".doc")!=-1:
            print("这是doc文件")
        if ConetentResponseSoupOld.find(".docx")!=-1:
            print("这是docx文件")