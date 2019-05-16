# coding:utf-8
import re
from bs4 import BeautifulSoup
import openpyxl
import os,shutil
from G_1行政案例处理.工具包 import 链接数据库


# 因为gif图片是一个个小图标，没用现在全部删除
def dispose_of_img_gif_label_1(content):
    content = str(content)
    rs = re.findall(r'<img.*? src=".*?.gif".*?>', content)
    if rs:
        for ig in rs:
            content = content.replace(ig, '')
    return content


# z注意处理顺序从上往下处理，否则出了问题不负责  顺序：1
# 该方法主要是去除无用的标签，以及常用标签的多余的属性，去除跳转的情况，保留附件超链接（但是没办法核对附件）为块级元素加一个《br/》
def dispose_of_data_1(content):
    content = content
    content = content.replace("&nbsp;", '')
    content = re.sub('<ul.*?>.*?</ul>',  '',  content, flags=re.S | re.I)
    content = re.sub(r'\f',  '/',  content)
    content = re.sub(r'\\',  '/',  content)

    content = re.sub(r'<a name=.*?>',  '',  content)

    content = re.sub(r'<font.*?>', '', content, flags=re.I).replace('</font>', '').replace('</FONT>', '')  # 去除字体标签
    content = re.sub(r'<strong.*?>', '', content, flags=re.I).replace('</strong>', '').replace('</STRONG>', '')  # 去除加粗

    content = re.sub('<o:p>', '', content, flags=re.I).replace("</o:p>", '')  # 去除<o:p>
    content = re.sub('<o:p.*?>', '', content)
    content = re.sub('</o:p.*?>', '', content)

    content = re.sub(r'<style.*?>.*?</style>', ' ', content, flags=re.M | re.S)   # 去除脚本style
    content = re.sub('<script.*?>.*?</script>', '', content, flags=re.I | re.S)

    content = re.sub('<span.*?>', '', content, flags=re.I | re.S)
    content = re.sub('</span>', '', content, flags=re.I | re.S)
    content = re.sub('<br>', '', content, flags=re.I | re.S)
    content = re.sub('<br/>', '', content, flags=re.I | re.S)
    content = re.sub(r'<b.*?>', '', content, flags=re.I).replace('</b>', '').replace('</B>', '')  # 去除b标签

    # 这一组是处理 标题标签（h1-或h6）：保留标签，去掉属性
    content = re.sub('<h1.*?>', '<h1>', content, flags=re.I)
    content = re.sub('<h2.*?>', '<h2>', content, flags=re.I)
    content = re.sub('<h3.*?>', '<h3>', content, flags=re.I)
    content = re.sub('<h4.*?>', '<h4>', content, flags=re.I)
    content = re.sub('<h5.*?>', '<h5>', content, flags=re.I)
    content = re.sub('<h6.*?>', '<h6>', content, flags=re.I)


    """
        找到所有的p标签，在所有p标签的集合中再匹配出<p.*?text-align>、<p.*?align>、<p.*?style=".*?(text-align|align)
        最终替换掉原文中的p标签
    """
    all_p = re.findall('<p.*?>', content, flags=re.I)
    if all_p:
        for ids, p in enumerate(all_p):
            p_format_1 = re.findall('<p.*?(text-align|align)="(.*?)".*?>', p, re.I)
            p_format_2 = re.findall('<p.*?style="(text-align|align):.*?".*?>', p, re.I)
            if p_format_1:
                for p_1 in p_format_1:
                    p_format_1_1 = re.findall('.*?(right|left|center)', p, re.I)
                    if p_format_1_1:
                        content = content.replace(p, '<p align="%s">' % (p_format_1_1[0]))
                    else:
                        content = content.replace(p, "<p>")
            elif p_format_2:
                for pp in p_format_2:
                    p_format_2_1 = re.findall('.*?(right|left|center)', p, re.I)
                    if p_format_2_1:
                        content = content.replace(p, '<p align="%s">' % (p_format_2_1[0]))
                    else:
                        content = content.replace(p, '<p>')
            else:
                content = content.replace(p, '<p>')
    content = content

    all_div = re.findall('<div.*?>', content, flags=re.I)
    if all_div:
        for ids, div in enumerate(all_div):
            div_format_1 = re.findall('<div.*?(text-align|align)="(.*?)".*?>', div, re.I)
            div_format_2 = re.findall('<div.*?style="(text-align|align):.*?".*?>', div, re.I)
            if div_format_1:
                for div_1 in div_format_1:
                    div_format_1_1 = re.findall('.*?(right|left|center)', div, re.I)
                    if div_format_1_1:
                        content = content.replace(div, '<div align="%s">' % (div_format_1_1[0]))
                    else:
                        content = content.replace(div, "<div>")
            elif div_format_2:
                print("2222")
                for divdiv in div_format_2:
                    print(divdiv)
                    div_format_2_1 = re.findall('.*?(right|left|center)', div, re.I)
                    if div_format_2_1:
                        print("div_format_2_1" + str(div_format_2_1))
                        content = content.replace(div, '<div align="%s">' % (div_format_2_1[0]))
                    else:
                        content = content.replace(div, '<div>')
            else:
                content = content.replace(div, '<div>')

    """
    先取出掉<span class="wzxq2_lianjie">分享的情况
    
    """
    content = re.sub('<span.*?class="wzxq2_lianjie".*?>.*?</span>', '', content,  flags=re.I | re.S)

    """
    因为全文在一个div中<div class="content" id="contentRegion" style="overflow-x:auto;width:920;padding-bottom:30px">  且该div中有一个table包含了分享的链接，所以先去掉这个class的table
    <table class="dth14l22" width="804" height="20" cellspacing="0" cellpadding="0" border="0">
    
    """
    content = re.sub('<table.*?class="dth14l22".*?>.*?</table>',  '',  content,  flags=re.S)

    # 这一组是处理表格相关标签
    all_table = re.findall('<table.*?>', content, flags=re.I)
    if all_table:
        for ids, table in enumerate(all_table):
            table_format_1 = re.findall('<table.*?(text-align|align)="(.*?)".*?>', table, re.I)
            table_format_2 = re.findall('<table.*?style="(text-align|align):.*?".*?>', table, re.I)
            if table_format_1:
                for table_1 in table_format_1:
                    table_format_1_1 = re.findall('.*?(right|left|center)', table, re.I)
                    if table_format_1_1:
                        content = content.replace(table, '<table align="%s">' % (table_format_1_1[0]))
                    else:
                        content = content.replace(table, "<table>")
            elif table_format_2:
                print("2222")
                for table_2 in table_format_2:
                    print(table_2)
                    table_format_2_1 = re.findall('.*?(right|left|center)', table, re.I)
                    if table_format_2_1:
                        print("table_format_2_1" + str(table_format_2_1))
                        content = content.replace(table, '<table align="%s">' % (table_format_2_1[0]))
                    else:
                        content = content.replace(table, '<table>')
            else:
                content = content.replace(table, '<table>')

    all_tr = re.findall('<tr.*?>', content, flags=re.I)
    if all_tr:
        for ids, tr in enumerate(all_tr):
            tr_format_1 = re.findall('<tr.*?(text-align|align)="(.*?)".*?>', tr, re.I)
            tr_format_2 = re.findall('<tr.*?style="(text-align|align):.*?".*?>', tr, re.I)
            if tr_format_1:
                for tr_1 in tr_format_1:
                    tr_format_1_1 = re.findall('.*?(right|left|center)', tr, re.I)
                    if tr_format_1_1:
                        content = content.replace(tr, '<tr align="%s">' % (tr_format_1_1[0]))
                    else:
                        content = content.replace(tr, "<tr>")
            elif tr_format_2:
                print("2222")
                for tr_2 in tr_format_2:
                    print(tr_2)
                    tr_format_2_1 = re.findall('.*?(right|left|center)', tr, re.I)
                    if tr_format_2_1:
                        print("tr_format_2_1" + str(tr_format_2_1))
                        content = content.replace(tr, '<tr align="%s">' % (tr_format_2_1[0]))
                    else:
                        content = content.replace(tr, '<tr>')
            else:
                content = content.replace(tr, '<tr>')

    all_td = re.findall('<td.*?>', content, flags=re.I)
    if all_td:
        for ids, td in enumerate(all_td):
            td_format_1 = re.findall('<td.*?(text-align|align)="(.*?)".*?>', td, re.I)
            td_format_2 = re.findall('<td.*?style="(text-align|align):.*?".*?>', td, re.I)
            if td_format_1:
                for td_1 in td_format_1:
                    td_format_1_1 = re.findall('.*?(right|left|center)', td, re.I)
                    if td_format_1_1:
                        content = content.replace(td, '<td align="%s">' % (td_format_1_1[0]))
                    else:
                        content = content.replace(td, "<td>")
            elif td_format_2:
                print("2222")
                for td_2 in td_format_2:
                    print(td_2)
                    td_format_2_1 = re.findall('.*?(right|left|center)', td, re.I)
                    if td_format_2_1:
                        print("td_format_2_1" + str(td_format_2_1))
                        content = content.replace(td, '<td align="%s">' % (td_format_2_1[0]))
                    else:
                        content = content.replace(td, '<td>')
            else:
                content = content.replace(td, '<td>')

    # 这一组是去除<?xml:namespace prefix = o ns = "urn:schemas-microsoft-com:office:office" /><o:p></o:p>
    content = re.sub(r'<?xml:namespace .*?>',  '',  content, flags=re.I)

    # 这一组是去除时间脚本
    # <st1:chsdate year="2017" month="3" day="30" islunardate="False" isrocdate="False" w:st="on">...</st1:chsdate>
    content = re.sub(r'<st1:chsdate .*?>',  '',  content,  flags=re.I)
    content = re.sub(r'</st1:chsdate>',  '',  content,  flags=re.I)

    # 去除掉财务司数据的分享链接  http://www.nhfpc.gov.cn/caiwusi/s7788c/201809/14967bc6df764c0b843472712ace91aa.shtml
    content = re.sub('<div class="fx fr">.*?<script>.*?</div>',  '',  content,  flags=re.I | re.S)
    content = re.sub('<div class="clear"></div>',  '',  content,  flags=re.I)

    # <v:line></v:line> 什么鬼的直接链接符啥？啥玩意儿这是，一脸懵逼
    content = re.sub(r'<v:line.*?>.*?</v:line>', '', content, flags=re.S | re.I)

    # 处理单引号问题，文中单引号往数据库插入数据是行不通的
    content = re.sub(r"'",  '"',  content,  flags=re.I)
    # 处理 a表签问题
    content = re.sub(r'<aname=.*?>',  '',  content,  flags=re.I)
    # print("处理A标签前的全文内容1" + content)
    content = re.sub(r'<A',  '<a',  content,  flags=re.I).replace("</A>", '</a>')
    # print("处理A标签前的全文内容2" + content)

    #
    """
    处理a标签、img标签问题： 
        附件问题，将所有的超链接去掉
        在检测的时候：处理注释掉，先调用：dispose_of_adjunct_label_3 处理掉a、img其他的属性，在main函数中调用 dispose__hyper_link
        在抓取的时候调用 ：方法一：去除文中的附件标签 或者 方法二： 检测本地附件是否存在 
    """
    # content = re.sub("<a.*?>", '', content, flags=re.I)
    # content = re.sub("</a>", '', content, flags=re.I)
    #
    # content = re.sub("<img.*?>", '', content, flags=re.I)

    content = str(dispose_of_adjunct_label_3(content))

    # 大致去除已有数据：存在微博分享的情况、 时间被《span》标签分割的情况、
    content = content.replace("人民微博", '').replace("新浪微博", '').replace("腾讯微博", '')


    content = content
    # print("处理后的全文  :  " + content)
    return content


