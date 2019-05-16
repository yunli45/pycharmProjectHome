# coding:utf-8
import requests
import re
from bs4 import BeautifulSoup
from lxml import etree
str1 = """ 
<p style="TEXT-ALIGN: left">津滨市场监管 食 罚 {2015}22号</p>
"""
# print(str1.find("<table"))
# print(str1.rfind("</table>"))
table = str1[str1.find("<table"):str1.rfind("</table>")+8]
# print(table)
notable = re.sub(str1[str1.find("<table"):str1.rfind("</table>")+8],'',str1)
print(notable)





