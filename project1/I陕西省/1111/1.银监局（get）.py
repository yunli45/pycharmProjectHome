# coding:gb18030
import re
import requests
from bs4 import BeautifulSoup
from I陕西省.工具包 import 链接数据库,附件下载程序,预处理模块, 提取信息, 动态访问
from I陕西省.工具包.判断url前面的点返回完整的请求地址 import returnSRC
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
            response = response.content.decode('utf-8')
        else:
            if status_code == 202:
                while True:
                    response = requests.post(url, data=data, headers=self.heders)
                    status_code = response.status_code
                    # print("状态码2" + str(status_code))
                    if status_code == 200:
                        response = response.content.decode('utf-8')
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
            response = response.content.decode('utf-8')
        else:
            if status_code == 202:
                while True:
                    response = requests.get(url, headers=self.heders)
                    status_code = response.status_code
                    # print("状态码2" + str(status_code))
                    if status_code == 200:
                        response = response.content.decode('utf-8')
                    else:
                        pass

            elif status_code == 400:
                print("这里出现网址找不到，查看网址是否正确" + str(url))

            elif status_code == 404:
                print("这里出现网址找不到，查看网址是否正确" + str(url))
                pass

        print("状态码3" + str(status_code))
        return response

    def pare_page_data(self, page_url, table_name, save_path, source_library, province):

        # for page_no in range(1, 49):
        for page_no in range(1, 7):
            src_list, date_list, title_list = [], [], []
            if page_no == 1:
                page_url_1 = page_url
            else:
                page_url_1 = page_url[:page_url.rfind("=")+1]+str(page_no)

            print("# # # # # # # # # # # # # # #这是第：" + str(page_no) + "页 # # # # # # # # # # # # # # # # # # # #")
            # print(page_url_1)

            response = self.get_page_data_1(page_url_1)
            # break
            print(response)
            """
            
            提取页面信息
            
            """
            rs_soup = BeautifulSoup(response, 'lxml')
            rs_soup = rs_soup.find_all('table', attrs={'id': 'testUI'})
            rs_soup = str(rs_soup[0]).replace("\n", '').replace("\r", '').replace("\t", '')
            rs_list = re.findall('<a.*?href="(.*?)".*?>(.*?)</a></td><td.*?>(.*?)</td>', rs_soup)
            if rs_list:
                for i in rs_list:
                    src_list.append(i[0])
                    title_list.append(i[1])
                    date_list.append(i[2])
                if src_list:
                    for ids, src in enumerate(src_list):
                        title = title_list[ids]
                        release_time = date_list[ids]  # 发布时间
                        content_src = returnSRC().returnSrc(page_url_1, src, '')
                        # data_id 用于区分这条数据的唯一性（取这条数据请求地址最后一个反斜杠后面的字符串）
                        data_id = content_src[content_src.rfind("/") + 1:]

                        """
                        
                        提取详细数据页面的相关信息
                        
                        """
                        cont = self.get_page_data_1(content_src)
                        cont_soup = BeautifulSoup(cont, 'lxml')
                        cont_soup = cont_soup.find_all('table', attrs={'class': 'MsoNormalTable'})
                        if cont_soup:
                            cont = str(cont_soup[0])
                        else:
                            raise Exception("对不起全文不是一个MsoNormalTable表格，请查看下具体的情况 ")
                        # print(cont)
                        cont = cont.replace("\r", '').replace('\n','')
                        cont = 预处理模块.dispose_of_data('', content_src, str(cont), '')
                        # return (book_number, legal_person, punished_people, punished_institution, law_enforcement, area, date, cont)
                        info = 提取信息.extracting_information_table_4(cont)

                        # (book_num, legal_person, punished_people2, punished_institution,
                        # law_enforcement, area5, date, cont, title8)
                        title = title
                        book_num = info[0]
                        legal_person = info[1]
                        punished_people = info[2]
                        punished_institution = info[3]
                        law_enforcement = info[4]
                        date = info[6]
                        area = info[5]
                        cont = info[7]

                        # 去除部分数据
                        if title == '中国证券监督管理委员会行政处罚听证规则':
                            pass

                        else:

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
                                    insert_sql = "insert into 行政案例数据库.dbo.{0}(标题, 书文号, [法定代表人 ], 被处罚人, 被处罚单位或机构, [执法机构 ], [处罚时间 ], 这条数据请求地址, 这条数据完整的请求地址, 这条数据属于第几页的第几条, 模块首页的url, 来自于那个模块, 省份, 区域, showid, dataid, 文本内容1) VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}') ".format(table_name, title, book_num,  legal_person,  punished_people,  punished_institution,  law_enforcement, date, content_src, content_src, page_no_position, page_url_1, source_library, province, area, max_show_id, data_id, cont)

                                elif 30000 < len(cont) < 60000:
                                    cont1 = cont[:30000]
                                    cont2 = cont[30000:60000]
                                    insert_sql = "insert into 行政案例数据库.dbo.{0}(标题, 书文号, [法定代表人 ], 被处罚人, 被处罚单位或机构, [执法机构 ], [处罚时间 ], 这条数据请求地址, 这条数据完整的请求地址, 这条数据属于第几页的第几条, 模块首页的url, 来自于那个模块, 省份, 区域, showid, dataid, 文本内容1, 文本内容2) VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}') ".format(table_name, title, book_num,  legal_person,  punished_people,  punished_institution,  law_enforcement, date, src, content_src, page_no_position, page_url_1, source_library, province, area, max_show_id, data_id, cont1, cont2)
                                elif 60000 < len(cont) < 90000:
                                    cont1 = cont[:30000]
                                    cont2 = cont[30000:60000]
                                    cont3 = cont[60000:90000]

                                    insert_sql = "insert into 行政案例数据库.dbo.{0}(标题, 书文号, [法定代表人 ], 被处罚人, 被处罚单位或机构, [执法机构 ], [处罚时间 ], 这条数据请求地址, 这条数据完整的请求地址, 这条数据属于第几页的第几条, 模块首页的url, 来自于那个模块, 省份, 区域, showid, dataid, 文本内容1, 文本内容2, 文本内容3) VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}') ".format(table_name, title, book_num,  legal_person,  punished_people,  punished_institution,  law_enforcement, date, src, content_src, page_no_position, page_url_1, source_library, province, area, max_show_id, data_id, cont1, cont2, cont3)

                                elif 90000 < len(cont) < 120000:
                                    cont1 = cont[:30000]
                                    cont2 = cont[30000:60000]
                                    cont3 = cont[60000:90000]
                                    cont4 = cont[90000:12000]

                                    insert_sql = "insert into 行政案例数据库.dbo.{0}(标题, 书文号, [法定代表人 ], 被处罚人, 被处罚单位或机构, [执法机构 ], [处罚时间 ], 这条数据请求地址, 这条数据完整的请求地址, 这条数据属于第几页的第几条, 模块首页的url, 来自于那个模块, 省份, 区域, showid, dataid, 文本内容1, 文本内容2, 文本内容3, 文本内容4) VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}','{20}') ".format(table_name, title, book_num,  legal_person,  punished_people,  punished_institution,  law_enforcement, date, src, content_src, page_no_position, page_url_1, source_library, province, area, max_show_id, data_id, cont1, cont2, cont3, cont4)
                                else:
                                    print("这条数据大于12万字已经自动忽略掉了,它的标题是：  "+str(title))
                                    pass
                                print(insert_sql)
                                链接数据库.insert(cursor, insert_sql)
                            链接数据库.break_connect(conn)


if __name__ =="__main__":

    # 注意本网站使用的是post请求获取页面信息，信息页面信息使用的get，并且网址
    AdminiStrative = Utils()

    index_url = "http://www.cbrc.gov.cn/chinese/home/docViewPage/60200406&current=1"  #
    table_name = '行政案例数据表'
    # table_name = '行政案例测试表'
    save_path = "E:\行政案例附件\datafolder\陕西省\银监局\%s"
    source_library = '陕西省>银监局'
    province = source_library[:source_library.find(">")]
    # AdminiStrative.get_index_page_data(index_url)
    res = AdminiStrative.pare_page_data(index_url, table_name, save_path, source_library, province)
    # res = AdminiStrative.get_page_data_1(index_url)
    # print(res)