# 以下两个方法是处理文中附件标签（a img）的情况
# 方法一：去除文中的附件标签
def dispose_of_adjunct_label_1(content):
    content = str(content)
    content = re.sub('<a.*?>', '', content, flags=re.I)
    content = re.sub('</a.*?>', '', content, flags=re.I)
    content = re.sub('<img.*?>', '', content, flags=re.I)
    return content


#  方法二： 检测本地附件是否存在
# 处理a、img标签，除去各种跳转的情况，匹配本地相关附件是否存在
# file_path：为本地附件总目录F://环保局
def dispose_of_adjunct_label_2(title, content):
    content = str(content)
    附件不在链接没改 = []
    附件不在链接修改了 = []
    附件存在链接没改 = []
    """
      注意：每次根据本地附件所在位置来检测
      比如我现在将辽宁省的附件全部放在了G盘（移动硬盘）
     
    """
    result_a_list = re.findall("<a.*?>", content, flags=re.I)
    if result_a_list:
        
        pass


# 方法三：在检测的时候第一次调用，去掉a、img的其他属性，a保留：href 、 img保留：src
def dispose_of_adjunct_label_3(content):
    result_a_list = re.findall("<a.*?>.*?</a>", content, flags=re.I)
    if result_a_list:
        for a in result_a_list:
            rs_a = re.findall(r'<a.*?href="(.*?)".*?>(.*?)</a>', str(a), flags=re.I)
            print(rs_a)
            if rs_a:
                new_a = '<a href="{0}">{1}</a>'.format(rs_a[0][0], rs_a[0][1])
                content = content.replace(a, new_a)
            else:
                content = content.replace(a, '')

    result_img_list = re.findall("<img.*?>", content, flags=re.I)
    if result_img_list:
        for img in result_img_list:
            rs_img = re.findall(r'<img.*?src="(.*?)".*?>', str(img), flags=re.I)
            if rs_img:
                new_img = '<img src="{0}">'.format(rs_img[0])
                content = content.replace(img, new_img)
            else:
                content = content.replace(img, '')

    return content


