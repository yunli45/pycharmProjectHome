# coding:utf-8
import re
import openpyxl
import os
import shutil


# 读取excel文件返回该文件所有数据和最大的行数，保存数据的时候记得使用返回的第一个参数 【data.save(excelFilePath)】
def open_excel_file(excel_file_path):
    data = openpyxl.load_workbook(excel_file_path)
    active = data.active
    table = data['Sheet1']
    rows = table.max_row

    return data, table, rows


# 为块级元素加一个《/br》
def br(excel_file_path):
    data_table_rows = open_excel_file(excel_file_path)
    data = data_table_rows[0]
    table = data_table_rows[1]
    rows = data_table_rows[2]
    # U
    for row in range(2, rows+1):
        # title = table['E{0}'.format(row)].value
        title = table['E%s'%(row)].value
        cont = table['U%s'%(row)].value  # 因为处理后的全文一个单元就能装下，所以此次加《/br》,只考虑一列

        cont = cont.replace("</div>", "</div><br/>")
        cont = cont.replace("</h1>", "</h1><br/>")
        cont = cont.replace("</h2>", "</h2><br/>")
        cont = cont.replace("</h3>", "</h3><br/>")
        cont = cont.replace("</h4>", "</h4><br/>")
        cont = cont.replace("</h5>", "</h5><br/>")
        cont = cont.replace("</h6>", "</h6><br/>")
        cont = cont.replace("</hr>", "</hr><br/>")
        cont = cont.replace("</p>", "</p><br/>")
        cont = cont.replace("</table>", "</table><br/>")
        table['U%s'%(row)] = cont

    data.save(excel_file_path)


# 读取表格中数据检查并处理全文中超链接、附件等是否有问题
def check_hyper_link(excel_file_path):
    data_table_rows = open_excel_file(excel_file_path)
    data = data_table_rows[0]
    table = data_table_rows[1]
    rows = data_table_rows[2]

    # cont1 = 'K2'
    # cont2 = 'L2'
    key_id = 1

    附件不在链接没改 = []
    附件不在链接修改了= []
    附件存在链接没改 = []
    for row in range(2, rows+1):
        print("正在读取第："+str(row)+"行的数据")
        # title = table['E{0}'.format(row)].value
        title = table['B%s'%(row)].value
        cont1 = table['K%s'%(row)].value
        cont2 = table['L%s'%(row)].value
        cont = (str(cont1) + str(cont2)).replace("None", '')
        cont = cont .replace("\\", '')  # 处理黄寿红转义符的问题
        now_cont = processing_label_format(cont)  # 处理标签的格式，以及将中文的括号改为英文状态的括号

        print("处理标签后的全文now_cont"+str(title)+"\n\n"+str(now_cont))

        # 处理过后的数据重新存放在新的四列中，每个单元格寸3万个字符，超出的放入下一个单元格
        if 0 < len(now_cont) < 30000:
            table['K%s'%(row)] = now_cont

        elif 0 < len(now_cont) < 60000:
            table['K%s' % (row)] = now_cont[:30000]
            table['L%s' % (row)] = now_cont[30000:]
        else:
            print("这条数据好像超出6万个字符。因为原文只用2个单元格就能存下，貌似存在问题，请查看下啊" + str(title)+"\n")

    data.save(excel_file_path)


