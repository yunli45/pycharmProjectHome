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


# 全文在一个ul下面 http://www.hxcredit.gov.cn/jcms/sgs.do?type=penalty  http://www.hxcredit.gov.cn/jcms/PenaltyDetail.do?id=10025
def extracting_information_table_7(content):
    content = str(content)
    content = content.replace(u'\xa0', u'')
    content_soup = BeautifulSoup(content, 'lxml')
    content_soup = content_soup.find_all('ul', attrs={'class':'creditsearch-tagsinfo-ul'})
    area = ''
    if content_soup:
        for i in content_soup:
            li = i.find_all("li")
            if li:
                book_number = li[1].text.replace("'",'').replace("行政处罚决定书文号：", '').replace('行政许可决定书文号：', '')
                legal_person = li[13].text.replace("'法定代表人姓名:",'').replace("'", '').replace("法定代表人姓名：", '')
                if legal_person =="null":
                    legal_person = ''
                # print(legal_person)
                date = li[16].text.replace("'",'').replace("处罚决定日期：", '').replace('数据更新时间戳：', '')
                cont = str(li).replace('[', '').replace(']', '').replace(',', '\n').replace("null", '')
                cont = re.sub('<li.*?>', '<li style="list-style-type:none;">', str(cont))
                cont = re.sub('<strong.*?>', '', str(cont))
                cont = re.sub('</strong.*?>', '', str(cont)).replace('?', '')

    else:
        raise Exception("""对不起没有找到<ul class="creditsearch-tagsinfo-ul">这个标签""")
    return (book_number, legal_person, area, date, cont)
    # return (book_number, legal_person, punished_people, punished_institution, law_enforcement, area, date)


def extracting_information_table_8(content):
    content = str(content)
    content_soup = BeautifulSoup(content, 'lxml')
    content_soup = content_soup.find_all('table', attrs={'class': 'table table-hover'})
    area = ''
    if content_soup:
        for i in content_soup:
            tr = i.find_all('tr')
        if  tr:
            book_number = tr[3].text.replace("\n", '').replace('行政许可决定书文号','').replace(' ', '')
            book_number = re.sub('制作日期.*?文书字轨','', str(book_number)).replace(":", '').replace("：",'')
            legal_person = tr[11].text.replace("\n", '').replace('法定代表人姓名','').replace(' ', '')
            cont = str(tr).replace('[', '').replace(']', '').replace(',', '\n').replace("null", '')
            cont = re.sub('<tr.*?>', '<tr>', str(cont))
            cont = re.sub('<td.*?>', '<td>', str(cont))
            cont = re.sub('<th.*?>', '<th>', str(cont))
            cont = '<table border="1" cellspacing="0" align="center">\n' + cont +'\n</table>'
    return (book_number,legal_person, cont)

def extracting_information_table_9(content):
    content = str(content)
    content_soup = BeautifulSoup(content, 'lxml')
    content_soup = content_soup.find_all('table', attrs={'class': 'table table-hover'})
    area = ''
    if content_soup:
        for i in content_soup:
            tr = i.find_all('tr')
        if  tr:
            title = tr[0].text.replace("\n", '').replace('案件名称','').replace(' ', '')
            punished_people = tr[5].text.replace("\n", '').replace('行政相对人名称','').replace(' ', '')
            law_enforcement = tr[16].text.replace("\n", '').replace('处罚机关','').replace(' ', '')
            book_number = tr[6].text.replace("\n", '').replace(' ', '').replace('行政处罚决定文书号','')
            book_number = re.sub('制作日期.*?文书字轨','', str(book_number)).replace(":", '').replace("：",'')
            legal_person = tr[12].text.replace("\n", '').replace('法定代表人姓名','').replace(' ', '')
            date = tr[14].text.replace("\n", '').replace('处罚决定日期','').replace(' ', '')
            cont = str(tr).replace('[', '').replace(']', '').replace(',', '\n').replace("null", '')
            cont = re.sub('<tr.*?>', '<tr>', str(cont))
            cont = re.sub('<td.*?>', '<td>', str(cont))
            cont = re.sub('<th.*?>', '<th>', str(cont))
            cont = '<table border="1" cellspacing="0" align="center">\n' + cont +'\n</table>'
    return (title, book_number, punished_people, law_enforcement, legal_person, date, cont)


