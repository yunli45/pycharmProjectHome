import datetime
import re
from fake_useragent import UserAgent
from selenium import webdriver
import requests
import time
from 大邑县卫计局.工具包 import 链接数据库,附件下载程序,预处理模块


def readTableRecord():
    sql = "select max(id) from 大邑县卫生局数据"
    con = 链接数据库.getConnect(sql)
    conn = con[0]
    cursor = con[1]
    row = cursor.fetchone()
    print(row)  # (None, )
readTableRecord()



# def creatCookie():
#     header = {"User-Agent": UserAgent().random}
#     jar = requests.cookies.RequestsCookieJar()
#     # 不加cookie会返回202状态吗
#     jar.set(name='banggoo.nuva.cookie', value='1|W71xc|W71xb', path='/', domain='www.nhfpc.gov.cn')
#     cookies = jar
#     return header, cookies
# header,cookies = creatCookie()
# url = "http://www.nhfpc.gov.cn/zwgk/jdjd/201809/9eb3f794162046a3a9305f5bd1fe9cc4.shtml"
# response = requests.get(url,headers=header)
# status_code = response.status_code
# if status_code == 200:
#     response = response.content.decode('utf-8', errors='ignore')
# elif status_code == 202:
#     while True:
#         print("jj")
#         header1, cookies1 = creatCookie()
#         if status_code == 200:
#             break
#         else:
#             time.sleep(1)
#             response = requests.get(url, headers=header1, cookies=cookies1)
#             status_code = response.status_code
#             response = response.content.decode('utf-8', errors='ignore')
# print(response)


