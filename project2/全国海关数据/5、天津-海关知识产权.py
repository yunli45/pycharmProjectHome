# coding = utf-8
import threading
import time
from lxml import etree
from queue import Queue
import requests
import re
from bs4 import BeautifulSoup
import json
from 工具包 import 链接数据库,附件下载程序,预处理模块, 提取信息, 动态访问, 判断url前面的点返回完整的请求地址

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
    def __init__(self, headers, index_url, page_no, page_url, para, request_type,save_path, table_name, source_library,annex_local, province, proxies):
        self.headers = headers
        self.index_url = index_url
        self.page_no = page_no
        self.page_url = page_url
        self.request_type = request_type
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
                response = response.content.decode('utf-8').replace(u'\xa0', u'')
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
                # response = requests.get(url, proxies= self.proxies, headers=self.headers).content.decode('GB18030').replace(u'\xa0', u'')
                # response = requests.get(url, proxies= self.proxies, headers=self.headers).content.decode('utf-8').replace(u'\xa0', u'')
                response = requests.get(url,  headers=self.headers).content.decode('utf-8').replace(u'\xa0', u'')
                # print(response)
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
        if self.request_type == 'get':
            response = self.get_page_get(self.page_url)
        else:
            response = self.get_page_post(self.page_url, self.para)
        # print("页面数据" + str(response))
        """
            提取页面信息 : 
        """
        # response = response.replace("\n", '')
        response = response.replace(u'\xa0', u'').replace("'", '') # 处理python读取nbsp；为？乱码的情况
        soup = BeautifulSoup(response, 'lxml')
        rs = soup.find_all('div', attrs={'class':' portlet'})
        # for i in rs:
        #     tr = i.find_all('tr')

        rs_2 = str(rs).replace("\n",'').replace('\t', '').replace('\r', '').replace("'", '').replace("(",'（').replace(")",'）')
        rs_list = re.findall(r"""<li><a href="(.*?)".*?title="(.*?)">.*?</a><span>(.*?)</span></li>""", str(rs_2))
        """
            # 这一组市用于解析json 
            json_text = response.strip('() \n\t\r').strip('[ ]')
            obj = json.loads(json_text)
            rs_list = data_list = obj['punishList']
            for  ids,i in enumerate(rs_list):
                src_list.append(i['id'])
                book_num_list.append(i['wsh'])
         """


        # print(input())
        # 统一社会信用代码 组织机构代码 工商登记码 税务登记号  案件名称 处罚类别1 处罚类别2 事由 依据 结果
        tyshxydm_list, zzjgdm_list, gszch_list,  swdjh_list, mc_list, cflb1_list, cflb2_list, sy_list, yj_list, jg_list= [], [], [], [], [], [], [], [], [], []
        if rs_list:
            # rs_list= rs_list[:86] + rs_list[90:295] + rs_list[296:299]
            # for i in rs_list:
            for ids,i in enumerate(rs_list):
                src_list.append(i[0])
                # book_num_list.append(i[3])
                title_list.append(i[1])
                # law_enforcement_list.append(i[2]) # 执法机关
                # penalty_date_list.append(i[])
                release_date_list.append(i[2])  # 发布时间（公示时间）
                # punished_people_list.append(i[3]) # 被处罚人
                # punished_institution_list.append(0) # 被处罚单位

            if src_list:
                for ids, src in enumerate(src_list):
                    title = title_list[ids].replace('"', '')
                    index_url = self.index_url
                    # src = src.replace("../../", '/')
                    # src = 判断url前面的点返回完整的请求地址.returnSRC().returnSrc(index_url, src, '')

                    content_src = self.index_url + src.replace("&amp;", '&')
                    # content_src = content_src + src.replace("&amp;", '&')
                    print("content_src" + str(content_src))

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
                           注意：
                           关于海关知识产权处罚，
                           标题：
                               '北京海关关于珠海市候笙柳实业有限公司出口侵犯“ZKTECO”品牌指纹扫描仪案件行政处罚决定书（案件编号：京关知字【2019】1号）'从标题中可以提取出被处罚人 、书文号 
                           全文中：
                               在一个<div class="easysite-news-text" id="easysiteText"> </div>中，且只有一个附件
                        """
                        """
                            提取详细数据页面的相关信息：
                        """
                        rs_cont = self.get_page_get(content_src).replace("'", '"').replace("\n", '')
                        rs_cont_soup = BeautifulSoup(rs_cont, 'lxml')

                        rs_cont_soup = rs_cont_soup.find_all('div', attrs={'class':'easysite-news-text'})
                        rs_cont_soup = rs_cont_soup[0]


                        cont = 预处理模块.dispose_of_data(indexUrl=self.index_url, page_url=self.page_url, content_src=content_src, content=str(rs_cont_soup), save_path=self.save_path, module_name=self.annex_local)

                        # cont_t =  提取信息.extracting_information_table_12(rs_cont)
                        # (book_number, punished_people, law_enforcement, legal_person, date, cont)
                        # return (legal_person, date, cont)
                        print("\n\n")
                        print("全文的地址"+content_src+"\n")
                        print(title)
                        title_1 = title.replace("）", '')
                        if str(title).find('编号')!=-1:
                            rr = re.findall(r'.*?关于(.*?)侵犯.*?编号[: ：](.*)', str(title_1))
                        else:
                            rr = re.findall(r'.*?关于(.*?)侵犯.*?（(.*?)）', str(title))

                        if rr !=[]:
                            book_num = rr[0][1]          # 书文号
                            punished_people = rr[0][0]   # 被处罚人
                        else:
                            raise Exception("对不起在标题中没有提取出书文号和被处罚人")

                        punished_institution = ''        # 被处罚机构
                        law_enforcement =  '北京海关'     # 执法机构
                        legal_person = ''                # 法人
                        penalty_date =  release_date_list[ids].replace("年", '-').replace("月", '-').replace("日", '')         # 处罚时间
                        cont = cont
                        release_date = penalty_date   # 公示时间
                        area = ''
                        """
                            文字等级计算 ：
                            0 <= x <100 --> -1, 100<= x <200 ->1, 200<= x <1500 ->2, 1500<=x ->0
                        """
                        text_len = re.sub(r'<[^>]+>', '', str(cont), flags=re.S)  # 删除html标记
                        text_len = re.sub('\\s*|\t|\r|\n', '', str(text_len))  # //去除tab、空格、空行
                        text_len = text_len.replace(" ", '')  # 去掉空格
                        text_len = re.sub('<script[^>]*?>[\\s\\S]*?<\\/script>', '', str(text_len))  # 删除js
                        text_len = re.sub('<style[^>]*?>[\\s\\S]*?<\\/style>', '', str(text_len))  # 删除style
                        text_len = len(text_len)
                        if 0<= text_len <100:
                            text_level = -1
                        elif 100<= text_len <200:
                            text_level = 1
                        elif 200<= text_len <1500:
                            text_level = 2
                        elif 200 <= text_len :
                            text_level = 0
                        else:
                            raise  Exception("文字等级出现错误，现在居然是负数，文字的字数长度为{0}".format(text_len))
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
                            insert_sql = "insert into 行政案例数据库.dbo.{0}(标题, 书文号, 法定代表人, 被处罚人, 被处罚单位或机构, 执法机构, 处罚时间, 这条数据请求地址, 这条数据完整的请求地址, 这条数据属于第几页的第几条, 模块首页的url, 来自于那个模块, 省份, 区域, showid, dataid, 文本内容1, 发布时间,文字等级, 文字字数) VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}',{19},{20}) ".format(self.table_name, title, book_num, legal_person, punished_people, punished_institution,
                                    law_enforcement, penalty_date, content_src, content_src, page_no_position,
                                    self.page_url, self.source_library, self.province, area, max_show_id, data_id, cont,
                                    release_date, text_level, text_len)
                        print(insert_sql)
                        链接数据库.insert(cursor, insert_sql)
                    链接数据库.break_connect(conn)

def main():
    # index_url = "http://xyhb.hebi.gov.cn/xzcf/"
    index_url = "http://tianjin.customs.gov.cn"
    table_name = '行政案例数据表'
    # table_name = '行政案例测试表'
    source_library = '天津市>海关>海关知识产权'
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
    # 注意税务局这里存在多个市的数据，每个url都不一样但是取数据是一样的
    for page_no in range(1, 20):
        para = ''
        # if page_no ==1 :
        #     page_url = index_url + "/pub/root9/216/675/index.htm"
        #     print(page_url)
        # else:
        #     page_url = index_url + "/szjt/1600/right_{0}.shtml".format(page_no-1)
        page_url = index_url + "/tianjin_customs/427875/427916/427918/427913/b6fd3207-{0}.html".format(page_no)
        request_type = 'get'
        MySpider(headers,index_url, page_no, page_url, para, request_type, save_path, table_name, source_library, annex_local, province, proxies).parse_page()



    # for page_no in range(1, 3):
    #     page_url = index_url + '/CreditHnExtranetWeb/xygs/datalist.do'
    #     para = {
    #         "pageNo": "{0}".format(page_no),
    #         'messageid': 'AE80F048BA0B4D34A0C26229BFA0D35B',
    #         'domainid':'015'
    #     }
    #     request_type = 'post'
    #     MySpider(headers,index_url, page_no, page_url, para, request_type, save_path, table_name, source_library, annex_local, province, proxies).parse_page()
if __name__ == '__main__':
    start = time.time()
    main()
    print('[info]耗时：%s' % (time.time() - start))