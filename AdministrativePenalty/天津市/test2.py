    # coding=utf-8
from bs4 import BeautifulSoup
import re
import requests
import pymssql
url = ('http://www.cbrc.gov.cn/chinese/home/docView/359AAE7956524D0A9DC1CF7B4F26E5B1.html')
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
response = requests.get(url,headers = header)
response = response.content.decode('UTF-8')
# print(response)
soup = BeautifulSoup(response,'lxml')



str1 = """
<div class="Section1">
<p class="MsoNormal"><span lang="EN-US" style="font-size:15.0pt;font-family:黑体;
mso-hansi-font-family:黑体;mso-bidi-font-family:黑体"><o:p> </o:p></span></p>
<p align="center" class="MsoNormal" style="text-align:center"><span lang="EN-US" style="font-size:15.0pt;font-family:黑体;mso-hansi-font-family:黑体;mso-bidi-font-family:
黑体"><o:p> </o:p></span></p>
<p align="center" class="MsoNormal" style="text-align:center"><span style="font-size:15.0pt;font-family:黑体;mso-hansi-font-family:黑体;mso-bidi-font-family:
黑体">天津银监局行政处罚信息公开表<span lang="EN-US"><o:p></o:p></span></span></p>
<p align="center" class="MsoNormal" style="text-align:center"><span lang="EN-US" style="font-size:14.0pt;font-family:黑体;mso-hansi-font-family:黑体;mso-bidi-font-family:
黑体"><o:p> </o:p></span></p>
<p align="center" class="MsoNormal" style="text-align:center"><span style="font-size:14.0pt;font-family:楷体_GB2312;mso-hansi-font-family:楷体_GB2312;
mso-bidi-font-family:楷体_GB2312">（平安银行股份有限公司）<span lang="EN-US"><o:p></o:p></span></span></p>
<table border="1" cellpadding="0" cellspacing="0" class="MsoNormalTable" style="border-collapse:collapse;mso-table-layout-alt:fixed;border:none;
 mso-border-alt:solid windowtext .5pt;mso-padding-alt:0cm 5.4pt 0cm 5.4pt;
 mso-border-insideh:.5pt solid windowtext;mso-border-insidev:.5pt solid windowtext">
<tr style="height:1.0cm;mso-height-rule:exactly">
<td colspan="3" style="width:221.4pt;border:solid windowtext 1.0pt;
  mso-border-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt;height:1.0cm;
  mso-height-rule:exactly" width="295">
<p align="center" class="MsoNormal" style="text-align:center"><b><span style="font-size:14.0pt;font-family:仿宋_GB2312;mso-hansi-font-family:仿宋_GB2312;
  mso-bidi-font-family:仿宋_GB2312">行政处罚决定书文号</span></b></p>
</td>
<td style="width:221.4pt;border:solid windowtext 1.0pt;border-left:
  none;mso-border-left-alt:solid windowtext .5pt;mso-border-alt:solid windowtext .5pt;
  padding:0cm 5.4pt 0cm 5.4pt;height:1.0cm;mso-height-rule:exactly" width="295">
<p class="MsoNormal"><span class="GramE"><span style="font-size:14.0pt;
  font-family:仿宋_GB2312;mso-hansi-font-family:仿宋_GB2312;mso-bidi-font-family:
  仿宋_GB2312">津银监罚决</span></span><span style="font-size:14.0pt;font-family:仿宋_GB2312;
  mso-hansi-font-family:仿宋_GB2312;mso-bidi-font-family:仿宋_GB2312">字〔<span lang="EN-US">2018</span>〕<span lang="EN-US">35</span>号<span lang="EN-US"><o:p></o:p></span></span></p>
</td>
</tr>
<tr style="height:1.0cm;mso-height-rule:exactly">
<td rowspan="3" style="width:73.8pt;border:solid windowtext 1.0pt;
  border-top:none;mso-border-top-alt:solid windowtext .5pt;mso-border-alt:solid windowtext .5pt;
  padding:0cm 5.4pt 0cm 5.4pt;height:1.0cm;mso-height-rule:exactly" width="98">
<p align="center" class="MsoNormal" style="text-align:center"><b><span style="font-size:14.0pt;font-family:仿宋_GB2312;mso-hansi-font-family:仿宋_GB2312;
  mso-bidi-font-family:仿宋_GB2312">被处罚当事人姓名或全称</span></b></p>
</td>
<td colspan="2" style="width:147.6pt;border-top:none;border-left:
  none;border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-left-alt:solid windowtext .5pt;
  mso-border-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt;height:1.0cm;
  mso-height-rule:exactly" width="197">
<p class="MsoNormal"><span style="font-size:14.0pt;font-family:仿宋_GB2312;
  mso-hansi-font-family:仿宋_GB2312;mso-bidi-font-family:仿宋_GB2312">个人姓名</span><span lang="EN-US" style="font-size:14.0pt"><o:p></o:p></span></p>
</td>
<td style="width:221.4pt;border-top:none;border-left:none;
  border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-left-alt:solid windowtext .5pt;
  mso-border-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt;height:1.0cm;
  mso-height-rule:exactly" width="295">
<p class="MsoNormal"><span style="font-size:14.0pt;font-family:仿宋_GB2312;
  mso-hansi-font-family:仿宋_GB2312;mso-bidi-font-family:仿宋_GB2312">—<span lang="EN-US"><o:p></o:p></span></span></p>
</td>
</tr>
<tr style="height:34.15pt;mso-height-rule:exactly">
<td rowspan="2" style="width:35.1pt;border-top:none;border-left:none;
  border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-left-alt:solid windowtext .5pt;
  mso-border-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt;layout-flow:
  vertical-ideographic;height:34.15pt;mso-height-rule:exactly" width="47">
<p align="center" class="MsoNormal" style="margin-top:0cm;margin-right:5.65pt;
  margin-bottom:0cm;margin-left:5.65pt;margin-bottom:.0001pt;text-align:center"><span style="font-size:14.0pt;font-family:仿宋_GB2312;mso-hansi-font-family:仿宋_GB2312;
  mso-bidi-font-family:仿宋_GB2312">单<span lang="EN-US"><span style="mso-spacerun:yes">  </span></span>位<span lang="EN-US"><o:p></o:p></span></span></p>
</td>
<td style="width:112.5pt;border-top:none;border-left:none;
  border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-left-alt:solid windowtext .5pt;
  mso-border-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt;height:34.15pt;
  mso-height-rule:exactly" width="150">
<p class="MsoNormal"><span style="font-size:14.0pt;font-family:仿宋_GB2312;
  mso-hansi-font-family:仿宋_GB2312;mso-bidi-font-family:仿宋_GB2312">名称<span lang="EN-US"><o:p></o:p></span></span></p>
</td>
<td style="width:221.4pt;border-top:none;border-left:none;
  border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-left-alt:solid windowtext .5pt;
  mso-border-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt;height:34.15pt;
  mso-height-rule:exactly" width="295">
<p align="left" class="MsoNormal" style="text-align:left"><span style="font-size:
  14.0pt;font-family:仿宋_GB2312;mso-hansi-font-family:仿宋_GB2312;mso-bidi-font-family:
  仿宋_GB2312">平安银行股份有限公司<span lang="EN-US"><o:p></o:p></span></span></p>
</td>
</tr>
<tr style="height:48.6pt;mso-height-rule:exactly">
<td style="width:112.5pt;border-top:none;border-left:none;
  border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-left-alt:solid windowtext .5pt;
  mso-border-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt;height:48.6pt;
  mso-height-rule:exactly" width="150">
<p class="MsoNormal"><span style="font-size:14.0pt;font-family:仿宋_GB2312;
  mso-hansi-font-family:仿宋_GB2312;mso-bidi-font-family:仿宋_GB2312">法定代表人（主要负责人）姓名<span lang="EN-US"><o:p></o:p></span></span></p>
</td>
<td style="width:221.4pt;border-top:none;border-left:none;
  border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-left-alt:solid windowtext .5pt;
  mso-border-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt;height:48.6pt;
  mso-height-rule:exactly" width="295">
<p align="left" class="MsoNormal" style="text-align:left"><span style="font-size:
  14.0pt;font-family:仿宋_GB2312;mso-hansi-font-family:仿宋_GB2312;mso-bidi-font-family:
  仿宋_GB2312">谢永林<span lang="EN-US"><o:p></o:p></span></span></p>
</td>
</tr>
<tr style="height:71.3pt;mso-height-rule:exactly">
<td colspan="3" style="width:221.4pt;border:solid windowtext 1.0pt;
  border-top:none;mso-border-top-alt:solid windowtext .5pt;mso-border-alt:solid windowtext .5pt;
  padding:0cm 5.4pt 0cm 5.4pt;height:71.3pt;mso-height-rule:exactly" width="295">
<p align="center" class="MsoNormal" style="text-align:center"><b><span style="font-size:14.0pt;font-family:仿宋_GB2312;mso-hansi-font-family:仿宋_GB2312;
  mso-bidi-font-family:仿宋_GB2312">主要违法违规事实（案由）</span></b><span lang="EN-US" style="font-size:14.0pt"><o:p></o:p></span></p>
</td>
<td style="width:221.4pt;border-top:none;border-left:none;
  border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-left-alt:solid windowtext .5pt;
  mso-border-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt;height:71.3pt;
  mso-height-rule:exactly" width="295">
<p class="MsoNormal"><span style="font-size:14.0pt;font-family:仿宋_GB2312;
  mso-hansi-font-family:仿宋_GB2312;mso-bidi-font-family:仿宋_GB2312">贷前调查不到位，向环保未达标的企业提供融资；贷后管理失职，流动资金贷款被挪用<span lang="EN-US"><o:p></o:p></span></span></p>
</td>
</tr>
<tr style="height:166.2pt;mso-height-rule:exactly">
<td colspan="3" style="width:221.4pt;border:solid windowtext 1.0pt;
  border-top:none;mso-border-top-alt:solid windowtext .5pt;mso-border-alt:solid windowtext .5pt;
  padding:0cm 5.4pt 0cm 5.4pt;height:166.2pt;mso-height-rule:exactly" width="295">
<p align="center" class="MsoNormal" style="text-align:center"><span style="font-size:14.0pt;font-family:仿宋_GB2312;mso-hansi-font-family:仿宋_GB2312;
  mso-bidi-font-family:仿宋_GB2312">行政处罚依据</span><span lang="EN-US" style="font-size:14.0pt"><o:p></o:p></span></p>
</td>
<td style="width:221.4pt;border-top:none;border-left:none;
  border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-left-alt:solid windowtext .5pt;
  mso-border-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt;height:166.2pt;
  mso-height-rule:exactly" width="295">
<p class="MsoNormal"><span style="font-size:14.0pt;font-family:仿宋_GB2312;
  mso-hansi-font-family:仿宋_GB2312;mso-bidi-font-family:仿宋_GB2312">《中国银监会关于印发<span lang="EN-US">&lt;</span>节能减排授信工作指导意见<span lang="EN-US">&gt;</span>的通知》（银监发〔<span lang="EN-US">2007</span>〕<span lang="EN-US">83</span>号）第五条，《中国银监会关于印发绿色信贷指引的通知》（银监发〔<span lang="EN-US">2012</span>〕<span lang="EN-US">4</span>号）第十七条，《流动资金贷款管理暂行办法》第九条、第十三条、第三十条，《中华人民共和国银行业监督管理法》第二十一条、第四十六条。<span lang="EN-US"><o:p></o:p></span></span></p>
</td>
</tr>
<tr style="height:27.75pt;mso-height-rule:exactly">
<td colspan="3" style="width:221.4pt;border:solid windowtext 1.0pt;
  border-top:none;mso-border-top-alt:solid windowtext .5pt;mso-border-alt:solid windowtext .5pt;
  padding:0cm 5.4pt 0cm 5.4pt;height:27.75pt;mso-height-rule:exactly" width="295">
<p align="center" class="MsoNormal" style="text-align:center"><span style="font-size:14.0pt;font-family:仿宋_GB2312;mso-hansi-font-family:仿宋_GB2312;
  mso-bidi-font-family:仿宋_GB2312">行政处罚决定</span><span lang="EN-US" style="font-size:14.0pt"><o:p></o:p></span></p>
</td>
<td style="width:221.4pt;border-top:none;border-left:none;
  border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-left-alt:solid windowtext .5pt;
  mso-border-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt;height:27.75pt;
  mso-height-rule:exactly" width="295">
<p class="MsoNormal"><span style="font-size:14.0pt;font-family:仿宋_GB2312;
  mso-hansi-font-family:仿宋_GB2312;mso-bidi-font-family:仿宋_GB2312">罚款人民币<span lang="EN-US">50</span>万元<span lang="EN-US"><o:p></o:p></span></span></p>
</td>
</tr>
<tr style="height:30.05pt;mso-height-rule:exactly">
<td colspan="3" style="width:221.4pt;border:solid windowtext 1.0pt;
  border-top:none;mso-border-top-alt:solid windowtext .5pt;mso-border-alt:solid windowtext .5pt;
  padding:0cm 5.4pt 0cm 5.4pt;height:30.05pt;mso-height-rule:exactly" width="295">
<p align="center" class="MsoNormal" style="text-align:center"><span class="GramE"><span style="font-size:14.0pt;font-family:仿宋_GB2312;mso-hansi-font-family:仿宋_GB2312;
  mso-bidi-font-family:仿宋_GB2312">作出</span></span><span style="font-size:14.0pt;
  font-family:仿宋_GB2312;mso-hansi-font-family:仿宋_GB2312;mso-bidi-font-family:
  仿宋_GB2312">处罚决定的机关名称</span><span lang="EN-US" style="font-size:14.0pt"><o:p></o:p></span></p>
</td>
<td style="width:221.4pt;border-top:none;border-left:none;
  border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-left-alt:solid windowtext .5pt;
  mso-border-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt;height:30.05pt;
  mso-height-rule:exactly" width="295">
<p class="MsoNormal"><span style="font-size:14.0pt;font-family:仿宋_GB2312;
  mso-hansi-font-family:仿宋_GB2312;mso-bidi-font-family:仿宋_GB2312">天津银监局</span></p>
</td>
</tr>
<tr style="mso-yfti-lastrow:yes;height:26.95pt;mso-height-rule:exactly">
<td colspan="3" style="width:221.4pt;border:solid windowtext 1.0pt;
  border-top:none;mso-border-top-alt:solid windowtext .5pt;mso-border-alt:solid windowtext .5pt;
  padding:0cm 5.4pt 0cm 5.4pt;height:26.95pt;mso-height-rule:exactly" width="295">
<p align="center" class="MsoNormal" style="text-align:center"><span class="GramE"><span style="font-size:14.0pt;font-family:仿宋_GB2312;mso-hansi-font-family:仿宋_GB2312;
  mso-bidi-font-family:仿宋_GB2312">作出</span></span><span style="font-size:14.0pt;
  font-family:仿宋_GB2312;mso-hansi-font-family:仿宋_GB2312;mso-bidi-font-family:
  仿宋_GB2312">处罚决定的日期</span><span lang="EN-US" style="font-size:14.0pt"><o:p></o:p></span></p>
</td>
<td style="width:221.4pt;border-top:none;border-left:none;
  border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-left-alt:solid windowtext .5pt;
  mso-border-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt;height:26.95pt;
  mso-height-rule:exactly" width="295">
<p class="MsoNormal"><st1:chsdate day="28" islunardate="False" isrocdate="False" month="6" w:st="on" year="2018"><span lang="EN-US" style="font-size:14.0pt;font-family:仿宋_GB2312;mso-hansi-font-family:仿宋_GB2312;
   mso-bidi-font-family:仿宋_GB2312">2018</span><span style="font-size:14.0pt;
   font-family:仿宋_GB2312;mso-hansi-font-family:仿宋_GB2312;mso-bidi-font-family:
   仿宋_GB2312">年<span lang="EN-US">6</span>月<span lang="EN-US">28</span>日</span></st1:chsdate></p>
</td>
</tr>
</table>


"""