def dispose__hyper_link(title, cont, file_path):

    all_file_name_list = each_file_name(file_path)  # 找到本地所有附件的名字
    all_file_path_list = each_file_path(file_path)  # 找到本地所有附件的路径
    附件不在链接没改 = {}
    附件不在链接修改了 = {}
    附件存在链接没改 = {}

    all_a = re.findall(r'<a.*?href=".*?".*?>.*?</a>', cont)
    if all_a:
        for a in all_a:
            # 循环所有的a标签,再遍历每一个a标签，在每一个a标签中去匹配是否是附件形式 ，不是就直接替换掉，是的话在进行下一步：匹配附件a标签中冲链接和文本能容
            annex_a = re.findall(r'<a.*?href=".*?(pdf|docx|doc|xlsx|xls|rar|zip|jpeg|jpg|png|gif|txt|7z|gz)".*?>.*?</a>', a)
            if annex_a:
                print("这个a标签是一个附件")
                # 假如是附件的形式，使用all_a结果集中每个元素的第一个值（超链接）和第二个值（文本内容）反向匹配这个标签的全部内容，并生成新的本地超链接a标签
                rs_a = re.findall('<a.*?href="(.*?)".*?>(.*?)</a>', a)
                a_hyper = rs_a[0][0]  # a标签的超链接
                a_text = rs_a[0][1]  # a标签的文本内容
                old_annex_a = a  # 原标签
                new_annex_a = '<a href="{0}">{1}</a>'.format(a_hyper, a_text)  # 现在的标签
                cont = cont.replace(old_annex_a, new_annex_a)  # 替换全文

                # 匹配本地附件是否存在
                # 超链接地址已经做了修改是属于我们服务器上面的地址， file_path = 'E:\环保局\环保局汇总'
                #
                if str(a_hyper).find("/datafolder/") != -1:
                    print("这个超链接的地址是已经修改过的，现在开始检测本地是否存在相应的附件和位置是否保存正确..........................")

                    file_path1 = file_path    # F:\广西建设网\行政案例数据
                    # /datafolder/行政案例数据/广西建设网文件通知/20180612164246643.pdf
                    # 将标签中反斜杠 替换为本地磁盘中访问地址的反斜杠
                    a_hyper_link = a_hyper.replace("/", "\\")
                    # 本地的地址：F:\广西建设网\行政案例数据 + 将超链接的地址,拼接为一个本地附件完整路径，用于检测
                    a_local_link = str(file_path1 + a_hyper_link)

                    if a_local_link in all_file_path_list:
                        print("这个附件检测完毕：在本地是存在的,且保存的位置也是正确的。")
                        pass

                    else:

                        print("这个附件的超链接地址已经修改过的，现在开始检查本地是否存在相应的附件...................................")
                        print("如果存在就将本地的文件移动到超链接中记录的目录地址下, 不存在那就是这条数据的附件可能存在缺失" + str(title) + "\n" + str(a_hyper))
                        a_annex_name = a_hyper[a_hyper.rfind("/")+1:]
                        print("这个附件 的名字是："+a_annex_name)
                        # 如果这个文件名在本地目录找到这个附件名，那么在本地是存在的，只是本地保存的地址好像错了
                        if a_annex_name in all_file_name_list:
                            for local_file_path in all_file_path_list:
                                if local_file_path.find(a_annex_name) != -1:
                                    print("检测结果：这个附件名在本地是存在的"+str(local_file_path))
                                    print("只是本地保存的地址好像错了，现在开始将该附件移动到文本超链接记录的目录下")
                                    # /datafolder/行政案例数据/广西建设网文件通知/20180612164246643.pdf
                                    # 将标签中反斜杠 替换为本地磁盘中访问地址的反斜杠
                                    a_hyper_link1 = a_hyper.replace("/", '\\')
                                    a_hyper_link1 = a_hyper_link1[:(a_hyper_link1.rfind("\\"))]  # 因为是可能是附件的本地地址错了，现在开是将附件的名字取出来，移动到正确的位置
                                    # 将位置保存错了的附件的正确地址拼接出来
                                    a_local_link1 = file_path1 + a_hyper_link1
                                    a_local_path = a_local_link1
                                    mk_dir(a_local_path)
                                    # 本地文件所在位置
                                    old_path = local_file_path
                                    new_path = a_local_path
                                    # old_path 为原来文件全路径名（加上文件名），new_path为新的文件目录
                                    try:
                                        shutil.move(old_path, new_path)  # 不考虑文件在本地的路径是正确的情况，如果报错该文件在本地是存在的，那么就是上面的语法写错了
                                    except:
                                        pass
                                # 这个附件名在本地是不存在的，
                                else:
                                    print("检测结果：这个附件名在本地是不存在的，但是他的链接地址是修改过的"+title)
                                    # print("这个标签是" + str(a))
                                    附件不在链接修改了.update({'{}'.format(title): '{}'.format(a)})
                                    # 附件不在链接修改了.update({'{}'.format(title): '{}'.format(str(id)+";"+str(虚假标题)+";"+str(下载地址))})
                        # 这种情况是 超链接修改了，但是本地没有任何的相应附件
                        else:
                            # print("这种情况是 超链接修改了，但是本地没有任何的相应附件")
                            附件不在链接修改了.update({'{}'.format(title): '{}'.format(a)})
                            # 附件不在链接修改了.update({'{}'.format(title): '{}'.format(str(id) + ";" + str(虚假标题) + ";" + str(下载地址))})

                # 这种情况就是：超链接地址没有做修改，还不知道本地的附件是否存在。首先检查下本地的附件是否存在 ， 再改成我们的地址
                else:
                    print("这个超链接没有修改，现在开始检查本地的相应的附件是否存在 .................................")
                    a_annex_name1 = a_hyper[a_hyper.rfind("/")+1:]
                    if a_annex_name1 in all_file_name_list:
                        print("检测结果：该附件在本地是存在的，只是超链接的地址没有修改，请手动修改    "+str(title))
                        附件存在链接没改.update({'{}'.format(title): '{}'.format(a)})
                        # 附件存在链接没改.update({'{}'.format(title): '{}'.format(str(id)+";"+str(虚假标题)+";"+str(下载地址))})
                    else:
                        print("检测结果：这条数据的附件不存在，并且超链接的地址也没有修改，请重新下载该数据，并且修改链接地址   "+str(title))
                        附件不在链接没改.update({'{}'.format(title): '{}'.format(a)})
                        # 附件不在链接没改.update({'{}'.format(title): '{}'.format(str(id)+";"+str(虚假标题)+";"+str(下载地址))})
            # 这些a标签不是附件直接替换掉这个a标签
            else:
                print("这个a标签不是附件，是跳转"+str(a)+"\n"+"\n")
                a_text1 = re.findall(r'<a.*?href=".*?".*?>(.*?)</a>', a)
                before_a = a
                new_a1 = '{0}'.format(a_text1[0])
                cont = cont.replace(before_a, new_a1)

    all_img = re.findall('<img.*?src=".*?".*?>', cont)
    if all_img:
        for img in all_img:
            picture = re.findall('<img.*?src=".*?(jpeg|jpg|png|gif)".*?>', img)
            if picture:
                rs_img = re.findall('<img.*?src="(.*?)".*?>', img)
                img_hyper = rs_img[0]
                old_img = img
                new_img = '<img src="{0}">'.format(img_hyper)  # 新的img标签
                cont = cont.replace(old_img, new_img)  # 替换
                # 匹配本地的图片是否存在
                if img.find("/datafolder/") != -1:
                    print("这个图片的超链接的地址是已经修改过的,现在开始检测本地是否存在相应的图片............")
                    file_path1 = file_path
                    img_hyper_link = img_hyper.replace("/", "\\")
                    img_local_link = str(file_path1 + img_hyper_link)  # 上面那个是用于测试附件本地位置保存错误的情况
                    if img_local_link in all_file_path_list:
                        print("检测结果：这个图片附件在本地路径是存在的，且附件的链接地址也是修改过的")
                        pass
                    else:
                        print("这个图片附件的地址已经修改但是本地附件好像保存错位置了，现在开始检查本地是否存在相应的附件.................")
                        # "如果存在就将本地的文件移动到超链接中记录的地址,不存在那就是这条数据的附件存在缺失"
                        img_annex_name = img_hyper[img_hyper.rfind("/") + 1:]
                        if img_annex_name in all_file_name_list:
                            for local_file_path in all_file_path_list:
                                if local_file_path.find(img_annex_name) != -1:
                                    print("找到了这个图片文件名在本地的路径:   " + local_file_path)
                                    print("检测结果：这个图片附件名在本地是存在的，只是本地保存的地址好像错了，现在开始将该附件移动到文本超链接记录的目录下")
                                    img_hyper_link1 = img_hyper.replace("/datafolder/行政案例数据/", '').replace("/", '\\')
                                    img_hyper_link1 = img_hyper.replace("/", '\\')
                                    img_hyper_link1 = img_hyper_link1[:(img_hyper_link1.rfind("\\"))]
                                    img_hyper_link1 = file_path1 + img_hyper_link1   # F:\广西建设网
                                    img_local_path = img_hyper_link1
                                    # print("img_hyper_link1" + img_hyper_link1)
                                    mk_dir(img_local_path)
                                    old_path = local_file_path   # 原来文件完整路径
                                    new_path = img_local_path    # 需要移动到目录
                                    # old_path 为原来文件全路径名（加上文件名），new_path为新的文件目录
                                    try:
                                        shutil.move(old_path, new_path)  # 不考虑文件在本地的路径是正确的情况，如果报错该文件在本地是存在的，那么就是上面的语法写错了
                                        print("已经将该图片移动到正确的位置下了。")
                                    except:
                                        pass
                        else:
                            print("检测结果：这个图片的附件名在本地是不存在的，但是链接修改过了，请重新下载该附件" + title)
                            print("这个标签是" + str(img))
                            附件不在链接修改了.update({'{}'.format(title): '{}'.format(img)})
                            # 附件不在链接修改了.update({'{}'.format(title): '{}'.format(str(id)+";"+str(虚假标题)+";"+str(下载地址))})

                # 超链接地址没有做修改是，需要改成我们的地址，首先检查下本地的附加是否存在
                else:
                    print("检测到这个夫图片的链接地址没有修改，请查看相应的内容：" + title + "\n" + str(img))
                    print("现在开始检查本地的相应的附件是否存在................................")
                    img_annex_name1 = img_hyper[img_hyper.rfind("/") + 1:]
                    if img_annex_name1 in all_file_name_list:
                        print("检测结果：该图片附件在本地是存在的，只是超链接的地址没有修改，请手动修改")
                        附件存在链接没改.update({'{}'.format(title): '{}'.format(img)})
                        # 附件存在链接没改.update({'{}'.format(title): '{}'.format(str(id)+";"+str(虚假标题)+";"+str(下载地址))})
                    else:
                        print("检测结果：这条数据的该图片不存在，并且超链接的地址也没有修改，请重新下载该数据,并修改相应的链接地址")
                        附件不在链接没改.update({'{}'.format(title): '{}'.format(img)})
                        # 附件不在链接没改.update({'{}'.format(title): '{}'.format(str(id)+";"+str(虚假标题)+";"+str(下载地址))})
            else:
                print("这个img标签不是附件，是跳转" + str(img) + "\n" + "\n")
                rs_img1 = re.findall('<img.*?src="(.*?)".*?>', img)
                old_img = img
                new_img1 = ''
                cont = cont.replace(old_img, new_img1)

    return cont, 附件不在链接没改, 附件不在链接修改了, 附件存在链接没改


