import re
from bs4 import BeautifulSoup
import requests
import xlrd
from 宁夏.工具包 import 附件下载程序
import time
# 全文的内容在表格中，key在左边value在右边   http://www.nxszs.gov.cn/zwgk/hangzhengchufa.htm

def getNeed(ConetentResponseSoupOld, ConetentResponse, ContentPNum, ContentPNum1, ContentTrNum, ContentTdNum,
                   RSTime,RSTitle,SavePath,header,ContentSrc,RSlawEnforcement,RSdocumentNum,RSdataId):

    ConetentResponseSoupOld1 = re.findall(r'<div class="zz-xl-ct">(.*?)<div class="zz-xl-ct".*?>',ConetentResponseSoupOld,flags=re.S|re.M)
    ConetentResponseSoupOld1 = str(ConetentResponseSoupOld1).replace('[','').replace(']','')
    ContentPNum2 = BeautifulSoup(str(ConetentResponseSoupOld1),'lxml')
    ContentPNum2 = ContentPNum2.find_all('p')
    # print(ContentPNum2)
    # print(len(ContentPNum2))

    RSdocumentNumList=[]
    RSbePunishedList=[]
    RSprincipalList=[]
    RSlawEnforcementList=[]
    RSpunishedDateList=[]
    RScontentList=[]
    RSagencyList=[]
    RSTitleList= []
    RSdataIdList=[]

    if ConetentResponseSoupOld.find("<table")!=-1:
        # http://www.nxld.gov.cn/xxgk/xzcf/201808/t20180828_1023074.html
        if ContentTdNum // ContentTrNum == 22:
            print("全文是一个1行22格表格形式的")
            SoupTr = BeautifulSoup(ConetentResponseSoupOld,'lxml')
            SoupTr = SoupTr.find_all('tr')
            SoupTr = SoupTr[2:]
            for tr in SoupTr:
                SoupTd = BeautifulSoup(str(tr), 'lxml')
                SoupTd = SoupTd.find_all('td')
                RSdocumentNumList.append(SoupTd[0].text.strip())
                RSTitleList.append(SoupTd[1].text.strip())
                RSbePunishedList.append(SoupTd[6].text.strip())
                RSpunishedDateList.append(SoupTd[14].text.strip())
                RSagencyList.append(SoupTd[17].text.strip())
                RSlawEnforcementList.append(SoupTd[17].text.strip())
                RSprincipalList.append(SoupTd[12].text.strip())
                cont = "<p>处罚类别1:"+SoupTd[2].text.strip()+"</p>\n<p>处罚类别2:"+SoupTd[3].text.strip()+"</p>\n<p>处罚事由:"+SoupTd[4].text.strip()+"</p>\n<p>处罚依据:"+SoupTd[5].text.strip()+"</p>\n<p>行政相对人名称:"+SoupTd[6].text.strip()+ "</p>\n<p>行政相对人代码_1(统一社会信用代码):"+SoupTd[7].text.strip()+ "</p>\n<p>行政相对人代码_2(组织机构代码):"+SoupTd[8].text.strip()+"</p>\n<p>行政相对人代码_3(工商登记码):"+SoupTd[9].text.strip()+"</p>\n<p>行政相对人代码_4(税务登记号):"+SoupTd[10].text.strip()+"</p>\n<p>行政相对人代码_5(居民身份证号):"+SoupTd[11].text.strip()+"</p>\n<p>法定代表人姓名:"+SoupTd[12].text.strip()+"</p>\n<p>处罚结果:"+SoupTd[13].text.strip()+"</p>\n<p>处罚时间:"+SoupTd[14].text.strip()+"</p>\n<p>处罚截止期:"+SoupTd[15].text.strip()+"</p>\n<p>公示期限年限1或者3年限（数字）1或者3:"+SoupTd[16].text.strip()+"</p>\n<p>处罚机构:"+SoupTd[17].text.strip()
                RScontentList.append(cont)
                RSdataIdList.append(RSdataId)
        # http://www.nxld.gov.cn/xxgk/xzcf/./201708/t20170814_431170.html
        if ContentTdNum // ContentTrNum == 19:
            print("全文是一个1行19格表格形式的")
            SoupTr = BeautifulSoup(ConetentResponseSoupOld, 'lxml')
            SoupTr = SoupTr.find_all('tr')
            SoupTr = SoupTr[2:]
            for tr in SoupTr:
                SoupTd = BeautifulSoup(str(tr), 'lxml')
                SoupTd = SoupTd.find_all('td')
                RSdocumentNumList.append(SoupTd[0].text.strip())
                RSTitleList.append(SoupTd[1].text.strip())
                RSbePunishedList.append(SoupTd[5].text.strip())
                RSpunishedDateList.append(SoupTd[13].text.strip())
                RSagencyList.append(SoupTd[15].text.strip())
                RSlawEnforcementList.append(SoupTd[15].text.strip())
                RSprincipalList.append(SoupTd[11].text.strip())
                cont = "<p>处罚类别:"+SoupTd[2].text.strip()+"</p>\n<p>处罚事由:"+SoupTd[3].text.strip()+"</p>\n<p>处罚依据:"+SoupTd[4].text.strip()+"</p>\n<p>行政相对人名称:"+SoupTd[5].text.strip()+ "</p>\n<p>行政相对人代码_1(统一社会信用代码):"+SoupTd[6].text.strip()+ "</p>\n<p>行政相对人代码_2(组织机构代码):"+SoupTd[7].text.strip()+"</p>\n<p>行政相对人代码_3(工商登记码):"+SoupTd[8].text.strip()+"</p>\n<p>行政相对人代码_4(税务登记号):"+SoupTd[9].text.strip()+"</p>\n<p>行政相对人代码_5(居民身份证号):"+SoupTd[10].text.strip()+"</p>\n<p>法定代表人姓名:"+SoupTd[11].text.strip()+"</p>\n<p>处罚结果:"+SoupTd[12].text.strip()+"</p>\n<p>处罚时间:"+SoupTd[13].text.strip()+"</p>\n<p>处罚截止期:"+SoupTd[14].text.strip()+"</p>\n<p>处罚机构:"+SoupTd[15].text.strip()
                RScontentList.append(cont)
                RSdataIdList.append(RSdataId)
        # http://www.nxld.gov.cn/xxgk/xzcf/201711/t20171121_589655.html
        if ContentTdNum//ContentTrNum == 2 or ContentTdNum//ContentTrNum == 3 :
            print("全文是一个1行3格表格形式的")
            if ConetentResponseSoupOld.find("<thead>")!=-1:
                ConetentResponseSoupOld = re.sub('<thead>.*?</thead>','',ConetentResponseSoupOld,flags=re.S|re.M)
                SoupTr = BeautifulSoup(ConetentResponseSoupOld,'lxml')
                SoupTr = SoupTr.find_all('tr')
            else:
                SoupTr = BeautifulSoup(ConetentResponseSoupOld, 'lxml')
                SoupTr = SoupTr.find_all('tr')
                # 第一个tr包含了参数说明  http://www.nxld.gov.cn/xxgk/xzcf/201708/t20170814_431164.html
                if (SoupTr[0].text.strip()).find("序号")!=-1:
                    SoupTr = SoupTr[1:]
                #  第二个tr包含了参数说明 http://www.nxld.gov.cn/xxgk/xzcf/201708/t20170814_431155.html
                elif (SoupTr[1].text.strip()).find("序号")!=-1:
                    SoupTr = SoupTr[2:]
            SoupTd = BeautifulSoup(str(SoupTr), 'lxml')
            SoupTd = SoupTd.find_all('td')
            RSdocumentNumList.append(SoupTd[2].text.strip())
            RSTitleList.append(SoupTd[5].text.strip())
            RSbePunishedList.append(SoupTd[17].text.strip())
            RSpunishedDateList.append(SoupTd[41].text.strip())
            RSagencyList.append(SoupTd[47].text.strip())
            RSlawEnforcementList.append(SoupTd[47].text.strip())
            RSprincipalList.append(SoupTd[35].text.strip())
            cont = "<p>处罚类别:"+SoupTd[8].text.strip()+"</p>\n<p>处罚事由:"+SoupTd[11].text.strip()+"</p>\n<p>处罚依据:"+SoupTd[14].text.strip()+"</p>\n<p>行政相对人名称:"+SoupTd[17].text.strip()+ "</p>\n<p>行政相对人代码_1(统一社会信用代码):"+SoupTd[20].text.strip()+ "</p>\n<p>行政相对人代码_2(组织机构代码):"+SoupTd[23].text.strip()+"</p>\n<p>行政相对人代码_3(工商登记码):"+SoupTd[26].text.strip()+"</p>\n<p>行政相对人代码_4(税务登记号):"+SoupTd[29].text.strip()+"</p>\n<p>行政相对人代码_5(居民身份证号):"+SoupTd[32].text.strip()+"</p>\n<p>法定代表人姓名:"+SoupTd[35].text.strip()+"</p>\n<p>处罚结果:"+SoupTd[38].text.strip()+"</p>\n<p>处罚时间:"+SoupTd[41].text.strip()+"</p>\n<p>处罚截止期:"+SoupTd[44].text.strip()+"</p>\n<p>"+"</p>\n<p>处罚机构:"+SoupTd[47].text.strip()
            RScontentList.append(cont)
            RSdataIdList.append(RSdataId)
    else:
        print("这里不是表格形式的")
        # http://www.nxld.gov.cn/xxgk/xzcf/./201711/t20171106_552199.html
        if  ConetentResponseSoupOld.find("附件下载")!=-1:
            print("这里全文就是一个附件形式的，需要点时间提取出来")
            adjunct = re.findall(re.compile(r'<a.*?href="(.*?)".*?>(.*?)</a>', re.I | re.S), str(ConetentResponseSoupOld))
            if adjunct:
                for i in adjunct:
                    print(i)
                    baseUrl =ContentSrc[:ContentSrc.rfind("/")+1]
                    print(baseUrl)
                    rsDocuniqueSign = i[0]  # 附件标签中的url地址
                    rsDocName = i[1]  # 附件的名i在
                    rsDocuniqueSign = rsDocuniqueSign.replace("./",'')
                    xiaZai = str(i)
                    # 提取附件是那种类型
                    rsDoc1 = re.findall(re.compile(r'.*?.doc', re.I), xiaZai)
                    rsDoc2 = re.findall(re.compile(r'.*?.docx', re.I), xiaZai)
                    rsXlsx = re.findall(re.compile(r'.*?.xlsx', re.I), xiaZai)
                    rsXls = re.findall(re.compile(r'.*?.xls', re.I), xiaZai)
                    if rsDoc1 :
                        rsDocName = rsDocName + ".doc"
                        rsDocName = rsDocName.replace("/", '_')
                        SavePath = SavePath % (rsDocName)
                        if rsDocuniqueSign.find("http") == -1:
                            rsDocuniqueSign = "%s" % (baseUrl) + rsDocuniqueSign
                        else:
                            rsDocuniqueSign = rsDocuniqueSign
                        # print(rsDocuniqueSign)
                        try:
                            r = requests.get(rsDocuniqueSign, headers=header, timeout=30)
                            with open(SavePath, "wb") as f:
                                f.write(r.content)
                            f.close()
                        except:
                            pass

                            # 下载xls文件
                    if rsDoc2:
                        rsDocName = rsDocName + ".docx"
                        rsDocName = rsDocName.replace("/", '_')
                        SavePath = SavePath % (rsDocName)
                        if rsDocuniqueSign.find("http") == -1:
                            rsDocuniqueSign = "%s" % (baseUrl) + rsDocuniqueSign
                        else:
                            rsDocuniqueSign = rsDocuniqueSign
                        # print(rsDocuniqueSign)
                        try:
                            r = requests.get(rsDocuniqueSign, headers=header, timeout=30)
                            with open(SavePath, "wb") as f:
                                f.write(r.content)
                            f.close()
                        except:
                            pass

                            # 下载xls文件
                    if rsXlsx:
                        rsDocName = rsDocName + ".xlsx"
                        rsDocName = rsDocName.replace("/", '_')
                        SavePath = SavePath % (rsDocName)
                        if rsDocuniqueSign.find("http") == -1:
                            rsDocuniqueSign = baseUrl + rsDocuniqueSign
                        else:
                            rsDocuniqueSign = rsDocuniqueSign
                        # print(rsDocuniqueSign)
                        r = requests.get(rsDocuniqueSign, header)
                        with open(SavePath, "wb") as f:
                            f.write(r.content)
                        f.close()
                    if rsXls:
                        rsDocName = rsDocName + ".xls"
                        # print(rsDocName)
                        SavePath1 = SavePath % (rsDocName)
                        print(SavePath1)
                        rsDocuniqueSign = baseUrl + rsDocuniqueSign
                        print(rsDocuniqueSign)
                        r = requests.get(rsDocuniqueSign, header)
                        with open(SavePath1, "wb") as f:
                            f.write(r.content)
                        f.close()
                        readbook = xlrd.open_workbook(r"%s"%(SavePath1))
                        sheet = readbook.sheet_by_index(0)  # 索引的方式，从0开始
                        nrows = sheet.nrows  # 获取最大行,从0开始
                        ncols = sheet.ncols  # 列，从0开始
                        # lng = sheet.cell_value(1, 4)  # 获取 x行x列的表格值
                        if ncols == 22:
                            print("这个文件是一个1行22列的")
                            for nrow in range(2, nrows):
                                RSdocumentNumList.append(str(sheet.cell_value(nrow, 0)))
                                RSTitleList.append(str(sheet.cell_value(nrow, 1)))
                                RSbePunishedList.append(str(sheet.cell_value(nrow,6)))
                                RSprincipalList.append(str(sheet.cell_value(nrow,12)))
                                RSlawEnforcementList.append(str(sheet.cell_value(nrow,17)))
                                data =  xlrd.xldate_as_tuple(sheet.cell_value(nrow, 14), 0)
                                data = str(data[0])+"年"+str(data[1])+"月"+str(data[2])+"日"
                                RSpunishedDateList.append(data)
                                RSagencyList.append(str(sheet.cell_value(nrow,17)))
                                cont = "<p>处罚类别1:" + str(sheet.cell_value(nrow, 2)) + "</p>\n<p>处罚类别2:" + str(sheet.cell_value(nrow, 3)) + "</p>\n<p>处罚事由:" + str(sheet.cell_value(nrow,4)) + "</p>\n<p>处罚依据:" + str(sheet.cell_value(nrow, 5)) + "</p>\n<p>行政相对人名称:" + str(sheet.cell_value(nrow,6)) + "</p>\n<p>行政相对人代码_1(统一社会信用代码):" + str(sheet.cell_value(nrow, 7)) + "</p>\n<p>行政相对人代码_2(组织机构代码):" + str(sheet.cell_value(nrow, 8))+ "</p>\n<p>行政相对人代码_3(工商登记码):" + str(sheet.cell_value(nrow, 9) )+ "</p>\n<p>行政相对人代码_4(税务登记号):" + str(sheet.cell_value(nrow,10)) + "</p>\n<p>行政相对人代码_5(居民身份证号):" + str(sheet.cell_value(nrow, 11)) + "</p>\n<p>法定代表人姓名:" + str(sheet.cell_value(nrow,12)) + "</p>\n<p>处罚结果:" + str(sheet.cell_value(nrow, 13)) + "</p>\n<p>处罚时间:" + str(data) + "</p>\n<p>处罚截止期:" + str(sheet.cell_value(nrow, 15)) + "</p>\n<p>公示期限年限1或者3年限（数字）1或者3:" + str(sheet.cell_value(nrow,16)) + "</p>\n<p>处罚机构:" + str(sheet.cell_value(nrow, 17))
                                RScontentList.append(cont)
                                RSdataIdList.append(RSdataId)
                        else:
                            print("自己查看是一行几列的，没处理")
        else:
            print("这里不是附件形式的，直接从网页中提取")
            soupCont = BeautifulSoup(ConetentResponseSoupOld,'lxml')
            soupCont = soupCont.find_all('p')
            RSlawEnforcementList.append(RSlawEnforcement)
            RSdocumentNumList.append(RSdocumentNum)
            RSbePunishedList.append(soupCont[0].text.strip().replace("当 事 人：",''))
            RSprincipalList.append('')
            RSpunishedDateList.append(RSTime)
            RScontentList.append(ConetentResponseSoupOld)
            RSagencyList.append(RSlawEnforcement)
            RSTitleList.append(RSTitle)
            RSdataIdList.append(RSdataId)

    return RSdocumentNumList, RSbePunishedList, RSprincipalList, RSlawEnforcementList, RSpunishedDateList, RScontentList, RSagencyList,RSTitleList,RSdataIdList
