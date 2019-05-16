from bs4 import BeautifulSoup
import re

str1 = """
吴忠银监分局行政处罚信息公开表
（宁夏青铜峡贺兰山村镇银行股份有限公司）
<table border="1" cellpadding="0" cellspacing="0" class="MsoNormalTable" style="border-collapse:collapse;mso-table-layout-alt:fixed;border:none;
 mso-border-alt:solid windowtext .5pt;mso-padding-alt:0cm 5.4pt 0cm 5.4pt;
 mso-border-insideh:.5pt solid windowtext;mso-border-insidev:.5pt solid windowtext">
<tr>
<td>

行政处罚决定书文号

</td>
<td>
吴银监罚决字〔2018〕11号
</td>
</tr>
<tr>
<td>

被处罚当事人姓名或名称

</td>
<td>

个人姓名

</td>
<td>

 

</td>
</tr>
<tr>
<td>

单位

</td>
<td>

名称

</td>
<td>

宁夏青铜峡贺兰山村镇银行股份有限公司 

</td>
</tr>
<tr>
<td>

法定代表人（主要负责人）姓名

</td>
<td>

李凌峰

</td>
</tr>
<tr>
<td>

主要违法违规事实（案由）

</td>
<td>

以不正当手段吸收存款、违规发放贷款

</td>
</tr>
<tr>
<td>

行政处罚依据

</td>
<td>

《中华人民共和国商业银行法》第七十四条第三项和第八项、《中华人民共和国银行业监督管理法》第四十六条第五项

</td>
</tr>
<tr>
<td>

行政处罚决定

</td>
<td>

罚款三十万元

</td>
</tr>
<tr>
<td>

作出处罚决定的机关名称

</td>
<td>

中国银监会吴忠监管分局

</td>
</tr>
<tr>
<td>

作出处罚决定的日期

</td>
<td>

2018年4月23日

</td>
</tr>
</table>

"""

TableSoup = BeautifulSoup(str1, 'lxml')
TR = TableSoup.find_all('tr')
print(len(TR))
print(TR)
# for ids, tr in enumerate(TableSoup.find_all('tr')):
#     # print(ids)
#     # print("tr的内容" + str(tr))
#     TrDocNUM1 = re.findall(re.compile(r'吴.*?[工 商 市 场 罚].*?\d.*?号'), str(tr))
#     TrDocNUM2 = re.findall(re.compile(r'吴.*?[银 工 商 市 场 罚].*?\d.*?号'), str(tr))
#     if TrDocNUM1 != []:
#         TrDocNUM = TrDocNUM1
#     elif TrDocNUM2 != []:
#         TrDocNUM = TrDocNUM2
#
#
#     if TrDocNUM != []:
#         TrNUM = ids
#         print(TrNUM)
#         print("表格中书文号：" + str(TrDocNUM))
#         break