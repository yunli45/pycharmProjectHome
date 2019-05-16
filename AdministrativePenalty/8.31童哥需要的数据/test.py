import re
import pymssql
import requests
import openpyxl

data = openpyxl.load_workbook(r"E:\Python\PyCharm\project\AdministrativePenalty\8.31童哥需要的数据\xxx.xlsx")
active = data.active
table = data['Sheet1']
maxRow = table.max_row

for row in range(2,maxRow+1):
    rowH = 'H%s'%(row)
    rowH_Va = table[rowH].value

    rowH_Va = re.sub("<table.*?>.*?</table>",'',str(rowH_Va),flags=re.M|re.S)
    t = rowH_Va.find(r"<span class=\"wzxq2_lianjie\">【字体")
    rowH_Va= rowH_Va[0:t]
    table[rowH]=rowH_Va
data.save(r"E:\Python\PyCharm\project\AdministrativePenalty\8.31童哥需要的数据\xxx.xlsx")




