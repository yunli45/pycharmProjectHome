# coding:utf-8
import re
from bs4 import BeautifulSoup


# 大体上从全文中去提取
def extracting_information(title, content):
    content = str(content).replace('<a name="qfDate"></a>', '')
    content = str(content).replace('<a name=.*?>.*?</a>', '')
    content = re.sub('<a.*?>', '', content).replace("</a>", '')
    content = content.replace("&nbsp;", '').replace("\u3000", '').replace("\t", '')

    # 浏阳市的数据先取发布时间和处罚（发布）机构
    cont_soup = BeautifulSoup(content, 'lxml')
    cont_soup_date = cont_soup.find_all('span', attrs={'class': 'span_sy'})
    if cont_soup_date != []:
        cont_date = re.findall('发布时间：.*?来源：(.*?)', str(cont_soup_date[0]))
        if cont_date and len(cont_date) == 2:
            date = cont_date[0]  # 处罚（发布）时间
            law_enforcement = "浏阳市" + cont_date[0]  # 执法机构  在另一个标签中
        else:
            date = ''
            law_enforcement = ''

    # 被处罚人
    punished_people1 = re.findall('.*?当事人[: ：](.*?)[; ；。，,<]', content)
    punished_people2 = re.findall('.*?处罚人[: ：](.*?)[; ；。，,<]', content)
    punished_people3 = re.findall('>.*?(.*?)[: ：]<', content)  # 这种情况是全文只有一个被处罚人或者单位，且在第一行，一般在一个span中

    if punished_people1 != [] and punished_people2 == [] and punished_people3 == []:
        if len(str(punished_people1[0])) < 15:
            punished_people = str(punished_people1[0])
        else:
            punished_people = ''
    elif punished_people2 != [] and punished_people1 == [] and punished_people3 == []:
        if len(str(punished_people2[0])) < 15:
            punished_people = str(punished_people2[0])
        else:
            punished_people = ''
    elif punished_people3 != [] and punished_people1 == [] and punished_people2 == [] and len(punished_people3[0]) < 12:
        if len(str(punished_people3[0])) < 15:
            punished_people = str(punished_people3[0])
        else:
            punished_people = ''
    else:
        punished_people = ''

    # 被处罚机构
    punished_institution1 = re.findall('.*?事人[: ：](.*?)[; ；。，,<]', content)
    punished_institution2 = re.findall('.*?[受 被]被处罚机构[: ：](.*?)[; ；。，,<]', content)
    punished_institution3 = re.findall('.*?被处罚单位[: ：](.*?)[; ；。，,<]', content)

    if punished_institution1 != [] and punished_institution2 == [] and punished_institution3 == []:
        if len(str(punished_institution1[0])) < 15:
            punished_institution = str(punished_institution1[0])
        else:
            punished_institution = ''
    elif punished_institution2 != [] and punished_institution1 == [] and punished_institution3 == []:
        if len(str(punished_institution2[0])) < 15:
            punished_institution = str(punished_institution2[0])
        else:
            punished_institution = ''
    elif punished_institution3 != [] and punished_institution1 == [] and punished_institution2 == []:
        if len(str(punished_institution3[0])) < 15:
            punished_institution = str(punished_institution3[0])
        else:
            punished_institution = ''
    else:
        punished_institution = ''

    # 区域
    # area1 = re.findall(r'住所[: ：](.*?)<', content)
    # area2 = re.findall(r'住址[: ：](.*?)<', content)
    #
    # if area1 and area2 == []:
    #     area = area1[0]
    # elif area2 and area1 == []:
    #     area = area2[0]
    # else:
    #     area = ''

    area = ''

    # 法人
    legal_person1 = re.findall('法人[: ：](.*?)[; ；。，,<]', content)
    legal_person2 = re.findall('法定代表人[: ：](.*?)[; ；。，,<]', content)
    legal_person3 = re.findall('法定代表人或负责人[: ：](.*?)[; ；。，,<]', content)
    legal_person4 = re.findall('法定代表人(负责人)[: ：](.*?)[; ；。，,<]', content)

    if legal_person1 != [] and legal_person2 == [] and legal_person3 == [] and legal_person4 == []:
        if len(legal_person1[0]) < 15:
            legal_person = legal_person1[0]
        else:
            legal_person = ''
    elif legal_person2 != [] and legal_person1 == [] and legal_person3 == [] and legal_person4 == []:
        if len(legal_person2[0]) < 15:
            legal_person = legal_person2[0]
        else:
            legal_person = ''
    elif legal_person3 != [] and legal_person1 == [] and legal_person2 == [] and legal_person4 == []:
        if len(legal_person3[0]) < 15:
            legal_person = legal_person3[0]
        else:
            legal_person = ''

    elif legal_person4 != [] and legal_person1 == [] and legal_person2 == [] and legal_person3 == []:
        if len(legal_person4[0]) < 15:
            legal_person = legal_person4[0]
        else:
            legal_person = ''
    else:
        legal_person = ''

    # 书文号，在标题中
    # rs_book_number = re.findall(r'.*?([\（ \(].*?\d号)', title)  # 在标题中匹配到书文号

    """
    浏阳市书文号：
        在标题中，先取行政处罚决定书（。*？）
        没有找到的情况下：
            先【判断 \d号 是否存在，存在那标题就是一个完整的书文号，不存在那就没有书文号

    """

    if title.find("行政处罚决定书") != -1:
        book_number = title[title.find("行政处罚决定书") + 7:]
        # 去掉书文号中的空格
        book_number = book_number.replace(" ", '')

    else:
        rs_title = re.findall(".*?\d号", title)
        if rs_title:
            book_number = title.replace(" ", '')
        else:
            book_number = ''

    # 执法机构  在另一个标签中
    # law_enforcement = ''

    # 处罚时间被几个span标签分开了，先去除
    content_soup = BeautifulSoup(content, 'lxml')
    content_soup = content_soup.find_all('p')
    print(content_soup)
    if content_soup != []:
        date_p = content_soup[-1].text.strip()
        date1 = re.findall(r'.*?\d{4}年\d{1,2}月\d{1,2}日.*?', date_p)
        if date1 != [] and len(date1[-1]) < 15:
            date = date1[-1]
        else:
            content = re.sub(r'<span.*?>', '', content).replace('</span>', '').replace("&nbsp;", '').replace(" ",
                                                                                                             '').replace(
                "\u3000", '').replace("\t", '')
            content = content.replace('<aname="qfDate"></a>', '')
            date2 = re.findall(r'<st1:chsdate.*?day="(.*?)".*?month="(.*?)".*?year="(.*?)".*?>', content)
            if date2 != []:
                if date2 != [] and len(date2[-1]) == 3:  # ('19', '6', '2008')
                    date = date2[-1][2] + "年" + date2[-1][1] + "月" + date2[-1][0] + "日"
                else:
                    date = ''
            else:
                date = ''

    return (book_number, legal_person, punished_people, punished_institution, law_enforcement, area, date)


