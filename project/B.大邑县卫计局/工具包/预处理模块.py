# coding:utf-8
import re
from 大邑县卫计局.工具包 import 链接数据库,附件下载程序,判断url前面的点返回完整的请求地址
# 演示文章
str1 ="""<div class="content" id="xw_box"><p align="left"><font size="4" face="仿宋_GB2312">&nbsp;&nbsp;&nbsp; 为指导各地科学、规范、有效地开展流感疫苗预防接种工作，做好流感预防控制工作，卫生部近日印发《中国流行性感冒疫苗预防接种指导意见》。指导意见指出，在流感流行高峰前1～2个月接种流感疫苗能更有效发挥疫苗的保护作用。推荐接种时间为9至11月份。各省可根据当地流行的高峰季节及对疫情监测结果的分析预测，确定并及时公布当地的最佳接种时间。 <br>&nbsp;&nbsp;&nbsp; 指导意见提出，推荐接种人群为60岁以上人群；慢性病患者及体弱多病者；医疗卫生机构工作人员，特别是一线工作人员；小学生和幼儿园儿童；养老院、老年人护理中心、托幼机构的工作人员；服务行业从业人员，特别是出租车司机，民航、铁路、公路交通的司乘人员，商业及旅游服务的从业人员等；经常出差或到国内外旅行的人员。慎用人群为怀孕3个月以上的孕妇。禁止接种流感疫苗的人群是对鸡蛋或疫苗中其他成分过敏者；格林巴利综合症患者；怀孕3个月以内的孕妇；急性发热性疾病患者；慢性病发作期；严重过敏体质者；&nbsp;12岁以下儿童不能使用全病毒灭活疫苗；医生认为不适合接种的人员。由于接种疫苗后人体内产生的抗体水平会随着时间的延续而下降，并且每年疫苗所含毒株成分因流行优势株不同而有所变化，所以每年都需要接种当年度的流感疫苗。&nbsp; <br>&nbsp;&nbsp;&nbsp; 指导意见要求，疾病预防控制机构、接种单位及其医疗卫生人员发现预防接种异常反应、疑似预防接种异常反应或者接到相关报告的，应当依照预防接种工作规范及时处理，并立即报告所在地县级人民政府卫生主管部门、药品监督管理部门。接到报告的卫生主管部门、药品监督管理部门应当立即组织调查处理，并将异常反应及处理情况逐级上报至卫生部和国家食品药品监督管理局。 </font></p><font size="4" face="仿宋_GB2312">
<p align="right"><br>卫生部新闻办公室 <br>二○○五年十一月三日 <br></p></font></div>"""

