# -*- coding:utf-8 -*-
import requests
import re
import time
from bs4 import BeautifulSoup
import pymssql

url = "http://scjg.tj.gov.cn/jgdt/xzcfxxgs/sjxzcfxx/25256.html"
response = requests.get(url)
response = response.content.decode('utf-8')
ConetentResponseSoup = BeautifulSoup(response, 'lxml')
ConetentResponseSoupOld = ConetentResponseSoup.find('div', attrs={'class': 'news_content'})
ConetentResponseSoupOld = re.sub("<strong.*?>",'',str(ConetentResponseSoupOld)).replace("</strong>",'')
ConetentResponseSoupOld = re.sub("<u.*?>",'',ConetentResponseSoupOld, flags=re.S | re.M).replace("</u>",'')
ConetentResponseSoupOld = re.sub("<b.*?>",'',ConetentResponseSoupOld, flags=re.S | re.M).replace("</b>",'')
ConetentResponseSoupOld = re.sub('<span.*?>','',ConetentResponseSoupOld, flags=re.S | re.M).replace('</span>','')
ConetentResponseSoupOld = str(ConetentResponseSoupOld)

ContentNum = BeautifulSoup(str(ConetentResponseSoupOld), 'lxml')
ContentTrNum = len(ContentNum.findAll('tr'))
ContentTdNum = len(ContentNum.findAll('td'))
ContentPNum = len(ContentNum.findAll('p'))

print("这条数据原来有：" + str(ContentPNum) + "个P")
print("这条数据原来一共有：" + str(ContentTrNum) + "个tr")
print("这条数据原来一共有：" + str(ContentTdNum) + "个td")
# 先尝试着找到到table，如果存在就删除再去找p标签的个数,
if ConetentResponseSoupOld.find("<table") != -1:
    ConetentResponseSoupOld1 = re.sub('<table.*?>.*?</table>', '', ConetentResponseSoupOld,
                                      flags=re.S | re.M)
else:
    ConetentResponseSoupOld1 = ConetentResponseSoupOld

ContentNum1 = BeautifulSoup(str(ConetentResponseSoupOld1), 'lxml')
ContentPNum1 = len(ContentNum1.findAll('p'))


print("还没修改完全的全文+"+ConetentResponseSoupOld)

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
ConetentResponse = re.sub(r'<p.*?>', '<p>', str(ConetentResponse), flags=re.S | re.M)
ConetentResponse = ConetentResponse.replace("'", "''").replace('<b>', '').replace('</b>', '').replace(
    "2312>'，", '')

print("修改后i的全文")
print(ConetentResponse)


