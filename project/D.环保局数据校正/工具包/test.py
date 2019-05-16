import openpyxl
import re


# 读取excel文件返回该文件所有数据和最大的行数，保存数据的时候记得使用返回的第一个参数 【data.save(excelFilePath)】
def open_excel_file(excel_file_path):
    data = openpyxl.load_workbook(excel_file_path)
    active = data.active
    table = data['Sheet1']
    rows = table.max_row

    return data, table, rows


# 读取表格中数据检查并处理全文中超链接、附件等是否有问题
def handle(excel_file_path):
    data_table_rows = open_excel_file(excel_file_path)
    data = data_table_rows[0]
    table = data_table_rows[1]
    rows = data_table_rows[2]
    for row in range(1, rows+1):
        print("正在读取第："+str(row)+"行的数据")
        # title = table['E{0}'.format(row)].value
        title = table['E%s'%(row)].value
        cont1 = table['U%s'%(row)].value
        cont2 = table['V%s'%(row)].value
        cont3 = table['W%s'%(row)].value
        cont4 = table['X%s'%(row)].value

        cont = (cont1 + str(cont2) + str(cont3) + str(cont4)).replace("None", '')
        cont = cont.replace('/"/', '"/').replace('/"', '"')
        now_cont = cont
        print("处理标签后的全文now_cont"+title+"\n\n"+str(now_cont))
        # cont, 附件不在链接没改, 附件不在链接修改了, 附件存在链接没改

        # 处理过后的数据重新存放在新的四列中，每个单元格寸3万个字符，超出的放入下一个单元格
        if 0 < len(now_cont) < 30000:
            table['U%s'%(row)] = now_cont

        elif 0 < len(now_cont) < 60000:
            table['U%s' % (row)] = now_cont[:30000]
            table['V%s' % (row)] = now_cont[30000:]

        elif 0 < len(now_cont) < 90000:
            table['U%s' % (row)] = now_cont[:30000]
            table['V%s' % (row)] = now_cont[30000:60000]
            table['W%s' % (row)] = now_cont[60000:]

        elif 0 < len(now_cont) < 120000:
            table['U%s' % (row)] = now_cont[:30000]
            table['V%s' % (row)] = now_cont[30000:60000]
            table['W%s' % (row)] = now_cont[60000:90000]
            table['X%s' % (row)] = now_cont[90000:]

        else:
            print("这条数据好像超出12万个字符。貌似存在问题，请查看下啊" + str(title)+"\n")
    data.save(excel_file_path)


handle('D:\Python\PyCharm 20181.4\project\project1\环保局数据校正\环境保护-校对完整版-上送版.xlsx')
