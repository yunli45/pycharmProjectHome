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




header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
OnlyID = 1
showId = 12308160
url = "http://cgj.tjftz.gov.cn/system/more/64110000/0000/64110000_00000001.shtml"
baseUrl = "http://cgj.tjftz.gov.cn"
path = "F:\行政处罚数据\天津\城市管理局\%s"


response = requests.get(url, headers=header)
response = response.content.decode('gb2312')
print(response)
rsList = re.findall(re.compile(r'<td width="76%" ><a href="(.*?)" target="_blank">.*?</a></td>.*?<td width="20%" align="right">(.*?)</td>',re.S|re.M),str(response))
print(rsList)
# print(response)
srcList= []
timeList = []
for i in rsList:
    srcList.append(i[0])
    timeList.append(i[1])

for src in srcList:
    RSdataId = re.sub('.*?/','',src).replace('.shtml','')
    RSTitle = timeList[srcList.index(src)] # 时间

    if src.find("http")!=-1:
        ContentSrc = src
    else:
        ContentSrc = baseUrl + src
    # print(ContentSrc)

    responseContent = requests.get(ContentSrc,headers = header)
    responseContent = responseContent.content.decode('gb2312')
    responseContent = str(responseContent)
    ContentSoup = BeautifulSoup(responseContent,'lxml')
    RStitleFind = ContentSoup.findAll('td',attrs={'class':'title'})
    # 标题
    if RStitleFind:
        RStitle = RStitleFind[0].text.strip()
    else:
        RStitle = ''
    ConetentResponseSoupOld = ContentSoup.find('td',attrs={'class':'hanggao35 zi14'})
    #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
    #
    # 提取文书号等信息
    #
    #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #

    ConetentResponse = re.sub('<span.*?>', '', str(ConetentResponseSoupOld), flags=re.S | re.M).replace(
        '</span>', '')
    ConetentResponse = re.sub('<col.*?>', '', ConetentResponse)
    ConetentResponse = re.sub('<tr.*?>', '', ConetentResponse)
    ConetentResponse = re.sub('<td.*?>', '', ConetentResponse)
    ConetentResponse = re.sub('<table.*?>', '', ConetentResponse).replace('<td>', '<p><p>').replace('</td>',
                                                                                                    '</p><p>').replace(
        'tr', 'p').replace('tbody', 'p').replace('table', '').replace('</p><p></p>', '</p><p>')
    ConetentResponse = re.sub(r'<p.*?><o:p> </o:p></p>', '', str(ConetentResponse)).replace('<o:p></o:p>', '')
    ConetentResponse = re.sub(r'<st1:.*?>', '', str(ConetentResponse)).replace('</st1:chsdate>', '').replace(
        '<a name="TCSignYear"></a>', '')
    ConetentResponse = re.sub(r'<o:p>\xa0</o:p>', '', str(ConetentResponse))
    ConetentResponse = re.sub(r'</p></p><p><p', '</p><p', str(ConetentResponse)).replace('</p></p>', '</p>')
    ConetentResponse = re.sub(r'<font.*?>', '', str(ConetentResponse)).replace('</font>', '')

    ConetentResponse = ConetentResponse.replace("'", "''").replace('\u2002', ' ').replace('<b>', '').replace(
        '</b>', '')
    # print(ConetentResponse)

    dataId = RSdataId
    title = RStitle
    documentNum = ' '  # 书文号
    bePunished = ' '  # 被处罚人或机构
    principal = ' '  # 法定代表人
    lawEnforcement = ' '  # 被处罚单位
    punishedDate = ' '  # 受处罚时间
    content = ConetentResponse  # 全文RScontent
    uniqueSign = ContentSrc  # url地址
    address = '天津'  # 省份
    area = '天津港保税区 '  # 地区
    agency = '天津城市管理局'  # 处罚机构
    if len(content) <= 100:
        grade = -1  # 级别
    elif 100 < len(content) <= 200:
        grade = 1  # 级别
    elif 200 < len(content) <= 1500:
        grade = 2  # 级别
    elif len(content) > 1500:
        grade = 0  # 级别
    showId = showId  # 系统ID



    #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
    #
    # 附件下载
    #
    #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
    adjunct = re.findall(re.compile(r'<a.*?href="(.*?)".*?>(.*?)</a>', re.I | re.S), ConetentResponse)

    if ConetentResponse:
        conn = pymssql.connect(host='(local)', user='sa', password='123456', database='AdministrativePun')
        # 打开游标
        cur = conn.cursor();
        if not cur:
            raise Exception('数据库连接失败！')
        else:
            print("数据库链接成功")
        sql1 = " INSERT INTO  crawlData14(dataId,title,documentNum,bePunished,principal,lawEnforcement,punishedDate,content,uniqueSign,address,area,agency,grade,showId) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " % (  dataId, title, documentNum, bePunished,principal,lawEnforcement,punishedDate,content,uniqueSign,address, area, agency,grade,showId)

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
                    r = requests.get(rsDocuniqueSign, headers=header, timeout=300)
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
                    r = requests.get(rsDocuniqueSign, headers=header)
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
                    r = requests.get(rsDocuniqueSign, headers=header)
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
                    r = requests.get(rsDocuniqueSign, headers=header)
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
                    r = requests.get(rsDocuniqueSign, headers=header)
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
                    r = requests.get(rsDocuniqueSign, headers=header, timeout=300)
                    with open(path1, "wb") as f:
                        f.write(r.content)
                    f.close()

        cur.execute(sql1)
        OnlyID += 1
        showId += 1
    conn.commit()
    conn.close()
    print("下一页开始的id是" + str(OnlyID))
    print("这一夜爬取成功相关数据和文件，文件保存的目录在" + path)




