# rs2 = soup.find('div',attrs={'class':'Section1'})
rs2 = re.sub(r'<tr.*?>', '', str(str1), flags=re.M | re.S).replace('</tr>', '')
rs2 = re.sub(r'<td.*?>', '', str(rs2), flags=re.M | re.S).replace('</td>', '')
rs2 = re.sub(r'<span.*?>', '', str(rs2), flags=re.M | re.S).replace('</span>', '')
rs2 = re.sub(r'<table.*?>', '', str(rs2), flags=re.M | re.S).replace('</table>', '')
rs2 = re.sub(r'<p.*?><o:p> </o:p></p>', '', str(rs2)).replace('<o:p></o:p>', '')
rs2 = re.sub(r'<b .*?><o:p> </o:p></b>', '', str(rs2))
rs2 = re.sub(r'<st1:.*?>', '', str(rs2)).replace('</st1:chsdate>', '').replace('<a name="TCSignYear"></a>', '')
rs2 = re.sub(r'<o:p>\xa0</o:p>', '', str(rs2))
rs2 = re.sub(r'<p.*?class="MsoNormal".*?>', '<p class="MsoNormal">', str(rs2), flags=re.M | re.S)
# rs2 = re.sub(r'<p .*?></p>', '', str(rs2))
rs3 = rs2.replace("'", "''").replace('\u2002', ' ').replace('<b>', '').replace('</b>', '')
print(rs3)