# 浏阳市住建部数据比较规范，书文号第三个p,被处罚人在第四个 ，处罚机构在倒数第二个，时间倒数第一个
def extracting_information_2(title, content):
    content = str(content)
    cont_soup = BeautifulSoup(content, 'lxml')
    cont_soup = cont_soup.find_all('p')
    book_number = str(cont_soup[2].text.strip()).replace(" ", '')
    legal_person = ''
    punished_people = str(cont_soup[3].text.strip()).replace("当事人：", '').replace(" ", '')
    punished_institution = ''
    law_enforcement = str(cont_soup[-2].text.strip()).replace(" ", '')
    area = ''
    date = str(cont_soup[-1].text.strip()).replace(" ", '')

    return (book_number, legal_person, punished_people, punished_institution, law_enforcement, area, date)


# 浏阳市林业局数据比较规范，书文号就是标题,被处罚人在第3个 ，处罚机构就是浏阳市森林公安局，时间倒数第一个或第二个
def extracting_information_3(title, content):
    content = str(content)
    rs_book_num = re.findall('.*?\d号', title)
    if rs_book_num != []:
        book_number = title
    else:
        book_number = ''

    cont_soup = BeautifulSoup(content, 'lxml')
    cont_soup = cont_soup.find_all('p')
    if cont_soup != []:
        legal_person = ''

        if str(cont_soup[0].text.strip()).find("被处罚") != -1 and len(str(cont_soup[0].text.strip())) < 50:
            punished_people = str(cont_soup[0].text.strip()).replace("被处罚人姓名：", '').replace(" ", '').replace("被处罚单位名称：", '').replace("。", '')
        elif str(cont_soup[1].text.strip()).find("被处罚") != -1 and len(str(cont_soup[2].text.strip())) < 50:
            punished_people = str(cont_soup[2].text.strip()).replace("被处罚人姓名：", '').replace(" ", '').replace("被处罚单位名称：", '').replace("。", '')

        elif str(cont_soup[2].text.strip()).find("被处罚") != -1 and len(str(cont_soup[2].text.strip())) < 50:
            punished_people = str(cont_soup[2].text.strip()).replace("被处罚人姓名：", '').replace(" ", '').replace("被处罚单位名称：", '').replace("。", '')
        elif str(cont_soup[3].text.strip()).find("被处罚") != -1 and len(str(cont_soup[3].text.strip())) < 50:
            punished_people = str(cont_soup[3].text.strip()).replace("被处罚人姓名：", '').replace(" ", '').replace("被处罚单位名称：", '').replace("。", '')
        else:
            punished_people = ''

        punished_institution = ''
        law_enforcement = '浏阳市森林公安局'
        area = ''
        p_1 = str(cont_soup[-1].text.strip()).replace(" ", '')
        p_2 = str(cont_soup[-1].text.strip()).replace(" ", '')
        if p_1 !=  '' and len(p_1) < 20:
            date = str(cont_soup[-1].text.strip()).replace(" ", '')
        else:
            if p_2 != ''and len(p_2) < 20:
                date = str(cont_soup[-2].text.strip()).replace(" ", '')
            else:
                date = ''
    else:
        legal_person = ''
        punished_people = ''
        punished_institution = ''
        law_enforcement = '浏阳市森林公安局'
        area = ''
        date = ''

    return (book_number, legal_person, punished_people, punished_institution, law_enforcement, area, date)


 # 全文在一个表格中，参照
    # http://www.cbrc.gov.cn/zhuanti/xzcf/getPcjgXZCFDocListDividePage/dalian.html?current=1
    # http://www.cbrc.gov.cn/dalian/docPcjgView/1794379C259845B0A9865CDEA6F5466C/22.html