# 获取本地所有附件的名字
def each_file_name(files_path):

    file_name_list = []

    for root, dirs, files in os.walk(files_path, topdown=True):
        for name in files:
            file = os.path.join(root, name)
            file1 = file[file.rfind("\\")+1:]
            file_name_list.append(file1)
    return file_name_list


# 获取本所有附件完整的地址
def each_file_path(files_path):

    file_path_list = []
    for root, dirs, files in os.walk(files_path, topdown=True):
        for name in files:
            file_path_list.append(os.path.join(root, name))
    return file_path_list


# 判断传进来的路径是否存在，不存在就创建
def mk_dir(path):

    # 去除首位空格
    path = path.strip()

    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print(path + "创建成功")
    else:
        print(path + "目录已存在")
        pass



# 大致去除已有数据：时间被《span》标签分割的情况、本次不适用，因为我为了将该标签去除了，只保留div p 表格相关标签
def dispose_of_data_2(content):
    # 时间被《span》标签分割的情况
    """<span style="font-size: 19px;font-family: 仿宋_GB2312">2017</span>
    <span style="font-size: 19px;font-family: 仿宋_GB2312">年5月31日</span>"""
    all_span = re.findall('<span.*?>.*?</span>', content)

    if all_span:
        for span in all_span:
            span_1 = re.findall('<span.*?>(.*?)</span>', str(span))
            span_span = re.sub('<span.*?>', '', str(span_1[0])).replace("</span>", '').replace("  ", '').replace(
                "\n", '').replace("nbsp;", '')
            if span_1 and len(span_span) <= 6:
                now_span = span_1[0]
                content = content.replace(span, now_span)
    return content


