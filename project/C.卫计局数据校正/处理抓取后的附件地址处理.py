# -*- coding=gbk -*-
import re
import openpyxl
from bs4 import BeautifulSoup


data = openpyxl.load_workbook(r'E:\Python\PyCharm\project\project1\大邑县卫计局\卫计局(2).xlsx')
active = data.active
table = data['Sheet1']
rows = table.max_row

for row in range(2,rows+1) :
    # rowH = 'H%s'%(row)
    print("正在处理第" +str(row)+"行数据")
    rowE = 'E%s'%(row)  #  发布时间
    rowE_va = table[rowE].value
    rowF = 'F%s' % (row)  #
    rowF_va = table[rowF].value
    rowG = 'G%s' % (row)  # 实施时间
    rowG_va = table[rowG].value
    rowH = 'H%s' % (row)  #
    rowH_va = table[rowH].value
    # if rowR_va==None:
    #     pass
    # else:
    #     # rowR_va = rowR_va.replace('?', '')
    #     rowR_va = re.sub('<div.*?>', '<div>', rowR_va)
    #     rowR_va = re.sub('class=".*?"', '', rowR_va)
    #     rowR_va = re.sub('id=".*?"', '', rowR_va)
    #     rowR_va = re.sub('<style.*?>.*?</style>', '', rowR_va,flags=re.I|re.S)
    #     rowR_va = re.sub('style=".*?"', '', rowR_va)
    #     rowR_va = str(rowR_va).replace('<!--', '')
    #     rowR_va = str(rowR_va).replace('-->', '')
    #     rowR_va = str(rowR_va).replace('?', '')
    # table[rowR] = rowR_va

    # if  rowB_va ==None:
    #     pass
    # else:
    #     卫生标准1 = re.findall(r'卫生计生标准>卫生标准>.*?', rowB_va)
    #     if rowB_va =='中华人民共和国国家卫生健康委员会>热点栏目>解读':
    #         table[rowC] =  '卫生计生政策法规解读'
    #     elif 卫生标准1 !=[]:
    #         table[rowC] =  '卫生标准'
    #     else:
    #         table[rowC] = '国家卫生健康委员会各司文件'

    # 日期格式转化为 8位数字

    print()




    print("已处理第" +str(row)+"行数据")
data.save(r'E:\Python\PyCharm\project\project1\大邑县卫计局\卫计局(2).xlsx')