def extracting_information_table(title, content):
    content = content
    print(content)
    content_soup = BeautifulSoup(str(content), 'lxml')
    content_tr_num = len(content_soup.findAll('tr'))
    print("这条数据一共有：" + str(content_tr_num) + "个tr")
    content_td_num = len(content_soup.findAll('td'))
    print("这条数据一共有：" + str(content_td_num) + "个td")
    content_p_num = len(content_soup.findAll('p'))
    print("这条数据有：" + str(content_p_num) + "个P")

    td_list = content_soup.find_all('td')
    for ids, td in enumerate(td_list):
        print(ids, td)
        if str(td).find("处罚决定书文号") != -1:
            idd = ids
            break

    if idd:
        # 书文号
        book_number = str(td_list[idd + 1].text.strip())

        # 被处罚人
        punished_people = str(td_list[idd + 4].text.strip().replace("-", ''))

        # 被处罚单位
        punished_institution = str(td_list[idd + 7].text.strip().replace("-", ''))

        # 法人
        legal_person = str(td_list[idd + 9].text.strip().replace("-", ''))

        cont = "<p>主要违法事实（案由）：" + str(td_list[idd + 11].text.strip()) + "</p>\n<p>行政处罚依据：" + str(
            td_list[idd + 13].text.strip()) + "</p>\n<p>行政处罚决定：" + str(
            td_list[idd + 15].text.strip()) + "</p>\n<p>作出行政处罚的机关名称：" + str(
            td_list[idd + 17].text.strip()) + "</p>\n<p>作出处罚决定的日期：" + str(td_list[idd + 19].text.strip()) + "</p>"

        # 时间
        date = str(td_list[idd + 19].text.strip())
        rss = re.split('[年 月 日]', date)
        year = rss[0]
        moth = rss[1]
        day = rss[2]
        if len(moth) == 1:
            moth = "0" + moth
        day = rss[2]
        if len(day) == 1:
            day = "0" + day
        date = year + moth + day
        print("时间格式" + date)

        # 执法机构
        law_enforcement = str(td_list[idd + 17].text.strip())

        area = ''
        return (book_number, legal_person, punished_people, punished_institution, law_enforcement, area, date, cont)


