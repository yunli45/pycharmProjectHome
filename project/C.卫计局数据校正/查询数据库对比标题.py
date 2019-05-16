from 卫计局数据校正 import 链接数据库
import openpyxl
import requests
from bs4 import BeautifulSoup
import time
import re
import datetime
from fake_useragent import UserAgent
from selenium import webdriver
from 大邑县卫计局.工具包 import 链接数据库,附件下载程序,预处理模块
from 大邑县卫计局.工具包.判断url前面的点返回完整的请求地址 import returnSRC
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}



def readExcel(excelPath):
    data = openpyxl.load_workbook(excelPath)
    active = data.active
    table = data['Sheet1']
    rows = table.max_row
    listTitle = []
    for row in range(2,rows+1):
        #     print("正在读取第："+str(row)+"的数据")
        rowA = 'A%s' % (row)  # 标题
        rowA_Va = table[rowA].value
        # print(rowC_Va)

        # SQL = "select 标题,这条数据的完整请求url,来源模块首页url,这条数据的url,来源库名称 from 大邑县卫生局数据 where 标题='%s' and 来源库名称='中华人民共和国国家卫生健康委员会>热点栏目>解读'"%(str(rowA_Va).strip())
        # print(SQL)
        SQL = "select 标题,这条数据的完整请求url,来源模块首页url,这条数据的url,来源库名称 from 大邑县卫生局数据 where 标题='%s'" % (
            str(rowA_Va).strip())

        RS = 链接数据库.getConnect(SQL)[2]
        # print(RS)
        if RS !=None:
            # print(RS)
            标题 = RS[0]
            完整的URL = RS[1]
            indexUrl = RS[2]
            url = RS[3]
            来源库名称 =  RS[4]
            print(来源库名称)
            # listTitle.append(标题)


    print(listTitle)

readExcel('E:\Python\PyCharm\project\project1\卫计局\根据标题修改文本.xlsx')