MsoNormal = re.findall(re.compile(r'<p.*?class="MsoNormal".*?>(.*?)</p>', re.S), rs3)


RSdocumentNum = re.findall(re.compile(r'<p.*?>.*?(.*?津银.*?号).*?</p>'), rs3)  # 书文号
print("shuwenh")
print(RSdocumentNum)
RSlawEnforcement = re.findall(re.compile(r'机构名称(.*?)</p>', re.S),rs3)  # 被处罚机构或单位
RSlawEnforcement1 = re.findall(re.compile(r'单位名称(.*?)</p>', re.S), rs3)  # 被处罚机构或单位
RSpunishedDate = re.findall(re.compile(r'<p.*?>(.*?年.*?月.*?日)</p>'), rs3)
print("zheshishijain")
print(RSpunishedDate)
if RSdocumentNum:
    documentNum = RSdocumentNum[0]
else:
    documentNum = ''
if RSlawEnforcement:
    lawEnforcement = RSlawEnforcement[0]
elif RSlawEnforcement1:
    lawEnforcement = RSlawEnforcement1[0]
else:
    lawEnforcement = ''
if RSpunishedDate:
    punishedDate = RSpunishedDate[-1]

resTitle =''
bePunished = ''  # 被处罚人或机构
  # 受处罚时间
