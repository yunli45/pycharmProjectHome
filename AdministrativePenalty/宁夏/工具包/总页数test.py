import re
import requests
from bs4 import BeautifulSoup


headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
url = "http://www.cbrc.gov.cn/zhuanti/xzcf/getPcjgXZCFDocListDividePage/ningxia.html?current=4"

response = requests.get(url,headers=headers)
response = response.content.decode('utf-8')
print(response)
rs = re.findall(re.compile(r'<a.*?href="(.*?)">末页</a>'),str(response))
print(rs)