# 处理头部的标题、行政处罚决定书、   顺序：2
def dispose_title(content):
    # 这一组是处理行政处罚决定书字样
    # 因为在前面是去除掉了span标签的影响，现在只考虑p
    行政处罚决定书 = re.findall(r'<p>.*?行政处罚决定书.*?</p>', content)

    if 行政处罚决定书:
        # 因为这个是在头部所以只考虑在匹配到后的集合中取第一个
        行政处罚决定书_cont = dispose_blank_character(行政处罚决定书[0])  # 去除这个p标签所有的空白符 nbsp;
        行政处罚决定书_1_char_num = word_count(行政处罚决定书_cont)  # 去除这个所有标签和非空字符统计字数

        # d当结果统计出来等于7个的时候是最完美的时候，为了防止出现其他情况特意放到了15
        # 先去除所有标签和空白字符，这样就只剩文字了，再加一个剧中的标签
        if 行政处罚决定书_1_char_num < 15:
            行政处罚决定书_cont_now = remove_label(行政处罚决定书_cont)
            content = content.replace(行政处罚决定书[0], ''.join(['<p align="center">' + 行政处罚决定书_cont_now + '</p>']))

    # 这一组是处理书文号的情况
    book_num = re.findall(re.compile(r'<p>.*?[监 罚 处 环  局 卫 医 残 政 办 建 管 字 市 房 产 管 理].*?\d号</p>'), content)
    if book_num:
        book_num_cont = dispose_blank_character(book_num[0])
        book_num_char_num = word_count(book_num_cont)

        if book_num_char_num<60:
            book_num_cont_now = remove_label(book_num_cont)
            content = content.replace(book_num[0], ''.join(['<p align="center">' + book_num_cont_now + '</p>']))

    # 这一组是处理处罚机构的落款问题
    # 执法机构 = re.findall(r'<p>[\u4E00-\u9FA5\uF900-\uFA2D]+[\局 ,\协会,\厅]</p>', content)
    执法机构 = re.findall(r'<p>.*?[\局 ,\协会,\厅,\处]</p>', content)
    if 执法机构:
        for 执法机构_i in 执法机构:
            执法机构_i_cont = dispose_blank_character(执法机构_i)
            执法机构_i_char_num = word_count(执法机构_i_cont)
            if 执法机构_i_char_num < 20:
                执法机构_i_cont_now = remove_label(执法机构_i_cont)
                content = content.replace(执法机构_i, ''.join(['<p align="right">' + 执法机构_i_cont_now + '</p>']))

    # 这一组是处理其他的落款问题：可能存在其他的落款
    # 判断依据是p标签个数大于12，且后面5个p标签的内容必须少于20个字
    # 这组是处理落款时间的格式: 以前直接使用p标签去匹配很容易匹配不到结果
    soup_p = BeautifulSoup(str(content), 'lxml')
    soup_p = soup_p.find_all('p')

    # 匹配日期
    for p in soup_p:
        # 匹配中文日期,必须除去 &nbsp; 的影响不然不饿能解决， 中文日期以年月日来分割来解决
        time_rs = re.findall(r'<p.*?>[ 零 ○ 0 O o 〇 Ｏ 一 二 三 四 五 六 七 八 九 十]{4}年[一 二 三 四 五 六 七 八 九 十 〇]{1,2}月[一 二 三 四 五 六 七 八 九 十 〇]{1,3}日</p>', str(dispose_blank_character(str(p))))  # 替换掉 空格和&nbsp; 的影响
        if time_rs:
            time_cont = p.text.strip().replace(" ", '').replace("&nbsp;", '')  # 匹配到的内容,除去空格的影响
            if len(time_cont) <= 15:  # 完整的中文日期最多只有13个字符：二零一七年十一月二十三日。防止出现问题，特意多留了两个
                print("匹配到中文的日期"+str(p))
                chinese_time = re.split('[年 月 日]', time_cont)  # 分割出来会以年 月 日 加一个空值组成一个长度为4的集合

                time1 = ['零', '○', '0', 'O', 'o', '〇', 'Ｏ', '一', '二', '三', '四', '五', '六', '七', '八', '九',
                         '十']
                time2 = ['0', '0', '0', '0', '0', '0', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                         ' 10']
                year_list = []
                month_list = []
                day_list = []
                if len(chinese_time[0]) == 4:  # 年份的长度必须等于4，一旦不成立那么这个日期就是有问题的直接就不替换为数字
                    for y in chinese_time[0]:
                        if y in time1:
                            index = time1.index(y)
                            yy = time2[index]
                            year_list.append(yy)

                    if len(chinese_time[1]) <= 2:  # 月份的长度必须小于等于2：十二
                        for m in chinese_time[1]:
                            if m in time1:
                                index1 = time1.index(m)
                                mm = time2[index1]
                                month_list.append(mm)
                    else:
                        break  # 月份的长度必须小于等于2，不满足就直接退出

                    if len(chinese_time[2]) <= 2:  # 日期长度可能为：1（一） 、 2（十二） 、 3（二十三）
                        print("ff")

                        for d in chinese_time[2]:
                            if d in time1:
                                print(d)
                                index1 = time1.index(d)
                                dd = time2[index1]
                                day_list.append(dd)

                    elif 2 < len(chinese_time[2]) <= 3:
                        for d in chinese_time[2]:
                            if d in time1:
                                print(d)
                                index1 = time1.index(d)
                                dd = time2[index1]
                                day_list.append(dd)
                    print(day_list)
                if year_list != [] and month_list != [] and day_list != []:  # 必须保证取出来的三个集合均不为空
                    print("yes")
                    Year = ''.join(str(i) for i in year_list).replace(" ", '')
                    if len(month_list) == 1:
                        Moth = str(month_list[0])
                    if len(month_list) >= 2:
                        print(month_list)
                        Moth = str(1)+str(month_list[-1])

                    if len(day_list) == 1:
                        Day = str(day_list[0])
                    if len(day_list) >= 2:
                        print(day_list[0])
                        if day_list[0].find("10") != -1:
                            Day = str(1)+str(day_list[-1])
                        if day_list[0].find("2") != -1 and day_list[1].find("10") != -1:
                            Day = str(2) + str(day_list[-1])
                        if day_list[0].find("1") != -1 and day_list[1].find("10") != -1:
                            Day = str(1) + str(day_list[-1])
                        if day_list[0].find("3") != -1 and day_list[1].find("10") != -1:
                            Day = str(3) + str(day_list[-1])
                        else:
                            Day = str(day_list[0])+str(day_list[-1])
                    Time1 = Year + "年" + Moth + "月" + Day + "日"
                    # print("中文时间" + Time1)
                    # 如果存在落款时间就加上个<p style="text-align: right;"> 让它居右显示
                    if Time1:
                        content = content.replace(str(p), ''.join(
                            ['<p align="right">' + Time1 + '</p>']))

                # 匹配数字日期：格式多样化，只有你想不到的没有他们做不到的

        # 匹配数字日期: 分为两类：一类是(年月日)、一类是(/ . - )
        """
        常规：2018年12月23日 
        eg：
            2018/12/23
            2018.12.23
            2018 年  12 月 23 日
    
        """
        # print("ppp"+ str(dispose_blank_character(str(p))))
        time_rs_1 = re.findall(r'<p.*?>\d{4}年\d{1,2}月\d{1,2}日</p>',  str(dispose_blank_character(str(p))))# 替换掉 空格和&nbsp; 的影响

        time_rs_2 = re.findall(r'<p.*?>\d{4}[\/ ,\. ,\-, \ ,\  ]\d{1,2}[\/ ,\. ,\-, \ ,\  ]\d{1,2}</p>', str(dispose_blank_character(str(p))))  # 替换掉 空格和&nbsp; 的影响

        # 如果是以年月日这类的日期，且长度小于15那就替换源标签为一个居右的标签
        if time_rs_1:
            time_cont_1 = dispose_blank_character(p.text.strip()) # 匹配到的内容,除去空格的影响
            if len(time_cont_1) <= 15:
                print("匹配到数字的日期" + str(p))
                chinese_time = re.split('[年 月 日]', time_cont_1)  # 分割出来会以年 月 日 加一个空值组成一个长度为4的集合

                if len(chinese_time) == 4:
                    year = chinese_time[0]
                    moth = chinese_time[1]
                    day = chinese_time[2]
                    date_now = '<p align="right">'+year+"年"+moth+"月"+day+"日"+'</p>'
                    content = content.replace(str(p), date_now)

        # 假如是第二类那将结果中的这些符号去除，再看结果的长度
        if time_rs_2:
            # 匹配到的内容,除去空格、&nbsp;、 / 、 - 、. 的影响
            time_cont_1 = dispose_blank_character(p.text.strip()).replace(" ", '').replace(".", '').replace("/", '').replace("-", '')
            if len(time_cont_1) <= 13:  # 长度最多为11
                # 现在将对应年月日的数字匹配出来,这个集合的长度必须是3
                time_rs_2_1 = re.findall(
                    r'<p.*?>(\d{4})[\/ ,\. ,\-, \ ,\  ](\d{1,2})[\/ ,\. ,\-, \ ,\  ](\d{1,2})</p>',
                    str(dispose_blank_character(str(p))))  # 替换掉 空格和&nbsp; 的影响

                # [('2014', '10', '31')] 结果是一个长度为1的集合，且内部是一个长度为3的元组
                if len(time_rs_2_1) == 1 and len(time_rs_2_1[0]) ==3:
                    print("yes")
                    date_now_2_1 = '<p align="right">' + str(time_rs_2_1[0][0]) + "年" + str(time_rs_2_1[0][1]) + "月" + str(time_rs_2_1[0][2]) + "日" + '</p>'
                    content = content.replace(str(p), date_now_2_1)
                else:
                    print("no")
    return content


