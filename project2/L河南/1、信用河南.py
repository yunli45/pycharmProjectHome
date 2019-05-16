# coding = utf-8
import threading
import time
from queue import Queue
import requests
import re
from bs4 import BeautifulSoup
from L河南.工具包 import 链接数据库,附件下载程序,预处理模块, 提取信息, 动态访问

class MySpider():
    """
    参数说明：
        headers：浏览器请求头
        index_url: 爬取的首页
        page_no： 页码
        page_url：每一页对应的网址，post的网址基本是不变的，get会发生改变
        para：post请求需要的蚕食，get请求的时候传空值不适用就好了
        save_path ： 附件本地保存的地址
        table_name： 数据存放的表
        source_library：数据来自于哪里，用于推测出省份（province）、annex_local（附件在数据中修改的地址,在预处理模块中是 参数module_name，会自动拼接 "/datafolder/" + module_name+"/"）
        河南省>信用河南   province（省份）：河南省  annex_local（附件文中地址）：河南省/信用河南
        预处理模块参数module_name ："/datafolder/" + 河南省/信用河南 +"/"
        annex_local：附件文中地址
        province： 省份

    """
    def __init__(self, headers, index_url, page_no, page_url, para, save_path, table_name, source_library,annex_local, province, proxies):
        self.headers = headers
        self.index_url = index_url
        self.page_no = page_no
        self.page_url = page_url
        self.para = para
        self.save_path = save_path
        self.table_name = table_name
        self.source_library = source_library
        self.annex_local = annex_local
        self.province = province
        self.proxies = proxies

    # 访问网址:post
    def get_page_post(self, url, para):
        i = 0
        while i < 3:
            try:
                response = requests.post(url, data=para, headers=self.headers)
                response = response.content.decode('utf-8')
                # response = response.content.decode('GB18030')
            except Exception as e:
                print("[info] {0}{1}".format(e, url))
                i += 1
            else:
                return response

    # 访问网址：get
    def get_page_get(self, url):
        i = 0
        while i < 3:
            try:
                response = requests.get(url, proxies= self.proxies,headers=self.headers).content.decode('GB18030')
            except Exception as e:
                print("[info] {0}{1}".format(e, url))
                i += 1
            else:
                return response

    def parse_page(self):
        # 分别是 某一条数据的地址、 发布（公示）时间、 处罚时间、 标题、 执法机构、 书文号、 被处罚人、 被处罚单位
        src_list, penalty_date_list, release_date_list, title_list, law_enforcement_list, book_num_list = [], [], [], [], [], []
        punished_people_list, punished_institution_list = [], []
        print("# # # # # # # # # # # # # # #这是第：" + str(self.page_no) + "页 # # # # # # # # # # # # # # # # # # # #")
        # 获取页面数据
        #说明是一个get请求
        if self.para == "":
            response = self.get_page_get(self.page_url)
        else:
            response = self.get_page_post(self.page_url, self.para)
        # print("页面数据" + str(response))
        """
            提取页面信息 : 
        """
        rs_list = re.findall(
            '"cf_cfmc":"(.*?)","cf_wsh":"(.*?)","cf_xdr_mc":"(.*?)","cf_xzjg":"(.*?)".*?"id":"(.*?)".*?"sj":"(.*?)".*?}',
            str(response))
        print('rs_list的内容' + str(rs_list))
        if rs_list:
            for i in rs_list:
                src_list.append(i[4])
                book_num_list.append(i[1])
                title_list.append(i[0])
                law_enforcement_list.append(i[3])
                # penalty_date_list.append(i[3])
                release_date_list.append(i[5])  # 发布时间（公示时间）
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
                    content_src = self.index_url + "res_root/xyhn/templates/00000005/article_cf_new_cs.html?id=" + src
                    print("content_src" + str(content_src))
                    law_enforcement = law_enforcement_list[ids]  # 执法机构
                    punished_people = punished_people_list[ids]  # 被处罚人
                    punished_institution = ''  # 被处罚机构
                    book_num = book_num_list[ids]  # 书文号
                    # data_id 用于区分这条数据的唯一性（取这条数据请求地址最后一个反斜杠后面的字符串）(本次取网址取下来的url)
                    data_id = src
                    page_no_position = "这是第" + str(self.page_no) + "页的第" + str(ids + 1) + "条的数据"
                    # 以这条数据的完整请求地址来查询已有的数据是否存在，存在那这条数据就pass
                    sql_1 = "select *  from 行政案例数据库.dbo.{0} where 这条数据完整的请求地址='{1}'".format(self.table_name, content_src)

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
                        """
                        book_num = book_num
                        legal_person = ""
                        punished_people = punished_people
                        punished_institution = punished_institution
                        adj_url_name = src + ".png"
                        cont = """
                                <img id="imge" src="/datafolder/河南省/信用河南/{0}">
                                """.format(adj_url_name)
                        """
                            文字等级计算 ：
                            0 <= x <100 --> -1, 100<= x <200 ->1, 200<= x <1500 ->2, 1500<=x ->0 
                        """
                        text_level = re.sub(r'<[^>]+>', '', str(cont), flags=re.S)  # 删除html标记
                        text_level = re.sub('\\s*|\t|\r|\n', '', str(text_level))  # //去除tab、空格、空行
                        text_level = text_level.replace(" ", '')  # 去掉空格
                        text_level = re.sub('<script[^>]*?>[\\s\\S]*?<\\/script>', '', str(text_level))  # 删除js
                        text_level = re.sub('<style[^>]*?>[\\s\\S]*?<\\/style>', '', str(text_level))  # 删除style
                        text_level = len(text_level)

                        """
                           附件下载
                       """
                        adj_url = self.index_url + "/CMSInterface/cms/xzcf/img?id=" + src
                        附件下载程序.download_data(adj_url, adj_url_name, self.save_path)
                        time.sleep(2)
                        law_enforcement = law_enforcement
                        penalty_date = penalty_date  # 处罚时间
                        release_date = release_date
                        area = ''

                        # 查询数据库中最大showid,第一次不存在指定为13300000，以后每条数据加1
                        sql_2 = "select max(showid)  from 行政案例数据库.dbo.{0}".format(self.table_name)

                        # 查询
                        max_show_id_rs = 链接数据库.query(cursor, sql_2)
                        if max_show_id_rs[0] is None:
                            max_show_id = 13301990
                        else:
                            max_show_id = max_show_id_rs[0] + 1
                            # 插入数据库
                        if len(cont) < 30000:
                            insert_sql = "insert into 行政案例数据库.dbo.{0}(标题, 书文号, 法定代表人, 被处罚人, 被处罚单位或机构, 执法机构, 处罚时间, 这条数据请求地址, 这条数据完整的请求地址, 这条数据属于第几页的第几条, 模块首页的url, 来自于那个模块, 省份, 区域, showid, dataid, 文本内容1, 发布时间,文字等级) VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}') ".format(self.table_name, title, book_num, legal_person, punished_people, punished_institution,
                                    law_enforcement, penalty_date, content_src, content_src, page_no_position,
                                    self.page_url, self.source_library, self.province, area, max_show_id, data_id, cont,
                                    release_date, text_level)
                        print(insert_sql)
                        链接数据库.insert(cursor, insert_sql)
                    链接数据库.break_connect(conn)

def main():
    # index_url = "http://www.hnep.gov.cn/ztzl/gdzt/xzxkjxzcfgs/xzcf/H6006021402index_1.htm"
    index_url = "http://www.xyhn.gov.cn/"
    table_name = '行政案例数据表'
    # table_name = '行政案例测试表'
    source_library = '河南省>信用河南'
    annex_local = source_library.replace("<", '/').replace(">", '/')
    save_path = "E:\行政案例附件\datafolder\\"+annex_local.replace("/", '\\')
    province = source_library[:source_library.find(">")]
    headers =  {'User-Agent': 'Mozilla/5.0 (Windows NT 10-12.0; WOW64) AppleWebKit/537.36 (KHTML,  like Gecko) Chrome/67.0.3396.99 Safari/537.36',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10-12.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
    proxies = {
        "HTTP": "http://183.146.179.159:9000",
        "HTTP": "http://112.85.164.150:9999",
        "HTTP": "http://115.151.4.237:9999"
    }
    # 构造所有的url
    page_url = index_url + "CMSInterface/cms/xzcflist"
    for page_no in range(440, 14247):
        para = {

            "pagesize": "20",
            "page": "{0}".format(page_no)
        }

        MySpider(headers,index_url, page_no, page_url, para, save_path, table_name, source_library, annex_local, province, proxies).parse_page()

if __name__ == '__main__':
    start = time.time()
    main()
    print('[info]耗时：%s' % (time.time() - start))