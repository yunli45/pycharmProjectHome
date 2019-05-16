# -*- coding: utf-8 -*-
"""
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""

import re
import requests
import chardet
import sys
import json
import time
from L河南.工具包 import 链接数据库,附件下载程序,预处理模块, 提取信息, 动态访问
# print(sys.getdefaultencoding())

def getReq(url):

    proxies = {
        "HTTP": "http://183.146.179.159:9000",
        "HTTP": "http://112.85.164.150:9999",
        "HTTP": "http://115.151.4.237:9999"
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10-12.0; WOW64) AppleWebKit/537.36 (KHTML,  like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10-12.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}

    querystring = {
        'm':'content' ,
        'c' :'index',
        'a':'lists',
        'catid':'253',
        'page':'1'
    }
    response = requests.get(url, headers=headers, params=querystring, proxies =proxies)
    print("这次使用的饿IP事："+str(proxies))
    response = response.content.decode("utf-8")
    print(response)

    return response


def postReq(url, data):
    response = requests.post(url, data)
    # response = response.content.decode('gb18030')
    response = response.content.decode('utf-8')
    print(response)
    return response

def getReq1(url):
    response = requests.get(url)
    # 'Content-Type': 'image/gif',
    # 'Content-Type': 'application/vnd.ms-excel'

    ss = response.headers
    print(ss['Content-Type'])
    # response = response.content.decode('gb18030')
    # response = response.content.decode('utf-8')
    print(response)
    return response

# rs = getReq("https://www.toutiao.com/api/search/content/?offset={0}&keyword={1}&count={2}".format(0,"公安+执法资格+考试", 20))
ul = 'http://www.hnwsjsw.gov.cn/channels/458.shtml'
para = {
            'getMlXzcfMhJson':'',
            'commonquery':'',
            "page": "1",

        }
#
rs = getReq1(ul)
# 动态访问.get_index_page_1(ul)


from bs4 import BeautifulSoup

# content_soup = BeautifulSoup(rs, 'lxml')
# content_soup = content_soup.find_all('ul', attrs={'class': 'creditsearch-tagsinfo-ul'})
# area = ''
# if content_soup:
#     for i in content_soup:
#         li = i.find_all("li")
#         if li:
#             book_number = li[1].text.replace("'", '').replace("行政处罚决定书文号：", '')
#             legal_person = li[13].text.replace("'法定代表人姓名:", '').replace("'", '').replace("法定代表人姓名：", '')
#             if legal_person == "null":
#                 legal_person = ''
#             # print(legal_person)
#             date = li[16].text.replace("'", '').replace("处罚决定日期：", '')
#             cont = str(li).replace('[', '').replace(']', '').replace(',', '\n').replace("null", '')
#             cont = re.sub('<li.*?>', '<li style="list-style-type:none;">', str(cont))
#             cont = re.sub('<strong.*?>', '', str(cont))
#             cont = re.sub('</strong.*?>', '', str(cont)).replace('?', '')
# print(cont)

src = "../publicity/GetPunishInfo.html?id=42"
print(src.replace("..",''))