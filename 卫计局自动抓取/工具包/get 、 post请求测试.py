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
from 工具包 import 链接数据库,附件下载程序,预处理模块, 提取信息, 动态访问
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
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '232',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Mobile Safari/537.36'}
    response = requests.post(url= url,  params=data, headers=headers)
    # response = response.content.decode('gb18030')
    response = response.content.decode('utf-8')
    print(response)
    return response
#
def getReq1(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Mobile Safari/537.36'
    }

    response = requests.get(url )
    response = response.content.decode('utf-8')
    # 'Content-Type': 'image/gif',
    # 'Content-Type': 'application/vnd.ms-excel'
    print(response)
    # ss = response.headers
    # print(ss['Content-Type'])
    # response = response.content.decode('gb18030')
    # response = response.content.decode('utf-8')
    print(response)
    return response



para = {
    'page': '2',
    'treeName': '办公厅',
    'treeCodeId': '03abc986600345c383c34297ddbe4813',
    'topicType': '',
    'serverType': '',
    'styleType': '',
    'manuscript.websiteId': '03abc986600345c383c34297ddbe4813',
    'keyword': '',
    'searchType': '',
    'publishedTimeStr': '',
    'pagination_input': ''
}
ul = 'http://www.nhc.gov.cn/cms-search/xxgk/searchList.htm?type=search'
postReq(ul,para)

