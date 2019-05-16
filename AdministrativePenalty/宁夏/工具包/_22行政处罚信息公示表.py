import re
from bs4 import BeautifulSoup
from 宁夏.工具包  import 替换标签
import requests


# def publicTable(ConetentResponseSoupOld, ConetentResponse, ContentPNum, ContentPNum1, ContentTrNum, ContentTdNum,
#                    RSTime,RSTitle,SavePath,header):
def publicTable(ConetentResponseSoupOld, ConetentResponse, ContentPNum, ContentPNum1, ContentTrNum, ContentTdNum,
                   RSTime,RSTitle,SavePath,header):
    RSdocumentNum = []
    RSbePunished= []
    RSprincipal= []
    RSlawEnforcement= []
    RSpunishedDate= []
    RScontent= []
    RSagency = []
    RSTitleList =[]
    # 全文是一个表格
    if ConetentResponseSoupOld.find("<table")!=-1:
        soupTable = BeautifulSoup(ConetentResponseSoupOld,'lxml')
        soupTable = soupTable.find_all('tr')
        # 一行8格形式 http://www.nxfda.gov.cn/html/ajgg/20180531/11940.html
        if ContentTrNum * 8 == ContentTdNum:
            print("一行8格形式")
            trList = []
            for tr in soupTable:
                trList.append(tr)

            for i in trList:
                ttr =i
                soupTd = BeautifulSoup(str(ttr), 'lxml')
                soupTd = soupTd.find_all('td')

                RSdocumentNum.append(soupTd[1].text.strip())
                RSbePunished.append('')
                RSprincipal.append('')
                RSlawEnforcement.append('稽查局')
                RSpunishedDate.append(soupTd[-2].text.strip())
                content =  "案件类别:"+ soupTd[3].text.strip()+"\n案值（万元）:"+soupTd[4].text.strip()+"\n处罚结果:"+soupTd[5].text.strip()
                RScontent.append(content)
                RSagency.append('稽查局')
                RSTitleList.append(soupTd[2].text.strip())
        # 一行9格形式 http://www.nxfda.gov.cn/html/ajgg/20180608/11820.html
        elif  ContentTrNum * 9 == ContentTdNum:
            print("一行9格形式")
            trList = []
            for tr in soupTable:
                trList.append(tr)
            for i in trList:
                ttr =i
                soupTd = BeautifulSoup(str(ttr), 'lxml')
                soupTd = soupTd.find_all('td')

                RSdocumentNum.append(soupTd[1].text.strip())
                RSbePunished.append('')
                RSprincipal.append('')
                RSlawEnforcement.append(soupTd[-2].text.strip())
                RSpunishedDate.append(soupTd[-3].text.strip())
                content =  "案件类别:"+ soupTd[3].text.strip()+"\n案值（万元）:"+soupTd[4].text.strip()+"\n处罚结果:"+soupTd[5].text.strip()
                RScontent.append(content)
                RSagency.append(soupTd[-2].text.strip())
                RSTitleList.append(soupTd[2].text.strip())
        # 一行10格形式 http://www.nxfda.gov.cn/html/ajgg/20171219/10754.html
        elif ContentTrNum * 10 == ContentTdNum:
            print("一行10格形式")
            trList = []
            for tr in soupTable:
                trList.append(tr)
            for i in trList:
                ttr = i
                soupTd = BeautifulSoup(str(ttr), 'lxml')
                soupTd = soupTd.find_all('td')
                RSdocumentNum.append(soupTd[1].text.strip())
                RSbePunished.append(soupTd[6].text.strip())
                RSprincipal.append(RSTime)
                RSlawEnforcement.append('稽查局')
                RSpunishedDate.append(soupTd[-1].text.strip())
                content = "处罚类别:" + soupTd[3].text.strip() + "\n处罚事由:" + soupTd[
                    4].text.strip() + "\n处罚依据:" + soupTd[5].text.strip()+"\n行政处罚结果:"+ soupTd[8].text.strip()
                RScontent.append(content)
                RSagency.append('稽查局')
                RSTitleList.append(soupTd[2].text.strip())
        # 一行11格形式  http://www.nxfda.gov.cn/html/ajgg/20171122/10409.html
        elif ContentTrNum * 11 == ContentTdNum:
            print("一行11格形式")
            trList = []
            for tr in soupTable:
                trList.append(tr)
            for i in trList:
                ttr = i
                soupTd = BeautifulSoup(str(ttr), 'lxml')
                soupTd = soupTd.find_all('td')

                RSdocumentNum.append(soupTd[1].text.strip())
                RSbePunished.append(soupTd[3].text.strip())
                RSprincipal.append(soupTd[5].text.strip())
                RSlawEnforcement.append(soupTd[-2].text.strip())
                RSpunishedDate.append(soupTd[-2].text.strip())
                content = "主要违法事实:" + soupTd[6].text.strip() + "\n行政处罚的种类和依据:" + soupTd[
                    7].text.strip() + "\n行政处罚的履行方式和期限:" + soupTd[8].text.strip()
                RScontent.append(content)
                RSagency.append(soupTd[-2].text.strip())
                RSTitleList.append(soupTd[2].text.strip())
        else:
            RSdocumentNum.append('')
            RSbePunished.append('')
            RSprincipal.append('')
            RSlawEnforcement.append('稽查局')
            RSpunishedDate.append(RSTime)
            RScontent.append(ConetentResponse)
            RSagency.append('稽查局')
            RSTitleList.append( RSTitle)


    # 全文不是一个表格
    if ConetentResponseSoupOld.find("<table") == -1:
        RSdocumentNum.append('')
        RSbePunished .append('')
        RSprincipal.append('')
        RSlawEnforcement.append('')
        RSpunishedDate.append(RSTime)
        RScontent.append(ConetentResponseSoupOld)
        RSagency.append('宁夏食品监管局')
        RSTitleList.append(RSTitle)
    return RSdocumentNum, RSbePunished, RSprincipal, RSlawEnforcement, RSpunishedDate, RScontent, RSagency,RSTitleList






















































