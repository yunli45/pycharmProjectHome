# coding:utf-8
import re
from bs4 import BeautifulSoup

cont = """[<table border="0" cellpadding="0" cellspacing="0" class="form_table lh40" width="100%">
<tr>
<th class="tr wp15">行政处罚决定书文号：</th>
<td class="tl">义税 简罚 〔2018〕 34 号</td>
</tr>
<tr>
<th class="tr">处罚名称：</th>
<td class="tl">违反税收管理</td>
</tr>
<tr>
<th class="tr">当前状态：</th>
<td class="tl"><span class="colorBrown">正常</span></td>
</tr>
<tr>
<th class="tr">行政相对人名称：</th>
<td class="tl">锦州金属回收有限责任公司义县分公司</td>
</tr>
<tr>
<th class="tr">统一社会信用代码：</th>
<td class="tl"></td>
</tr>
<tr>
<th class="tr">组织机构代码：</th>
<td class="tl"></td>
</tr>
<tr>
<th class="tr">工商登记码：</th>
<td class="tl"></td>
</tr>
<tr>
<th class="tr">税务登记号：</th>
<td class="tl">210727318915462</td>
</tr>
<tr>
<th class="tr">法定代表人姓名：</th>
<td class="tl">杨杨</td>
</tr>
<tr>
<th class="tr">处罚事由：</th>
<td class="tl">未按照规定期限办理纳税申报和报送纳税资料</td>
</tr>
<tr>
<th class="tr">处罚依据：</th>
<td class="tl">《中华人民共和国税收征收管理法》第六十二条</td>
</tr>
<tr>
<th class="tr">处罚类别1：</th>
<td class="tl">罚款</td>
</tr>
<tr>
<th class="tr">处罚类别2：</th>
<td class="tl">简易程序处罚</td>
</tr>
<tr>
<th class="tr">处罚结果：</th>
<td class="tl">20.0</td>
</tr>
<tr>
<th class="tr">处罚机关：</th>
<td class="tl">国家税务总局义县税务局第二税务所</td>
</tr>
<tr>
<th class="tr">处罚决定日期：</th>
<td class="tl">2018/10/16</td>
</tr>
<tr>
<th class="tr">地方编码：</th>
<td class="tl">210100</td>
</tr>
<tr>
<th class="tr">数据更新时间戳：</th>
<td class="tl">2018/11/07</td>
</tr>
<tr>
<th class="tr">公开范围：</th>
<td class="tl">社会公开</td>
</tr>
</table>]"""

""""""
soup = BeautifulSoup(cont,'lxml')
content_soup = soup.find_all('td')
print(content_soup)
title = content_soup[1].text.strip()
book_num = content_soup[0].text.strip()
legal_person = content_soup[8].text.strip()
punished_people=''
punished_institution = content_soup[3].text.strip()
law_enforcement =content_soup[14].text.strip()
area =''
date =content_soup[17].text.strip().replace("/", '')
date_1 = date[:4]+"年"+date[4:6]+"月"+date[6:]+"日"
cont ="<p>行政处罚决定书文号："+book_num+"</p><p>处罚名称："+title+"</p><p>行政相对人名称："+punished_institution+"</p><p>统一社会信用代码："+content_soup[4].text.strip()+"</p><p>组织机构代码："+content_soup[5].text.strip()+"</p><p>工商登记码："+content_soup[6].text.strip()+"</p><p>税务登记号："+content_soup[7].text.strip()+"</p><p>法定代表人姓名："+legal_person+"</p><p>处罚事由："+content_soup[9].text.strip()+"</p><p>处罚依据："+content_soup[10].text.strip()+"</p><p>处罚类别1："+content_soup[11].text.strip()+"</p><p>处罚类别2："+content_soup[12].text.strip()+"</p><p>处罚结果："+content_soup[13].text.strip()+"</p><p>处罚机关："+law_enforcement+"</p><p>处罚决定日期："+date_1+"</p><p>地方编码："+content_soup[16].text.strip()
#
print(content_soup)
# print(cont)