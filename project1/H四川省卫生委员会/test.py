# coding:utf-8

str1 = """
<p align="justify">　　<font size="3" face="宋体">联系人：周军海</font>&nbsp;</p>
<p align="justify">　　<font size="3" face="宋体">电 &nbsp;话：86136360</font>&nbsp;</p>
<p align="justify">　　<font size="3" face="宋体">邮 &nbsp;箱：scyzygc@163.com&nbsp;</font>&nbsp;</p>
<p align="justify">　　<font size="3" face="宋体">&nbsp;</font>&nbsp;</p>
<p align="justify">　　<font size="3" face="宋体">附件：1.四川省长春长生公司狂犬病疫苗跟踪观察、咨询服务工作专家组名单</font>&nbsp;</p>
<p align="justify">　　　　　<font size="3" face="宋体"><a href="http://www.scwst.gov.cn/xx/xwdt/szyw/201808/t20180808_18369.html">2.国家卫生健康委员会办公厅关于做好长春长生公司狂犬病疫苗接种者跟踪观察和咨询服务相关工作的通知</a></font>&nbsp;</p>
<p align="justify">　　<font size="3" face="宋体">&nbsp;</font>&nbsp;</p>
<p style="text-align: right;" align="justify">　　<font size="3" face="宋体">&nbsp;四川省卫生和计划生育委员会办公室</font>&nbsp;</p>
<p style="text-align: right;" align="justify">　　<font size="3" face="宋体">2018年8月7日 &nbsp;</font>&nbsp;</p>
<p align="justify">　　<font size="3" face="宋体">&nbsp;</font>&nbsp;</p>
<p align="justify">　　<font size="3" face="宋体">&nbsp;</font>&nbsp;</p>


<p align="justify">　　<span lang="EN-US">&nbsp;</span>&nbsp;</p>
<p style="text-align: right;" align="justify"><span>四川省卫生和计划生育委员会<span lang="EN-US"><o:p></o:p></span></span>&nbsp;</p>
<span lang="EN-US">
<div style="text-align: right;"><span lang="EN-US">2018</span>年<span lang="EN-US">11</span>月<span lang="EN-US">5</span>日</div>
</span></div>

<p style="text-align: center; _line-height_: 30pt" _class_="msonormal" align="center">川卫办发〔2016〕157号</p>
"""

str1 ="""
<div class="wy_contMain fontSt">
      &nbsp;
    </div>

"""
import re
str1 = re.sub('<span.*?>', '', str1, flags=re.I).replace("</span>", '').replace("</SPAN>", '')
str1 = re.sub('<font.*?>', '', str1, flags=re.I).replace("</font>", '').replace("</FONT>", '')
str1 = re.sub('\u3000', '', str1, flags=re.I).replace("&nbsp;", '')
content = re.sub('<o:p>', '', str1, flags=re.I).replace("</o:p>", '')
from bs4 import BeautifulSoup
content_soup = BeautifulSoup(content, 'lxml')
content_soup_all_p = content_soup.find_all('p')
# print(content_soup_all_p)
if content_soup_all_p:
    for p in content_soup_all_p:
        p_cont = str(p.text.strip())
        p_cont = p_cont.replace("\n", '').replace("\t", '').replace(" ", '')
        # print(p_cont)
        if p_cont<30:
            pp = re.findall(".*?川卫[办 发].*?\d号", p_cont)
            # print(pp)
            if pp:
                book_num = pp[0]
                # print(pp)
                break
            else:
                book_num = ''
else:
    book_num = ''

content = re.sub('<[^>]*>','',content)
content = re.sub(" ",'',content)
print(content)
print(len(content))
print(book_num)