# 全文只是一个表格
if  ContentPNum1 <10 and ConetentResponseSoupOld.find("<table")!=-1:
    print("全文只是一个表格")

    if ContentTrNum == 6 and ContentTdNum == 12 and ContentPNum1 < 10:
        print("这是一个表格，6行12格的形式")
        ConetentResponseTable = re.sub('<span.*?>', '', str(ConetentResponseSoupOld)).replace('</span>', '')
        ConetentResponseTable = re.sub('<p.*?>', '', str(ConetentResponseTable)).replace('</p>', '')
        ConetentResponseTable = re.sub('<font.*?>', '', str(ConetentResponseTable)).replace('</font>', '')

        # 替换标签
        ConetentResponseTable = re.sub('<col.*?>', '', ConetentResponseTable).replace('</colgroup>', '')
        ConetentResponseTable = re.sub('<td.*?>', '<td>', ConetentResponseTable)
        ConetentResponseTable = re.sub('<tr.*?>', '<tr>', ConetentResponseTable).replace("<td><td>", "<td>")
        # print("表格的内容" + ConetentResponseTable)
        TableSoup = BeautifulSoup(ConetentResponseTable, 'lxml')
        listTr1 = []
        for ids, tr in enumerate(TableSoup.find_all('tr')):
            listTr1.append(tr)
        print()
        RSdocumentNum = listTr1[0]  # 书文号
        RSdocumentNum = re.sub(r'.*?</td><td>', '', str(RSdocumentNum)).replace("</td></tr>", '')
        RSDSR = listTr1[1].text.strip()
        rs = re.findall(re.compile(r'当事人：(.*?)\xa0注册'), RSDSR)
        RSbePunished = rs[0]  # 被处罚人或机构
        RSlawEnforcement = rs[0]  # 被处罚单位
        fr = re.findall(re.compile(r'法定代表人：(.*?)\xa0经济性质'), RSDSR)
        RSprincipal = fr[0].replace(r"\xa0", '')  # 法定代表人
        RSagency = listTr1[-2]  # 作出行政处罚决定机关名称
        RSagency = re.sub(r'.*?</td><td>', '', str(RSagency)).replace("</td></tr>", '')
        RSpunishedDate = listTr1[-1]  # 受处罚时间
        RSpunishedDate = re.sub(r'.*?</td><td>', '', str(RSpunishedDate)).replace("</td></tr>", '')
        当事人基本情况 = listTr1[1]
        当事人基本情况 = str(当事人基本情况).replace("<tr><td>", '').replace("\xa0", ' ').replace('</td><td>',
                                                                                    ' ').replace(
            "</td></tr>", '')
        违法行为类型 = listTr1[2]
        违法行为类型 = re.sub(r'.*?</td><td>', '', str(违法行为类型)).replace("</td></tr>", '')
        行政处罚内容 = listTr1[3]
        行政处罚内容 = re.sub(r'.*?</td><td>', '', str(行政处罚内容)).replace("</td></tr>", '')
        RScontent = 当事人基本情况 + "\n违法行为类型：" + 违法行为类型 + "\n行政处罚内容：" + 行政处罚内容
    elif str(ConetentResponseSoupOld).find("<table") != -1 and ContentPNum1 < 10:
        print("全文的表格不是一个6行12格的形式")
        # 先处理标签问题，先简化  只剩td tr标签
        ConetentResponseAndTabe = re.sub('<span.*?>', '', str(ConetentResponseSoupOld),
                                         flags=re.S | re.M).replace('</span>', '')
        ConetentResponseAndTabe = re.sub(r'<p.*?>', '', str(ConetentResponseAndTabe)).replace('</p>', '')
        ConetentResponseTable = re.sub('<col.*?>', '', ConetentResponseAndTabe).replace('</colgroup>', '')
        ConetentResponseTable = re.sub('<td.*?>', '<td>', ConetentResponseTable)
        ConetentResponseTable = re.sub('<tr.*?>', '<tr>', ConetentResponseTable).replace("<td><td>",
                                                                                         "<td>").replace(
            "'",
            '"')
        print("表格的内容" + ConetentResponseTable)
        TableSoup = BeautifulSoup(ConetentResponseTable, 'lxml')
        listTr1 = []
        for ids, tr in enumerate(TableSoup.find_all('tr')):
            listTr1.append(ids)
            TrDocNUM = re.findall(re.compile(r'<td>津.*?[工 商 市 场 罚].*?\d.*?号.*?</td>'), str(tr))
            print("表格中书文号：" + str(TrDocNUM))
            print("这里是表格形式的")
            if TrDocNUM != []:
                TrNUM = ids
                # 以书文号一行为基准找数据
                if listTr1[TrNUM]:
                    print("找到书文号啦" + str(listTr1[TrNUM]))
                    tds = tr.find_all('td')
                    if len(tds) > 10:
                        print("这是大于10的表格")
                        RSbePunished = tds[1].text.strip()  # 被处罚人或机构
                        RSlawEnforcement = tds[1].text.strip()  # 被处罚单位
                        RSprincipal = tds[4].text.strip()  # 法定代表人
                        RSdocumentNum = tds[5].text.strip()  # 书文号
                        RSagency = tds[10].text.strip()  # 作出行政处罚决定机关名称
                        RSpunishedDate = tds[11].text.strip()  # 受处罚时间
                        RScontent = "主要违法事实:" + tds[6].text.strip() + "\n 处罚种类:" + tds[
                            7].text.strip() + "\n 处罚依据:" + tds[8].text.strip() + "\n 行政处罚的履行方式和期限:" + tds[
                                        9].text.strip()
                    # 特殊情况
                    elif len(tds) == 10:
                        print("这是等于10的 表格")
                        RSbePunished = tds[1].text.strip()  # 被处罚人或机构
                        RSlawEnforcement = tds[1].text.strip()  # 被处罚单位
                        RSprincipal = ''  # 法定代表人
                        RSdocumentNum = tds[3].text.strip()  # 书文号
                        RSagency = tds[8].text.strip()  # 作出行政处罚决定机关名称
                        RSpunishedDate = tds[9].text.strip()  # 受处罚时间
                        RScontent = "违法行为:" + tds[4].text.strip() + "\n 处罚种类:" + tds[
                            5].text.strip() + "\n 罚款金额，单位：万元:" + tds[6].text.strip()
                    elif len(tds) == 9:
                        print("这是等于9的 表格")
                        RSbePunished = tds[0].text.strip()  # 被处罚人或机构
                        RSlawEnforcement = tds[0].text.strip()  # 被处罚单位
                        RSprincipal = ''  # 法定代表人
                        RSdocumentNum = tds[2].text.strip()  # 书文号
                        RSagency = tds[7].text.strip()  # 作出行政处罚决定机关名称
                        RSpunishedDate = tds[8].text.strip()  # 受处罚时间
                        RScontent = "违法行为:" + tds[3].text.strip() + "\n 处罚种类:" + tds[
                            4].text.strip() + "\n 罚款金额，单位：万元:" + tds[5].text.strip()
                else:
                    RSbePunished = '特殊情况1，查看你下'  # 被处罚人或机构
                    RSlawEnforcement = '特殊情况1，查看你下'  # 被处罚单位
                    RSprincipal = '特殊情况1，查看你下'  # 法定代表人
                    RSdocumentNum = '特殊情况1，查看你下'  # 书文号
                    RSagency = '特殊情况1，查看你下'  # 作出行政处罚决定机关名称
                    RSpunishedDate = '特殊情况1，查看你下'  # 受处罚时间
                    RScontent = ConetentResponse



