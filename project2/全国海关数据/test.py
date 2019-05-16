import re

title = "天津海关关于徐州耀展进出口贸易有限公司出口侵犯“耐克钩图形”商标权运动鞋案行政处罚决定书（编号：津关法知字〔2018〕048号"
title_1 = title.replace("）", '')
if str(title).find('编号') != -1:
    print(title_1)
    rr = re.findall(r'.*?关于(.*?)侵犯.*?编号[: ：](.*)', str(title_1))
    print(rr)
    print(66)
else:
    rr = re.findall(r'.*?关于(.*?)侵犯.*?（(.*?)）', str(title))
print(rr)

title = '中华人民共和国亦庄海关行政处罚决定书（ 京经关缉违字〔2019〕013号）'
rr = re.findall('行政处罚决定书（(.*?)）', str(title))
print(rr[0])

title = '中华人民共和国北京海关行政处罚决定书京关缉违字［2016］007 号'.replace("（", '').replace("）",'')
if title.find("违规") != -1:
    rr = title[0:title.find("违规")]
    book = title[title.find("行政处罚决定书")+7:]
    print(rr)
    print(book)
else:
    jg = title[:title.find("行政处罚决定书")]
    book = title[title.find("行政处罚决定书") + 7:]
    print(jg)
    print(book)