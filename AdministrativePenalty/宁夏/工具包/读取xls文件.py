import xlrd

# pip3 install xlrd
# （1）读文件
sheet = xlrd.open_workbook(r"F:\行政处罚数据\宁夏\固原市隆德县人民政府\行政处罚信息公示数据标准6-1（4件）.xls.xls")
nrows = sheet.nrows  # 获取最大行，以0为索引
ncols = sheet.ncols  # 获取最大列
num= 3
row_num = 3
col_num =3
# （2）打开工作簿，以0开始为索引
sheet = sheet.sheet_by_index(0)  # 索引的方式，从0开始
# 读取整行的数据
row_value = sheet.row_values(num-1)  # num为第几行，从0开始的索引
# 读取整列的数据
col_value = sheet.col_values(num-1)# col为第几列
#（4）读取某行某列元素
value = sheet.row_values(row_num)[col_num].value # 用行索取：
value = sheet.col_values(col_num)[row_num].value # 用列索取：
value = sheet.cell(row_num,col_num).value #用单元格获取：

# 用xlrd读取excel表里的时间时，读出来的东西都是一堆浮点类型。
# xlrd 的 xldate_as_tuple 函数可以做转换。
# 扩展阅读 http://blog.chinaunix.net/uid-9185047-id-444998.html
for nrow in range(2, nrows):
    print(sheet.cell_value(nrow, 13))
    data = xlrd.xldate_as_tuple(sheet.cell_value(nrow, 14), 0)
    print(data)
    data = str(data[0]) + "年" + str(data[1]) + "月" + str(data[2]) + "日"
    print(data)