# -*- coding=gbk -*-
import re
import openpyxl
from bs4 import BeautifulSoup


data = openpyxl.load_workbook(r'test.xlsx')
active = data.active
table = data['Sheet1']
rows = table.max_row

for row in range(2,rows+1) :
    # rowH = 'H%s'%(row)
    rowA = 'A%s'%(row)
    rowA_va = table[rowA].value
    rowB = 'B%s'%(row)
    print(type(rowA_va))


data.save(r'test.xlsx')

