# -*- coding=gbk -*-
import re
import openpyxl
from bs4 import BeautifulSoup


data = openpyxl.load_workbook(r'E:\Python\PyCharm\project\project1\���������ƾ�\���ƾ�(2).xlsx')
active = data.active
table = data['Sheet1']
rows = table.max_row

for row in range(2,rows+1) :
    # rowH = 'H%s'%(row)
    print("���ڴ����" +str(row)+"������")
    rowE = 'E%s'%(row)  #  ����ʱ��
    rowE_va = table[rowE].value
    rowF = 'F%s' % (row)  #
    rowF_va = table[rowF].value
    rowG = 'G%s' % (row)  # ʵʩʱ��
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
    #     ������׼1 = re.findall(r'����������׼>������׼>.*?', rowB_va)
    #     if rowB_va =='�л����񹲺͹�������������ίԱ��>�ȵ���Ŀ>���':
    #         table[rowC] =  '�����������߷�����'
    #     elif ������׼1 !=[]:
    #         table[rowC] =  '������׼'
    #     else:
    #         table[rowC] = '������������ίԱ���˾�ļ�'

    # ���ڸ�ʽת��Ϊ 8λ����

    print()




    print("�Ѵ����" +str(row)+"������")
data.save(r'E:\Python\PyCharm\project\project1\���������ƾ�\���ƾ�(2).xlsx')