def extracting_information_table_10(content):
    content = str(content)
    content_soup = BeautifulSoup(content, 'lxml')
    content_soup = content_soup.find_all('table')
    area = ''
    if content_soup:
        for i in content_soup:
            td = i.find_all('td')
            book_number = td[9].text
            punished_people = td[0].text
            law_enforcement = td[15].text
            legal_person = td[5].text
            date = td[8].text
            cont =  i
            cont = re.sub('<table.*?>', '<table border="1" cellspacing="0" align="center">', str(cont))
            cont = re.sub('<tr.*?>', '<tr>', str(cont))
            cont = re.sub('<td.*?>', '<td>', str(cont))
            cont = re.sub('<th.*?>', '<th>', str(cont))
            cont = re.sub('<span.*?>', '', str(cont)).replace('</span>', '')
    return (book_number, punished_people, law_enforcement, legal_person, date, cont)


def extracting_information_table_11(content):
    content = str(content).strip("\n \t").replace("\n", '').replace("\t", '')
    content_soup = BeautifulSoup(content, 'lxml')
    content_soup = content_soup.find_all('table', attrs={'id':'maintable'})
    area = ''
    if content_soup:
        for i in content_soup:
            td = i.find_all('td')
            legal_person = td[23].text
            date = td[27].text
            cont = str(i)
            cont = re.sub('<table.*?>', '<table border="1" cellspacing="0" align="center">', str(cont))
            cont = re.sub('<tr.*?>', '<tr>', str(cont))
            cont = re.sub('<td.*?>', '<td>', str(cont))
            cont = re.sub('<th.*?>', '<th>', str(cont))
            cont = re.sub('<span.*?>', '', str(cont)).replace('</span>', '')
    return (legal_person, date, cont)
    # return (book_number, punished_people, law_enforcement, legal_person, date, cont)



