# coding:gb18030
import re
import requests
from bs4 import BeautifulSoup
from H四川省卫生委员会.工具包 import 链接数据库,附件下载程序,预处理模块, 提取信息, 动态访问
from H四川省卫生委员会.工具包.判断url前面的点返回完整的请求地址 import returnSRC
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


# 访问网址：get
    def get_page_data(self, url):
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

    def pare_page_data(self, index_url, table_name, save_path, source_library, province):

        pro_list = {}
        for page_no in range(12, 15):
            src_list,  title_list, publicity_time_list = [], [], []   #Publicity  公示时间   release_list 发布时间
            if page_no == 1:
                page_url = index_url
            else:
                page_url = index_url[:index_url.rfind(".")] + "_" + str(page_no - 1) + index_url[index_url.rfind("."):]

            print("# # # # # # # # # # # # # # #这是第：" + str(page_no) + "页 # # # # # # # # # # # # # # # # # # # #")
            print(page_url)

            page_response = self.get_page_data(page_url)
            # page_response = 动态访问.get_index_page_1(page_url)
            page_response_soup = BeautifulSoup(page_response, 'lxml')
            page_response_soup = page_response_soup.find_all('div', attrs={'class': r'wy_contMain fontSt'})
            # print("page_response_soup"+str(page_response_soup))
            # 信息提取
            rs_list = re.findall(r'<span.*?>(.*?)</span>.*?<a href="(.*?)".*?title="(.*?)">.*?/a></li>', str(page_response_soup))
            # print(rs_list)

            if rs_list:
                for i in rs_list:
                    publicity_time_list.append(i[0])
                    src_list.append(i[1])
                    title_list.append(i[2])
            if src_list:
                # print(src_list)
                for ids, src in enumerate(src_list):
                    content_src = returnSRC().returnSrc(index_url, src, '')
                    title = title_list[ids]
                    publicity_time = publicity_time_list[ids]  # 这条数据公示时间（发布到网址上的时间）
                    # data_id 用于区分这条数据的唯一性（取这条数据请求地址最后一个反斜杠后面的字符串）
                    data_id = content_src[content_src.rfind("/") + 1:]
                    # cont = self.get_page_data(content_src)
                    cont = 动态访问.get_index_page(content_src)
                    cont_soup = BeautifulSoup(cont, 'lxml')
                    cont_1 = cont_soup.find_all('div', attrs={'class': 'wy_contMain fontSt'})  # 这是全文部分
                    cont_2 = cont_soup.find_all('div', attrs={'class': 'TRS_Editor'})  # 这是全文部分
                    cont_1_num = 提取信息.word_count(str(cont_1))
                    cont_2_num = 提取信息.word_count(str(cont_2))
                    if cont_1 and cont_1_num>=150:
                        cont = str(cont_1[0])

                    elif cont_1_num < 150 and cont_2_num >= 150:
                        cont = str(cont_2[0])
                    else:
                        if cont_1 and cont_2==[]:
                            cont = str(cont_1[0])
                        elif cont_1==[] and cont_2:
                            cont = str(cont_2[0])
                        else:
                            cont=''
                    # wy_wj_more fujian
                    # annex_info_1 = cont_soup.find_all('div', attrs={'id': 'fujian'})  # 这是附件部分
                    annex_info_1 = cont_soup.find_all('div', attrs={'class': 'wy_wj_more'})  # 这是附件部分
                    annex_info_2 = cont_soup.find_all('div', attrs={'class': 'contMain fontSt'})  # 这是附件部分
                    annex_1_num = 提取信息.word_count(str(annex_info_1))
                    annex_2_num = 提取信息.word_count(str(annex_info_2))

                    if annex_info_1 and annex_1_num > 50:
                        annex_info = annex_info_1[0]
                    elif annex_info_1==[] and annex_info_2 and annex_2_num > 50:
                        annex_info = annex_info_2[0]
                    else:
                        annex_info = ''
                    # cont_info1 = 预处理模块.dispose_of_data_sc(page_url, content_src, cont1, save_path)
                    cont_info2 = 预处理模块.dispose_of_data_sc(page_url, content_src, cont, save_path)
                    # cont_info = cont_info1+cont_info2
                    cont_info = cont_info2
                    cont_annex = 预处理模块.dispose_of_data_sc(page_url, content_src, str(annex_info), save_path)
                    whole_content = cont_info + cont_annex
                    xlsx = re.findall('<.*?".*?/(.*?.xlsx)".*?>', cont)
                    if xlsx:
                        pro_list.update({'{}'.format(title): '{}'.format(str(xlsx))})

                    jpg = re.findall('<.*?".*?/(.*?.jpg)".*?>', cont)
                    if jpg:
                        pro_list.update({'{}'.format(title): '{}'.format(str(jpg))})

                    png = re.findall('<.*?".*?/(.*?.png)".*?>', cont)
                    if png:
                        pro_list.update({'{}'.format(title): '{}'.format(str(png))})


                    info = 提取信息.extracting_information_sc(whole_content)  # 提取书文号, 发布时间, 发布机构
                    book_num = info[0]
                    publisher = info[1].replace("?", '')
                    # print("发布机构"+publisher)
                    release_time = info[2].replace("?", '')
                    # print("发布时间dd"+release_time)
                    # 现在开始分析全文的内容存在不，不存在就是一个附件的形式
                    num = 提取信息.word_count(cont_info)




                    # 查询数据库是否存在这一条数据，不存在就插入数据库
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
                        # 当统计出来小于50个字符的时候全文就是一个附件的形式
                    else:
                        if num < 50 and cont_annex.find(".pdf") != -1:
                            print("全文是一个pdf附件的形式")
                            insert_sql = "insert into 行政案例数据库.dbo.{0}([标题]  ,[发布机构 ] ,[发布时间 ] ,[这条数据请求地址] ,[这条数据完整的请求地址] ,[这条数据属于第几页的第几条] ,[模块首页的url] ,[来自于那个模块] ,[省份],[文本内容1] ,[公布时间] ,[书文号] ,[全文是否是一个pdf]) VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}')".format(table_name, title, publisher, release_time, src, content_src, page_no_position, index_url, source_library, province, whole_content, publicity_time, book_num, '是')

                        elif num < 50 and cont_annex.find(".pdf") == -1:
                            print("这是一个附件且不是pdf")
                            insert_sql = "insert into 行政案例数据库.dbo.{0}([标题]  ,[发布机构 ] ,[发布时间 ] ,[这条数据请求地址] ,[这条数据完整的请求地址] ,[这条数据属于第几页的第几条] ,[模块首页的url] ,[来自于那个模块] ,[省份],[文本内容1] ,[公布时间] ,[书文号] ,[全文是否是一个pdf])  VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}')".format(
                                table_name, title, publisher, release_time, src, content_src, page_no_position,
                                index_url, source_library, province, whole_content, publicity_time, book_num, '全文是一个附件,且不是pdf格式的')
                        else:
                            print("全文是一个附件+文章或者就是要给文章的形式")
                            insert_sql = "insert into 行政案例数据库.dbo.{0}([标题]  ,[发布机构 ] ,[发布时间 ] ,[这条数据请求地址] ,[这条数据完整的请求地址] ,[这条数据属于第几页的第几条] ,[模块首页的url] ,[来自于那个模块] ,[省份],[文本内容1] ,[公布时间] ,[书文号])  VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}')".format(
                                table_name, title, publisher, release_time, src, content_src, page_no_position, index_url,
                                source_library, province, whole_content, publicity_time, book_num)

                        print(insert_sql)
                        链接数据库.insert(cursor, insert_sql)
                    链接数据库.break_connect(conn)
        print("问题结果集：   "+ str(pro_list))

if __name__ =="__main__":

    # 注意本网站使用的是post请求获取页面信息，信息页面信息使用的get，并且网址
    AdminiStrative = Utils()
    index_url = "http://www.scwst.gov.cn/wj/zcwjjjd/zcwj/index.html"  #
    table_name = '[四川省卫生委员会]'
    save_path = "E:\行政案例附件\四川省卫生委员会政策文件\%s"
    source_library = '四川省>四川省卫生委员会政策文件'
    province = source_library[:source_library.find(">")]
    res = AdminiStrative.pare_page_data(index_url, table_name, save_path, source_library, province)