# 去除空白字符：&nbsp;; 、 换行（\n）、制表符（\t）、 纸张换页（\f）、回车（\r）
def dispose_blank_character(content):
    content = str(content)
    content = content.replace('&nbsp;', '').replace("\n", '').replace("\f", '').replace("\r", '').replace("\t", '').replace("　", '').replace(" ", '').replace(" ",'')
    return content


# 去除标签：会去除空格和其他的空白字符
def remove_label(content):
    content = dispose_blank_character(content)
    content = content.replace(" ",'')
    content = re.sub('<[^>]*>', '', content)
    return content


# 去除标签统计字数:会去除空格和其他的空白字符
def word_count(content):
    content = dispose_blank_character(content)
    content = re.sub('<[^>]*>', '', content)
    content = re.sub(" ", '', content)
    word_num = len(content)
    return word_num


#  顺序：3
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


# 读取excel文件返回该文件所有数据和最大的行数，保存数据的时候记得使用返回的第一个参数 【data.save(excelFilePath)】
def open_excel_file(excel_file_path):
    data = openpyxl.load_workbook(excel_file_path)
    active = data.active
    table = data['Sheet1']
    rows = table.max_row

    return data, table, rows


# 处理表格中日期的问题【暂时只能处理数字的日期，中文日期还没写】 ： 2018/2/12 这种转化为6位数的字符串
def dispose_of_date_format(content):
    content = str(content)
    print(content)
    print(type(content))
    print(len(content))
    if content.find("/") != -1:
        content = content.replace(" ", '')
        rs = content.split("/")
        if len(rs) == 3:  # 假如是以向右的反斜杠来表示时间的，分割后必须是长度为3的一个集合，空格对分割无影响，不过还是先去除空格为好
            year = rs[0]
            moth = rs[1]
            day = rs[2]
            if len(year) == 4:
                if len(moth) == 1:
                    moth = str("0") + moth
                elif len(moth) == 2:
                    moth = moth
                else:
                    raise Exception("这个日期有问题，月份不是两位数也不是一位数，查看下")

                if len(day) == 1:
                    day = str("0") + day
                elif len(day) == 2:
                    day = day
                else:
                    raise Exception("这个日期有问题，日子不是一位数也不是两位数，查看下")
            else:
                raise Exception("这个日期有问题，年不是四位数，查看下")
        else:
            raise Exception("这个日期有问题，是以反斜杠表示的，但是分割后长度不等于3，丫的有问题，查看下")
    elif content.find("-") != -1:
        content = content.replace(" ", '')
        rs = content.split("-")
        if len(rs) == 3:  # 假如是以向右的短横线来表示时间的，分割后必须是长度为3的一个集合，空格对分割无影响，不过还是先去除空格为好
            year = rs[0]
            moth = rs[1]
            day = rs[2]
            if len(year) == 4:
                if len(moth) == 1:
                    moth = str("0") + moth
                elif len(moth) == 2:
                    moth = moth
                else:
                    raise Exception("这个日期有问题，月份不是两位数也不是一位数，查看下")

                if len(day) == 1:
                    day = str("0") + day
                elif len(day) == 2:
                    day = day
                else:
                    raise Exception("这个日期有问题，日子不是一位数也不是两位数，查看下")
            else:
                raise Exception("这个日期有问题，年不是四位数，查看下")
        else:
            raise Exception("这个日期有问题，是以反斜杠表示的，但是分割后长度不等于3，丫的有问题，查看下")
    elif content == '' or content == ' ' or content == 'None':
        pass
    elif len(str(content)) == 8:
        content = str(content)

    else:
        raise Exception("日期的格式不是反斜杠和短横线的形式，查看拿下")

    if content == '' or content == ' ' or content == 'None':
        pass
    elif len(str(content)) == 8:
        pass
    elif year and moth and day:
        date = year+moth+day
        return date
        print(date)

    else:
        raise Exception("日期不存在")