ss = """



<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>双公示行政处罚（标准）</title>
<style type="text/css">
body{
	margin:0 auto;
	font-size:12px;
	}
td{
	padding: 10px 12px !important;
	height:25px;
}
.title {
    line-height: 50px;
    font-size: 24px;
    border-width: 0 0 1px 0;
    text-align: center;
    padding-top: 10px;
    padding-right: 20px;
    padding-bottom: 0;
    padding-left: 20px;
}
.info_item {
    line-height: 30px;
    position: relative;
    height: 30px;
    margin-bottom: 10px;
    border-top-width: 0;
    border-right-width: 0;
    border-bottom-width: 1px;
    border-left-width: 0;
    border-top-style: solid;
    border-right-style: solid;
    border-bottom-style: solid;
    border-left-style: solid;
    border-top-color: #CCC;
    border-right-color: #CCC;
    border-bottom-color: #CCC;
    border-left-color: #CCC;
}
</style>
</head>
<body>
<div class="container clearfix">




<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<link href="../../hnxm/css/page.css" rel="stylesheet" type="text/css" />
<div class="logo">
<a href="#"><img src="../../hnxm/images/logo.png"></a>
<form name="searchform4" id="searchform" action="../../index/Search.html" method="post" style=" font-size:12px">
<div class="search" style="width:600px;">
<div style="float:right;">
    <div style="float:left; margin-bottom:5px;"><input name="keyword" id="keyword" type="text" value="请输入你想要搜索的内容" style="line-height:28px;" onclick="onclear();" /></div>
    <div style="float:left"><a href="#" style="float:right; margin:0px;"><img src="../../hnxm/images/searchbtn.png" border="0" width="56" height="28" onclick="to_submit();"/></a></div>
    </div>
    <div style="float:right;width:355px;">
    <span style="color:#2f6698; font-weight:bold;float:left;">热门搜索：</span><a style="margin:0px;margin-right:5px;"  href="javascript:void(0);" onclick="to_submit1("畜牧");">畜牧</a><a style="margin:0px;margin-right:5px;"  href="javascript:void(0);" onclick="to_submit1("信息化");">信息化</a><a style="margin:0px;margin-right:5px;" href="javascript:void(0);" onclick="to_submit1("检疫");">检疫</a><a style="margin:0px;margin-right:5px;"  href="javascript:void(0);" onclick="to_submit1("法规");">法规</a><a style="margin:0px;margin-right:5px;"  href="javascript:void(0);" onclick="to_submit1("节能减排");">节能减排</a></div>
   </div>
</form>
		</div>
        <!--login end-->
        <!-- nav -->
        <div class="nav">
        	<ul class="clearfix">
        		<li><a href="../../">首页</a></li>
        		<li><a href="../../hnxm/B125index_1_PS17.html">要闻动态</a></li>
        		<li><a href="../../info/ListInfo1Act.html">政务公开</a></li>
        		<li><a href="../../hnxm/B132index_1_PS17.html">网上办事</a></li>
        		<li><a href="../../hnxm/B137index_1_PS17.html">科技推广</a></li>
        	</ul>
        </div>
<script type="text/javascript">
    	function  to_submit(){
			var keyword=document.getElementById("keyword").value;
			if(keyword!=""){
				if(keyword!="请输入你想要搜索的内容"){
					document.getElementById("searchform").submit();
				}else{
					alert("请输入你想要搜索的内容");
					return false;
				}
			}else{
				alert("请输入你想要搜索的内容");
				return false;
			}			
		}
		function onclear(){
			document.getElementById("keyword").value="";
		}
		function  to_submit1(keyword){
			document.getElementById("keyword").value=keyword;
			if(keyword!=""){
				if(keyword!="请输入你想要搜索的内容"){
					document.getElementById("searchform").submit();
				}else{
					alert("请输入你想要搜索的内容");
					return false;
				}
			}else{
				alert("请输入你想要搜索的内容");
				return false;
			}			
		}
    </script>
<div style="width:1000px; margin:0 auto; background:#FFF; margin-bottom:5px;">
<div style="width:998px; height:30px; margin:0 auto;border:solid 1px #DADADA;background-repeat:repeat-x; background:url(../hnxm/images/tylm_1.jpg);">
	<div style="float:left; width:20px; height:30px;"></div><div style="width:20px; text-align:center; float:left; height:30px;"><img src="../hnxm/images/tylm_7.gif" style="margin-top:5px;"></div><div style="float:left;line-height:30px;padding-left:10px;"><span style="color:#2F2F2F; font-weight:bold;">您当前的位置：</span><a href="/"style="color:#2F2F2F;">首页</a> >双公示><a href="../publicity/ListPunishInfo.html">行政处罚（标准）</a>  
</div>
</div>
</div>
<div class="title">对河南邦达科技有限公司有兽药生产许可证生产假兽药的行政处罚</div>
<div class="info_item">&nbsp;&nbsp; <span class="qz">作者:省畜牧局</span> &nbsp;&nbsp; <span id="cms_article_arsource" class="qz">阅读次数：2016 &nbsp;&nbsp;</span><span id="cms_article_pubdate" class="qz">发布时间：2018-02-23 16:54&nbsp;&nbsp;</span>											
 </div>
<table bgcolor="#CCCCCC" class="tableborder" id="maintable" border="0" cellspacing="1" cellpadding="3" width="100%" align="center" style="color:#666; line-height:25px; height:25px;">
        <tr bgcolor="#ffffff">
          <td width="20%" align="right">行政处罚文书决定号</td>
          <td width="80%">豫牧（兽药）罚决字〔2018〕第1号
          </td>
        </tr>
        <tr bgcolor="#ffffff">
          <td width="20%" align="right">案件名称</td>
          <td width="80%">有兽药生产许可证生产假兽药案
          </td>
        </tr>
        <tr bgcolor="#ffffff">
          <td width="20%" align="right">处罚类别</td>
          <td width="80%">
             暂扣或者吊销许可证、暂扣或者吊销执照
          </td>
        </tr>
        <tr bgcolor="#ffffff">
          <td width="20%" align="right">处罚事由</td>
          <td width="80%" style="text-indent:2em;">有兽药生产许可证生产假兽药

          </td>
        </tr>
        <tr bgcolor="#ffffff">
          <td width="20%" align="right">处罚依据</td>
          <td width="80%" style="text-indent:2em;">《兽药管理条例》第五十六条第一款、第七十条第一款

          </td>
        </tr>
        <tr bgcolor="#ffffff">
          <td width="20%" align="right">处罚结果</td>
          <td width="80%">吊销当事人的兽药生产许可证、主要负责人终身不得从事兽药生产、经营活动

          </td>
        </tr>
        <tr bgcolor="#ffffff">
          <td width="20%" align="right">行政相对人名称</td>
          <td width="80%">河南邦达科技有限公司
          </td>
        </tr>
        <tr bgcolor="#ffffff">
          <td width="20%" align="right">统一社会信用代码</td>
          <td width="80%">91410105674139084T（1-1）
          </td>
        </tr>
        <tr bgcolor="#ffffff">
          <td width="20%" align="right">组织机构代码</td>
          <td width="80%">
          </td>
        </tr>
        <tr bgcolor="#ffffff">
          <td width="20%" align="right">工商登记号</td>
          <td width="80%">
          </td>
        </tr>
        <tr bgcolor="#ffffff">
          <td width="20%" align="right">税务登记号</td>
          <td width="80%">
          </td>
        </tr>
        <tr bgcolor="#ffffff">
          <td width="20%" align="right">法定代表人姓名</td>
          <td width="80%">王军胜
          </td>
        </tr>
        <tr bgcolor="#ffffff">
          <td width="20%" align="right">居民身份证号</td>
          <td width="80%">410105197705012796
          </td>
        </tr>
        <tr bgcolor="#ffffff">
          <td width="20%" align="right">许可生效期</td>
          <td width="80%">2018-02-05
          </td>
        </tr>
        <tr bgcolor="#ffffff">
          <td width="20%" align="right">许可截止期</td>
          <td width="80%">
          </td>
        </tr>
        <tr bgcolor="#ffffff">
          <td width="20%" align="right">许可机关</td>
          <td width="80%">河南省畜牧局
          </td>
        </tr>
        <tr bgcolor="#ffffff">
          <td width="20%" align="right">地方编码</td>
          <td width="80%">410000
          </td>
        </tr>
        
        <tr bgcolor="#ffffff">
          <td width="20%" align="right">当前状态</td>
          <td width="80%">
          正常
          </td>
        </tr>        
        <tr bgcolor="#ffffff">
          <td width="20%" align="right">数据更新时间</td>
          <td width="80%">2018-02-23 16:54
          </td>
        </tr>
        <tr bgcolor="#ffffff">
          <td width="20%" align="right">备注</td>
          <td width="80%">
          </td>
        </tr>
    </table>


<link href="../../hnxm/css/index.css" rel="stylesheet" type="text/css" />
<div class="footer" style="width:1000px;float: left;">
    <hr width="60%" style="margin:0px auto;">
    <p style="line-height:25px;">Copyright©2010-2020 河南畜牧业信息网 WWW.HNXMY.GOV.CN. All rights reserved.</p>
    <p style="line-height:25px;"><a href="../../hnxm/RSTY--Contact--RSNO--201322.html">联系我们</a>&nbsp;&nbsp;<a href="http://www.miibeian.gov.cn/" target="_blank">豫ICP备14022199号</a></p>
   <div style="width:450px;float:left;text-align:right;"><script type="text/javascript">document.write(unescape("%3Cspan id="_ideConac" %3E%3C/span%3E%3Cscript src="http://dcs.conac.cn/js/17/000/0000/40670185/CA170000000406701850001.js" type="text/javascript"%3E%3C/script%3E"));</script></div>
<div style="width:200px;float:left;padding-top:12px;"><script id="_jiucuo_" sitecode="4100000006" src="http://pucha.kaipuyun.cn/exposure/jiucuo.js"></script></div>
</div>
</div>
</body>
</html>
"""



extracting_information_table_11(ss)