# 全文没有表格
elif ContentPNum1 >10 and ConetentResponseSoupOld.find("<table")==-1:
    print("这里是不含有表格的,只有文章内容")
    ConetentNoTable = ConetentResponse.replace(' ', '').replace("当事人名称或姓名：", '').replace("法定代表人（负责人）：",
                                                                                         '').replace(
        "法定代表人：", '').replace("当事人姓名或者单位名称:", '').replace("法定代表人（负责人）:", '').replace("负责人:", '')
    # 全文还可能是一个图片的形式
    RSimgFind = re.findall(re.compile(r'<img.*?src="(.*?)".*?>'), ConetentResponse)

    print(ConetentNoTable)
    ConetentNOW = BeautifulSoup(ConetentNoTable, 'lxml')
    ConetentNOWp = ConetentNOW.find_all('p')
    print(ConetentNOWp)
    if 1 <= len(ConetentNOWp) <= 3:
        RSdocumentNum = ''  # 书文号
        RSagency = ''
        RSbePunished = ""  # 被处罚人或机构
        RSlawEnforcement = ""  # 被处罚单位
        RSprincipal = ""  # 法定代表人
        RSpunishedDate = ""  # 受处罚时间
    else:
        for p in ConetentNOWp:
            RSdocumentNumFind = re.findall(re.compile(r'.*?津.*?[市 场 监].*?号'), str(p))
            AdressNumFind = re.findall(re.compile(r'.*?地址|住址.*?'), str(p))
            RSagencyNumFind = re.findall(re.compile(r'<p>.*? 天[津 市 区 市 场  质 量 监 督 管 理 局]>*?</p> '), str(p))
            if RSdocumentNumFind != []:
                RSdocumentNum = RSdocumentNumFind[0]  # 书文号
                documentPNum = ConetentNOWp.index(p)
            else:
                RSdocumentNum = ' '
            if RSagencyNumFind != []:
                RSagencyNum = ConetentNOWp.index(p)
                RSagency = ConetentNOWp[RSagencyNum].text.strip()
            else:
                RSagency = ''
            if AdressNumFind != []:
                print(p)
                AdressNum = ConetentNOWp.index(p)
                print("hajhahah ")
                print(AdressNum)
                RSbePunished = ConetentNOWp[AdressNum - 2].text.strip()  # 被处罚人或者单位
                RSlawEnforcement = ConetentNOWp[AdressNum - 2].text.strip()  # 被处罚单位
                RSprincipal = ConetentNOWp[AdressNum + 1].text.strip()  # 法人
                print(RSbePunished)
                print(RSlawEnforcement)
                print(RSprincipal)
                break
            elif AdressNumFind == []:
                print("mmmpppp")
                RSbePunished = "地址没有的情况"
                RSlawEnforcement = "地址没有的情况"
                RSprincipal = "地址没有的情况"

            if ConetentNOWp[-1].text.strip() == "" or " ":
                RSpunishedDate = ConetentNOWp[-2].text.strip()  # 受处罚时间
            else:
                RSpunishedDate = ConetentNOWp[-1].text.strip()  # 受处罚时间
        if RSimgFind:
            print(RSTitle)
            print(RSimgFind)
            print(ConetentResponse)
            ConetentResponse = "这可能是一个图片形式的，请查看本地是否有相应的标题图片" + ConetentResponse
            RSdocumentNum = ''  # 书文号
            imgSrc = RSimgFind[0]
            RSbePunished = ''  # 被处罚人或者单位
            RSlawEnforcement = ''  # 被处罚单位
            RSprincipal = ''  # 法人
            RSpunishedDate = ''  # 受处罚时间

            try:
                imgSrc = imgSrc
                for TitleNum in enumerate(RSimgFind):
                    imgTitle = RSTitle + str(TitleNum[0]) + ".jpg"
                    path1 = path % (imgTitle)
                    r = requests.get(imgSrc, headers=self.header, timeout=3)
                    with open(path1, "wb") as f:
                        f.write(r.content)
                    f.close()
            except:
                print("这条数据的网址出错了")
                print("id是" + str(self.OnlyID))
                pass
        else:
            ConetentResponse = ConetentResponse

    RScontent = ConetentResponse
