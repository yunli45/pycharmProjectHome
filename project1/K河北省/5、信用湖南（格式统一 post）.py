# coding:gb18030
import re
import requests
from bs4 import BeautifulSoup
from K河北省.工具包 import 链接数据库,附件下载程序,预处理模块, 提取信息, 动态访问
from K河北省.工具包.判断url前面的点返回完整的请求地址 import returnSRC
import time

class Utils(object):
    # 一些共用的初始化参数
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10-12.0; WOW64) AppleWebKit/537.36 (KHTML,  like Gecko) Chrome/67.0.3396.99 Safari/537.36',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10-12.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}

        # 这一组用于提取每一面中信息（标题、src、时间）
        self.page_regular_expression = '<a href="(.*?)" .*?>(.*?)</a></div><div class="xzx01">.*?</div><div class="xzx01 mot02">(.*?)</div><div class="xzx01 mot02">.*?</div><div class="xzx01 mot02">.*?</div>'
        self.page_label_type = 'div'
        self.page_label_selector = 'class'
        self.page_label_selector_name = 'table-box'

        # 这一组用于提取详细数据页面的信息
        self.cont_label_type = 'div'
        self.cont_label_selector = 'class'
        self.cont_label_selector_name = 'row'

# 访问网址:post
    def get_page_data(self, url, data):
        response = requests.post(url, data=data, headers=self.headers)
        status_code = response.status_code
        # print("状态码1"+str(status_code))
        if status_code == 200:
            # response = response.content.decode('utf-8')
            response = response.content.decode('gb18030')
        else:
            if status_code == 202:
                while True:
                    response = requests.post(url, data=data, headers=self.heders)
                    status_code = response.status_code
                    # print("状态码2" + str(status_code))
                    if status_code == 200:
                        # response = response.content.decode('utf-8')
                        response = response.content.decode('gb18030')
                    else:
                        pass

            elif status_code == 400:
                print("这里出现网址找不到，查看网址是否正确" + str(url))

            elif status_code == 404:
                print("这里出现网址找不到，查看网址是否正确" + str(url))
                pass

        print("状态码3" + str(status_code))
        return response

