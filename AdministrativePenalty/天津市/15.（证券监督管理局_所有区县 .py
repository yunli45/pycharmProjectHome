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
showId = 12308180
url = "http://www.csrc.gov.cn/pub/tianjin/xzcf/"
baseUrl = "http://www.csrc.gov.cn/pub/tianjin/xzcf/"
path = "F:\行政处罚数据\天津\证券监督管理局\%s"


response = requests.get(url, headers=header)
response = response.content.decode('utf-8')
print(response)
soup = BeautifulSoup(response,'lxml')
soup = soup.findAll('div',attrs={'class':'fl_list'})
print(soup)
rsList = re.findall(re.compile(r'<a href="(.*?)".*?title="(.*?)">.*?</a>.*?<span>(.*?)</span>',re.S|re.M),str(soup))
print(rsList)
# print(response)
srcList= []
titleList = []
timeList = []
for i in rsList:
    srcList.append(i[0])
    titleList.append(i[1])
    timeList.append(i[2])

for src in srcList:
    RSdataId = re.sub('.*?/','',src).replace('.shtml','')
    RSTime = timeList[srcList.index(src)] # 时间
    RSTitle = titleList[srcList.index(src)]

    if src.find("http")!=-1:
        ContentSrc = src
    else:
        ContentSrc = baseUrl + src.replace("./",'/')
    print(ContentSrc)
    print("\n")
    responseContent = requests.get(ContentSrc,headers = header)
    responseContent = responseContent.content.decode('utf-8')
    print(responseContent)
    ContentSoup = BeautifulSoup(responseContent, 'lxml')
    responseContent = ContentSoup.findAll('div', attrs={'class': 'content'})
    responseContent = str(responseContent)
    print(responseContent)


    #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
    #
    # 提取文书号等信息
    #
    #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #

    ConetentResponse = re.sub('<span.*?>', '', str(responseContent), flags=re.S | re.M).replace(
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
    print(ConetentResponse)

    dataId = RSdataId
    title = RSTitle
    documentNum = ' '  # 书文号


    if RSTitle.find("公司") >= 0:
        bePunished = RSTitle[RSTitle.find("（"):RSTitle.find("公司")] + "公司"  # 被处罚人或机构
        lawEnforcement = bePunished  # 被处罚单位
        principal = ' '  # 法定代表人
    else:

        RSTitle = RSTitle.replace("）",'')
        bePunished = RSTitle[RSTitle.find("（"):]
        lawEnforcement = ''
        principal =''

    punishedDate = RSTitle  # 受处罚时间
    content = ConetentResponse  # 全文RScontent
    uniqueSign = ContentSrc  # url地址
    address = '天津'  # 省份
    area = '  '  # 地区
    agency = '中国证券监督管理委员会天津监管局'  # 处罚机构
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
        sql1 = " INSERT INTO  crawlData15(dataId,title,documentNum,bePunished,principal,lawEnforcement,punishedDate,content,uniqueSign,address,area,agency,grade,showId) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " % (  dataId, title, documentNum, bePunished,principal,lawEnforcement,punishedDate,content,uniqueSign,address, area, agency,grade,showId)

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




























