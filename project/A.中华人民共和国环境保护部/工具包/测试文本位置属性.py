import re
from bs4 import BeautifulSoup
处理中的全文 ="""
<table class="dth14l22" width="804" height="20" cellspacing="0" cellpadding="0" border="0">
<td align="rigth" style="sssd">王胜是个大神</td>
<td text-align="left" style="ssss">是的我们都知道</td>
<td style="text-align:center;line-height:38px">1边的人也知道</td>

</table>
<table>
<td style="align:center;line-height:38px">1.1边的人也知道</td>
<td style="text-align:left">2部边的人也知道</td>
<td style="align:center">2.2部边的人也知道</td>
<td id="kk" style="line-height:38px">3部边的人也知道</td>
</table>

"""
# 分享table = BeautifulSoup(处理中的全文, 'lxml')
# 分享table = 分享table.find_all('table',attrs={'class':'dth14l22'})
# print(len(分享table))

处理中的全文 = re.sub('<table.*?class="dth14l22".*?>.*?</table>','',处理中的全文,flags=re.S)
print(处理中的全文)