# coding:utf-8
import re
from G_1行政案例处理.工具包 import 链接数据库


# z注意处理顺序从上往下处理，否则出了问题不负责
# 该方法主要是去除无用的标签，以及常用标签的多余的属性，去除跳转的情况，保留附件超链接（但是没办法核对附件）为块级元素加一个《br/》
def dispose_of_data_1(content):
    content = content
    content = content.replace("　", '').replace("	", '').replace(" ", '')
    content = re.sub('<ul.*?>.*?</ul>',  '',  content, flags=re.S | re.I)
    content = re.sub(r'\f',  '/',  content)
    content = re.sub(r'\\',  '/',  content)
    content = re.sub(r'<font.*?>', '', content, flags=re.I).replace('</font>', '').replace('</FONT>', '')
    content = re.sub(r'<strong.*?>', '', content, flags=re.I).replace('</strong>', '').replace('</STRONG>', '')

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

    # 处理a标签问题：
    """
    附件问题，将所有的超链接去掉
    """
    all_a = re.findall(r'<a.*?href=".*?".*?>.*?</a>', content)
    if all_a:
        for a in all_a:
            # 循环所有的a标签,再遍历每一个a标签，在每一个a标签中去匹配是否是附件形式 ，不是就直接替换掉，是的话在进行下一步：匹配附件a标签中冲链接和文本能容
            a_text1 = re.findall(r'<a.*?href=".*?".*?>(.*?)</a>', a)
            before_a = a
            new_a1 = '{0}'.format(a_text1[0])
            content = content.replace(before_a, new_a1)

    # 处理全文图片，先改地址，并下载到本地
    all_img = re.findall('<img.*?src=".*?".*?>', content)
    if all_img:
        for img in all_img:
            print("这个img标签不是附件，是跳转" + str(img) + "\n" + "\n")
            old_img = img
            new_img1 = ''
            content = content.replace(old_img, new_img1)

    content = content
    print("处理后的全文  :  " + content)
    return content
# print(disposeOfData('', '', str1, '', ''))


# 大致去除已有数据：存在微博分享的情况、 时间被《span》标签分割的情况、
def dispose_of_data_2(content):

    content = content.replace("人民微博", '').replace("新浪微博", '').replace("腾讯微博", '')

    # 时间被《span》标签分割的情况
    """<span style="font-size: 19px;font-family: 仿宋_GB2312">2017</span><span style="font-size: 19px;font-family: 仿宋_GB2312">年5月31日</span>"""
    all_span = re.findall('<span.*?>.*?</span>', content)

    if all_span:
        for span in all_span:
            span_1 = re.findall('<span.*?>(.*?)</span>', str(span))
            if span_1 and len(span_1[0]) <= 6:
                now_span = span_1[0]
                content = content.replace(span, now_span)
    return content


# # # 替换文中的中文时间为阿拉伯数字格式
# def conversion_time_to_num(content):
#     content = content
#     #  替换中文时间
#     rs = re.findall(re.compile(
#         r'[零 ○ 0 O o 〇 Ｏ 一 二 三 四 五 六 七 八 九 十]{4}年[零 〇 一 二 三 四 五 六 七 八 九 十]{1,2}月[零 〇 一 二 三 四 五 六 七 八 九 十]{1,3}日'),
#                     str(content))
#     if rs:
#          ”循环时间组”
#         start_index \
#             = content.find(rs[0])
#         end_index = start_index + len(rs[0])
#         if rs.find("年") and rs.find("月") and rs.find("日") :
#             rss = re.split('[年 月 日]', rs)
#             time1 = ['零', '○', '0', 'O', 'o', '〇', 'Ｏ', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
#             time2 = ['零', '0', '0', '0', '0', '0', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' 10']
#             year_list = []
#             month_list = []
#             day_list = []
#             if len(rss[0]) == 4:
#                 for y in rss[0]:
#                     if y in time1:
#                         index = time1.index(y)
#                         yy = time2[index]
#                         year_list.append(yy)
#                 # print(year_list)
#
#                 if len(rss[1]) <= 2:
#                     for m in rss[1]:
#                         if m in time1:
#                             index1 = time1.index(m)
#                             mm = time2[index1]
#                             month_list.append(mm)
#                 # print(month_list)
#                 elif 2 < len(rss[1]) <= 3:
#                     for m in rss[1]:
#                         if m in time1:
#                             index1 = time1.index(m)
#                             mm = time2[index1]
#                             month_list.append(mm)
#                 print(month_list)
#                 if len(rss[2]) <= 2:
#                     print(rss[2])
#                     for d in rss[2]:
#                         if d in time1:
#                             index1 = time1.index(d)
#                             dd = time2[index1]
#                             day_list.append(dd)
#                 elif 2 < len(rss[2]) <= 3:
#                     for d in rss[2]:
#                         if d in time1:
#                             index1 = time1.index(d)
#                             dd = time2[index1]
#                             day_list.append(dd)
#             print(day_list)
#             if year_list != [] and month_list != [] and day_list != []:
#                 year = ''.join(str(i) for i in year_list).replace(" ", '')
#                 moth = ''.join(str(i) for i in month_list).replace(" ", '')
#                 day = ''.join(str(i) for i in day_list).replace(" ", '')
#                 if len(moth) > 2:
#                     moth = moth[0] + moth[-1]
#                 if len(day) > 2:
#                     day = day[0] + day[-1]
#                 result = year + "年" + moth + "月" + day + "日"
#                 content = content.replace(content[start_index:end_index], result)
#
#     else:
#         pass
#
#     return content


