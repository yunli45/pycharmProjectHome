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

# print(sys.getdefaultencoding())

def getReq(url):
    response = requests.get(url)

    # response = response.content.decode('gb18030')
    html_encoding = response.encoding
    response = response.content.decode("utf-8")
    return response


def postReq(url, data):
    response = requests.post(url, data)
    response = response.content.decode('gb18030')
    return response


para = "{'startrecord': '11', 'endrecord': '20', 'perpage': '10', 'totalRecord': '17706'}"
url_1 = 'http://www.cdx.gov.cn/article/151/11248.html'
ss = getReq(url_1)
print(ss)