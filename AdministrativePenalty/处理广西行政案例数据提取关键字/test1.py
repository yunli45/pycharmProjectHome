# coding:utf-8
import re
from bs4 import BeautifulSoup
import requests

str1 ="""
<p>当事人：上海羽展汽车销售有限公司</p><p>地址：上海市宝山区沪太路3198号</p><p>法定代表人：张羽展</p><p>依据《中华人民共和国保险法》（以下简称《保险法》）的有关规定，我局对你公司涉嫌违法一案进行了调查、审理，并依法向你公司告知了作出行政处罚的事实、理由、依据以及你公司依法享有的权利，你公司未提出陈述申辩意见。本案现已审理终结。</p><p>经查，你公司存在利用业务便利为其他机构和个人牟取不正当利益的行为。2016年1月至2017年6月期间，阳光财产保险股份有限公司上海市分公司（以下简称“阳光上分”）将自身直接业务虚构为你公司中介业务，你公司收到手续费后，扣除一定费用，将剩余部分返还给阳光上分。</p><p>上述事实，有现场检查事实确认书、相关人员谈话笔录、相关业务、财务凭证复印件等证据证明。</p><p>综上，我局决定作出如下处罚：你公司存在利用业务便利为其他机构或个人牟取不正当利益的行为，违反了《保险法》第一百三十一条第八项的规定，根据《保险法》第一百六十五条的规定，责令你公司改正，处罚款6万元。</p><p>你公司应当在接到本处罚决定书之日起15日内持所附缴款码到财政部指定的12家代理银行中的任一银行进行同行缴款，逾期，将每日按罚款数额的3%加处罚款。</p><p>你公司如对本处罚决定不服，可在收到本处罚决定书之日起60日内向中国银行保险监督管理委员会申请行政复议，也可在收到本处罚决定书之日起6个月内直接向有管辖权的人民法院提起行政诉讼。复议和诉讼期间，上述决定不停止执行。</p><p><p>上海保监局</p></p><p style="text-align: center;"><p>2018年5月21日</p></p>


"""
#
# rs = re.findall(re.compile(r'<p.*?>[〇 一 二 三 四 五 六 七 八 九 十]{4,5}年[〇 一 二 三 四 五 六 七 八 九 十]{1,2}月[〇 一 二 三 四 五 六 七 八 九 十]{1,3}日\s*</p>'),str1)
#
# print(rs)
# print(len(rs[0]))
# str2 = str1.find(rs[0])
# print(str1[str2+1])
# str3 = str1.find(rs[0])+len(rs[0])
# # str4 = str1[str2:str3]
# print(str1[str2:str3])
# print(str1.replace(str1[str2:str3],'2018年5月22日'))

str1 = re.sub(r'<span .*?>', '', str1, flags=re.I).replace('</span>', '').replace('</SPAN>', '')

# 这一组是去除<FONT> ....</FONT>
str1 = re.sub(r'<FONT .*?>', '', str1, flags=re.I).replace('</FONT>', '').replace('</font>', '')

# 这一组是去除<p style="text-align:center;line-height:38px">...</p>
str1 = re.sub(r'<p .*?>', '<p>', str1)
# # 这一组是去除<P style="text-align:center;line-height:38px">...</P>
str1 = re.sub(r'<P .*?>', '<p>', str1)
str1 = re.sub(r'</P>', '</p>', str1)

# # 这一组是去除<img width=  ..... #ddd"/>
# str1 = re.sub(r'<img .*? solid #ddd"/>', '', str1)

# 这一组是去除<?xml:namespace prefix = o ns = "urn:schemas-microsoft-com:office:office" /><o:p></o:p>
str1 = re.sub(r'<?xml:namespace .*?>', '', str1)
str1 = str1.replace('<o:p></o:p>', '').replace('<o:p>', '').replace('</o:p>', '')

# 这一组是去除<<strong>> ....</<strong>>
str1 = re.sub(r'<strong.*?>', '', str1, flags=re.I).replace('</strong>', '')

# <st1:chsdate year="2017" month="3" day="30" islunardate="False" isrocdate="False" w:st="on">...</st1:chsdate>
str1 = re.sub(r'<st1:chsdate .*?>', '', str1)
str1 = re.sub(r'</st1:chsdate>', '', str1)
# print('这是第' + str(j) + '条数据' + str1.encode('latin-1').decode('gbk'))

# 这组是替换掉去开头<p><p> =><p>
str1 = str1.replace(r'<p><p>', '<p>')

# 这组是 替换掉<br> 为</p><p>
str1 = str1.replace('<br>', '</p><p>').replace('</br>', '</p><p>').replace('<br/>', '</p><p>')
str1 = str1.replace('<BR>', '</p><p>').replace('</BR>', '</p><p>')

# 这组是处理<p></p>这种无用标签和所有的&nbsp;
str1 = re.sub(r'&nbsp;', '', str1)
str1 = re.sub(r'<p></p>', '', str1)
# 设置编码，python3
# str1 = str1.encode('latin-1').decode('gbk')
# str1 = str1.encode("utf-8").decode("latin1")

# 处理标题
title = re.findall(re.compile(r'<p>.*?[监 罚 处].*?\d号</p>'), str1)
if title!=[]:
    ti = str1.find(title[-1])
    if ti<100  and len(title[-1])<20 :
        title[0] = title[0].replace("<p>",'').replace("</p>",'')
        str1 = str1.replace(title[0],''.join(['<p style="text-align: center;">'+title[-1]+'</p>']))

# 这组是处理落款时间的格式
yy = r'<p>\s*[ 零 ○ 0 O o 〇 Ｏ 一 二 三 四 五 六 七 八 九 十]{4}年[一 二 三 四 五 六 七 八 九 十 〇]{1,2}月[一 二 三 四 五 六 七 八 九 十 〇]{1,2}日\s*</p>|<p>\s*\d{4}年\d{1,2}月\d{1,2}日</p>'
str2 = re.findall(re.compile(yy), str1)
if len(str2) != 0 :
    find1 = str1.find(str2[-1])
    if find1 > 100  and len(str2[-1])<20 :
        str2[-1] = str2[-1].replace("<p>",'').replace("</p>",'')
        # 如果存在落款时间就加上个<p style="text-align: right;"> 让它居右显示
        str1 = str1.replace(str2[-1], ''.join(['<p style="text-align: right;">'+ str2[-1]+ '</p>']))
    else:
        pass
else:
    pass

# 这组是处理落款单位

yy2 = r'<p>[\u4E00-\u9FA5\uF900-\uFA2D]+[\局 ,\协会,\厅]</p>'
rs = re.findall(re.compile(yy2), str1)
print(rs)
if len(rs) != 0:
    find1 = str1.find(rs[-1])
    if find1 > 100 and len(rs[-1])<20:
        rs[-1] = rs[-1].replace("<p>",'').replace("</p>",'')
        str1 = str1.replace(rs[-1], ''.join(['<p style="text-align: right;">' + rs[-1] + '</p>']))
    else:
        pass

else:
    pass
str3 = str1

print(str3)