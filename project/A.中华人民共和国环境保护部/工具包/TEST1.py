import re
str1 = """
老的a标签<a href="./W020121205595071029516.pdf">环境标志产品技术要求 印刷 第二部分: 商业票据印刷(HJ 2530-2012)</a>
"""
KK = '<a href="./W020121205595071029516.pdf">环境标志产品技术要求 印刷 第二部分: 商业票据印刷(HJ 2530-2012)</a>'
LL = '<a href="/datafolder/环保局/标准文本/W020121205595071029516.pdf">环境标志产品技术要求 印刷 第二部分: 商业票据印刷(HJ 2530-2012)</a>'
str2 =re.sub(KK,LL,str1)
print(str2)