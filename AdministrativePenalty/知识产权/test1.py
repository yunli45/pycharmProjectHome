# coding :utf-8
import openpyxl

data = openpyxl.load_workbook(r'E:\Python\PyCharm\project\AdministrativePenalty\知识产权\知识产权局—政策解读.xlsx')
# data.active
table = data['Sheet1']
rows = table.max_row
print(type(table['A%s'%(rows)].value))
政策解读总记录数1 = 100
# if 政策解读总记录数1 != 政策解读总记录数:
#     table['A%s'%(rows+1)].value = 政策解读总记录数1

data.save(r'E:\Python\PyCharm\project\AdministrativePenalty\知识产权\知识产权局—政策解读.xlsx')