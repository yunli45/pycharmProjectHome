# coding = utf-8
import time
import requests
import re
from bs4 import BeautifulSoup
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
    def __init__(self, headers, index_url, page_no, page_url, para, request_type,save_path, table_name, source_library,annex_local, model_name, category):
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
        self.model_name = model_name
        self.category = category
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
                resp = requests.get(url, timeout=5)
                respon= resp.content.decode('utf-8').replace(u'\xa0', u'')

            except Exception as e:
                print("[info] {0}{1}".format(e, url))
                i += 1
            else:
                return respon

    def parse_page(self):
        # 分别是 某一条数据的地址、 发布（公示）时间、 处罚时间、 标题、 书文号、 被处罚人、 被处罚单位
        src_list, penalty_date_list, release_date_list, title_list,  book_num_list = [], [], [], [], []

        print("# # # # # # # # # # # # # # #这是第：" + str(self.page_no) + "页 # # # # # # # # # # # # # # # # # # # #")
        # 获取页面数据
        #说明是一个get请求
        if self.request_type == 'get':
            # response = self.get_page_get(self.page_url)
            # 因为网址重新修改后，使用requests去访问的时候经常会访问不到数据，所以需要使用动态访问去爬取
            response = 动态访问.get_index_page(self.page_url)
        else:
            response = self.get_page_post(self.page_url, self.para)

        """
            提取页面信息 : 
        """
        response = str(response).replace(u'\xa0', u'').replace("'", '') # 处理python读取nbsp；为？乱码的情况
        soup = BeautifulSoup(response, 'lxml')
        rs = soup.find_all('ul', attrs={'class':'zxxx_list mt20'})

        rs_2 = str(rs).replace("\n",'').replace('\t', '').replace('\r', '').replace("'", '').replace("(",'（').replace(")",'）')
        rs_list = re.findall(r"""<li> <a href="(.*?)".*?title="(.*?)">.*?</a><span.*?>(.*?)</span></li>""", str(rs_2))
        print("rs_list"+str(rs_list))

        if rs_list:
            for ids,i in enumerate(rs_list):
                src_list.append(i[0])
                title_list.append(i[1])
                release_date_list.append(i[2])  # 发布时间（公示时间）


            if src_list:
                print("长度"+ str(len(src_list)))
                for ids, src in enumerate(src_list):
                    title = title_list[ids].replace('"', '')
                    index_url = self.index_url

                    # src = src.replace("&amp;", '&')
                    content_src = 判断url前面的点返回完整的请求地址.returnSRC().returnSrc(index_url, src, '')
                    print("content_src" + str(content_src))

                    page_no_position = "这是第" + str(self.page_no) + "页的第" + str(ids + 1) + "条的数据"
                    # 以这条数据的标题来查询已有的数据是否存在，存在那这条数据就pass,妈的之前米有存储这条数据请求地址导致不好处理
                    sql_1 =  """ select 标题 from {0} where 标题='{1}' """.format(self.table_name, title)
                    # 改进了链接数据的各个方法，现在可以一次链接获取链接对象和游标，多次使用
                    connect_cursor = 链接数据库.get_connect_cursor()
                    conn = connect_cursor[0]
                    cursor = connect_cursor[1]
                    # 查询
                    data_id_rs = 链接数据库.query(cursor, sql_1)

                    # 当以标题在数据库中查询的后返回的结果为 None的时候说明在数据库中没有这条数据
                    if data_id_rs == None :
                        print("这条数据不存在：    "+src+"     "+title)
                        """
                            提取详细数据页面的相关信息：
                        """
                        # rs_cont = self.get_page_get(content_src).replace("'", '"').replace("\n", '')
                        rs_cont = 动态访问.get_index_page(content_src).replace("'", '"').replace("\n", '')
                        # print("rs_cont" +rs_cont)
                        rs_cont_soup = BeautifulSoup(rs_cont, 'lxml')

                        cont_soup = rs_cont_soup.find_all('div', attrs={'class': 'con'})
                        source_soup = rs_cont_soup.find_all('span', attrs={'class': 'mr'})

                        # 先去除下部的分享链接
                        # cont_so = re.sub('<div class="fx fr">.*?</div', '' , str(cont_soup[0]))
                        cont_so = re.sub('<div class="fx fr">.*?</div', '' , str(cont_soup[0]))
                        content_res = 预处理模块.dispose_of_data(indexUrl=self.index_url, page_url=self.page_url,
                                                     content_src=content_src, content=str(cont_so),
                                                     save_path=self.save_path, module_name=self.annex_local)
                        if source_soup !=[]:
                            # 发布部门
                            release_department = source_soup[0].text.replace("来源",'').replace(":",'').replace("：", '').replace(" ",'').replace("	",'')
                        else:
                            release_department =''

                        cont = content_res[0]
                        adj_list = content_res[1]
                        release_date = release_date_list[ids].replace("年", '').replace("月", '').replace("日",'').replace("-", '')  # 发布日期
                        grasp_time = time.strftime("%Y-%m-%d", time.localtime())

                        url = "模块名字：{0},模块首页url：{1},这条数据的请求地址：{2},这条数据的完整请求地址：{3},抓取时间：{4}".format(self.model_name, self.index_url, src, content_src, str(grasp_time))

                        # 因为预处理后返回的附件信息是一个数组被转化为字符串了，需要替换掉括号方便查看，替换掉单引号，替换逗号为竖斜杠方便查看是否有多个附件
                        adj = str(adj_list).replace("[", '').replace("]", '').replace(",", "|").replace("'",'') # 附件名字
                        # 插入数据库
                        insert_sql = "insert into 行政案例数据库.dbo.{0}(标题, 类别, 发布部门, 发布日期, 全文, url, 附件) VALUES ('{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}') ".format(self.table_name, title, self.category, release_department, release_date, cont, url, adj)
                        print(insert_sql)
                        链接数据库.insert(cursor, insert_sql)
                    else:
                        print("这条数据在数据库中是存在的：   "+src+"     "+title)
                        pass
                        # 链接数据库.break_connect(conn)
                        # break
                    链接数据库.break_connect(conn)


