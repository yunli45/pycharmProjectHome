# coding:utf-8
import re
from bs4 import BeautifulSoup


# 大体上从全文中去提取
def extracting_information(title, content):
    print(content)
    print(title)
    content = str(content)
    # 被处罚机构
    # punished_institution = re.findall('当事人[: ：](.*?)<', content)
    # punished_institution_1 = punished_institution[0]
    #
    # if punished_institution_1.find(",")!=-1 or punished_institution_1.find("，") !=-1:
    #     if punished_institution_1.find(",") != -1:
    #         punished_institution_1 = punished_institution_1[:punished_institution_1.find(",")]
    #     elif punished_institution_1.find("，") !=-1:
    #         punished_institution_1 = punished_institution_1[:punished_institution_1.find("，")]
    punished_institution_1 = ''

    # 被处罚人
    # punished_people = re.findall('当事人[: ：](.*?)<', content)
    # punished_people_1 = punished_people[0]
    #
    # if punished_people_1.find(",") != -1 or punished_people_1.find("，") != -1:
    #     if punished_people_1.find(",") != -1:
    #         punished_people_1 = punished_people_1[:punished_people_1.find(",")]
    #     elif punished_people_1.find("，") != -1:
    #         punished_people_1 = punished_people_1[:punished_people_1.find("，")]
    punished_people_1 = ''

    # 区域
    # area = re.findall(r'住所|住址[: ：](.*?)<', content)
    # area_1 = area[0].replace("。", '')
    area_1 = ''
    # 法人
    legal_person = ''

    # 书文号，在标题中
    # book_number =title[:title.rfind("号")+1]
    book_number = ''
    # 执法机构
    law_enforcement = '国家能源局东北监管局'
    date, cont = '',''

    return  (book_number, legal_person, punished_people_1, punished_institution_1, law_enforcement, area_1)


# 全文在一个表格中，参照 http://www.cbrc.gov.cn/zhuanti/xzcf/getPcjgXZCFDocListDividePage/dalian.html?current=1 、http://www.cbrc.gov.cn/dalian/docPcjgView/1794379C259845B0A9865CDEA6F5466C/22.html
def extracting_information_table(title,content):

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
        print(ids,td)
        if str(td).find("处罚决定书文号")!=-1:
            idd = ids
            break

    if idd:
        # 书文号
        book_number = str(td_list[idd+1].text.strip())

        # 被处罚人
        punished_people = str(td_list[idd+4].text.strip().replace("-",''))

        # 被处罚单位
        punished_institution = str(td_list[idd+7].text.strip().replace("-",''))

        # 法人
        legal_person = str(td_list[idd+9].text.strip().replace("-",''))

        cont = "<p>主要违法事实（案由）："+str(td_list[idd+11].text.strip()) + "</p>\n<p>行政处罚依据："+str(td_list[idd+13].text.strip())+"</p>\n<p>行政处罚决定："+str(td_list[idd+15].text.strip())+"</p>\n<p>作出行政处罚的机关名称："+str(td_list[idd+17].text.strip())+"</p>\n<p>作出处罚决定的日期："+str(td_list[idd+19].text.strip())+"</p>"

        # 时间
        date = str(td_list[idd+19].text.strip())
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
        print("时间格式"+date)

        # 执法机构
        law_enforcement = str(td_list[idd+17].text.strip())

        area = ''
        return(book_number, legal_person, punished_people, punished_institution, law_enforcement, area, date, cont)