# 全文是几个table组合的，参照：http://www.sycredit.gov.cn:8282/credit-web-portal/website/wsreportingdoublepublicityquery/punishdetail?id=20181115132001479214256
def extracting_information_table_1(title, content):
    content_soup = BeautifulSoup(str(content), 'lxml')
    content_soup = content_soup.find_all('td')
    if content_soup:
        book_number = content_soup[1].text.strip()
        legal_person = content_soup[17].text.strip()
        punished_people = content_soup[7].text.strip()
        punished_institution = content_soup[7].text.strip()
        law_enforcement = content_soup[29].text.strip()
        area = ''
        date = content_soup[-7].text.strip().replace("/", '')

        cont = "<p>行政处罚决定书文号：" + content_soup[1].text.strip() + "</p>\n<p>行政相对人名称：" + content_soup[
            7].text.strip() + "</p>\n<p>统一社会信用代码：" + content_soup[9].text.strip() + "</p>\n<p>法定代表人姓名:" + content_soup[
                   17].text.strip() + "</p>\n<p>处罚事由：" + content_soup[19].text.strip() + "</p>\n<p>处罚依据：" + \
               content_soup[21].text.strip() + "</p>\n<p>处罚类别1：" + \
               content_soup[23].text.strip() + "</p>\n<p>处罚类别2：" + content_soup[25].text.strip() + "</p>\n<p>处罚结果：" + \
               content_soup[27].text.strip() + "</p>\n<p>处罚机关:" + content_soup[29].text.strip() + "</p>\n<p>处罚决定日期:" + \
               content_soup[31].text.strip() + "</p>"

    return (book_number, legal_person, punished_people, punished_institution, law_enforcement, area, date, cont)


# 全文十一额table，
# 参照：http://credit.dl.cn/sgs/punish.jsp  credit.dl.cn/sgs/punish-view.jsp?id=e896b6fd87f741dabcf6921eeaf26637
def extracting_information_table_2(title, content):
    content_soup = BeautifulSoup(str(content), 'lxml')
    content_soup = content_soup.find_all('td')
    if content_soup:
        book_number = content_soup[2].text.strip()
        legal_person = content_soup[34].text.strip()
        punished_people = ''
        punished_institution = content_soup[20].text.strip()
        law_enforcement = content_soup[32].text.strip()
        area = ''
        date_1 = content_soup[38].text.strip()

        print("date_1" + str(date_1))
        if date_1:
            date_1 = str(date_1).split(" ")
            moth_e = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            moth_n = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
            moth_1 = date_1[1].replace("\n", '').replace("\r", '').replace(" ", '')
            day = date_1[2]

            for ids, moth_2 in enumerate(moth_e):
                if moth_1 == moth_2:
                    moth = moth_n[ids]

            date = date_1[-1].replace("\n", '').replace("\r", '').replace(" ", '') + moth + day
            date_2 = date_1[-1].replace("\n", '').replace("\r", '').replace(" ", '') + "年" + moth + "月" + day + "日"
        else:
            date = ''
            date_2 = ''

        cont = '<p align="center">行政处罚决定书</p>' + "<p>行政处罚决定书文号:" + content_soup[2].text.strip() + "</p>\n<p>事项编号:" + \
               content_soup[4].text.strip() + "</p>\n<p>公示日期:" + content_soup[6].text.strip() + "</p>\n<p>案件名称:" + \
               content_soup[8].text.strip() + "</p>\n<p>处罚结果:" + content_soup[10].text.strip() + "</p>\n<p>处罚事由:" + \
               content_soup[12].text.strip() + "</p>\n<p>处罚依据:" + content_soup[14].text.strip() + "</p>\n<p>处罚类别1:" + \
               content_soup[16].text.strip() + "</p>\n<p>处罚类别2:" + content_soup[
                   18].text.strip() + "</p>\n<p>行政相对人名称(单位名称):" + content_soup[20].text.strip() + "</p>\n<p>统一社会信用代码:" + \
               content_soup[22].text.strip() + "</p>\n<p>组织机构代码:" + content_soup[26].text.strip() + "</p>\n<p>工商注册号:" + \
               content_soup[28].text.strip() + "</p>\n<p>税务登记码:" + content_soup[30].text.strip() + "</p>\n<p>处罚机关:" + \
               content_soup[32].text.strip() + "</p>\n<p>法定代表人姓名:" + content_soup[34].text.strip() + "</p>\n<p>地方编码:" + \
               content_soup[36].text.strip() + "</p>\n<p>处罚决定日期:" + date_2

    return (book_number, legal_person, punished_people, punished_institution, law_enforcement, area, date, cont)


# 全文是个表格 MsoNormalTable ，直接保留表格，去除所有的属性，提取相关信息  银监局
# http://www.cbrc.gov.cn/chinese/home/docViewPage/60200406&current=1
# www.cbrc.gov.cn/chinese/home/docView/A3C559FA994D4E86B896168327FAFC45.html
def extracting_information_table_4(content):
    content = str(content)
    content_soup = BeautifulSoup(content, 'lxml')
    content_soup = content_soup.find_all('td')
    if content_soup:
        book_number = content_soup[1].text.strip()
        legal_person = content_soup[9].text.strip()
        punished_people = content_soup[4].text.strip()
        punished_institution = content_soup[7].text.strip()
        law_enforcement = content_soup[-3].text.strip()
        area = ''
        date = content_soup[-1].text.strip()
        cont = content

    return (book_number, legal_person, punished_people, punished_institution, law_enforcement, area, date, cont)