# 入口1 处理 全文
# if __name__ == '__main__':
#
#     excel_file_path = "D:\Python\PyCharm 20181.4\project\project1\G_1行政案例处理\工具包\四川省卫生委员会.xlsx"
#
#     data_table_rows = open_excel_file(excel_file_path)
#     data = data_table_rows[0]
#     table = data_table_rows[1]
#     rows = data_table_rows[2]
#
#     for row in range(2, rows+2):
#
#         print("正在读取第："+str(row)+"行的数据")
#         # title = table['E{0}'.format(row)].value
#         title_way = 'B'  # 标题所在单元格位置
#         cont_way1 = 'K'   # 全文所在单元位置
#         cont_way2 = 'L'   # 全文所在单元位置
#         word_count_way = 'Q'  # 预处理后的全文字数所在单元格位置
#         title = table['%s%s'%(title_way, row)].value
#         cont1 = table['%s%s'%(cont_way1, row)].value
#         cont2 = table['%s%s'%(cont_way2, row)].value
#         cont = (str(cont1) + str(cont2)).replace("None", '')
#         # cont = str(str(cont2))
#         print(cont)
#         print(type(cont))
#         cont = cont .replace("\\", '') .replace("?", '')  # 处理黄寿红转义符的问题
#         now_cont = dispose_of_data_1(cont)  # 处理标签的格式，以及将中文的括号改为英文状态的括号
#         now_cont = dispose_title(now_cont)
#         now_cont = dispose_of_data_end(now_cont)
#         print("处理标签后的全文now_cont,标题是"+str(title)+"\n\n，全文是"+str(now_cont))
#
#         # 处理过后的数据重新存放在新的四列中，每个单元格寸3万个字符，超出的放入下一个单元格
#
#         if 0 < len(now_cont) < 30000:
#             table['%s%s'%(cont_way1, row)] = now_cont
#             table['%s%s'%(word_count_way, row)] = word_count(now_cont)
#         elif 30000 < len(now_cont) < 60000:
#             table['%s%s'%(cont_way1, row)] = now_cont[:30000]
#             table['%s%s'%(cont_way2, row)] = now_cont[30000:]
#             table['%s%s'%(word_count_way, row)] = word_count(now_cont)
#         else:
#             print("这条数据好像超出6万个字符。因为原文只用2个单元格就能存下，貌似存在问题，请查看下啊" + str(title)+"\n")
#
#     data.save(excel_file_path)