principal = ''  # 法定代表人
dataId = re.sub(r'.*/', '', '').replace(".html", '')
content =  rs3
uniqueSign = '222'  # url地址
address = '天津'  # 省份
area = '所有区县'  # 地区
agency = "中国银行业监督管理委员会天津监管局"  # 处罚机构
if len(content) <= 100:
    grade = -1  # 级别
elif 100 < len(content) <= 200:
    grade = 1  # 级别
elif 200 < len(content) <= 1500:
    grade = 2  # 级别
elif len(content) > 1500:
    grade = 0  # 级别
showId = '2'  # 系统ID
showAddress = None
showArea = None
conn = pymssql.connect(host='(local)', user='sa', password='123456', database='AdministrativePun')
            # 打开游标
cur = conn.cursor();
if not cur:
    raise Exception('数据库连接失败！')
else:
    print("数据库链接成功")
    sql1 = " INSERT INTO  crawlData2(dataId,title,documentNum,bePunished,principal,lawEnforcement,punishedDate,content,uniqueSign,address,area,agency,grade,showId,showAddress,showArea) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " % (  dataId, resTitle, documentNum, bePunished,principal,lawEnforcement,punishedDate,content,uniqueSign,address, area, agency,grade,showId,showAddress,showArea)


    print(sql1)