# 处理a、img标签，除去各种跳转的情况，匹配本地相关附件是否存在
# file_path：为本地附件总目录F://环保局
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
                print("这个a标签是附件")
                # 假如是附件的形式，使用all_a结果集中每个元素的第一个值（超链接）和第二个值（文本内容）反向匹配这个标签的全部内容，并生成新的本地超链接a标签
                rs_a = re.findall('<a.*?href="(.*?)".*?>(.*?)</a>', a)
                a_hyper = rs_a[0][0]  # a标签的超链接
                a_text = rs_a[0][1]  # a标签的文本内容
                old_annex_a = a  # 原标签
                new_annex_a = '<a href="{0}">{1}</a>'.format(a_hyper, a_text)  # 现在的标签
                cont = cont.replace(old_annex_a, new_annex_a)  # 替换全文

                # 匹配本地附件是否存在
                # 超链接地址已经做了修改是属于我们服务器上面的地址， file_path = 'E:\环保局\环保局汇总'
                if str(a_hyper).find("/datafolder/环保局/") != -1:
                    print("这个超链接的地址是已经修改过的")
                    file_path1 = file_path
                    a_hyper_link = a_hyper.replace("/datafolder/环保局/", '').replace("/", "\\")
                    print("a_hyper_link"+a_hyper_link)
                    a_local_link = str(file_path1 + "\\" + a_hyper_link)
                    print("a_local_link"+a_local_link)
                    print(type(a_local_link))
                    # print("all_file_path_list" + str(all_file_path_list))
                    if a_local_link in all_file_path_list:
                        print("这个附件在本地是存在的")
                        pass
                    else:

                        print("这个附件的地址，/datafolder/环保局/已经修改但是本地附件好像保存错位置了，现在开始检查本地是否存在相应的附件，如果存在就将本地的文件移动到超链接中记录的地址,")
                        print("不存在那就是这条数据的附件可能存在缺失，现在开始检查本地是否存在相应的附件，存在的话就只是本地保存的地址好像错了，需要将该附件移动到文本超链接记录的目录下" + str(title) + "\n" + str(a_hyper))
                        a_annex_name = a_hyper[a_hyper.rfind("/")+1:]
                        print("a_annex_name"+a_annex_name)
                        # 这个附件名在本地是存在的，只是本地保存的地址好像错了
                        if a_annex_name in all_file_name_list:
                            for local_file_path in all_file_path_list:
                                if local_file_path.find(a_annex_name) != -1:
                                    print("找到了这个文件名在本地的路径" + local_file_path)

                            print("这个附件名在本地是存在的，只是本地保存的地址好像错了，现在开始将该附件移动到文本超链接记录的目录下")
                            a_hyper_link1 = a_hyper.replace("/datafolder/环保局/", '').replace("/", '\\')
                            print("a_hyper_link1" + a_hyper_link1)
                            a_hyper_link1 = a_hyper_link1[:(a_hyper_link1.rfind("\\"))]
                            print("a_hyper_link1.1" + a_hyper_link1)
                            a_local_link1 = file_path1 + "\\"+a_hyper_link1
                            a_local_path = a_local_link1
                            print("a_local_path"+a_local_path)
                            mk_dir(a_local_path)
                            old_path = local_file_path
                            new_path = a_local_path
                            # old_path 为原来文件全路径名（加上文件名），new_path为新的文件目录
                            try:
                                shutil.move(old_path, new_path)  # 不考虑文件在本地的路径是正确的情况，如果报错该文件在本地是存在的，那么就是上面的语法写错了
                            except:
                                pass
                        # 这个附件名在本地是不存在的，
                        else:
                            print("这个附件名在本地是不存在的"+title)
                            print("这个标签是" + str(a))
                            附件不在链接修改了.update({'{}'.format(title): '{}'.format(a)})
                # 超链接地址没有做修改，需要改成我们的地址，首先检查下本地的附件是否存在
                else:
                    print("这个超链接没有修改，现在开始检查本地的相应的附件是否存在")
                    a_annex_name1 = a_hyper[a_hyper.rfind("/")+1:]
                    if a_annex_name1 in all_file_name_list:
                        print("该附件在本地是存在的，只是超链接的地址没有修改，请手动修改")
                        附件存在链接没改.update({'{}'.format(title): '{}'.format(a)})
                    else:
                        print("这条数据的附件不存在，并且超链接的地址也没有修改，请重新下载该数据")
                        附件不在链接没改.update({'{}'.format(title): '{}'.format(a)})
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
                if img.find("/datafolder/环保局/") != -1:
                    print("这个图片的超链接的地址是已经修改过的")
                    file_path1 = file_path
                    img_hyper_link = img.replace("/datafolder/环保局/", '').replace("/", "\\")
                    img_local_link = str(file_path1 + "\\" + img_hyper_link)  # 上面那个是用于测试附件本地位置保存错误的情况
                    if img_local_link in all_file_path_list:
                        print("这个图片附件在本地路径是存在的")
                        pass
                    else:
                        print("这个图片附件的地址，/datafolder/环保局/已经修改但是本地附件好像保存错位置了，现在开始检查本地是否存在相应的附件，如果存在就将本地的文件移动到超链接中记录的地址,")
                        print("不存在那就是这条数据的附件存在缺失" + str(title))
                        img_annex_name = img_hyper[img_hyper.rfind("/") + 1:]
                        print("img_annex_name" + img_annex_name)
                        if img_annex_name in all_file_name_list:
                            for local_file_path in all_file_path_list:
                                if local_file_path.find(img_annex_name) != -1:
                                    print("找到了这个图片文件名在本地的路径" + local_file_path)

                            print("这个图片附件名在本地是存在的，只是本地保存的地址好像错了，现在开始将该附件移动到文本超链接记录的目录下")
                            img_hyper_link1 = img_hyper.replace("/datafolder/环保局/", '').replace("/", '\\')
                            print("a_hyper_link1" + img_hyper_link1)
                            img_hyper_link1 = img_hyper_link1[:(img_hyper_link1.rfind("\\"))]
                            print("img_hyper_link1.1" + img_hyper_link1)
                            img_hyper_link1 = file_path1 + "\\" + img_hyper_link1
                            img_local_path = img_hyper_link1
                            print("img_hyper_link1" + img_hyper_link1)
                            mk_dir(img_local_path)
                            old_path = local_file_path
                            new_path = img_local_path
                            # old_path 为原来文件全路径名（加上文件名），new_path为新的文件目录
                            try:
                                shutil.move(old_path, new_path)  # 不考虑文件在本地的路径是正确的情况，如果报错该文件在本地是存在的，那么就是上面的语法写错了
                            except:
                                pass
                        else:
                            print("这个图片的附件名在本地是不存在的" + title)
                            print("这个标签是" + str(img))
                            附件不在链接修改了.update({'{}'.format(title): '{}'.format(img)})

                # 超链接地址没有做修改是，需要改成我们的地址，首先检查下本地的附加是否存在
                else:
                    print("这个超链接没有修改，请查看相应的内容：" + title + "\n" + str(img))
                    print("现在开始检查本地的相应的附件是否存在")
                    img_annex_name1 = img_hyper[img_hyper.rfind("/") + 1:]
                    if img_annex_name1 in all_file_name_list:
                        print("该图片附件在本地是存在的，只是超链接的地址没有修改，请手动修改")
                        附件存在链接没改.update({'{}'.format(title): '{}'.format(img)})
                    else:
                        print("这条数据的附件不存在，并且超链接的地址也没有修改，请重新下载该数据")
                        附件不在链接没改.update({'{}'.format(title): '{}'.format(img)})
            else:
                print("这个img标签不是附件，是跳转" + str(img) + "\n" + "\n")
                rs_img1 = re.findall('<img.*?src="(.*?)".*?>', img)
                old_img = img
                new_img1 = ''
                cont = cont.replace(old_img, new_img1)

    return cont, 附件不在链接没改, 附件不在链接修改了, 附件存在链接没改


