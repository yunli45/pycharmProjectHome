# -*- coding:GBK  -*-
import re
import requests
from bs4 import BeautifulSoup


header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}

response2=requests.get(url='http://scjg.tj.gov.cn/hebei/zwgk/xzcfxx/28434.html',headers =header)
# response2=requests.post(url='http://xxgk.tj.spb.gov.cn/extranet/detail.html?yc_id=c6717499-3f5e-4f04-84f2-7cead3dcc9bd')
response2 = response2.content.decode('UTF-8')
# print(response2)
# soup2 = BeautifulSoup(response2,'lxml')
# rs2 = soup2.find('div', attrs={'class': 'content'})
# rs2 = soup2.find('div', attrs={'class': 'news_content'})
#
RS = re.sub('<span.*?>', '', str(response2), flags=re.S | re.M).replace('</span>', '')
# RS = re.sub('<col.*?>', '', RS)
# RS = re.sub('<tr.*?>', '', RS)
# RS = re.sub('<td.*?>', '', RS)
# RS = re.sub('<table.*?>', '', RS).replace('<td>', '<p><p>').replace('</td>', '</p><p>').replace('tr', 'p').replace(
#     'tbody', 'p').replace('table', '').replace('</p><p></p>','</p><p>')
RS = re.sub(r'</p></p><p><p','</p><p',RS).replace('</p></p>','</p>')
RS = re.sub(r'<td.*?>','<td>',RS)
# rs = re.findall(re.compile(r'<a href="(.*?)" target="_blank" title="(.*?)">.*?</a>.*?<span>(.*?)</span>',re.S),str(rs2))
# RS = BeautifulSoup(RS,'lxml')
# rs = RS.findAll('table')
rs = re.sub(r'<p.*?>','',str(RS)).replace('</p>','')
rs = re.sub(r'<span.*?>','',str(rs)).replace('</span>','')
# print(rs)
# print(rs2)
rs = BeautifulSoup(rs,'lxml')
# rs = len(rs.findAll('tr'))
# if rs== 3 or 4:
#     print( "sdd")
# for i in rs:
#     print(i)
# for idx, tr in enumerate(rs.find_all('tr')):
school = 0
pro_code = 1
pro_name = 2
xuewei = 3
pdf = 4
for ids,tr in  enumerate(rs.find_all('tr')):
    td = tr.find_all('td')
    try:
        if ids==0:
            ���ĺ�=td[-1].text.strip()
            print(���ĺ�)
        if ids == 1:
            ������ = td[-1].text.strip()
            print(������)
        if ids==2:
           print(td[-1])
        if ids ==3:
            ��λ = td[-1].text.strip()
            print(��λ)
        if ids==5:
           print(td[-1].text.strip())
        if ids ==6:
            print(td[-1].text.strip())

        if ids == 9:
            print(td[-1].text.strip())
        if ids == 10:
            print(td[-1].text.strip())
    except IndexError as e:
        pass
    # if idx !=0:
    #     # print(tr)
    #
    #     title = tds[1]
    #     title1= tds[2]
    #     print(title1)
#     if idx !=0:
#         tds = tr.find_all('td')
#         title = tds[0].contents[0]
#         ������ = tds[1].contents[0]
#         �������������� = tds[4].contents[0]
#         �����������ĺ� =  tds[5].contents[0]
#         ȫ�� = "��ҪΥ����ʵ��"+ tds[6].contents[0]+"��\n ��������:"+tds[7].contents[0]+"��\n �������ݣ�"+tds[8].contents[0]+"��\n �������������з�ʽ������:"+tds[9].contents[0]
#         ������������������������ =  tds[10].contents[0]
#         ���������������� = tds[11].contents[0]
# print(title)
# print(ȫ��)
# print(��������������)
# print(�����������ĺ�)
# print(������������������������)
# print(����������������)



# rs = re.findall(re.compile(r'[^<](.*?��.*?��)'),str1)
# rs = re.sub(r'.*?>','',str(rs[0]))

# print(re.sub(r'.*?>','',str(rs[0])))














# print(re.findall(re.compile(r'"pub_date":"(.*?)"'),respo))
# print(re.findall(re.compile(r'"generate_date":"(.*?)"'),respo))
# print(re.findall(re.compile(r'"yc_id":"(.*?)"'),respo))
# print(re.findall(re.compile(r'"doc_number":"(.*?)"'),respo))
# print(re.findall(re.compile(r'"info_name":"(.*?)"'),respo))

# soup = BeautifulSoup(response,'lxml')
# soup1 = soup.find('tbody')
# rs = re.findall(re.compile(r'<td><a href="(.*?)".*?>(.*?)</a></td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>',re.S|re.M),str(soup1))
#
#
# print(rs)