 # coding:gb18030
import re
import requests
from bs4 import BeautifulSoup
from L河南.工具包 import 链接数据库,附件下载程序,预处理模块, 提取信息, 动态访问
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
            response = response.content.decode('utf-8')
            # response = response.content.decode('gb18030')
        else:
            if status_code == 202:
                while True:
                    response = requests.post(url, data=data, headers=self.heders)
                    status_code = response.status_code
                    # print("状态码2" + str(status_code))
                    if status_code == 200:
                        response = response.content.decode('utf-8')
                        # response = response.content.decode('gb18030')
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
            # response = response.content.decode('gb18030')
        else:
            if status_code == 202:
                while True:
                    response = requests.get(url, headers=self.heders)
                    status_code = response.status_code
                    # print("状态码2" + str(status_code))
                    if status_code == 200:
                        response = response.content.decode('utf-8')
                        # response = response.content.decode('gb18030')
                    else:
                        pass

            elif status_code == 400:
                print("这里出现网址找不到，查看网址是否正确" + str(url))

            elif status_code == 404:
                print("这里出现网址找不到，查看网址是否正确" + str(url))
                pass
        return response

    def pare_page_data(self, index_url, table_name, save_path, source_library, province, annex_local):

        # 共计1771页
        # 首页提取：名称、执法部门、处罚日期、发布日期、 文中提取被处罚人、法人
        for page_no in range(1, 14247):
            # penalty_date 处罚日期
            # release_date 发布日期
            para = {
                "page": "{0}".format(page_no),
                "pagesize":"20"
            }
            src_list, penalty_date_list, release_date_list, title_list, law_enforcement_list, book_num_list = [], [], [], [], [], []
            punished_people_list, punished_institution_list = [], []
            # if page_no == 1:
            #     page_url_1 = index_url
            # else:
            #     page_url_1 = index_url[:index_url.rfind("=")+1] + str(page_no)

            page_url_1 = index_url +"CMSInterface/cms/xzcflist"

            """
                因为是post请求网址不变，参数有变化,妈的数学不好的话，还真不好找出他传入参数的规律
            """
            print("# # # # # # # # # # # # # # #这是第：" + str(page_no) + "页 # # # # # # # # # # # # # # # # # # # #")
            response = self.get_page_data(page_url_1, para)
            print(response)

            # print(page_url_1)
            # page_url_1 = "http://www.credithunan.gov.cn:30816/publicity_hn/webInfo/punishmentProxy.do?startrecord="+str((int(page_no)-1)*10+1)+"&endrecord="+str(int(page_no)*10)+"&perpage=10&totalRecord=17707"
            # response = self.get_page_data(page_url_1, parameter)
            # response = self.get_page_data_1(page_url_1)
            # break
            # print(response)
            """
            
            # 提取页面信息 : 
            
            """
            # rs_soup = BeautifulSoup(response, 'lxml')
            # rs_soup = rs_soup.find_all('table', attrs={'id': 'info_list'})
            # rs_soup = str(rs_soup[0]).replace("\n", '').replace("\r", '').replace("\t"
            #                                                                       "", '').replace('\xa0','')
            # rs_list = re.findall("""<tr><td class="title"><a href="(.*?)" onmousemove=".*?showDetail\('(.*?)','(.*?)','(.*?)'.*?</td></tr>""", str(rs_soup))
            rs_list = re.findall('"cf_cfmc":"(.*?)","cf_wsh":"(.*?)","cf_xdr_mc":"(.*?)","cf_xzjg":"(.*?)".*?"id":"(.*?)".*?"sj":"(.*?)".*?}', str(response))
            if rs_list:
                for i in rs_list:
                    src_list.append(i[4])
                    book_num_list.append(i[1])
                    title_list.append(i[0])
                    law_enforcement_list.append(i[3])
                    # penalty_date_list.append(i[3])
                    release_date_list.append(i[5]) # 发布时间（公示时间）
                    punished_people_list.append(i[2])
                    # punished_institution_list.append(2)
                if src_list:
                    for ids, src in enumerate(src_list):
                        title_1 = title_list[ids]
                        # book_num_1 = book_num_list[ids]
                        title = title_1
                        release_date = release_date_list[ids]
                        # penalty_date = penalty_date_list[ids]
                        penalty_date = ''
                        # content_src = index_url + src.replace("&amp;", '&')
                        content_src = index_url + "res_root/xyhn/templates/00000005/article_cf_new_cs.html?id=" + src
                        print("content_src"+str(content_src))
                        law_enforcement = law_enforcement_list[ids]  # 执法机构
                        punished_people = punished_people_list[ids]  # 被处罚人
                        punished_institution = ''                    # 被处罚机构
                        book_num = book_num_list[ids]                # 书文号
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
                            # cont_sou = self.get_page_data_1(content_src)
                            # print(cont_sou)
                            # cont_soup = BeautifulSoup(cont_sou, 'lxml')
                            """
                            改善下： 现在将全文内容所在的标签、标签属性、标签名以参数的形式传入
                            """
                            # 全文内容
                            # Label_name = "td"
                            # Label_class = "class"
                            # Label_class_val = "con-con-cnt"
                            # cont_soup_1 = cont_soup.find_all('{0}'.format(Label_name), attrs={'{0}'.format(Label_class): '{0}'.format(Label_class_val)})
                            # if cont_soup_1 != []:
                            #     cont_con = str(cont_soup_1[0]).replace("\n", '').replace("\r", '').replace("\t"
                            #                                                   "", '')
                            # else:
                            #     raise Exception(""" 对不起全文没有找到<{0} {1}="{2}">这个标签，请查看下具体的情况""".format(Label_name, Label_class, Label_class_val) + str(
                            #         title) + "  " + str(content_src))
                            # cont_con = cont_con.replace("\r", '').replace('\n', '')
                            # info_header_booknum = 提取信息.extracting_information_table_6(cont_header)
                            # indexUrl, page_url, content_src, content, save_path, module_name
                            # cont_cont = 预处理模块.dispose_of_data(index_url, '', content_src, str(cont_con), save_path, annex_local)
                            # 提取书文号、被处罚机构、法人、处罚机构、处罚时间
                            book_num = book_num
                            legal_person = ""
                            punished_people = punished_people
                            punished_institution = punished_institution
                            adj_url_name =  src + ".png"
                            cont = """
                            <img id="imge" src="/datafolder/河南省/信用河南/{0}">
                            """.format(adj_url_name)

                            """
                                文字等级计算 ：
                                0 <= x <100 --> -1, 100<= x <200 ->1, 200<= x <1500 ->2, 1500<=x ->0 
                            """
                            text_level =re.sub(r'<[^>]+>','' ,str(cont), flags=re.S)  # 删除html标记
                            text_level = re.sub('\\s*|\t|\r|\n', '', str(text_level))  # //去除tab、空格、空行
                            text_level = text_level.replace(" ", '') # 去掉空格
                            text_level = re.sub('<script[^>]*?>[\\s\\S]*?<\\/script>', '' , str(text_level)) # 删除js
                            text_level = re.sub('<style[^>]*?>[\\s\\S]*?<\\/style>', '' , str(text_level)) # 删除style
                            text_level = len(text_level)
                            """
                            附件下载
                            """
                            adj_url = index_url + "/CMSInterface/cms/xzcf/img?id=" + src
                            # 附件下载程序.download_data(adj_url, adj_url_name, save_path)
                            law_enforcement = law_enforcement
                            penalty_date = penalty_date  # 处罚时间
                            release_date = release_date
                            area = ''

                            # 查询数据库中最大showid,第一次不存在指定为13300000，以后每条数据加1
                            sql_2 = "select max(showid)  from 行政案例数据库.dbo.{0}".format(table_name)

                            # 查询
                            max_show_id_rs = 链接数据库.query(cursor, sql_2)
                            if max_show_id_rs[0] is None:
                                max_show_id = 13301990
                            else:
                                max_show_id = max_show_id_rs[0] + 1

                            # 插入数据库
                            if len(cont) < 30000:
                                insert_sql = "insert into 行政案例数据库.dbo.{0}(标题, 书文号, 法定代表人, 被处罚人, 被处罚单位或机构, 执法机构, 处罚时间, 这条数据请求地址, 这条数据完整的请求地址, 这条数据属于第几页的第几条, 模块首页的url, 来自于那个模块, 省份, 区域, showid, dataid, 文本内容1, 发布时间,文字等级) VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}') ".format(table_name, title, book_num,  legal_person,  punished_people,  punished_institution,  law_enforcement, penalty_date, content_src, content_src, page_no_position, page_url_1, source_library, province, area, max_show_id, data_id, cont, release_date, text_level)

                            elif 30000 < len(cont) < 60000:
                                cont1 = cont[:30000]
                                cont2 = cont[30000:60000]
                                insert_sql = "insert into 行政案例数据库.dbo.{0}(标题, 书文号, 法定代表人, 被处罚人, 被处罚单位或机构,执法机构 , 处罚时间, 这条数据请求地址, 这条数据完整的请求地址, 这条数据属于第几页的第几条, 模块首页的url, 来自于那个模块, 省份, 区域, showid, dataid, 文本内容1, 文本内容2, 发布时间, 文字等级) VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}','{20}') ".format(table_name, title, book_num,  legal_person,  punished_people,  punished_institution,  law_enforcement, penalty_date, src, content_src, page_no_position, page_url_1, source_library, province, area, max_show_id, data_id, cont1, cont2, release_date, text_level)
                            elif 60000 < len(cont) < 90000:
                                cont1 = cont[:30000]
                                cont2 = cont[30000:60000]
                                cont3 = cont[60000:90000]

                                insert_sql = "insert into 行政案例数据库.dbo.{0}(标题, 书文号, 法定代表人, 被处罚人, 被处罚单位或机构, 执法机构, 处罚时间 , 这条数据请求地址, 这条数据完整的请求地址, 这条数据属于第几页的第几条, 模块首页的url, 来自于那个模块, 省份, 区域, showid, dataid, 文本内容1, 文本内容2, 文本内容3, 发布时间, 文字等级) VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}','{20}','{21}') ".format(table_name, title, book_num,  legal_person,  punished_people,  punished_institution,  law_enforcement, penalty_date, src, content_src, page_no_position, page_url_1, source_library, province, area, max_show_id, data_id, cont1, cont2, cont3, release_date, text_level)

                            elif 90000 < len(cont) < 120000:
                                cont1 = cont[:30000]
                                cont2 = cont[30000:60000]
                                cont3 = cont[60000:90000]
                                cont4 = cont[90000:12000]

                                insert_sql = "insert into 行政案例数据库.dbo.{0}(标题, 书文号, 法定代表人, 被处罚人, 被处罚单位或机构, 执法机构, 处罚时间, 这条数据请求地址, 这条数据完整的请求地址, 这条数据属于第几页的第几条, 模块首页的url, 来自于那个模块, 省份, 区域, showid, dataid, 文本内容1, 文本内容2, 文本内容3, 文本内容4, 发布时间, 文字等级) VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}','{20}','{21}','{22}') ".format(table_name, title, book_num,  legal_person,  punished_people,  punished_institution,  law_enforcement, penalty_date, src, content_src, page_no_position, page_url_1, source_library, province, area, max_show_id, data_id, cont1, cont2, cont3, cont4, release_date, text_level)
                            else:
                                print("这条数据大于12万字已经自动忽略掉了,它的标题是：  "+str(title))
                                pass
                            print(insert_sql)
                            链接数据库.insert(cursor, insert_sql)
                        链接数据库.break_connect(conn)


if __name__ == "__main__":

    AdminiStrative = Utils()
    index_url = "http://www.xyhn.gov.cn/"
    # table_name = '行政案例数据表'
    table_name = '行政案例测试表'
    save_path = "E:\行政案例附件\datafolder\河南省\信用河南"
    source_library = '河南省>信用河南'
    annex_local = source_library.replace("<", '/').replace(">", '/')
    province = source_library[:source_library.find(">")]
    # AdminiStrative.get_index_page_data(index_url)
    res = AdminiStrative.pare_page_data(index_url, table_name, save_path, source_library, province, annex_local)
    # res = AdminiStrative.get_page_data_1(index_url)
    # print(res)