# 访问网址：get
    def get_page_data_1(self, url):
        response = requests.get(url, headers=self.headers)
        status_code = response.status_code
        # print("状态码1"+str(status_code))
        if status_code == 200:
            # response = response.content.decode('utf-8')
            response = response.content.decode('gb18030')
        else:
            if status_code == 202:
                while True:
                    response = requests.get(url, headers=self.heders)
                    status_code = response.status_code
                    # print("状态码2" + str(status_code))
                    if status_code == 200:
                        # response = response.content.decode('utf-8')
                        response = response.content.decode('gb18030')
                    else:
                        pass

            elif status_code == 400:
                print("这里出现网址找不到，查看网址是否正确" + str(url))

            elif status_code == 404:
                print("这里出现网址找不到，查看网址是否正确" + str(url))
                pass
        return response

    def pare_page_data(self, page_url, table_name, save_path, source_library, province, annex_local):

        # 共计1771页
        # 首页提取：名称、执法部门、处罚日期、发布日期、 文中提取被处罚人、法人
        for page_no in range(1192, 1772):
            # penalty_date 处罚日期
            # release_date 发布日期
            src_list, penalty_date_list, release_date_list, title_list, law_enforcement_list = [], [], [], [], []
            # if page_no == 1:
            #     page_url_1 = page_url
            # else:
            #     page_url_1 = page_url[:page_url.rfind("=")+1] + str(page_no)
            """
                因为是post请求网址不变，参数有变化,妈的数学不好的话，还真不好找出他传入参数的规律
            """
            print("# # # # # # # # # # # # # # #这是第：" + str(page_no) + "页 # # # # # # # # # # # # # # # # # # # #")
            # print(page_url_1)
            page_url_1 = "http://www.credithunan.gov.cn:30816/publicity_hn/webInfo/punishmentProxy.do?startrecord="+str((int(page_no)-1)*10+1)+"&endrecord="+str(int(page_no)*10)+"&perpage=10&totalRecord=17707"
            # response = self.get_page_data(page_url_1, parameter)
            response = self.get_page_data_1(page_url_1)
            # break
            print(response)
            """
            
            # 提取页面信息 : 
            
            """
            # rs_soup = BeautifulSoup(response, 'lxml')
            # rs_soup = rs_soup.find_all('div', attrs={'class': 'default_pgContainer'})
            # rs_soup = str(rs_soup[0]).replace("\n", '').replace("\r", '').replace("\t"
            #                                                                       "", '').replace('\xa0','')
            # rs = re.findall(r'var initData = \[(.*?)\]', response)
            rs_list = re.findall(r'"CF\$(.*?)\$(.*?)\$(.*?)\$(.*?)\$(.*?)"', str(response))

            # rs_list = re.findall("""<td height="35" style="padding-left:20px"><a href="(.*?)".*?title="(.*?)">.*?</a></td><td align="center" width="150">.*?</td><td align="center" width="140">(.*?)</td><td align="center" width="110">(.*?)</td>""", str(rs_soup))
            if rs_list:
                for i in rs_list:
                    src_list.append(i[0])
                    # book_num_list.append(i[1])
                    title_list.append(i[1])
                    law_enforcement_list.append(i[2])
                    penalty_date_list.append(i[3])
                    release_date_list.append(i[4]) # 发布时间（公示时间）
                if src_list:
                    for ids, src in enumerate(src_list):
                        title_1 = title_list[ids]
                        # book_num_1 = book_num_list[ids]
                        title = title_1
                        release_date = release_date_list[ids]
                        penalty_date = penalty_date_list[ids]
                        content_src = "http://www.credithunan.gov.cn:30816/publicity_hn/webInfo/punishmentDetail.do?id="+ src
                        print("content_src"+str(content_src))
                        law_enforcement = law_enforcement_list[ids]

                        # data_id 用于区分这条数据的唯一性（取这条数据请求地址最后一个反斜杠后面的字符串）(本次取网址取下来的url)
                        data_id = src
                        page_no_position = "这是第" + str(page_no) + "页的第" + str(ids + 1) + "条的数据"
                        # 以这条数据的完整请求地址来查询已有的数据是否存在，存在那这条数据就pass
                        sql_1 = "select *  from 行政案例数据库.dbo.{0} where 这条数据完整的请求地址='{1}'".format(table_name, content_src)

                        # 改进了链接数据的各个方法，现在可以一次链接获取链接对象和游标，多次使用
                        connect_cursor = 链接数据库.get_connect_cursor()
                        conn = connect_cursor[0]
                        cursor = connect_cursor[1]

                        # 查询
                        data_id_rs = 链接数据库.query(cursor, sql_1)

                        if data_id_rs is not None:
                            print("这条数据在已有的数据库中已存在，现在已经paa掉了，依据的原则是这条数据完整的请求地址,标题为： " + str(title))
                            pass
                        else:
                            """
                            提取详细数据页面的相关信息：
                                提取头部信息：发布机构、发布时间、书文号
                                详细信息均在：<div id="zoom">这个标签中
                            """
                            cont = self.get_page_data_1(content_src)
                            print(cont)
                            # cont_soup = BeautifulSoup(cont, 'lxml')
                            """
                            改善下： 现在将全文内容所在的标签、标签属性、标签名以参数的形式传入
                            """
                            # 全文内容
                            # Label_name = "td"
                            # Label_class = "valign"
                            # Label_class_val = "top"
                            # cont_soup_1 = cont_soup.find_all('{0}'.format(Label_name), attrs={'{0}'.format(Label_class): '{0}'.format(Label_class_val)})
                            # if cont_soup_1 != []:
                            #     cont_header = str(cont_soup_1[0]).replace("\n", '').replace("\r", '').replace("\t"
                            #                                                   "", '')
                            # else:
                            #     raise Exception(""" 对不起全文没有找到<{0} {1}="{2}">这个标签，请查看下具体的情况""".format(Label_name, Label_class, Label_class_val) + str(
                            #         title) + "  " + str(content_src))
                            # cont_header = cont_header.replace("\r", '').replace('\n', '')
                            # info_header_booknum = 提取信息.extracting_information_table_6(cont_header)
                            # cont = 预处理模块.dispose_of_data('', content_src, str(cont_cont), save_path, annex_local)

                            # 提取书文号、被处罚机构、法人、处罚机构、处罚时间
                            cont_h = re.findall('<td.*?class="xzcf_xx".*?>(.*?)</td>', str(cont), flags=re.S|re.M)
                            cont_c = re.findall('<td.*?class="xzcf_jds".*?>(.*?)</td>', str(cont), flags=re.S|re.M)
                            title = title
                            if cont_h:
                                book_num = cont_h[0]
                                punished_people_and_legal = cont_h[1]
                                punished_people_and_legal = punished_people_and_legal.replace("&nbsp;", '')
                                punished_people = ''
                                punished_institution = punished_people_and_legal[:punished_people_and_legal.find("<span")]
                                legal_person = punished_people_and_legal[punished_people_and_legal.find("</span>") + 7:]
                            else:
                                raise Exception("""全文没有找到书文号等信息，<td.*?class="xzcf_xx".*?>(.*?)</td>""")
                            if cont_c:
                                cont_cc = cont_c[0]
                            else:
                                raise Exception("""全文没有找到全文内容，<td.*?class="xzcf_jds".*?>(.*?)</td>""")

                            cont = '<p>行政处罚决定书文号：' + book_num + "</p><p>行政相对人名称：" + punished_institution + "</p><p>法定代表人（或单位负责人）："+ legal_person + "</p><p>执法部门：" + law_enforcement + "</p><p>作出行政处罚的日期：" + penalty_date + "</p><p>行政处罚决定书（全文或摘要）："+ str(cont_cc)+"</p>"

                            law_enforcement = law_enforcement
                            penalty_date = penalty_date  # 处罚时间
                            area = ''

                            # 查询数据库中最大showid,第一次不存在指定为13300000，以后每条数据加1
                            sql_2 = "select max(showid)  from 行政案例数据库.dbo.{0}".format(table_name)

                            # 查询
                            max_show_id_rs = 链接数据库.query(cursor, sql_2)
                            if max_show_id_rs[0] is None:
                                max_show_id = 13300000
                            else:
                                max_show_id = max_show_id_rs[0] + 1

                            # 插入数据库
                            if len(cont) < 30000:
                                insert_sql = "insert into 行政案例数据库.dbo.{0}(标题, 书文号, 法定代表人, 被处罚人, 被处罚单位或机构, 执法机构, 处罚时间, 这条数据请求地址, 这条数据完整的请求地址, 这条数据属于第几页的第几条, 模块首页的url, 来自于那个模块, 省份, 区域, showid, dataid, 文本内容1, 发布时间) VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}') ".format(table_name, title, book_num,  legal_person,  punished_people,  punished_institution,  law_enforcement, penalty_date, content_src, content_src, page_no_position, page_url_1, source_library, province, area, max_show_id, data_id, cont, release_date)

                            elif 30000 < len(cont) < 60000:
                                cont1 = cont[:30000]
                                cont2 = cont[30000:60000]
                                insert_sql = "insert into 行政案例数据库.dbo.{0}(标题, 书文号, 法定代表人, 被处罚人, 被处罚单位或机构,执法机构 , 处罚时间, 这条数据请求地址, 这条数据完整的请求地址, 这条数据属于第几页的第几条, 模块首页的url, 来自于那个模块, 省份, 区域, showid, dataid, 文本内容1, 文本内容2, 发布时间) VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}') ".format(table_name, title, book_num,  legal_person,  punished_people,  punished_institution,  law_enforcement, penalty_date, src, content_src, page_no_position, page_url_1, source_library, province, area, max_show_id, data_id, cont1, cont2, release_date)
                            elif 60000 < len(cont) < 90000:
                                cont1 = cont[:30000]
                                cont2 = cont[30000:60000]
                                cont3 = cont[60000:90000]

                                insert_sql = "insert into 行政案例数据库.dbo.{0}(标题, 书文号, 法定代表人, 被处罚人, 被处罚单位或机构, 执法机构, 处罚时间 , 这条数据请求地址, 这条数据完整的请求地址, 这条数据属于第几页的第几条, 模块首页的url, 来自于那个模块, 省份, 区域, showid, dataid, 文本内容1, 文本内容2, 文本内容3, 发布时间) VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}','{20}') ".format(table_name, title, book_num,  legal_person,  punished_people,  punished_institution,  law_enforcement, penalty_date, src, content_src, page_no_position, page_url_1, source_library, province, area, max_show_id, data_id, cont1, cont2, cont3, release_date)

                            elif 90000 < len(cont) < 120000:
                                cont1 = cont[:30000]
                                cont2 = cont[30000:60000]
                                cont3 = cont[60000:90000]
                                cont4 = cont[90000:12000]

                                insert_sql = "insert into 行政案例数据库.dbo.{0}(标题, 书文号, 法定代表人, 被处罚人, 被处罚单位或机构, 执法机构, 处罚时间, 这条数据请求地址, 这条数据完整的请求地址, 这条数据属于第几页的第几条, 模块首页的url, 来自于那个模块, 省份, 区域, showid, dataid, 文本内容1, 文本内容2, 文本内容3, 文本内容4, 发布时间) VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}','{20}','{21}') ".format(table_name, title, book_num,  legal_person,  punished_people,  punished_institution,  law_enforcement, penalty_date, src, content_src, page_no_position, page_url_1, source_library, province, area, max_show_id, data_id, cont1, cont2, cont3, cont4, release_date)
                            else:
                                print("这条数据大于12万字已经自动忽略掉了,它的标题是：  "+str(title))
                                pass
                            print(insert_sql)
                            链接数据库.insert(cursor, insert_sql)
                        链接数据库.break_connect(conn)


if __name__ == "__main__":

    # 注意本网站使用的是post请求获取页面信息，信息页面信息使用的get，并且网址
    AdminiStrative = Utils()
    index_url = "http://www.credithunan.gov.cn:30816/publicity_hn/webInfo/punishmentList.do"
    table_name = '行政案例数据表'
    # table_name = '行政案例测试表'
    save_path = "E:\行政案例附件\datafolder\湖南省\信用湖南"
    source_library = '湖南省>信用湖南'
    annex_local = source_library.replace("<", '/').replace(">", '/')
    province = source_library[:source_library.find(">")]
    # AdminiStrative.get_index_page_data(index_url)
    res = AdminiStrative.pare_page_data(index_url, table_name, save_path, source_library, province, annex_local)
    # res = AdminiStrative.get_page_data_1(index_url)
    # print(res)