# 全文是几个table组合的，参照：http://www.sycredit.gov.cn:8282/credit-web-portal/website/wsreportingdoublepublicityquery/punishdetail?id=20181115132001479214256
def extracting_information_table_1(title,content):

    content_soup = BeautifulSoup(str(content), 'lxml')
    content_soup = content_soup.find_all('td')
    if content_soup:
        book_number = content_soup[1].text.strip()
        legal_person = content_soup[17].text.strip()
        punished_people = content_soup[7].text.strip()
        punished_institution = content_soup[7].text.strip()
        law_enforcement = content_soup[29].text.strip()
        area = ''
        date = content_soup[-7].text.strip().replace("/",'')

        cont  = "<p>行政处罚决定书文号："+content_soup[1].text.strip() + "</p>\n<p>行政相对人名称：" + content_soup[7].text.strip() + "</p>\n<p>统一社会信用代码：" + content_soup[9].text.strip() + "</p>\n<p>法定代表人姓名:" + content_soup[17].text.strip() + "</p>\n<p>处罚事由：" + content_soup[19].text.strip() + "</p>\n<p>处罚依据：" + content_soup[21].text.strip() + "</p>\n<p>处罚类别1：" + \
               content_soup[23].text.strip() + "</p>\n<p>处罚类别2：" + content_soup[25].text.strip() + "</p>\n<p>处罚结果：" + \
               content_soup[27].text.strip() + "</p>\n<p>处罚机关:" + content_soup[29].text.strip() + "</p>\n<p>处罚决定日期:" + \
               content_soup[31].text.strip() + "</p>"

    return (book_number, legal_person, punished_people, punished_institution, law_enforcement, area, date, cont)


# 全文十一额table， 参照：http://credit.dl.cn/sgs/punish.jsp
# credit.dl.cn/sgs/punish-view.jsp?id=e896b6fd87f741dabcf6921eeaf26637
def extracting_information_table_2(title,content):

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

        print("date_1"+str(date_1))
        if date_1:
            date_1 = str(date_1).split(" ")
            moth_e = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            moth_n = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
            moth_1 = date_1[1].replace("\n", '').replace("\r", '').replace(" ", '')
            day = date_1[2]

            for ids, moth_2 in enumerate(moth_e):
                if moth_1== moth_2:
                    moth = moth_n[ids]

            date = date_1[-1].replace("\n", '').replace("\r", '').replace(" ", '')+moth+day
            date_2 = date_1[-1].replace("\n", '').replace("\r", '').replace(" ", '')+"年"+moth+"月"+day+"日"
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


def extracting_information_table_3(content):

    soup = BeautifulSoup(content, 'lxml')
    content_soup = soup.find_all('td')
    title = content_soup[1].text.strip()
    book_num = content_soup[0].text.strip()
    legal_person = content_soup[8].text.strip()
    punished_people = ''
    punished_institution = content_soup[3].text.strip()
    law_enforcement = content_soup[14].text.strip()
    area = ''
    date = content_soup[17].text.strip().replace("/", '')
    date_1 = date[:4] + "年" + date[4:6] + "月" + date[6:] + "日"
    cont = "<p>行政处罚决定书文号：" + book_num + "</p>\n<p>处罚名称：" + title + "</p>\n<p>行政相对人名称：" + punished_institution + "</p>\n<p>统一社会信用代码：" + \
           content_soup[4].text.strip() + "</p>\n<p>组织机构代码：" + content_soup[5].text.strip() + "</p>\n<p>工商登记码：" + \
           content_soup[6].text.strip() + "</p>\n<p>税务登记号：" + content_soup[
               7].text.strip() + "</p>\n<p>法定代表人姓名：" + legal_person + "</p>\n<p>处罚事由：" + content_soup[
               9].text.strip() + "</p>\n<p>处罚依据：" + content_soup[10].text.strip() + "</p>\n<p>处罚类别1：" + content_soup[
               11].text.strip() + "</p>\n<p>处罚类别2：" + content_soup[12].text.strip() + "</p>\n<p>处罚结果：" + content_soup[
               13].text.strip() + "</p>\n<p>处罚机关：" + law_enforcement + "</p>\n<p>处罚决定日期：" + date_1 + "</p>\n<p>地方编码：" + \
           content_soup[16].text.strip()

    return (book_num, legal_person, punished_people, punished_institution, law_enforcement, area, date, cont, title)