# 全文是一个表格
# http://218.76.40.80:9000/hnxyfw/xzcf/index_515.jhtml 、 http://218.76.40.80:9000/hnxyfw/channel/pjallXzcfInfo.jspx?id=21
def extracting_information_table_5(content):
    # 在td中去取值
    content = str(content)
    cont_soup = BeautifulSoup(content, 'lxml')
    cont_soup_td = cont_soup.find_all('td')
    book_number = str(cont_soup_td[1].text.strip())
    date = str(cont_soup_td[7].text.strip())
    law_enforcement = "湖南省交通运输厅"
    punished_people = str(cont_soup_td[19].text.strip())
    punished_institution = ''
    area = ''
    legal_person = str(cont_soup_td[23].text.strip())

    return (book_number, legal_person, punished_people, punished_institution, law_enforcement, area, date)


# 全文的内容在一个form中，并且包含一个table，先不管table直接使用正则通过关键字提取
# http://xzzf.spb.gov.cn/SPXzzfApp/base/spBaseXzzfOpenAction_provinceOf!toSpXzzfOpenSC.action?infoTypeCode=3&undertakeUnitCode=10010044
def extracting_information_table_5(content):
    content = str(content)
    book_number = ''  # 没有书文号
    legal_person =  re.findall(r'法定代表人：(.*?)<br/>', content)[0]
    punished_people = re.findall(r'企业（个人）名称：(.*?)<br/>', content)[0]
    punished_institution = punished_people
    law_enforcement = re.findall(r'承办单位：(.*?)</td>', content)[0]
    area = ''
    date = re.findall(r'公开日期：(.*?)</td>', content)[0]
    return (book_number, legal_person, punished_people, punished_institution, law_enforcement, area, date)


# 全文是附件（或者一张图片）、也可能是文字形式的
# 现在头部的标签中包含了 书文号（可能存在，没有的话就去文章中，找不到就没有了）、发布时间（首页提取）、发布机构（首页也能提取）、
def extracting_information_table_5(content):
    content = str(content)
    # 必须先去除span标签的影响
    content = re.sub(r'<span.*?>', '', content).replace("</span>", '')
    book_number_1 = re.findall(r'行政处罚决定书文号：(.*?)</p>', content)
    if book_number_1!=[]:
        book_number = book_number_1[0]
    else:
        book_number = ''

    legal_person_1 = re.findall(r'法定代表人: (.*?)</p>', content)
    if legal_person_1 != []:
        legal_person = legal_person_1[0]
    else:
        legal_person = ''

    # 这种可以匹配两种情况，但是结果一个数组，数组的元素是一个元组（’匹配表达式'，'相应的匹配结果'），取值的时候取数组的第一个元素（元组）的第二个值
    punished_people_1 = re.findall(r"(被处罚人:|被检查单位：)(.*?)</p>", content)

    if punished_people_1 !=[]:
        punished_people = punished_people_1[0][1]
    else:
        punished_people = ''
    punished_institution = punished_people
    law_enforcement = ''
    area = ''
    date = ''
    return (book_number, legal_person, punished_people, punished_institution, law_enforcement, area, date)


def extracting_information_table_6(content):
    content = str(content)
    content_soup = BeautifulSoup(content, 'lxml')
    content_soup = content_soup.find_all('td')
    book_number = content_soup[5].string

    return book_number









# cont ="""[<div class="xxgk_bmxl" style=" margin-bottom: 30px;">
# <table cellpadding="0" cellspacing="0" width="100%">
# <tbody>
# <tr>
# <td width="70"><strong>名　　称：</strong></td>
# <td height="25" style="padding-right:5px">河北省财政厅关于河北省种子管理总站的行政处罚决定书</td>
# <td width="70"><strong>发布机构：</strong></td>
# <td nowrap="">省财政厅</td>
# </tr>
# <tr>
# <td><strong>发文字号：</strong></td>
# <td height="25" nowrap="">冀财处罚〔2019〕1号</td>
# <td><strong>发布日期：</strong></td>
# <td nowrap="">2019年01月22日</td>
# </tr>
# <tr>
# <td><strong>主 题 词：</strong></td>
# <td height="25" style="padding-right:5px"></td>
# <td><strong>主题分类：</strong></td>
# <td nowrap="">财政</td>
# </tr>
# </tbody>
# </table>
# </div>]
# """
# ss = extracting_information_table_6(content=cont)
# print(ss)