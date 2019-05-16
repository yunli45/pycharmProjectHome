import os, shutil
from 工具包 import 链接数据库, 附件下载程序, 判断url前面的点返回完整的请求地址,预处理模块
import requests
import re
from bs4 import BeautifulSoup
import time


class Utils(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10-12.0; WOW64) AppleWebKit/537.36 (KHTML,  like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10-12.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}

        self.table_name = '[hb-环保局-备份]'
        # table_name = '[hb-环保局-备份]'
        self.source_library = '环保局>环境保护政策法规解读'  # 用于本地存储位置 和 附件的本地地址
        self.model_name = '环境保护政策法规解读'  # 模块名字是url中的模块字段，用于区分一个类别下不同的模块
        self.category = '环境保护政策法规解读'  # 类别：数据表中的类别字段
        self.annex_local = self.source_library.replace("<", '/').replace(">", '/')  # 在预处理的时候会自动加上 ：/datafolder/+ annex_local+/
        self.save_path = "E:\自收录数据\datafolder\\" + self.annex_local.replace("/", '\\')

    # get 方法访问
    def get_page_data(self, url):
        i = 0
        while i < 3:
            try:
                resp = requests.get(url, timeout=5)
                respon = resp.content.decode('utf-8').replace(u'\xa0', u'')
            except Exception as e:
                print("[info] {0}{1}".format(e, url))
                i += 1
            else:
                return respon

    # 用于解析具体的页面：判断初始的src是否有跳转、是否是附件、以及具体页面数据的提取、标签的处理（这一个还没做）
    def pare_page(self,index_url, page_no, page_url):
        print("# # # # # # # # # # # # # # #这是第：" + str(page_no) + "页  # # # # # # # # # # # # # # # # # # # #")

        # 分别是 某一条数据的地址、 发布（公示）时间、 处罚时间、 标题、 书文号、 被处罚人、 被处罚单位
        src_list, penalty_date_list, release_date_list, title_list, book_num_list = [], [], [], [], []
        response = self.get_page_data(page_url)
        # print(response)
        if response !='':
            soup = BeautifulSoup(response, 'lxml')
            rs = soup.find_all('div', attrs={'class': 'main_rt_list'})

            rs_2 = str(rs).replace("\n", '').replace('\t', '').replace('\r', '').replace("'", '')
            rs_list = re.findall(r"""<li.*?><div.*?><span>(.*?)</span><a.*?href="(.*?)".*?title="(.*?)">.*?</a></div></li>""",str(rs_2))
            # print(rs_list)
            # input()
            if rs_list!=[]:
                for ids, i in enumerate(rs_list):
                    penalty_date_list.append(i[0])
                    src_list.append(i[1])
                    title_list.append(i[2])

                if src_list!=[]:
                    for ids, src in enumerate(src_list):
                        title = title_list[ids].replace('"', '')
                        # 当遇到跳转或者是附件的情况（完整的请求地址）的时候直接不要
                        if src.find("http://")!=-1:
                            pass
                        else:
                            content_src = 判断url前面的点返回完整的请求地址.returnSRC().returnSrc(index_url, src, page_url)
                            print("content_src" + str(content_src))
                            page_no_position = "这是第" + str(page_no) + "页的第" + str(ids + 1) + "条的数据"
                            # 以这条数据的标题来查询已有的数据是否存在，存在那这条数据就pass,妈的之前米有存储这条数据请求地址导致不好处理

                            sql_1 = """ select 标题 from {0} where 标题='{1}' """.format(self.table_name, title)
                            connect_cursor = 链接数据库.get_connect_cursor()
                            conn = connect_cursor[0]
                            cursor = connect_cursor[1]
                            # 查询
                            data_id_rs = 链接数据库.query(cursor, sql_1)

                            # 当以标题在数据库中查询的后返回的结果为 None的时候说明在数据库中没有这条数据
                            if data_id_rs == None:
                                print("这条数据不存在：    " + src + "     " + title)
                                cont_response = self.get_page_data(content_src)

                                # 现在开始提取全文内容和头部信息
                                cont_response_soup = BeautifulSoup(cont_response, 'lxml')

                                """
                                    这部分是提取全文:
                                        访问详细数据页面，返回数据, 下载附件、修改地址、处理格式
                                """
                                # 从属关系（父子）
                                # content_body_box == 》Custom_UnionStyle
                                cont_response_soup_1 = cont_response_soup.find_all("div",attrs={'class', 'content_body_box'})
                                cont_response_soup_2 = cont_response_soup.find_all("div",attrs={'class', 'Custom_UnionStyle'})

                                # content == >  Custom_UnionStyle
                                # content
                                cont_response_soup_3 = cont_response_soup.find_all("div", attrs={'class', 'content'})

                                # 这种存在分享<span class="wzxq2_lianjie">
                                cont_response_soup_4 = cont_response_soup.find_all("div",attrs={'class', 'wzxq_neirong2'})

                                if cont_response_soup_1 or cont_response_soup_3 or cont_response_soup_4 or cont_response_soup_2:
                                    if cont_response_soup_1 and len(str(cont_response_soup_1[0])) > 50:
                                        content = str(cont_response_soup_1[0])
                                    elif cont_response_soup_3 and len(str(cont_response_soup_3[0])) > 50:
                                        content = str(cont_response_soup_3[0])
                                    elif cont_response_soup_4 and len(str(cont_response_soup_4[0])) > 50:
                                        content = str(cont_response_soup_4[0])
                                        content = re.sub('<span.*?class="wzxq2_lianjie".*?>.?</span>', '', content)
                                        content = re.sub('<script.*?>.*?</script>', '', content)

                                    else:
                                        content = str(cont_response_soup_2[0])
                                else:
                                    raise Exception("这几个 content_body_box（div class）\ Custom_UnionStyle（div class）\ "
                                                    "content（div class）\  wzxq_neirong2（div class）没有取到数据,可能存在其他的标签,标题是： "
                                                    + str(title) + "  也可能是网址拼接错了 ：" + str(content_src))

                                """
                                    这一部分是提取信息摘要
                                """
                                # 从属关系： content_top(div class) == > content_top_box (div class)
                                # 从属关系： headInfo(div class) == > table (id headContainer)

                                cont_response_header_1 = cont_response_soup.find_all("div",attrs={'class', 'content_top'})
                                cont_response_header_2 = cont_response_soup.find_all("div", attrs={'class', 'headInfo'})
                                if cont_response_header_1 or cont_response_header_2:
                                    if cont_response_header_1:
                                        heder_info = str(cont_response_header_1[0])
                                        heder_info_1 = heder_info.replace(" ", '').replace("  ", '').replace("\u3000",
                                                                                                             '').replace(
                                            "\n", '')
                                        release_department_re = re.findall('发布机关</span>(.*?)</div>', heder_info_1)
                                        book_re = re.findall('文号</span>(.*?)</div>', heder_info_1)

                                        if release_department_re:
                                            release_department = release_department_re[0]
                                        else:
                                            release_department = ''
                                        if book_re:
                                            book = book_re[0]
                                        else:
                                            book = ''

                                    elif cont_response_header_2:
                                        heder_info = str(cont_response_header_2[0]).replace(" ", '').replace("  ",
                                                                                                             '').replace(
                                            "\u3000",
                                            '').replace(
                                            "\n", '').replace('\xa0', '')
                                        release_department_re = re.findall('发布机关.*?<span>(.*?)</span>', heder_info)
                                        book_re = re.findall('文号.*?<span>(.*?)</span>', heder_info)


                                        if release_department_re:
                                            release_department = release_department_re[0]
                                        else:
                                            release_department = ''

                                        if book_re:
                                            book = book_re[0]
                                        else:
                                            book = ''

                                    else:
                                        raise Exception("貌似content_top(div class)、 headInfo(div class)取出来是一个空的值啊")
                                else:

                                    release_department = ''
                                    book = ''

                                content_d  = 预处理模块.dispose_of_data(index_url, page_url, content_src, content,self.save_path, self.annex_local)
                                cont = content_d [0]
                                adj_list = content_d [1]
                                penalty_date = penalty_date_list[ids].replace("年", '').replace("月", '').replace("日",'').replace(
                                    "-", '')
                                release_date = penalty_date
                                grasp_time = time.strftime("%Y-%m-%d", time.localtime())

                                url = "模块名字：{0},模块首页url：{1},这条数据的请求地址：{2},这条数据的完整请求地址：{3},抓取时间：{4}".format(self.model_name, index_url, src, content_src, str(grasp_time))

                                # 因为预处理后返回的附件信息是一个数组被转化为字符串了，需要替换掉括号方便查看，替换掉单引号，替换逗号为竖斜杠方便查看是否有多个附件
                                adj = str(adj_list).replace("[", '').replace("]", '').replace(",", "|").replace("'",'')  # 附件名字
                                # 插入数据库
                                insert_sql = "insert into 行政案例数据库.dbo.{0}(标题, 类别, 发文字号, 发布部门, 发布日期, 全文, url, 附件) VALUES ('{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}','{8}') ".format(
                                    self.table_name, title, self.category, book, release_department, release_date, cont, url,
                                    adj)
                                print(insert_sql)
                                with open(r'D:\Python\pythonProjectHome\卫计局自动抓取\test', 'a') as f:
                                    f.write(str("insert_sql" + str(insert_sql + "\n\n")))
                                链接数据库.insert(cursor, insert_sql)

                            else:
                                print("这条数据在数据库中是存在的：   " + src + "     " + title)
                                pass
                            链接数据库.break_connect(conn)

        else:
            raise Exception("没有请求到每页的数据")


if __name__ == '__main__':
    """
    程序说明： 这是环保局下政策法规解读自动抓取程序，由于放入到系统的定时任务中程序名不能是中文所以要注意这一点，是中文的h话无法正常运行
    """
    index_url = "http://www.mee.gov.cn"
    for page_no in range(1,3):
        if page_no == 1:
            page_url =index_url + "/gzfw_13107/zcfg/zcfgjd/index.shtml"

        else:
            page_url =index_url + "/gzfw_13107/zcfg/zcfgjd/index_{0}.shtml".format(page_no - 1)
        until = Utils()
        until.pare_page(index_url, page_no, page_url)
        # time.sleep(4)




