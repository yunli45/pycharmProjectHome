# coding:utf-8
import  requests
from  bs4 import BeautifulSoup
import  re

response = requests.get("http://scjg.tj.gov.cn/heping/zwgk/xzcfxx/17109.html")
ConetentResponse = response.content.decode('UTF-8')

ConetentResponseSoup = BeautifulSoup(ConetentResponse, 'lxml')
ConetentResponseSoupOld = ConetentResponseSoup.find('div', attrs={'class': 'news_content'})
# ConetentResponseSoupOld = str(ConetentResponseSoupOld)
# print(ConetentResponseSoupOld)
# ContentTrNum = BeautifulSoup(str(ConetentResponseSoupOld), 'lxml')
ContentTrNum = len(ConetentResponseSoupOld.findAll('tr'))
print("这条数据有："+str(ContentTrNum)+"个tr")
ContentPNum = len(ConetentResponseSoupOld.findAll('p'))
print("这条数据有："+str(ContentPNum)+"个P")

ConetentResponse = re.sub('<span.*?>', '', str(ConetentResponseSoupOld), flags=re.S | re.M).replace('</span>', '')
ConetentResponse = re.sub('<col.*?>', '', ConetentResponse)
ConetentResponse = re.sub('<tr.*?>', '', ConetentResponse)
ConetentResponse = re.sub('<td.*?>', '', ConetentResponse)
ConetentResponse = re.sub('<table.*?>', '', ConetentResponse).replace('<td>', '<p><p>').replace('</td>','</p><p>').replace('tr','p').replace(
    'tbody', 'p').replace('table', '').replace('</p><p></p>', '</p><p>')
ConetentResponse = re.sub(r'<p.*?><o:p> </o:p></p>', '', str(ConetentResponse)).replace('<o:p></o:p>', '')
ConetentResponse = re.sub(r'<st1:.*?>', '', str(ConetentResponse)).replace('</st1:chsdate>', '').replace(
    '<a name="TCSignYear"></a>', '')
ConetentResponse = re.sub(r'<o:p>\xa0</o:p>', '', str(ConetentResponse))
ConetentResponse = re.sub(r'</p></p><p><p', '</p><p', str(ConetentResponse)).replace('</p></p>', '</p>')
ConetentResponse = re.sub(r'<font.*?>', '', str(ConetentResponse)).replace('</font>', '')

ConetentResponse = ConetentResponse.replace("'", "''").replace('\u2002', ' ').replace('<b>', '').replace('</b>', '')
# print(ConetentResponse)
if str(ConetentResponseSoupOld).find("<table") != -1 and 1<= ContentTrNum <=4 and ContentPNum <=3:
    # 先去除多余的标签
    # print("这是大表 有2个tr")
    ConetentResponseTable = re.sub('<span.*?>', '', str(ConetentResponseSoupOld)).replace('</span>', '')
    ConetentResponseTable = re.sub('<p.*?>', '', str(ConetentResponseTable)).replace('</p>', '')
    ConetentResponseTable = re.sub('<font.*?>', '', str(ConetentResponseTable)).replace('</font>', '')

    # 替换标签
    ConetentResponseTable = re.sub('<col.*?>','',ConetentResponseTable).replace('</colgroup>','')
    ConetentResponseTable = re.sub('<td.*?>','<td>',ConetentResponseTable)
    ConetentResponseTable = re.sub('<tr.*?>','<tr>',ConetentResponseTable).replace("<td><td>","<td>")
    # print(ConetentResponseTable)
    TableSoup = BeautifulSoup(ConetentResponseTable,'lxml')
    # print(TableSoup)
    # print(TableSoup.find_all('tr'))
    # print(ConetentResponseTable)
    list1 = []
    for idx, tr in enumerate(TableSoup.find_all('tr')):
       list1.append(idx)
       TrDocNUM = re.findall(re.compile(r'.*?津[市 场 罚].*?\d.*?号</td>'), str(tr))
       if TrDocNUM:
            TrNUM =idx
            print(TrNUM)
# if list1[-1]:  # 不等于0就会去表格的最后一行tr，方便取值
#         tds = tr.find_all('td')
#         当事人 = tds[1].text.strip()
#         法人 = tds[4].text.strip()
#         书文号 = tds[5].text.strip()
#         主要违法事实 = tds[6].text.strip()
#         处罚种类 = tds[7].text.strip()
#         处罚依据 = tds[8].text.strip()
#         行政处罚的履行方式和期限 = tds[9].text.strip()
#         作出行政处罚决定机关名称 = tds[10].text.strip()
#         日期 = tds[11].text.strip()
#
#         print(当事人)
#         print(法人)
#         print(书文号)
#         print(主要违法事实)
#         print(处罚种类)
#         print(处罚依据)
#         print(行政处罚的履行方式和期限)
#         print(作出行政处罚决定机关名称)
#         print(日期)