# 处理全文的格式问题
def disposeOfData(indexUrl,conentSrc,conent,SavePath,超链接本地地址):
    处理中的全文 = conent
    处理中的全文 = re.sub(r'<span.*?>', '', str(处理中的全文), flags=re.I).replace('</span>', '').replace('</SPAN>', '')
    # 这一组是去除<FONT> ....</FONT>
    处理中的全文 = re.sub(r'<font.*?>', '', 处理中的全文, flags=re.I).replace('</FONT>', '').replace('</font>', '')
    # 这一组是去除<p style="text-align:center;line-height:38px">...</p>
    处理中的全文 = re.sub(r'<p.*?>', '<p>', 处理中的全文,flags=re.I).replace("</P>",'</p>')
    # 这一组是去除<?xml:namespace prefix = o ns = "urn:schemas-microsoft-com:office:office" /><o:p></o:p>
    处理中的全文 = re.sub(r'<?xml:namespace .*?>', '', 处理中的全文,flags=re.I)
    处理中的全文 = re.sub(r'<o:p.*?>', '', 处理中的全文,flags=re.I)
    处理中的全文 = re.sub(r'</o:p>', '', 处理中的全文,flags=re.I)
    # 这一组是去除<strong> ..../<strong>
    处理中的全文 = re.sub(r'<strong.*?>', '', 处理中的全文, flags=re.I)
    处理中的全文 = re.sub(r'</strong>', '', 处理中的全文, flags=re.I)

    # <st1:chsdate year="2017" month="3" day="30" islunardate="False" isrocdate="False" w:st="on">...</st1:chsdate>
    处理中的全文 = re.sub(r'<st1:chsdate .*?>', '', 处理中的全文, flags=re.I)
    处理中的全文 = re.sub(r'</st1:chsdate>', '', 处理中的全文, flags=re.I)

    # 去除掉财务司数据的分享链接  http://www.nhfpc.gov.cn/caiwusi/s7788c/201809/14967bc6df764c0b843472712ace91aa.shtml
    处理中的全文 = re.sub('<div class="fx fr">.*?<script>.*?</div>', '', 处理中的全文, flags= re.I|re.S)
    处理中的全文 = re.sub('<div class="clear"></div>', '', 处理中的全文, flags= re.I)
    处理中的全文 = re.sub('<script>.*?</script>', '', 处理中的全文, flags= re.I|re.S)

    # print("fx fr +clear+ script "+处理中的全文)
    # 表格处理：保留表格但不保留样式
    处理中的全文= re.sub(r'<tr.*?>','<tr>',处理中的全文,flags=re.S | re.I).replace('</TR>','</tr>')
    处理中的全文 = re.sub(r'<td.*?>','<tr>',处理中的全文,flags=re.S | re.I).replace('</TD>','</td>')
    处理中的全文 = re.sub(r'<th.*?>','<tr>',处理中的全文,flags=re.S | re.I).replace('</TH>','</th>')

    # 处理<div style="TEXT-ALIGN: center; LINE-HEIGHT: 150%; FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 16pt" id="allStyleDIV">
    # 处理中的全文 = re.sub(r'<div.*?id="allStyleDIV".*?>','',处理中的全文,flags=re.S | re.I)

    # print('allStyleDIV'+ 处理中的全文)
    # <v:line></v:line> 什么鬼的直接链接符啥？啥玩意儿这是，一脸懵逼
    处理中的全文= re.sub(r'<v:line.*?>.*?</v:line>','',处理中的全文,flags=re.S | re.I)

    # 处理单引号问题，文中单引号往数据库插入数据是行不通的
    处理中的全文 = re.sub(r"'", '"', 处理中的全文, flags=re.I)

    # 处理 a表签问题
    处理中的全文 = re.sub(r'<aname=.*?>', '', 处理中的全文 , flags=re.I)
    处理中的全文 = re.sub(r'<A', '<a', 处理中的全文 , flags=re.I).replace("</A>",'</a>')
    # 处理掉网页带有其他网页的链接
    处理中的全文 = re.sub(re.compile(r'链接[: ：]<a.*?href="(.*?)">.*?</a>|相关链接[: ：]<a.*?href="(.*?)">.*?</a>', flags=re.I), '',
                    处理中的全文)
    处理中的全文 = re.sub('<a.*?href="http://www.*?.(shtml|shtm|html|htm)".*?>.*?</a>', '', 处理中的全文)
    # print(处理中的全文)

    # 处理中的全文 = re.sub(r'\(','【',处理中的全文)
    # 处理中的全文 = re.sub(r'\)','】',处理中的全文)
    # 附件的形式,调用下载程序进行下载

    # 先看全文有没有附件
    adjunct = re.findall(r'.*?(pdf|docx|doc|xlsx|xls|rar|zip)',处理中的全文,flags=re.I)
    if adjunct!=[]:
        # 匹配附件一共有几个，进行循环下载和替换格式，先匹配附件的整个a标签的内容用于后面使用
        adjunct1 = re.findall(re.compile(r'<a.*?href=".*?".*?>.*?</a>', re.I | re.S), 处理中的全文)
        if adjunct1:
            for src in adjunct1:
                print("需要替换的超链接"+str(src))
                # 匹配出每一个a标签的超链接和文件名
                adjunc2 = re.findall(re.compile(r'<a.*?href="(.*?)".*?>(.*?)</a>', re.I | re.S), src)
                if adjunc2 != []:
                    intactALink = adjunc2[0][0]
                    intactALink =  判断url前面的点返回完整的请求地址.returnSRC().returnSrc(indexUrl,intactALink,conentSrc)
                    intactAName = adjunc2[0][1]
                    intactALink1 = intactALink[intactALink.rfind("/")+1:]
                    附件下载程序.DownloadData(intactALink,'',intactALink1,SavePath)
                    # 替换成本地的格式
                    nweA = r'<a href="%s%s">%s</a>' % (超链接本地地址,intactALink1,intactAName)
                    处理中的全文 = re.sub(src, nweA, 处理中的全文)

    # 处理全文图片，先改地址，并下载到本地
    imgList = re.findall(r'<img.*?src=".*?".*?>',处理中的全文,flags=re.I)
    if imgList !=[]:
        for imgPhoto in imgList:
            img1 = re.findall(re.compile(r'<img.*?src="(.*?)".*?>', re.I), imgPhoto)
            if img1!=[]:
                imgAlink = img1[0]
                imgAlink = 判断url前面的点返回完整的请求地址.returnSRC().returnSrc(indexUrl,imgAlink,conentSrc)
                imgAlink1 = imgAlink[imgAlink.rfind("/")+1:]
                附件下载程序.DownloadData(imgAlink,'',imgAlink1,SavePath)
                # 替换成本地地址
                newImg = r'<img src="%s%s">'%(超链接本地地址 , imgAlink1)
                处理中的全文 = re.sub(imgPhoto,newImg,处理中的全文)

    处理后的全文 = 处理中的全文
    return 处理后的全文
# print(disposeOfData(str1))

# 将中文时间转化为阿拉伯数字
# def disposeOftime(conent):