# 入口2  检测附件
# if __name__ == '__main__':
#
#     excel_file_path = "D:\Python\PyCharm 20181.4\project\project1\G_1行政案例处理\工具包\【校对-上长传版】四川省卫生委员会.xlsx"
# #
#     data_table_rows = open_excel_file(excel_file_path)
#     data = data_table_rows[0]
#     table = data_table_rows[1]
#     rows = data_table_rows[2]
#     附件不在链接没改, 附件不在链接修改了, 附件存在链接没改  = [], [], []
#     for row in range(2, rows + 2):
#         print("正在读取第：" + str(row) + "行的数据")
#         # title = table['E{0}'.format(row)].value
#         title_way = 'B'  # 标题所在单元格位置
#         cont_way1 = 'K'   # 全文所在单元位置
#         cont_way2 = 'L'   # 全文所在单元位置
#         word_count_way = 'Q'  # 预处理后的全文字数所在单元格位置
#         title = table['%s%s'%(title_way, row)].value
#         cont1 = table['%s%s'%(cont_way1, row)].value
#         cont2 = table['%s%s'%(cont_way2, row)].value
#         cont = (str(cont1) + str(cont2)).replace("None", '')
#         # cont = str(str(cont2))
#         cont = cont .replace("\\", '') .replace("?", '')  # 处理黄寿红转义符的问题
#         file_path = "E:\行政案例附件"
#         rs = dispose__hyper_link(title, cont, file_path)
#         附件不在链接没改.append(rs[1])
#         附件不在链接修改了.append(rs[2])
#         附件存在链接没改.append(rs[3])
#     print("附件不在链接没改的情况" + str(附件不在链接没改))
#     print("附件不在链接修改了的情况" + str(附件不在链接修改了))
#     print("附件存在链接没改的情况" + str(附件存在链接没改))

# 入口三 ： 从excel导入到数据库

# if __name__ == '__main__':
#     excel_file_path = r"D:\Python\PyCharm 20181.4\project\project1\G_1行政案例处理\已处理完\1安全生产.xlsx"
#     # AdministrativeCase
#     data_table_rows = open_excel_file(excel_file_path)
#     data = data_table_rows[0]
#     table = data_table_rows[1]
#     rows = data_table_rows[2]
#     table_name = '[cnlaw2.0].dbo.[中华人民共和国环境生态部]'
#     # table_name = '[]'
#     conn_cursor = 链接数据库.get_connect_cursor()
#     conn = conn_cursor[0]
#     cursor = conn_cursor[1]
#     insert_sql = " "
#     i = 0
#     for row in range(2, rows+1):
#         print("正在读取第：" + str(row) + "行的数据")
#         i += 1
#         索引号 = str(table['{0}{1}'.format('N', row)].value)
#         if 索引号 == 'None':
#             索引号 = ''
#
#         生成日期 = str(table['{0}{1}'.format('R', row)].value)
#         if 生成日期 == 'None':
#             生成日期 = ''
#
#         # 机构=机构 区域=区域new1  类别=机构new   处罚日期=update处罚日期
#         insert_sql += """ UPDATE {0} set 索引号='{1}',生成日期='{2}' where id={3}""".format(table_name, 索引号, 生成日期, i)
#         print("测试语句" + str(insert_sql))
#         print("\n")
#         if row % 10 == 0 or row == rows:
#             print("最终语句" + str(insert_sql))
#             链接数据库.insert(conn, cursor, insert_sql)
#             insert_sql = ''


# 入口四 ： 根据excel中的id来导入数据到数据库
if __name__ == '__main__':
    excel_file_path = r"D:\Python\PyCharm 20181.4\project\project1\G_1行政案例处理\已处理完\公安数据2.xlsx"
    # AdministrativeCase
    data_table_rows = open_excel_file(excel_file_path)
    data = data_table_rows[0]
    table = data_table_rows[1]
    rows = data_table_rows[2]
    table_name = '[cnlaw2.0].dbo.[AdministrativeCase]'
    conn_cursor = 链接数据库.get_connect_cursor()
    conn = conn_cursor[0]
    cursor = conn_cursor[1]
    update_sql = " "
    i = 0
    for row in range(2, rows + 1):
        ID = str(table['{0}{1}'.format('A', row)].value)
        title = str(table['{0}{1}'.format('B', row)].value)
        update_sql += """update  {0} set 标题 = '{1}' WHERE ID={2} ;\n""".format(table_name, title, ID)
        print("测试语句" + str(update_sql))
        print("\n")
        if row % 100 == 0 or row == rows:
            print("最终语句" + str(update_sql))
            链接数据库.insert(conn, cursor, update_sql)
            update_sql = ''






