if __name__ == '__main__':
    """
        程序说明：这是卫计局的政策法规解读且使用的是动态访问的方式会比较慢
    
    """
    index_url = "http://www.nhc.gov.cn"
    table_name = '[wj-卫计局-备份]'
    # table_name = '[wj-卫计局]'
    source_library = '卫计局>卫生计生政策法规解读'  # 用于本地存储位置 和 附件的本地地址
    model_name = '政策法规解读'  # 模块名字是url中的模块字段，用于区分一个类别下不同的模块
    category = '卫生计生政策法规解读'  # 类别：数据表中的类别字段
    annex_local = source_library.replace("<", '/').replace(">", '/')  # 在预处理的时候会自动加上 ：/datafolder/+ annex_local+/
    save_path = "E:\datafolder\\" + annex_local.replace("/", '\\')
    # province = source_library[:source_library.find(">")]  # 省份
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10-12.0; WOW64) AppleWebKit/537.36 (KHTML,  like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10-12.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}

    # 构造所有的url
    # 注意:因为已经存在了之前的数据，现在只跑取前10的数据用于区分是否有更新
    for page_no in range(1, 3):
        para = ''
        if page_no == 1:
            page_url = index_url + "/wjw/zcjd/list.shtml"
            print(page_url)
        else:
            page_url = index_url + "/wjw/zcjd/list_{0}.shtml".format(page_no)
        # page_url = index_url + "/was5/search/search_hnpage.jsp?subcat1=&subcat2=&name2=&Publisher=ypxxgk&PreKeyword=行政处罚&dengyu1=1&Referer=&siteid=&type=a&page={0}".format(page_no)
        request_type = 'get'
        MySpider(headers, index_url, page_no, page_url, para, request_type, save_path, table_name, source_library,
                 annex_local, model_name, category).parse_page()
        time.sleep(4)