# 处理标题 和中文时间
def dispose_title(content):
    content = content
    title = re.findall(re.compile(r'<p>.*?[监 罚 处 环  局].*?\d号</p>'), content)
    行政处罚决定书 = re.findall(re.compile(r'<p>行政处罚决定书</p>'), content)
    执法局 = r'<p>[\u4E00-\u9FA5\uF900-\uFA2D]+[\局 ,\协会,\厅]</p>'
    执法局 = re.findall(re.compile(执法局), content)
    if title != []:
        ti = content.find(title[-1])
        if ti < 100 and len(title[-1]) < 20:
            title[0] = title[0].replace("<p>", '').replace("</p>", '')
            content = content.replace(title[0], ''.join(['<p style="text-align: center;">' + title[-1] + '</p>']))
    if 行政处罚决定书 !=[]:
        ti1 = content.find(行政处罚决定书[-1])
        if ti1 < 100 and len(行政处罚决定书[-1]) < 20:
            行政处罚决定书[0] = 行政处罚决定书[0].replace("<p>", '').replace("</p>", '')
            content = content.replace(行政处罚决定书[0], ''.join(['<p style="text-align: center;">' + 行政处罚决定书[-1] + '</p>']))
    if len(执法局) != 0:
        find1 = content.find(执法局[-1])
        if find1 > 100 and len(执法局[-1]) < 20:
            执法局[-1] = 执法局[-1].replace("<p>", '').replace("</p>", '')
            content = content.replace(执法局[-1], ''.join(['<p style="text-align: center;">' + 执法局[-1] + '</p>']))
        else:
            pass


    # 这组是处理落款时间的格式
    yy = r'<p>\s*[ 零 ○ 0 O o 〇 Ｏ 一 二 三 四 五 六 七 八 九 十]{4}年[一 二 三 四 五 六 七 八 九 十 〇]{1,2}月[一 二 三 四 五 六 七 八 九 十 〇]{1,2}日\s*</p>|<p>\s*\d{4}年\d{1,2}月\d{1,2}日</p>'
    str2 = re.findall(re.compile(yy), content)
    print("找到的结果" + str(str2))
    if len(str2) != 0:
        find1 = content.find(str2[-1])
        if find1 > 100 and len(str2[-1]) < 20:
            str2[-1] = str2[-1].replace("<p>", '').replace("</p>", '')
            print("str2[-1]" + str2[-1])
            rss = re.split('[年 月 日]', str2[-1])
            print(rss)

            time1 = ['零', '○', '0', 'O', 'o', '〇', 'Ｏ', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
            time2 = ['0', '0', '0', '0', '0', '0', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' 10']
            YearList = []
            MonthList = []
            DayList = []
            if len(rss[0]) == 4:
                for y in rss[0]:
                    if y in time1:
                        index = time1.index(y)
                        yy = time2[index]
                        YearList.append(yy)
                print(YearList)
                if len(rss[1]) <= 2:
                    for m in rss[1]:
                        if m in time1:
                            index1 = time1.index(m)
                            mm = time2[index1]
                            MonthList.append(mm)
                # print(MonthList)
                elif 2 < len(rss[1]) <= 3:
                    for m in rss[1]:
                        if m in time1:
                            index1 = time1.index(m)
                            mm = time2[index1]
                            MonthList.append(mm)
                print(MonthList)
                if len(rss[2]) <= 2:
                    print(rss[2])
                    for d in rss[2]:
                        if d in time1:
                            index1 = time1.index(d)
                            dd = time2[index1]
                            DayList.append(dd)
                elif 2 < len(rss[2]) <= 3:
                    for d in rss[2]:
                        if d in time1:
                            index1 = time1.index(d)
                            dd = time2[index1]
                            DayList.append(dd)
            print(DayList)
            if YearList != [] and MonthList != [] and DayList != []:
                print("yes")
                Year = ''.join(str(i) for i in YearList).replace(" ", '')
                Moth = ''.join(str(i) for i in MonthList).replace(" ", '')
                Day = ''.join(str(i) for i in DayList).replace(" ", '')
                if len(Moth) > 2:
                    Moth = Moth[0] + Moth[-1]
                    Day = Day[0] + Day[-1]
                Time1 = Year + "年" + Moth + "月" + Day + "日"
                print("中文时间" + str2[-1])
                # 如果存在落款时间就加上个<p style="text-align: right;"> 让它居右显示
                print("noe" + str2[-1])
                if Time1:
                    content = content.replace(str2[-1], ''.join(['<p style="text-align: right;">' + Time1 + '</p>']))
            else:
                content = content.replace(str2[-1], ''.join(['<p style="text-align: right;">' + str2[-1] + '</p>']))
    return content


# 处理落款格式
def dispose_inscriber(content):
    content = content
    yy2 = r'<p>[\u4E00-\u9FA5\uF900-\uFA2D]+[\局 ,\协会,\厅]</p>'
    rs = re.findall(re.compile(yy2), content)
    if len(rs) != 0:
        find1 = content.find(rs[-1])
        if find1 > 100 and len(rs[-1]) < 20:
            rs[-1] = rs[-1].replace("<p>", '').replace("</p>", '')
            content = content.replace(rs[-1], ''.join(['<p style="text-align: right;">' + rs[-1] + '</p>']))
        else:
            pass
    else:
        pass
    return content


def dispose_of_data_end(content):
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

    return content


# 将中文时间转化为阿拉伯数字
# content ="""
# <p>sdfasdfa2017年10月23日</p>
# <p>sdfasdfa二零一七年十一月二十三日</p>
# <p>sdfasdfa2017年10月23日</p>
#
#
# """
# dispose_title(content)



