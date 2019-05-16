#coding:utf-8
import re
from bs4 import BeautifulSoup
import requests
headers = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Connection':'keep-alive',
'Cookie': 'JSESSIONID=BB9EDFB4377B7FBD351CE198280F9E1B',
'Host': 'www.linhe.gov.cn',
'Referer':'http://www.linhe.gov.cn/sites/lhqzf/list.jsp?ColumnID=88&SiteID=lhqzf',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}
r = requests.get("http://www.linhe.gov.cn/ueditor/jsp/upload/image/20171102/1509614258352074717.png", headers=headers, timeout=1)
with open("F:\行政处罚数据\内蒙古\巴彦淖尔市_临河区\jj.png", "wb") as f:
    f.write(r.content)
f.close()



