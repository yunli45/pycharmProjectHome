import re  # 导入正则表达式模块

# 演示文章
str1 = """
为了指导各级卫生健康行政部门、各级各类医疗机构和广大医务人员切实做好《条例》贯彻工作，进一步维护医患双方合法权益，2018年9月14日国家卫生健康委会同国家中医药管理局联合印发《关于做好<医疗纠纷预防和处理条例>贯彻实施工作的通知》（以下简称《通知》）。 

<a href="http://www.nhfpc.gov.cn/yzygj/s7658/201809/27480bd4dfc84fb7b3b961562bb4630f.shtml" style="dsfjasdfadf;lasd" id="sdfsdf">关于做好《医疗纠纷预防和处理条例》贯彻实施工作的通知</a>

为了指导各级卫生健康行政部门、各级各类医疗机构和广大医务人员切实做好《条例》贯彻工作，进一步维护医患双方合法权益，2018年9月14日国家卫生健康委会同国家中医药管理局联合印发《关于做好<医疗纠纷预防和处理条例>贯彻实施工作的通知》（以下简称《通知》）。 

"""














from bs4 import BeautifulSoup






def disposeOfData(conent):
    处理中的全文 = conent
    处理中的全文 = re.sub(r'<span.*?>', '', str(处理中的全文), flags=re.I).replace('</span>', '').replace('</SPAN>', '')
    # 这一组是去除<FONT> ....</FONT>
    处理中的全文 = re.sub(r'<FONT.*?>', '', 处理中的全文, flags=re.I).replace('</FONT>', '').replace('</font>', '')
    # 这一组是去除<p style="text-align:center;line-height:38px">...</p>
    处理中的全文 = re.sub(r'<p.*?>', '<p>', 处理中的全文)
    # # 这一组是去除<P style="text-align:center;line-height:38px">...</P>
    处理中的全文 = re.sub(r'<P.*?>', '<p>', 处理中的全文)
    处理中的全文 = re.sub(r'</P>', '</p>', 处理中的全文)
    # 这一组是去除<?xml:namespace prefix = o ns = "urn:schemas-microsoft-com:office:office" /><o:p></o:p>
    处理中的全文 = re.sub(r'<?xml:namespace .*?>', '', 处理中的全文)
    处理中的全文 = 处理中的全文.replace('<o:p></o:p>', '').replace('<o:p>', '').replace('</o:p>', '')
    # 这一组是去除<strong> ..../<strong>
    处理中的全文 = re.sub(r'<strong.*?>', '', 处理中的全文, flags=re.I).replace('</strong>', '')
    # <st1:chsdate year="2017" month="3" day="30" islunardate="False" isrocdate="False" w:st="on">...</st1:chsdate>
    处理中的全文 = re.sub(r'<st1:chsdate .*?>', '', 处理中的全文)
    处理中的全文 = re.sub(r'</st1:chsdate>', '', 处理中的全文)

    # 这组是 替换掉<br> 为</p><p>
    处理中的全文 = 处理中的全文.replace('<br>', '</p><p>').replace('</br>', '</p><p>').replace('<br/>', '</p><p>')
    处理中的全文 = 处理中的全文.replace('<BR>', '</p><p>').replace('</BR>', '</p><p>')

    # 这组是处理<p></p>这种无用标签和所有的&nbsp;
    处理中的全文 = re.sub(r'&nbsp;', '', 处理中的全文)
    处理中的全文 = re.sub(r'<aname=.*?>', '', 处理中的全文).replace("</a>", '')
    处理中的全文 = re.sub(r'\u3000', '', 处理中的全文)
    处理中的全文 = re.sub(r'<b>', '', 处理中的全文).replace('</b>', '')
    处理中的全文 = re.sub(r'<font.*?>', '', 处理中的全文).replace('</font>', '').replace('</FONT>', '')
    # 处理中的全文 = re.sub(r'<td.*?>', '<p>', 处理中的全文).replace('</td>', '</p>')
    # 处理中的全文 = re.sub(r'<tr.*?>', ' ', 处理中的全文).replace('</tr>', ' ')
    # 处理中的全文 = re.sub(r'<th.*?>', ' ', 处理中的全文).replace('</th>', ' ')
    处理中的全文 = re.sub("<style.*?>.*?</style>", '', 处理中的全文)
    处理中的全文 = re.sub(r'<strong.*?>', '', 处理中的全文).replace('</strong>', '').replace('</u>', '').replace('<u>', '').replace(
        "<o:p>", '').replace("</o:p>", '')
    处理后的全文 = 处理中的全文
    return 处理后的全文