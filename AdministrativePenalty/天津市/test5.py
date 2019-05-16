import re
import requests
from bs4 import BeautifulSoup



data={
'doObj':'{"lx":1,"id":100000,"name":"信息公开目录","pagenum":"2","host":"xxgk.tj.spb.gov.cn","sousouVal":""}'
}
# res=requests.post(url='http://xxgk.tj.spb.gov.cn/extranet/getContent.jsp',data=data)
response2=requests.post(url='http://xxgk.tj.spb.gov.cn/extranet/detail.html?yc_id=c6717499-3f5e-4f04-84f2-7cead3dcc9bd')
response2 = response2.content.decode('UTF-8')
# print(response2)
soup2 = BeautifulSoup(response2,'lxml')
rs2 = soup2.find('div', attrs={'class': 'content'})
# print(rs2)
rs2 = str(rs2)
#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
#
# 提取文书号等信息
#
#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #

rs3 = re.sub(r'<tr.*?>', '', str(rs2), flags=re.M | re.S).replace('</tr>', '')
rs3 = re.sub(r'<td.*?>', '', str(rs3), flags=re.M | re.S).replace('</td>', '')
rs3 = re.sub(r'<span.*?>', '', str(rs3), flags=re.M | re.S).replace('</span>', '')
rs3 = re.sub(r'<table.*?>', '', str(rs3), flags=re.M | re.S).replace('</table>', '')
rs3 = re.sub(r'<p.*?><o:p> </o:p></p>', '', str(rs3)).replace('<o:p></o:p>', '')
rs3 = re.sub(r'<b .*?><o:p> </o:p></b>', '', str(rs3))
rs3 = re.sub(r'<st1:.*?>', '', str(rs3)).replace('</st1:chsdate>', '').replace('<a name="TCSignYear"></a>', '')
rs3 = re.sub(r'<o:p>\xa0</o:p>', '', str(rs3))
# rs3 = re.sub(r'<font.*?>', '', str(rs3)).replace('</font>', '')
rs3 = re.sub(r'<p.*?class="MsoNormal".*?>', '<p class="MsoNormal">', str(rs3), flags=re.M | re.S)
rs3 = rs3.replace("'", "''").replace('\u2002', ' ').replace('<b>', '').replace('</b>', '')





print(rs3)














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