# 全文含有表格
elif ContentPNum1 >10 and ConetentResponseSoupOld.find("<table")!=-1:
    print("全文含有表格")
    ConetentResponseSoupOld = re.sub(r'<table.*?>.*?</table>','',ConetentResponseSoupOld,flags=re.S|re.M)
    ConetentNoTable = ConetentResponseSoupOld.replace("当事人名称或姓名：", '').replace("法定代表人（负责人）：",
                                                                                         '').replace(
        "法定代表人：", '').replace("当事人姓名或者单位名称:", '').replace("法定代表人（负责人）:", '').replace("负责人:", '')
    ConetentNoTable = re.sub('<p.*?>', '<p>', ConetentNoTable).replace(" ", '').replace("\xa0", '')
    # 全文还可能是一个图片的形式
    RSimgFind = re.findall(re.compile(r'<img.*?src="(.*?)".*?>'), ConetentResponse)

    print(ConetentNoTable)
    ConetentNOW = BeautifulSoup(ConetentNoTable, 'lxml')
    ConetentNOWp = ConetentNOW.find_all('p')
    print(ConetentNOWp)
    if 1 <= len(ConetentNOWp) <= 3:
        RSdocumentNum = ''  # 书文号
        RSagency = ''
        RSbePunished = ""  # 被处罚人或机构
        RSlawEnforcement = ""  # 被处罚单位
        RSprincipal = ""  # 法定代表人
        RSpunishedDate = ""  # 受处罚时间
    else:
        # 书文号
        for p in ConetentNOWp:
            RSdocumentNumFind = re.findall(re.compile(r'.*?津.*?[市 场 监].*?号</p>'), str(p))
            if RSdocumentNumFind !=[]:
                documentPNum = ConetentNOWp.index(p)
                RSdocumentNum = ConetentNOWp[documentPNum].text.strip()
                break
            else:
                RSdocumentNum =''

        for p in ConetentNOWp:
            AdressNumFind = re.findall(re.compile(r'.*?地址|住址|住所.*?'), str(p))
            if AdressNumFind != []:
                AdressNum = ConetentNOWp.index(p)
                RSbePunished = ConetentNOWp[AdressNum - 2].text.strip()  # 被处罚人或者单位
                RSlawEnforcement = ConetentNOWp[AdressNum - 2].text.strip()  # 被处罚单位
                RSprincipal = ConetentNOWp[AdressNum + 1].text.strip()  # 法人
                break
            else:
                RSbePunished =''
                RSlawEnforcement=''
                RSprincipal=''

        for p in ConetentNOWp:
            RSagencyNumFind = re.findall(re.compile(r'<p>.*?[天 津 市 区   场 和 质量  监 督  管 理].*?局</p>'),
                                         str(p))
            if RSagencyNumFind !=[]:
                RSagencyNum = ConetentNOWp.index(p)
                RSagency = ConetentNOWp[RSagencyNum].text.strip()

                break
            else:
                RSagency =''
        for p in ConetentNOWp:
            DataNumFind = re.findall(re.compile(
                r'<p>[○ 0 O o 〇 Ｏ 一 二 三 四 五 六 七 八 九 十]{4}年[〇 一 二 三 四 五 六 七 八 九 十]{1,2}月[〇 一 二 三 四 五 六 七 八 九 十]{1,3}日</p>|<p>\d{4}年\d{1,2}月\d{1,2}日</p>'),
                                     str(p))
            if DataNumFind != []:
                DataNum  = ConetentNOWp.index(p)
                RSpunishedDate = ConetentNOWp[DataNum].text.strip()
                break
            else:
                RSpunishedDate = ''

        if RSimgFind:

            print(RSimgFind)
            print(ConetentResponse)
            ConetentResponse = "这可能是一个图片形式的，请查看本地是否有相应的标题图片" + ConetentResponse
            RSdocumentNum = ''  # 书文号
            imgSrc = RSimgFind[0]
            RSbePunished = ''  # 被处罚人或者单位
            RSlawEnforcement = ''  # 被处罚单位
            RSprincipal = ''  # 法人
            RSpunishedDate = ''  # 受处罚时间

        else:
            ConetentResponse = ConetentResponse

    RScontent = ConetentResponse
else:
    if ConetentResponseSoupOld.find("<img")!=-1:
        print("全文是一个图片的形式")
        RSimgFind = re.findall(re.compile(r'<img.*?src="(.*?)".*?>'), ConetentResponse)
        if RSimgFind:

            print(RSimgFind)
            print(ConetentResponse)
            ConetentResponse = "这可能是一个图片形式的，请查看本地是否有相应的标题图片" + ConetentResponse
            RSdocumentNum = '这是一个图片的形式，请人工查看'  # 书文号
            imgSrc = RSimgFind[0]
            RSbePunished = '这是一个图片的形式，请人工查看'  # 被处罚人或者单位
            RSlawEnforcement = ''  # 被处罚单位
            RSprincipal = ''  # 法人

        else:
            ConetentResponse = ConetentResponse
print(RSdocumentNum)
print(RSbePunished)







