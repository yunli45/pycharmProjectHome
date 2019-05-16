import re
import requests
from bs4 import BeautifulSoup


# 根据全文能否找到 关键字"table" 和去掉batle内容前后p标签的变化和个数来判断全文的类型
# 返回表中需要的字段内容和
def ContentType(ConetentResponseSoupOld,ConetentResponse,ContentPNum,ContentPNum1,ContentTrNum,ContentTdNum,RSTitle,RSTime,OnlyID,SavePath,header):
    # 全文只是一个表格
    if ContentPNum1 <10 and ConetentResponseSoupOld.find("<table") != -1:
        print("全文只是一个表格")
        # if ContentTrNum == 6 and ContentTdNum == 12 and ContentPNum1 < 15:
        #     print("这是一个表格，6行12格的形式")
        #     ConetentResponseTable = re.sub('<span.*?>', '', str(ConetentResponseSoupOld)).replace('</span>', '')
        #     ConetentResponseTable = re.sub('<p.*?>', '', str(ConetentResponseTable)).replace('</p>', '')
        #     ConetentResponseTable = re.sub('<font.*?>', '', str(ConetentResponseTable)).replace('</font>', '')
        #
        #     # 替换标签
        #     ConetentResponseTable = re.sub('<col.*?>', '', ConetentResponseTable).replace('</colgroup>', '')
        #     ConetentResponseTable = re.sub('<td.*?>', '<td>', ConetentResponseTable)
        #     ConetentResponseTable = re.sub('<tr.*?>', '<tr>', ConetentResponseTable).replace("<td><td>", "<td>")
        #     # print("表格的内容" + ConetentResponseTable)
        #     TableSoup = BeautifulSoup(ConetentResponseTable, 'lxml')
        #     listTr1 = []
        #     for ids, tr in enumerate(TableSoup.find_all('tr')):
        #         listTr1.append(tr)
        #     print()
        #     RSdocumentNum = listTr1[0]  # 书文号
        #     RSdocumentNum = re.sub(r'.*?</td><td>', '', str(RSdocumentNum)).replace("</td></tr>", '')
        #     RSDSR = listTr1[1].text.strip()
        #     rs = re.findall(re.compile(r'当事人|当 事 人：(.*?)\xa0注册|性别'), RSDSR)
        #     RSbePunished = rs[0]  # 被处罚人或机构
        #     RSlawEnforcement = rs[0]  # 被处罚单位表格LIst
        #     fr = re.findall(re.compile(r'法定代表人：(.*?)\xa0经济性质'), RSDSR)
        #     if fr != []:
        #         RSprincipal = fr[0].replace(r"\xa0", '')  # 法定代表人
        #     else:
        #         RSprincipal = ''
        #     RSagency = listTr1[-2]  # 作出行政处罚决定机关名称
        #     RSagency = re.sub(r'.*?</td><td>', '', str(RSagency)).replace("</td></tr>", '')
        #     RSpunishedDate = listTr1[-1]  # 受处罚时间
        #     RSpunishedDate = re.sub(r'.*?</td><td>', '', str(RSpunishedDate)).replace("</td></tr>", '')
        #     当事人基本情况 = listTr1[1]
        #     当事人基本情况 = str(当事人基本情况).replace("<tr><td>", '').replace("\xa0", ' ').replace('</td><td>',
        #                                                                                 ' ').replace(
        #         "</td></tr>", '')
        #     违法行为类型 = listTr1[2]
        #     违法行为类型 = re.sub(r'.*?</td><td>', '', str(违法行为类型)).replace("</td></tr>", '')
        #     行政处罚内容 = listTr1[3]
        #     行政处罚内容 = re.sub(r'.*?</td><td>', '', str(行政处罚内容)).replace("</td></tr>", '')
        #     RScontent = 当事人基本情况 + "\n违法行为类型：" + 违法行为类型 + "\n行政处罚内容：" + 行政处罚内容
        # # elif str(ConetentResponseSoupOld).find("<table") != -1 and ContentPNum1 < 15:

        if ConetentResponseSoupOld.find("行政处罚信息公开表") != -1 and ConetentResponseSoupOld.find("Section1") != -1:
            if ConetentResponseSoupOld.find("行政处罚信息公开表") != -1:
                MsoNormalTable = BeautifulSoup(ConetentResponseSoupOld, 'lxml')
                # 可能粗存在两个名字如下
                MsoNormalTable1 = MsoNormalTable.findAll('table', attrs={'class': 'MsoNormalTable'})
                MsoNormalTable2 = MsoNormalTable.findAll('table', attrs={'class': 'MsoTableGrid'})
                # print("111111")
                # 超过两个名字抛出异常
                if MsoNormalTable1 != []:
                    MsoNormalTable = MsoNormalTable1
                elif MsoNormalTable2 != []:
                    MsoNormalTable = MsoNormalTable2
                else:
                    raise RuntimeError('只有行政处罚信息表的的表格不止MsoNormalTable和MsoTableGrid这两个名字，请查看下')

                MsoNormalTable = re.sub(r'<table.*?>', '', str(MsoNormalTable), flags=re.M | re.S)
                MsoNormalTable = re.sub('<tr.*?>', '<tr>', str(MsoNormalTable), flags=re.M | re.S)
                MsoNormalTable = re.sub('<td.*?>', '<td>', str(MsoNormalTable), flags=re.M | re.S)
                MsoNormalTable = re.sub('<col.*?>', '', str(MsoNormalTable), flags=re.M | re.S)
                MsoNormalTable = re.sub('<div.*?>', '', str(MsoNormalTable), flags=re.M | re.S).replace("</div>", '')
                MsoNormalTable = re.sub('<st1.*?>', '', str(MsoNormalTable), flags=re.M | re.S).replace(
                    "</st1:chsdate>",
                    '').replace("\n",
                                '').replace(
                    "\t", '')
                MsoNormalTable = re.sub('<p.*?>', '', str(MsoNormalTable), flags=re.M | re.S).replace('</p>',
                                                                                                      '').replace(
                    '<o:p>', '').replace('</o:p>', '')
                # print("行政处罚信息公开表")
                # print(MsoNormalTable)
                MsoNormalTable = BeautifulSoup(MsoNormalTable, 'lxml')
                # print(MsoNormalTable)
                TrList = []
                TDList = []
                for ids, tr in enumerate(MsoNormalTable.findAll('tr')):
                    TrList.append(tr)
                    if ids != -1:
                        tds = tr.find_all('td')
                        TDList.append(tds)
                print("表格LIst")
                print(TDList)
                TableResultList = []
                if TDList != []:
                    RSdocumentNum = TDList[0][-1].text.strip()  # s书文号
                    RSbePunished = TDList[1][-1].text.strip()  # 被处罚人或机构
                    RSlawEnforcement = TDList[2][-1].text.strip()  # 处罚机构
                    RSprincipal = TDList[3][-1].text.strip()  # 法人
                    RSagency = TDList[-2][-1].text.strip()  # 处罚机构
                    RSpunishedDate = TDList[-1][-1].text.strip()  # 处罚时间
                    RScontent = "主要违法违规事实（案由）:" + TDList[4][-1].text.strip() + "\n 行政处罚依据:" + TDList[5][
                        -1].text.strip() + "\n 行政处罚决定:" + TDList[6][-1].text.strip()
                #     TableResultList.append(RSdocumentNum)
                #     TableResultList.append(RSbePunished)
                #     TableResultList.append(RSlawEnforcement)
                #     TableResultList.append(RSprincipal)
                #     TableResultList.append(RSagency)
                #     TableResultList.append(RSpunishedDate)
                #     TableResultList.append(RScontent)
                # return TableResultList

        else:
            print("全文的表格不是一个6行12格的形式")
            # 先处理标签问题，先简化  只剩td tr标签
            ConetentResponseAndTabe = re.sub('<span.*?>', '', str(ConetentResponseSoupOld),
                                             flags=re.S | re.M).replace('</span>', '')
            ConetentResponseAndTabe = re.sub(r'<p.*?>', '', str(ConetentResponseAndTabe),flags=re.S|re.M).replace('</p>', '')
            ConetentResponseTable = re.sub('<col.*?>', '', ConetentResponseAndTabe,flags=re.S|re.M).replace('</colgroup>', '')
            ConetentResponseTable = re.sub('<td.*?>', '<td>', ConetentResponseTable,flags=re.S|re.M).replace("<o:p>",'').replace('</o:p>','')
            ConetentResponseTable = re.sub('<div.*?>', '', ConetentResponseTable,flags=re.S|re.M).replace("</div>",'')
            ConetentResponseTable = re.sub('<tr.*?>', '<tr>', ConetentResponseTable,flags=re.S|re.M).replace("<td><td>",
                                                                                             "<td>").replace(
                "'",
                '"')
            print("表格的内容1" + ConetentResponseTable)
            TableSoup = BeautifulSoup(ConetentResponseTable, 'lxml')
            print("编译后的表格"+str(TableSoup))
            listTr1 = []
            for ids, tr in enumerate(TableSoup.find_all('tr')):
                print("tr的内容"+str(tr))
                listTr1.append(ids)
                TrDocNUM1 = re.findall(re.compile(r'吴.*?[工 商 市 场 罚].*?\d.*?号'), str(tr))
                TrDocNUM2 = re.findall(re.compile(r'吴.*?[银 工 商 市 场 罚].*?\d.*?号'), str(tr))
                if TrDocNUM1 != []:
                    TrDocNUM = TrDocNUM1
                elif TrDocNUM2 != []:
                    TrDocNUM = TrDocNUM2

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
                            RSagency = tds[-3].text.strip()  # 作出行政处罚决定机关名称
                            RSpunishedDate = tds[-2].text.strip()  # 受处罚时间
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
    elif ContentPNum1 == ContentPNum and ConetentResponseSoupOld.find("<table") == -1:
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
                        SavePath1 = SavePath % (imgTitle)
                        r = requests.get(imgSrc, headers=header, timeout=3)
                        with open(SavePath1, "wb") as f:
                            f.write(r.content)
                        f.close()
                except:
                    print("这条数据的网址出错了")
                    print("id是" + str(OnlyID))
                    pass
            else:
                ConetentResponse = ConetentResponse

        RScontent = ConetentResponse
    # 全文含有表格  因为表格中内容在全文能找到，就将表格格中内容去掉
    elif ContentPNum1 >= 10 and ConetentResponseSoupOld.find("<table") != -1:
        print("全文含有表格")
        ConetentResponseSoupOld = re.sub(r'<table.*?>.*?</table>', '', ConetentResponseSoupOld, flags=re.S | re.M)
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
                if RSdocumentNumFind != []:
                    documentPNum = ConetentNOWp.index(p)
                    RSdocumentNum = ConetentNOWp[documentPNum].text.strip()
                    break
                else:
                    RSdocumentNum = ''

            for p in ConetentNOWp:
                AdressNumFind = re.findall(re.compile(r'.*?地址|住址|住所.*?'), str(p))
                if AdressNumFind != []:
                    AdressNum = ConetentNOWp.index(p)
                    RSbePunished = ConetentNOWp[AdressNum - 2].text.strip()  # 被处罚人或者单位
                    RSlawEnforcement = ConetentNOWp[AdressNum - 2].text.strip()  # 被处罚单位
                    if RSbePunished.find("注册号") != -1:
                        RSbePunished = ConetentNOWp[AdressNum - 3].text.strip()
                        RSlawEnforcement = RSbePunished
                    elif RSbePunished.find("津市场") != -1:
                        RSbePunished = ConetentNOWp[AdressNum + 2].text.strip()
                        RSlawEnforcement = RSbePunished
                    RSprincipal = ConetentNOWp[AdressNum + 1].text.strip()  # 法人
                    if RSprincipal.find("企业类型") != -1:
                        RSprincipal = ConetentNOWp[AdressNum - 1].text.strip()
                    elif RSprincipal.find("组成形式") != -1:
                        RSprincipal = ConetentNOWp[AdressNum + 2].text.strip()
                    break
                else:
                    RSbePunished = ''
                    RSlawEnforcement = ''
                    RSprincipal = ''

            for p in ConetentNOWp:
                RSagencyNumFind = re.findall(re.compile(r'<p>.*?[天 津 市 区   场 和 质量  监 督  管 理].*?局</p>'),
                                             str(p))
                if RSagencyNumFind != []:
                    RSagencyNum = ConetentNOWp.index(p)
                    RSagency = ConetentNOWp[RSagencyNum].text.strip()
                    break
                else:
                    RSagency = ''
            for p in ConetentNOWp:
                DataNumFind = re.findall(re.compile(
                    r'<p>[○ 0 O o 〇 Ｏ 一 二 三 四 五 六 七 八 九 十]{4}年[〇 一 二 三 四 五 六 七 八 九 十]{1,2}月[〇 一 二 三 四 五 六 七 八 九 十]{1,3}日</p>|<p>\d{4}年\d{1,2}月\d{1,2}日</p>'),
                    str(p))
                if DataNumFind != []:
                    DataNum = ConetentNOWp.index(p)
                    RSpunishedDate = ConetentNOWp[DataNum].text.strip()
                    break
                else:
                    RSpunishedDate = ''

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
                        SavePath1 = SavePath% (imgTitle)
                        r = requests.get(imgSrc, headers=header, timeout=3)
                        with open(SavePath1, "wb") as f:
                            f.write(r.content)
                        f.close()
                except:
                    print("这条数据的网址出错了")
                    print("id是" + str(OnlyID))
                    pass
            else:
                ConetentResponse = ConetentResponse

        RScontent = ConetentResponse
    else:
        print("全文是图片的形式")
        if ConetentResponseSoupOld.find("<img") != -1:
            print("全文是一个图片的形式")
            RSimgFind = re.findall(re.compile(r'<img.*?src="(.*?)".*?>'), ConetentResponse)
            if RSimgFind:
                print(RSTitle)
                print(RSimgFind)
                print(ConetentResponse)
                ConetentResponse = "这可能是一个图片形式的，请查看本地是否有相应的标题图片" + ConetentResponse
                RSdocumentNum = '这是一个图片的形式，请人工查看'  # 书文号
                imgSrc = RSimgFind[0]
                RSbePunished = '这是一个图片的形式，请人工查看'  # 被处罚人或者单位
                RSlawEnforcement = ''  # 被处罚单位
                RSprincipal = ''  # 法人
                RSpunishedDate = RSTime  # 受处罚时间
                RSagency = ''

                try:
                    imgSrc = imgSrc
                    for TitleNum in enumerate(RSimgFind):
                        imgTitle = RSTitle + str(TitleNum[0]) + ".jpg"
                        SavePath1 = SavePath % (imgTitle)
                        r = requests.get(imgSrc, headers=header, timeout=3)
                        with open(SavePath, "wb") as f:
                            f.write(r.content)
                        f.close()
                except:
                    print("这条数据的网址出错了")
                    print("id是" + str(OnlyID))
                    pass
            else:
                ConetentResponse = ConetentResponse

        RScontent = ConetentResponse

    return RSdocumentNum,RSbePunished,RSprincipal,RSlawEnforcement,RSpunishedDate,RScontent,RSagency