def processing_label_format(cont):

    cont = re.sub(r'\f', '/', cont)
    cont = re.sub(r'\\', '/', cont)

    cont = re.sub(r'（', '(', cont)
    cont = re.sub(r'）', ')', cont)

    cont = re.sub('<font.*?>', '', cont, flags=re.I)
    cont = re.sub('</font>', '', cont, flags=re.I)

    a_name = re.findall(r'<a.*?name=.*?>.*?</a>', cont)

    if a_name !=[]:
        for a_name_label in a_name:
            a_name_text = re.findall(r'<a.*?>(.*?)</a>', a_name_label)
            if a_name_text !=[]:
                cont = cont.replace(a_name_label, str(a_name_text[0]))

    all_p = re.findall('<p.*?>', cont, flags=re.I)
    if all_p != []:
        for ids, p in enumerate(all_p):
            p_label_format1 = re.findall('<p.*?(text-align|align)="(.*?)".*?>', p, re.I)
            p_label_format2 = re.findall('<p.*?style=".*?(text-align|align):.*?".*?>', p, re.I)
            if p_label_format1 != []:
                cont = cont.replace(p, '<p align="%s">' % (p_label_format1[0][1]))
            elif p_label_format2 != []:
                for pp in p_label_format2:
                    p_label_format2_1 = re.findall('<p.*?style=".*?(text-align|align):(right|left|center).*?".*?>', p, re.I)
                    if p_label_format2_1:
                        cont = cont.replace(p, '<p align="%s">' % (p_label_format2_1[0][1]))
                    else:
                        # print(p)
                        cont = cont.replace(p, '<p>')
            else:
                cont = cont.replace(p, '<p>')

    all_div = re.findall('<div.*?>', cont, flags=re.I)
    if all_div != []:
        for ids, div in enumerate(all_div):
            div_label_format1 = re.findall('<div.*?(text-align|align)="(.*?)".*?>', div, flags=re.I)
            div_label_format2 = re.findall('<div.*?style=".*?(text-align|align):.*?".*?>', div, flags=re.I)
            if div_label_format1 != []:
                cont = cont.replace(div, '<div align="%s">' % (div_label_format1[0][1]))
            elif div_label_format2 != []:
                for divdiv in div_label_format2:
                    div_label_format2_1 = re.findall('<div.*?style=".*?(text-align|align):(right|left|center).*?".*?>', div,
                                            flags=re.I)
                    if div_label_format2_1:
                        cont = cont.replace(div, '<div align="%s">' % (div_label_format2_1[0][1]))
                    else:
                        # divrint(div)
                        cont = cont.replace(div, '<div>')
            else:
                cont = cont.replace(div, '<div>')

        """
        先取出掉<span class="wzxq2_lianjie">分享的情况

        """
    cont = re.sub('<span.*?class="wzxq2_lianjie".*?>.*?</span>', '', cont, flags=re.I | re.S)

    all_span = re.findall('<span.*?>', cont, flags=re.I)
    if all_span != []:
        for ids, span1 in enumerate(all_span):
            span_label_format1 = re.findall('<span.*?(text-align|align)="(.*?)".*?>', span1, flags=re.I)
            span_label_format2 = re.findall('<span.*?style=".*?(text-align|align):.*?".*?>', span1, flags=re.I)
            if span_label_format1 != []:
                cont = cont.replace(span1, '<span align="%s">' % (span_label_format1[0][1]))
            elif span_label_format2 != []:
                for span2 in span_label_format2:
                    span_label_format2_1 = re.findall('<span.*?style=".*?(text-align|align):(right|left|center).*?".*?>', span1,
                                             flags=re.I)
                    if span_label_format2_1:
                        cont = cont.replace(span1, '<span align="%s">' % (span_label_format2_1[0][1]))
                    else:
                        # print(p)
                        cont = cont.replace(span1, '<span>')
            else:
                cont = cont.replace(span1, '<span>')

    cont = re.sub('<script.*?>.*?</script>', '', cont, flags=re.I | re.S)
    cont = re.sub('<style.*?>.*?</style>', '', cont, flags=re.I | re.S)

    # td tr table
    cont = re.sub('<td.*?>', '<td>', cont, flags=re.I | re.S)
    cont = re.sub('<tr.*?>', '<tr>', cont, flags=re.I | re.S)
    cont = re.sub('<th.*?>', '<th>', cont, flags=re.I | re.S)
    cont = re.sub('<table.*?>', '<table>', cont, flags=re.I | re.S)

    cont = re.sub(r'<?xml:namespace .*?>', '', cont, flags=re.I)
    cont = re.sub(r'<o:p.*?>', '', cont, flags=re.I)
    cont = re.sub(r'</o:p>', '', cont, flags=re.I)

    cont = re.sub(r'<aname=.*?>', '', cont, flags=re.I)

    # 因为在此之前的抓取的数据附近地址没有修改，现在将所有的a标签，img标签替换为空
    cont = re.sub('<a.*?>', '', cont).replace('</a>', ' ')
    cont  = re.sub('<img.*?>', '', cont).replace('<img>','')

    # 为块级元素加一个br
    cont = cont.replace("</div>", "</div><br/>")
    cont = cont.replace("</h1>", "</h1><br/>")
    cont = cont.replace("</h2>", "</h2><br/>")
    cont = cont.replace("</h3>", "</h3><br/>")
    cont = cont.replace("</h4>", "</h4><br/>")
    cont = cont.replace("</h5>", "</h5><br/>")
    cont = cont.replace("</h6>", "</h6><br/>")
    cont = cont.replace("</hr>", "</hr><br/>")
    cont = cont.replace("</p>", "</p><br/>")
    cont = cont.replace("</table>", "</table><br/>")
    cont = cont.replace("<br/><br/><br/><br/><br/><br/>", "<br/>")
    cont = cont.replace("<br/><br/><br/><br/><br/>", "<br/>")
    cont = cont.replace("<br/><br/><br/><br/>", "<br/>")
    cont = cont.replace("<br/><br/><br/>", "<br/>")
    cont = cont.replace("<br/><br/>", "<br/>")

    return cont


def find_img(cont):
    all_img = re.findall(r'<img.*?>', cont)
    return True if all_img else False


def find_a(cont):
    all_img = re.findall(r'<a.*?>', cont)
    return True if all_img else False


def each_file_name(files_path):
    # 获取本地所有附件的名字
    file_name_list = []
    for root, dirs, files in os.walk(files_path, topdown=True):
        for name in files:
            file = os.path.join(root, name)
            file1 = file[file.rfind("\\")+1:]
            file_name_list.append(file1)
    return file_name_list


def each_file_path(files_path):
    # 获取本所有附件完整的地址
    file_path_list = []
    for root, dirs, files in os.walk(files_path, topdown=True):
        for name in files:
            file_path_list.append(os.path.join(root, name))
    return file_path_list


def mk_dir(path):
    # 判断传进来的路径是否存在，不存在就创建
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
        # pass
        print(path + "目录已存在")


# file_path = 'E:\环保局\环保局汇总\环保局'
excel_file_path = 'D:\Python\PyCharm 20181.4\project\project1\云南、上海预处理\云南省行政处罚案例数据.xlsx'
# check_hyper_link(excel_file_path, file_path)
check_hyper_link(excel_file_path)
# print(each_file_name(file_path))
# print(each_file_path(file_path))
