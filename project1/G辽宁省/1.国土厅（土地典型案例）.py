# coding:gb18030
import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from 辽宁省.工具包 import 链接数据库,附件下载程序,预处理模块
from 辽宁省.工具包.判断url前面的点返回完整的请求地址 import returnSRC

class Utils(object):
    # 一些共用的初始化参数
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10-12.0; WOW64) AppleWebKit/537.36 (KHTML,  like Gecko) Chrome/67.0.3396.99 Safari/537.36',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10-12.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}


# 访问网址
    def get_page_data(self, url):
        response = requests.get(url, headers=self.headers)
        status_code = response.status_code
        # print("状态码1"+str(status_code))
        if status_code == 200:
            response = response.content.decode('gb18030')
        else:
            if status_code == 202:
                while True:
                    response = requests.post(url, headers=self.heders)
                    status_code = response.status_code
                    # print("状态码2" + str(status_code))
                    if status_code == 200:
                        response = response.content.decode('gb18030')
                    elif status_code == 404:
                        pass
                    else:
                        pass

            elif status_code == 400:
                print("这里出现网址找不到，查看网址是否正确" + str(url))

            elif status_code == 404:
                print("这里出现网址找不到，查看网址是否正确" + str(url))
                pass

        print("状态码3" + str(status_code))
        return response

    def get_page_data_1(self, url):
        response = requests.get(url,  headers=self.headers)
        status_code = response.status_code
        print("状态码1"+str(status_code))
        if status_code == 200:
            response = response.content.decode('utf-8')
        else:
            if status_code == 202:
                while True:
                    response = requests.get(url,  headers=self.heders)
                    status_code = response.status_code
                    # print("状态码2" + str(status_code))
                    if status_code == 200:
                        response = response.content.decode('utf-8')
                    elif status_code == 404:
                        pass
                    else:
                        pass

            elif status_code == 400:
                print("这里出现网址找不到，查看网址是否正确" + str(url))

            elif status_code == 404:
                print("这里出现网址找不到，查看网址是否正确" + str(url))
                pass

        print("状态码3" + str(status_code))
        return response

    def pare_page_data(self, page_url, table_name):

        for page_no in range(1, 3):
            src_list, title_list, date_list = [], [], []
            print("这是第："+str(page_no)+"页")
            if page_no == 1:
                page_url_1 = page_url+".html"
            else:
                page_url_1 = page_url+"_"+str(page_no-1)+".html"
            response = self.get_page_data(page_url_1)

            soup = BeautifulSoup(response, 'lxml')

            soup_1 = soup.find_all('div', attrs={'class': 'datapage-listshow'})

            if soup:
                rs_list = re.findall('<li><a href="(.*?)".*?>(.*?)</a><span.*?>(.*?)</span></li>', str(soup_1))
                if rs_list:
                    print(rs_list)
                    for i in rs_list:
                        src_list.append(i[0])
                        title_list.append(i[1])
                        date_list.append(i[2])

            if src_list:
                for ids, src in enumerate(src_list):
                    # 这条数据请求地址
                    src = src
                    # data_id 用于区分这条数据的唯一性（取这条数据请求地址最后一个反斜杠后面的字符串）
                    data_id = src[src.rfind("/")+1:]
                    title = title_list[ids]
                    date = date_list[ids]
                    content_src = returnSRC().returnSrc(index_url, src, '')
                    cont_response = self.get_page_data(content_src)
                    cont_soup = BeautifulSoup(cont_response, 'lxml')
                    cont_soup_1 = cont_soup.find_all('div', attrs={'class': 'news-text'})
                    cont = cont_soup_1[0]

                    # 这个参数是用于表示这条数据属于第几页的第几条的数据
                    page_no_position = "这是第"+str(page_no)+"页的第"+str(ids+1)+"条的数据"

                    # 因为没有附件就传一个位置了
                    cont = 预处理模块.dispose_of_data(page_url_1, content_src, str(cont), ' ')

                    # 以这条数据的完整请求地址来查询已有的数据是否存在，存在那这条数据就pass
                    sql_1 = "select *  from 行政案例数据库.dbo.行政案例测试表 where 这条数据完整的请求地址='{0}'".format(content_src)

                    # 改进了链接数据的各个方法，现在可以一次链接获取链接对象和游标，多次使用
                    connect_cursor = 链接数据库.get_connect_cursor()
                    conn = connect_cursor[0]
                    cursor = connect_cursor[1]

                    # 查询
                    data_id_rs = 链接数据库.query(cursor, sql_1)
                    # if data_id_rs is None:
                    #
                    #     # 查询数据库中最大showid,第一次不存在指定为13300000，以后每条数据加1
                    #     sql_2 = "select max(showid)  from 行政案例数据库.dbo.行政案例测试表"
                    #     # 查询
                    #     max_show_id_rs = 链接数据库.query(cursor, sql_2)
                    #     if max_show_id_rs[0] is None:
                    #         max_show_id = 13300000
                    #     else:
                    #         max_show_id = max_show_id_rs[0]+1
                    # else:
                    #     print("这条数据在已有的数据库中已存在，现在已经paa掉了，依据的原则是这条数据完整的请求地址,标题为： " + str(title))
                    #     pass

                    # 在数据库查询到该条数据的相关信息
                    if data_id_rs is not None:
                        print("这条数据在已有的数据库中已存在，现在已经paa掉了，依据的原则是这条数据完整的请求地址,标题为： " + str(title))
                        pass
                    else:

                        # 查询数据库中最大showid,第一次不存在指定为13300000，以后每条数据加1
                        sql_2 = "select max(showid)  from 行政案例数据库.dbo.行政案例测试表"

                        # 查询
                        max_show_id_rs = 链接数据库.query(cursor, sql_2)
                        if max_show_id_rs[0] is None:
                            max_show_id = 13300000
                        else:
                            max_show_id = max_show_id_rs[0] + 1

                        # 插入数据库
                        if len(cont) < 30000:
                            insert_sql = "insert into 行政案例数据库.dbo.{0}(标题, 书文号, [法定代表人 ], 被处罚人, 被处罚单位或机构, [执法机构 ], [处罚时间 ], 这条数据请求地址, 这条数据完整的请求地址, 这条数据属于第几页的第几条, 模块首页的url, 来自于那个模块, 省份, 区域, showid, dataid, 文本内容1) VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}') ".format(table_name, title, '', '', title, '', '辽宁省国土资源厅执法监察局', date, src, content_src, page_no_position, page_url_1, '辽宁省>国土厅(土地典型案例)', '辽宁省', '', max_show_id, data_id, cont)

                        elif 30000 < len(cont) < 60000:
                            cont1 = cont[:30000]
                            cont2 = cont[30000:60000]
                            insert_sql = "insert into 行政案例数据库.dbo.{0}(标题, 书文号, [法定代表人 ], 被处罚人, 被处罚单位或机构, [执法机构 ], [处罚时间 ], 这条数据请求地址, 这条数据完整的请求地址, 这条数据属于第几页的第几条, 模块首页的url, 来自于那个模块, 省份, 区域, showid, dataid, 文本内容1, 文本内容2) VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}') ".format(table_name,
                                title, '', '', title, '', '辽宁省国土资源厅执法监察局', date, src, content_src, page_no_position,
                                page_url_1, '辽宁省>国土厅(土地典型案例)', '辽宁省', '', max_show_id, data_id, cont1, cont2)
                        elif 60000 < len(cont) < 90000:
                            cont1 = cont[:30000]
                            cont2 = cont[30000:60000]
                            cont3 = cont[60000:90000]

                            insert_sql = "insert into 行政案例数据库.dbo.{0}(标题, 书文号, [法定代表人 ], 被处罚人, 被处罚单位或机构, [执法机构 ], [处罚时间 ], 这条数据请求地址, 这条数据完整的请求地址, 这条数据属于第几页的第几条, 模块首页的url, 来自于那个模块, 省份, 区域, showid, dataid, 文本内容1, 文本内容2, 文本内容3) VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}') ".format(table_name,
                                title, '', '', title, '', '辽宁省国土资源厅执法监察局', date, src, content_src, page_no_position,
                                page_url_1, '辽宁省>国土厅(土地典型案例)', '辽宁省', '', max_show_id, data_id, cont1, cont2, cont3)

                        elif 90000 < len(cont) < 120000:
                            cont1 = cont[:30000]
                            cont2 = cont[30000:60000]
                            cont3 = cont[60000:90000]
                            cont4 = cont[90000:12000]

                            insert_sql = "insert into 行政案例数据库.dbo.{0}(标题, 书文号, [法定代表人 ], 被处罚人, 被处罚单位或机构, [执法机构 ], [处罚时间 ], 这条数据请求地址, 这条数据完整的请求地址, 这条数据属于第几页的第几条, 模块首页的url, 来自于那个模块, 省份, 区域, showid, dataid, 文本内容1, 文本内容2, 文本内容3, 文本内容4) VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}','{20}') ".format(table_name, title, '', '', title, '', '辽宁省国土资源厅执法监察局', date, src, content_src, page_no_position,
                                page_url_1, '辽宁省>国土厅(土地典型案例)', '辽宁省', '', max_show_id, data_id, cont1, cont2, cont3, cont4)
                        else:
                            print("这条数据大于12万字已经自动忽略掉了,它的标题是：  "+str(title))
                            pass

                        链接数据库.insert(cursor, insert_sql)
                    链接数据库.break_connect(conn)


if __name__ =="__main__":
    AdminiStrative = Utils()
    # index_url = "http://www.lgy.gov.cn/zfjc/tddxal/index.html"  # 国土厅（土地典型案例）
    index_url = "http://www.lgy.gov.cn/zfjc/tddxal/index"  # 国土厅（土地典型案例）
    table_name = '行政案例数据表'
    res = AdminiStrative.pare_page_data(index_url, table_name)





