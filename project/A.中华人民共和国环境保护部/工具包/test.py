# coding:UTF-8
import re
from bs4 import BeautifulSoup
import requests
from 中华人民共和国环境保护部.工具包 import 链接数据库,附件下载程序,判断url前面的点返回完整的请求地址
from bs4 import BeautifulSoup
# url = """http://wfs.mee.gov.cn/gywrfz/zhgl/xzjz/201212/t20121225_244225.htm"""
# url = """http://www.mee.gov.cn/gkml/sthjbgw/qt/201712/t20171229_428952.htm"""
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10-12.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
#                         'User-Agent': 'Mozilla/5.0 (Windows NT 10-12.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'
#          }
# response = requests.get(url,headers=headers)
# status_code = response.status_code
#
# response = response.content.decode('utf-8')
# print(response)
# print(status_code)

"""
<p align="center"><a href="./W020120803412205247618.pdf" _fcksavedurl="C:\Documents and Settings\fcy\桌面\9标准\《环境保护产品技术要求紫外线消毒装置》(报批稿).pdf" oldsrc="W020120803412205247618.pdf">环境保护产品技术要求 紫外线消毒装置(HJ 2522—2012)</a><br></p>
"""
处理中的全文="""
../../../gkml/sthjbgw/qt/201808/t20180828_454315.htm
"""

print(处理中的全文[处理中的全文.rfind("/")+1:])





# 处理中的全文= 处理中的全文.replace(r'<a href="./W020121205595071029516.pdf" oldsrc="W020121205595071029516.pdf">环境标志产品技术要求 印刷 第二部分: 商业票据印刷(HJ 2530-2012)</a>',newA)
# print(处理中的全文)





超链接本地地址= '/datafolder/环保局/标准文本/'
conentSrc='http://kjs.mee.gov.cn/hjbhbz/bzwb/other/hbcpjsyq/201208/t20120803_234327.shtml'
SavePath ='F:\环保局\%s'
处理中的全文 = re.sub(r'\f','/',处理中的全文)
处理中的全文 = re.sub(r'\\','/',处理中的全文)
# print(处理中的全文)






# 先看全文有没有附件
# adjunct = re.findall(r'.*?(pdf|docx|doc|xlsx|xls|rar|zip)',处理中的全文,flags=re.I)
# if adjunct!=[]:
#     print("yesssws")
#     # 匹配附件一共有几个，进行循环下载和替换格式，先匹配附件的整个a标签的内容用于后面使用
#     adjunct1 = re.findall(re.compile(r'<a.*?href=".*?".*?>.*?</a>', re.I | re.S), 处理中的全文)
#     if adjunct1:
#         for src in adjunct1:
#             print("需要替换的超链接"+str(src))
#             # 匹配出每一个a标签的超链接和文件名
#             adjunc2 = re.findall(re.compile(r'<a.*?href="(.*?)".*?>(.*?)</a>', re.I | re.S), src)
#             if adjunc2 != []:
#                 print("adjunc2"+str(adjunc2))
#                 intactALink = adjunc2[0][0]
#                 intactALink =  判断url前面的点返回完整的请求地址.returnSRC().returnSrc(conentSrc,intactALink,conentSrc)
#                 intactAName = adjunc2[0][1]
#                 intactALink1 = intactALink[intactALink.rfind("/")+1:]
#                 附件下载程序.DownloadData(intactALink,'',intactALink1,SavePath)
#                 # 替换成本地的格式
#                 nweA = r'<a href="%s%s">%s</a>' % (超链接本地地址,intactALink1,intactAName)
#                 print("老的a标签"+str(src))
#                 print("新的A标签"+str(nweA))
#                 处理中的全文 = re.sub(src, nweA, 处理中的全文)
#                 print("处理中的全文"+处理中的全文)
# # print(处理中的全文)