cur.execute(sql1)

conn.commit()
conn.close()



# rsList = re.findall(re.compile(r'<a href="(.*?)" target="_blank" title="(.*?)">.*?</a>.*?<span>(.*?)</span>', re.S | re.M),str(table))
# print(rsList)

# soup = BeautifulSoup(response,'lxml')
# table = soup.findAll('div',attrs={'class':'news_content'})
# RS = re.sub('<span.*?>','',str(table),flags=re.S|re.M).replace('</span>','')
# RS = re.sub('<col.*?>','',RS)
# RS = re.sub('<tr.*?>','',RS)
# RS = re.sub('<td.*?>','',RS)
# RS = re.sub('<table.*?>','',RS).replace('<td>','<p><p>').replace('</td>','</p><p>').replace('tr','p').replace('tbody','p').replace('table','').replace('</p><p></p>','</p><p>')
# print(RS)


# soup1 = BeautifulSoup(RS,'lxml')
# rs1 = soup1.findAll('p')
# for i in rs1:
#     print(i)
# print(rs1[29])
#
# list1 = [1,2,3,4,5,'六',7,8,9,0]
# for i in list1:
#     if str(i).find('六')!=-1:
#         print(list1[list1.index(i)-3])



# str1 ="""
# <p sy> 2018年5月23日 </p>
# <p sy> 2018年5月24日 </p>
# 机构名称：  上海浦东发展银行股份有限公司天津浦德支行</p>
# 单位名称:银行股份有限</p>
# """
#
# rs = re.findall(re.compile(r'<p.*?>.*?(.*?年.*?月.*?日).*?</p>',re.S),str1)
# print(rs[-1])
# # print(re.findall(re.compile(r'机构名称|单位名称(.*?)</p>',re.S),str1))














