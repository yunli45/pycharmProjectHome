# coding:utf-8
import re
from I陕西省.工具包 import 链接数据库, 附件下载程序, 判断url前面的点返回完整的请求地址


def dispose_of_data(page_url, content_src, content, save_path):
    print("进入到预处理模块")
    content = content
    # 本次改进了预处理模块将本地的附件位置保存为  E:\行政案例附件\datafolder\省份\来源库名称\,附件的链接地址就在sava_path的基础上进行截取就行，少穿一个参数
    # E:\行政案例附件\datafolder\辽宁省\人民银行沈阳分行\%s
    # \datafolder\辽宁省\人民银行沈阳分行\ == > /datafolder/辽宁省/人民银行沈阳分行/

    annex_local_url = save_path[save_path.find("datafolder")-1:-2].replace("\\", "/")

    """
    　　<span><strong>
    """

    content = content.replace("　", '').replace("	", '').replace(" ", '')
    # content = re.sub('<ul.*?>.*?</ul>',  '',  content, flags=re.S | re.I)
    content = re.sub(r'\f',  '/',  content)
    content = re.sub(r'\\',  '/',  content)
    content = re.sub(r'<font.*?>', '', content, flags=re.I).replace('</font>', '').replace('</FONT>', '')
    content = re.sub(r'<b.*?>', '', content, flags=re.I).replace('</b>', '').replace('</B>', '')
    content = re.sub(r'<span.*?>', '', content, flags=re.I).replace('</span>', '')

    """
        找到所有的p标签，在所有p标签的集合中再匹配出<p.*?text-align>、<p.*?align>、<p.*?style=".*?(text-align|align)
        最终替换掉原文中的p标签
    """
    all_p = re.findall('<p.*?>',  content,  flags=re.I)
    if all_p:
        for ids,  p in enumerate(all_p):
            p_format_1 = re.findall('<p.*?(text-align|align)="(.*?)".*?>',  p,  re.I)
            p_format_2 = re.findall('<p.*?style=".*?(text-align|align):.*?".*?>',  p,  re.I)
            if p_format_1:
                content = content.replace(p,  '<p align="%s">' % (p_format_1[0][1]))
            elif p_format_2:
                for pp in p_format_2:
                    p_format_2_1 = re.findall('<p.*?style=".*?(text-align|align):(right|left|center).*?".*?>',  p,  re.I)
                    if p_format_2_1:
                        content = content.replace(p,  '<p align="%s">' % (p_format_2_1[0][1]))
                    else:
                        content = content.replace(p,  '<p>')
            else:
                content = content.replace(p,  '<p>')

    all_div = re.findall('<div.*?>',  content,  flags=re.I)
    if all_div:
        for ids,  div in enumerate(all_div):
            div_format_1 = re.findall('<div.*?(text-align|align)="(.*?)".*?>',  div,   flags=re.I)
            div_format_2 = re.findall('<div.*?style=".*?(text-align|align):.*?".*?>',  div,  flags=re.I)
            if div_format_1:
                content = content.replace(div,  '<div align="%s">' % (div_format_1[0][1]))
            elif div_format_2:
                for divdiv in div_format_2:
                    div_format_2_1 = re.findall('<div.*?style=".*?(text-align|align):(right|left|center).*?".*?>',  div, flags=re.I)
                    if div_format_2_1:
                        content = content.replace(div,  '<div align="%s">' % (div_format_2_1[0][1]))
                    else:
                        content = content.replace(div,  '<div>')
            else:
                content = content.replace(div,  '<div>')

    """
    先取出掉<span class="wzxq2_lianjie">分享的情况
    
    """
    content = re.sub('<span.*?class="wzxq2_lianjie".*?>.*?</span>', '', content,  flags=re.I | re.S)

    all_span = re.findall('<span.*?>',  content,   flags=re.I)
    if all_span:
        for ids,  span1 in enumerate(all_span):
            span_format_1 = re.findall('<span.*?(text-align|align)="(.*?)".*?>',  span1,  flags=re.I)
            span_format_2 = re.findall('<span.*?style=".*?(text-align|align):.*?".*?>',  span1,  flags=re.I)
            if span_format_1:
                content = content.replace(span1,  '<span align="%s">' % (span_format_1[0][1]))
            elif span_format_2:
                for span2 in span_format_2:
                    span_format_2_1 = re.findall('<span.*?style=".*?(text-align|align):(right|left|center).*?".*?>',  span1,
                                             flags=re.I)
                    if span_format_2_1:
                        content = content.replace(span1,  '<span align="%s">' % (span_format_2_1[0][1]))
                    else:
                        # print(p)
                        content = content.replace(span1,  '<span>')
            else:
                content = content.replace(span1,  '<span>')


    """
    因为全文在一个div中<div class="content" id="contentRegion" style="overflow-x:auto;width:920;padding-bottom:30px">  且该div中有一个table包含了分享的链接，所以先去掉这个class的table
    <table class="dth14l22" width="804" height="20" cellspacing="0" cellpadding="0" border="0">
    
    """
    content = re.sub('<table.*?class="dth14l22".*?>.*?</table>',  '',  content,  flags=re.S)

    all_table = re.findall('<table.*?>', content, flags=re.I)
    if all_table:
        for ids,  table1 in enumerate(all_table):
            table_format_1 = re.findall('<table.*?(text-align|align)="(.*?)".*?>',  table1,  flags= re.I)
            table_format_2 = re.findall('<table.*?style=".*?(text-align|align):.*?".*?>',  table1,   flags=re.I)
            if table_format_1:
                content = content.replace(table1,  '<table align="%s">' % (table_format_1[0][1]))
            elif table_format_2:
                for table2 in table_format_2:
                    table_format_2_1 = re.findall('<table.*?style=".*?(text-align|align):(right|left|center).*?".*?>', table1,  flags=re.I)
                    if table_format_2_1:
                        content = content.replace(table1,  '<table align="%s">' % (table_format_2_1[0][1]))
                    else:
                        # print(p)
                        content = content.replace(table1,  '<table>')
            else:
                content = content.replace(table1,  '<table>')

    all_tr = re.findall('<tr.*?>',  content,  flags=re.I)
    if all_tr:
        for ids,  tr1 in enumerate(all_tr):
            tr_format_1 = re.findall('<tr.*?(text-align|align)="(.*?)".*?>',  tr1,  flags= re.I)
            tr_format_2 = re.findall('<tr.*?style=".*?(text-align|align):.*?".*?>',  tr1,   flags=re.I)
            if tr_format_1:
                content = content.replace(tr1,  '<tr align="%s">' % (tr_format_1[0][1]))
            elif tr_format_2:
                for tr2 in tr_format_2:
                    tr_format_2_1 = re.findall('<tr.*?style=".*?(text-align|align):(right|left|center).*?".*?>',  tr1,
                                           flags=re.I)
                    if tr_format_2_1:
                        content = content.replace(tr1,  '<tr align="%s">' % (tr_format_2_1[0][1]))
                    else:
                        content = content.replace(tr1,  '<tr>')
            else:
                content = content.replace(tr1,  '<tr>')

    all_td = re.findall('<td.*?>',  content,  flags= re.I)
    if all_td:
        for ids,  td1 in enumerate(all_td):
            td_format_1 = re.findall('<td.*?(text-align|align)="(.*?)".*?>',  td1,   flags=re.I)
            td_format_2 = re.findall('<td.*?style=".*?(text-align|align):.*?".*?>',  td1,   flags=re.I)
            if td_format_1:
                content = content.replace(td1,  '<td align="%s">' % (td_format_1[0][1]))
            elif td_format_2:
                for td2 in td_format_2:
                    td_format_2_1 = re.findall('<td.*?style=".*?(text-align|align):(right|left|center).*?".*?>',  td1,
                                           flags= re.I)
                    if td_format_2_1:
                        content = content.replace(td1,  '<td align="%s">' % (td_format_2_1[0][1]))
                    else:
                        # print(p)
                        content = content.replace(td1,  '<td>')
            else:
                content = content.replace(td1,  '<td>')

    # 这一组是去除<?xml:namespace prefix = o ns = "urn:schemas-microsoft-com:office:office" /><o:p></o:p>
    content = re.sub(r'<?xml:namespace .*?>',  '',  content, flags=re.I)
    content = re.sub(r'<o:p.*?>',  '',  content, flags=re.I)
    content = re.sub(r'</o:p>',  '',  content, flags=re.I)

    # <st1:chsdate year="2017" month="3" day="30" islunardate="False" isrocdate="False" w:st="on">...</st1:chsdate>
    content = re.sub(r'<st1:chsdate .*?>',  '',  content,  flags=re.I)
    content = re.sub(r'</st1:chsdate>',  '',  content,  flags=re.I)

    # 去除掉财务司数据的分享链接  http://www.nhfpc.gov.cn/caiwusi/s7788c/201809/14967bc6df764c0b843472712ace91aa.shtml
    content = re.sub('<div class="fx fr">.*?<script>.*?</div>',  '',  content,  flags= re.I|re.S)
    content = re.sub('<div class="clear"></div>',  '',  content,  flags= re.I)
    content = re.sub('<script.*?>.*?</script>',  '',  content,  flags= re.I|re.S)
    content = re.sub('<style.*?>.*?</style>',  '',  content,  flags= re.I|re.S)

    # <v:line></v:line> 什么鬼的直接链接符啥？啥玩意儿这是，一脸懵逼
    content= re.sub(r'<v:line.*?>.*?</v:line>', '', content, flags=re.S | re.I)

    # 处理单引号问题，文中单引号往数据库插入数据是行不通的
    content = re.sub(r"'",  '"',  content,  flags=re.I)
    # 处理 a表签问题
    content = re.sub(r'<aname=.*?>',  '',  content,  flags=re.I)
    # print("处理A标签前的全文内容1" + content)
    content = re.sub(r'<A',  '<a',  content,  flags=re.I).replace("</A>", '</a>')
    # print("处理A标签前的全文内容2" + content)
    print(content)
    # 处理a标签问题：
    """
    先匹配所有的a标签，在检测每个a标签属于附件还是跳转
    """
    all_a = re.findall(r'<a.*?href=".*?".*?>.*?</a>', content)
    if all_a:
        for a in all_a:
            # 循环所有的a标签,再遍历每一个a标签，在每一个a标签中去匹配是否是附件形式 ，不是就直接替换掉，是的话在进行下一步：匹配附件a标签中冲链接和文本能容
            annex_a = re.findall(
                r'<a.*?href=".*?(pdf|docx|doc|xlsx|xls|rar|zip|jpeg|jpg|png|gif|txt|7z|gz)".*?>.*?</a>', a)
            if annex_a:
                print("这个a标签是附件")
                # 假如是附件的形式，使用all_a结果集中每个元素的第一个值（超链接）和第二个值（文本内容）反向匹配这个标签的全部内容，并生成新的本地超链接a标签
                rs_a = re.findall('<a.*?href="(.*?)".*?>(.*?)</a>', a)
                a_hyper = rs_a[0][0]  # a标签的超链接

                # 下载附件
                # annex_download_url = 判断url前面的点返回完整的请求地址.returnSRC().returnSrc(page_url, a_hyper, content_src)
                # 因为链接的地址要从全文地址去提取，所以将page_url 改为content_src
                annex_download_url = 判断url前面的点返回完整的请求地址.returnSRC().returnSrc(content_src, a_hyper, content_src)
                # print("下载地址"+ str(annex_download_url))
                annex_name = a_hyper[a_hyper.rfind("/") + 1:]
                # 这里的附件下载程序已经优化过（因为加入了：判断url前面的点返回完整的请求地址，已经能直接给出附件的下载地址了。所以只需要三个参数就欧克了）
                print("下载地址："+str(annex_download_url))
                附件下载程序.download_data(annex_download_url, annex_name, save_path)

                # 替换标签
                a_text = rs_a[0][1]  # a标签的文本内容
                old_annex_a = a  # 原标签
                """
                修改链接地址 annex_local_url + annex_name  
                /datafolder/辽宁省/人民银行沈阳分行/ + 附件的名字
                """
                new_annex_a = '<a href="{0}">{1}</a>'.format(annex_local_url + annex_name, a_text)  # 现在的标签
                content = content.replace(old_annex_a, new_annex_a)  # 替换全文

            # 这些a标签不是附件直接替换掉这个a标签
            else:
                print("这个a标签不是附件，是跳转" + str(a) + "\n" + "\n")
                a_text1 = re.findall(r'<a.*?href=".*?".*?>(.*?)</a>', a)
                before_a = a
                new_a1 = '{0}'.format(a_text1[0])
                content = content.replace(before_a, new_a1)

    # 处理全文图片，先改地址，并下载到本地
    all_img = re.findall('<img.*?src=".*?".*?>', content)
    if all_img:
        for img in all_img:
            picture = re.findall('<img.*?src=".*?(jpeg|jpg|png|gif)".*?>', img)
            if picture:
                rs_img = re.findall('<img.*?src="(.*?)".*?>', img)
                img_hyper = rs_img[0]
                img_annex_name = img_hyper[img_hyper.rfind("/") + 1:]

                # 下载图片
                # img_download_url = 判断url前面的点返回完整的请求地址.returnSRC().returnSrc(page_url, img_hyper, content_src)
                img_download_url = 判断url前面的点返回完整的请求地址.returnSRC().returnSrc(content_src, img_hyper, content_src)
                附件下载程序.download_data(img_download_url, img_annex_name, save_path)

                # 替换图片链接
                old_img = img
                new_img = '<img src="{0}">'.format(annex_local_url+img_hyper)  # 新的img标签
                content = content.replace(old_img, new_img)  # 替换
            else:
                print("这个img标签不是附件，是跳转" + str(img) + "\n" + "\n")
                old_img = img
                new_img1 = ''
                content = content.replace(old_img, new_img1)

    # 因系统的需要，在块级元素后面加一个《br》
    content = content.replace("</div>", "</div><br/>")
    content = content.replace("</h1>", "</h1><br/>")
    content = content.replace("</h2>", "</h2><br/>")
    content = content.replace("</h3>", "</h3><br/>")
    content = content.replace("</h4>", "</h4><br/>")
    content = content.replace("</h5>", "</h5><br/>")
    content = content.replace("</h6>", "</h6><br/>")
    content = content.replace("</hr>", "</hr><br/>")
    content = content.replace("</p>", "</p><br/>")
    content = content.replace("</table>", "</table><br/>")

    content = content
    print("处理后的全文  :  " + content)
    return content


# 遇到全文是一个表格的时候使用
def dispose_of_data_table(content):
    content = re.sub("<strong.*?>", '', str(content), flags=re.I)
    content = re.sub("</strong.*?>", '', str(content), flags=re.I)
    content = re.sub("<u.*?>", '', content, flags=re.S | re.M).replace("</u>", '')
    content = re.sub("<b.*?>", '', content, flags=re.S | re.M).replace("</b>", '')
    content = re.sub('<span.*?>', '', content, flags=re.S | re.M).replace('</span>', '')
    content = re.sub('<span.*?>', '', str(content), flags=re.S | re.M).replace('</span>', '')
    content = re.sub('<col.*?>', '', content)
    content = re.sub('<tr.*?>', '<tr>', content)
    content = re.sub('<ol.*?>.*?</ol>', '', content, flags=re.S)
    content = re.sub('<td.*?>', '<td>', content)
    content = re.sub('<o:p.*?>', '', content)
    content = re.sub('</o:p.*?>', '', content)

    return content
