import re
from bs4 import BeautifulSoup


# ConetentResponseSoupOld ;还没有修改的全文
def  Table(ConetentResponseSoupOld):
    if ConetentResponseSoupOld.find("行政处罚信息公开表")!=-1:
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
        MsoNormalTable = re.sub('<st1.*?>', '', str(MsoNormalTable), flags=re.M | re.S).replace("</st1:chsdate>",
                                                                                                '').replace("\n",
                                                                                                            '').replace(
            "\t", '')
        MsoNormalTable = re.sub('<p.*?>', '', str(MsoNormalTable), flags=re.M | re.S).replace('</p>', '').replace(
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
        TableResultList =[]
        if TDList != []:
            RSdocumentNum = TDList[0][-1].text.strip()  # s书文号
            RSbePunished = TDList[1][-1].text.strip()  # 被处罚人或机构
            RSlawEnforcement = TDList[2][-1].text.strip()  # 处罚机构
            RSprincipal = TDList[3][-1].text.strip()  # 法人
            RSagency = TDList[-2][-1].text.strip()  # 处罚机构
            RSpunishedDate = TDList[-1][-1].text.strip()  # 处罚时间
            RScontent = "主要违法违规事实（案由）:" + TDList[4][-1].text.strip() + "\n 行政处罚依据:" + TDList[5][
                -1].text.strip() + "\n 行政处罚决定:" + TDList[6][-1].text.strip()
            TableResultList.append(RSdocumentNum)
            TableResultList.append(RSbePunished)
            TableResultList.append(RSlawEnforcement)
            TableResultList.append(RSprincipal )
            TableResultList.append(RSagency)
            TableResultList.append(RSpunishedDate)
            TableResultList.append(RScontent)
        return  TableResultList







