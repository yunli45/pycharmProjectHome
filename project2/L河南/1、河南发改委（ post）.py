 # coding:gb18030
import re
import requests
from bs4 import BeautifulSoup
from L����.���߰� import �������ݿ�,�������س���,Ԥ����ģ��, ��ȡ��Ϣ, ��̬����
from K�ӱ�ʡ.���߰�.�ж�urlǰ��ĵ㷵�������������ַ import returnSRC
import time

class Utils(object):
    # һЩ���õĳ�ʼ������
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10-12.0; WOW64) AppleWebKit/537.36 (KHTML,  like Gecko) Chrome/67.0.3396.99 Safari/537.36',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10-12.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}

        # ��һ��������ȡÿһ������Ϣ�����⡢src��ʱ�䣩
        self.page_regular_expression = '<a href="(.*?)" .*?>(.*?)</a></div><div class="xzx01">.*?</div><div class="xzx01 mot02">(.*?)</div><div class="xzx01 mot02">.*?</div><div class="xzx01 mot02">.*?</div>'
        self.page_label_type = 'div'
        self.page_label_selector = 'class'
        self.page_label_selector_name = 'table-box'

        # ��һ��������ȡ��ϸ����ҳ�����Ϣ
        self.cont_label_type = 'div'
        self.cont_label_selector = 'class'
        self.cont_label_selector_name = 'row'

# ������ַ:post
    def get_page_data(self, url, data):
        response = requests.post(url, data=data, headers=self.headers)
        status_code = response.status_code
        # print("״̬��1"+str(status_code))
        if status_code == 200:
            response = response.content.decode('utf-8')
            # response = response.content.decode('gb18030')
        else:
            if status_code == 202:
                while True:
                    response = requests.post(url, data=data, headers=self.heders)
                    status_code = response.status_code
                    # print("״̬��2" + str(status_code))
                    if status_code == 200:
                        response = response.content.decode('utf-8')
                        # response = response.content.decode('gb18030')
                    else:
                        pass

            elif status_code == 400:
                print("���������ַ�Ҳ������鿴��ַ�Ƿ���ȷ" + str(url))

            elif status_code == 404:
                print("���������ַ�Ҳ������鿴��ַ�Ƿ���ȷ" + str(url))
                pass

        print("״̬��3" + str(status_code))
        return response

# ������ַ��get
    def get_page_data_1(self, url):
        response = requests.get(url, headers=self.headers)
        status_code = response.status_code
        # print("״̬��1"+str(status_code))
        if status_code == 200:
            response = response.content.decode('utf-8')
            # response = response.content.decode('gb18030')
        else:
            if status_code == 202:
                while True:
                    response = requests.get(url, headers=self.heders)
                    status_code = response.status_code
                    # print("״̬��2" + str(status_code))
                    if status_code == 200:
                        response = response.content.decode('utf-8')
                        # response = response.content.decode('gb18030')
                    else:
                        pass

            elif status_code == 400:
                print("���������ַ�Ҳ������鿴��ַ�Ƿ���ȷ" + str(url))

            elif status_code == 404:
                print("���������ַ�Ҳ������鿴��ַ�Ƿ���ȷ" + str(url))
                pass
        return response

    def pare_page_data(self, index_url, table_name, save_path, source_library, province, annex_local):

        # ����1771ҳ
        # ��ҳ��ȡ�����ơ�ִ�����š��������ڡ��������ڡ� ������ȡ�������ˡ�����
        for page_no in range(1, 14247):
            # penalty_date ��������
            # release_date ��������
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
                ��Ϊ��post������ַ���䣬�����б仯,�����ѧ���õĻ������治���ҳ�����������Ĺ���
            """
            print("# # # # # # # # # # # # # # #���ǵڣ�" + str(page_no) + "ҳ # # # # # # # # # # # # # # # # # # # #")
            response = self.get_page_data(page_url_1, para)
            print(response)

            # print(page_url_1)
            # page_url_1 = "http://www.credithunan.gov.cn:30816/publicity_hn/webInfo/punishmentProxy.do?startrecord="+str((int(page_no)-1)*10+1)+"&endrecord="+str(int(page_no)*10)+"&perpage=10&totalRecord=17707"
            # response = self.get_page_data(page_url_1, parameter)
            # response = self.get_page_data_1(page_url_1)
            # break
            # print(response)
            """
            
            # ��ȡҳ����Ϣ : 
            
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
                    release_date_list.append(i[5]) # ����ʱ�䣨��ʾʱ�䣩
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
                        law_enforcement = law_enforcement_list[ids]  # ִ������
                        punished_people = punished_people_list[ids]  # ��������
                        punished_institution = ''                    # ����������
                        book_num = book_num_list[ids]                # ���ĺ�
                        # data_id ���������������ݵ�Ψһ�ԣ�ȡ�������������ַ���һ����б�ܺ�����ַ�����(����ȡ��ַȡ������url)
                        data_id = src
                        page_no_position = "���ǵ�" + str(page_no) + "ҳ�ĵ�" + str(ids + 1) + "��������"
                        # ���������ݵ����������ַ����ѯ���е������Ƿ���ڣ��������������ݾ�pass
                        sql_1 = "select *  from �����������ݿ�.dbo.{0} where �������������������ַ='{1}'".format(table_name, content_src)

                        # �Ľ����������ݵĸ������������ڿ���һ�����ӻ�ȡ���Ӷ�����α꣬���ʹ��
                        connect_cursor = �������ݿ�.get_connect_cursor()
                        conn = connect_cursor[0]
                        cursor = connect_cursor[1]

                        # ��ѯ
                        data_id_rs = �������ݿ�.query(cursor, sql_1)

                        if data_id_rs is not None:
                            print("�������������е����ݿ����Ѵ��ڣ������Ѿ�paa���ˣ����ݵ�ԭ�����������������������ַ,����Ϊ�� " + str(title))
                            pass
                        else:
                            """
                            ��ȡ��ϸ����ҳ��������Ϣ��
                                ��ȡͷ����Ϣ����������������ʱ�䡢���ĺ�
                                ��ϸ��Ϣ���ڣ�<div id="zoom">�����ǩ��
                            """
                            # cont_sou = self.get_page_data_1(content_src)
                            # print(cont_sou)
                            # cont_soup = BeautifulSoup(cont_sou, 'lxml')
                            """
                            �����£� ���ڽ�ȫ���������ڵı�ǩ����ǩ���ԡ���ǩ���Բ�������ʽ����
                            """
                            # ȫ������
                            # Label_name = "td"
                            # Label_class = "class"
                            # Label_class_val = "con-con-cnt"
                            # cont_soup_1 = cont_soup.find_all('{0}'.format(Label_name), attrs={'{0}'.format(Label_class): '{0}'.format(Label_class_val)})
                            # if cont_soup_1 != []:
                            #     cont_con = str(cont_soup_1[0]).replace("\n", '').replace("\r", '').replace("\t"
                            #                                                   "", '')
                            # else:
                            #     raise Exception(""" �Բ���ȫ��û���ҵ�<{0} {1}="{2}">�����ǩ����鿴�¾�������""".format(Label_name, Label_class, Label_class_val) + str(
                            #         title) + "  " + str(content_src))
                            # cont_con = cont_con.replace("\r", '').replace('\n', '')
                            # info_header_booknum = ��ȡ��Ϣ.extracting_information_table_6(cont_header)
                            # indexUrl, page_url, content_src, content, save_path, module_name
                            # cont_cont = Ԥ����ģ��.dispose_of_data(index_url, '', content_src, str(cont_con), save_path, annex_local)
                            # ��ȡ���ĺš����������������ˡ���������������ʱ��
                            book_num = book_num
                            legal_person = ""
                            punished_people = punished_people
                            punished_institution = punished_institution
                            adj_url_name =  src + ".png"
                            cont = """
                            <img id="imge" src="/datafolder/����ʡ/���ú���/{0}">
                            """.format(adj_url_name)

                            """
                                ���ֵȼ����� ��
                                0 <= x <100 --> -1, 100<= x <200 ->1, 200<= x <1500 ->2, 1500<=x ->0 
                            """
                            text_level =re.sub(r'<[^>]+>','' ,str(cont), flags=re.S)  # ɾ��html���
                            text_level = re.sub('\\s*|\t|\r|\n', '', str(text_level))  # //ȥ��tab���ո񡢿���
                            text_level = text_level.replace(" ", '') # ȥ���ո�
                            text_level = re.sub('<script[^>]*?>[\\s\\S]*?<\\/script>', '' , str(text_level)) # ɾ��js
                            text_level = re.sub('<style[^>]*?>[\\s\\S]*?<\\/style>', '' , str(text_level)) # ɾ��style
                            text_level = len(text_level)
                            """
                            ��������
                            """
                            adj_url = index_url + "/CMSInterface/cms/xzcf/img?id=" + src
                            # �������س���.download_data(adj_url, adj_url_name, save_path)
                            law_enforcement = law_enforcement
                            penalty_date = penalty_date  # ����ʱ��
                            release_date = release_date
                            area = ''

                            # ��ѯ���ݿ������showid,��һ�β�����ָ��Ϊ13300000���Ժ�ÿ�����ݼ�1
                            sql_2 = "select max(showid)  from �����������ݿ�.dbo.{0}".format(table_name)

                            # ��ѯ
                            max_show_id_rs = �������ݿ�.query(cursor, sql_2)
                            if max_show_id_rs[0] is None:
                                max_show_id = 13301990
                            else:
                                max_show_id = max_show_id_rs[0] + 1

                            # �������ݿ�
                            if len(cont) < 30000:
                                insert_sql = "insert into �����������ݿ�.dbo.{0}(����, ���ĺ�, ����������, ��������, ��������λ�����, ִ������, ����ʱ��, �������������ַ, �������������������ַ, �����������ڵڼ�ҳ�ĵڼ���, ģ����ҳ��url, �������Ǹ�ģ��, ʡ��, ����, showid, dataid, �ı�����1, ����ʱ��,���ֵȼ�) VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}') ".format(table_name, title, book_num,  legal_person,  punished_people,  punished_institution,  law_enforcement, penalty_date, content_src, content_src, page_no_position, page_url_1, source_library, province, area, max_show_id, data_id, cont, release_date, text_level)

                            elif 30000 < len(cont) < 60000:
                                cont1 = cont[:30000]
                                cont2 = cont[30000:60000]
                                insert_sql = "insert into �����������ݿ�.dbo.{0}(����, ���ĺ�, ����������, ��������, ��������λ�����,ִ������ , ����ʱ��, �������������ַ, �������������������ַ, �����������ڵڼ�ҳ�ĵڼ���, ģ����ҳ��url, �������Ǹ�ģ��, ʡ��, ����, showid, dataid, �ı�����1, �ı�����2, ����ʱ��, ���ֵȼ�) VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}','{20}') ".format(table_name, title, book_num,  legal_person,  punished_people,  punished_institution,  law_enforcement, penalty_date, src, content_src, page_no_position, page_url_1, source_library, province, area, max_show_id, data_id, cont1, cont2, release_date, text_level)
                            elif 60000 < len(cont) < 90000:
                                cont1 = cont[:30000]
                                cont2 = cont[30000:60000]
                                cont3 = cont[60000:90000]

                                insert_sql = "insert into �����������ݿ�.dbo.{0}(����, ���ĺ�, ����������, ��������, ��������λ�����, ִ������, ����ʱ�� , �������������ַ, �������������������ַ, �����������ڵڼ�ҳ�ĵڼ���, ģ����ҳ��url, �������Ǹ�ģ��, ʡ��, ����, showid, dataid, �ı�����1, �ı�����2, �ı�����3, ����ʱ��, ���ֵȼ�) VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}','{20}','{21}') ".format(table_name, title, book_num,  legal_person,  punished_people,  punished_institution,  law_enforcement, penalty_date, src, content_src, page_no_position, page_url_1, source_library, province, area, max_show_id, data_id, cont1, cont2, cont3, release_date, text_level)

                            elif 90000 < len(cont) < 120000:
                                cont1 = cont[:30000]
                                cont2 = cont[30000:60000]
                                cont3 = cont[60000:90000]
                                cont4 = cont[90000:12000]

                                insert_sql = "insert into �����������ݿ�.dbo.{0}(����, ���ĺ�, ����������, ��������, ��������λ�����, ִ������, ����ʱ��, �������������ַ, �������������������ַ, �����������ڵڼ�ҳ�ĵڼ���, ģ����ҳ��url, �������Ǹ�ģ��, ʡ��, ����, showid, dataid, �ı�����1, �ı�����2, �ı�����3, �ı�����4, ����ʱ��, ���ֵȼ�) VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}','{20}','{21}','{22}') ".format(table_name, title, book_num,  legal_person,  punished_people,  punished_institution,  law_enforcement, penalty_date, src, content_src, page_no_position, page_url_1, source_library, province, area, max_show_id, data_id, cont1, cont2, cont3, cont4, release_date, text_level)
                            else:
                                print("�������ݴ���12�����Ѿ��Զ����Ե���,���ı����ǣ�  "+str(title))
                                pass
                            print(insert_sql)
                            �������ݿ�.insert(cursor, insert_sql)
                        �������ݿ�.break_connect(conn)


if __name__ == "__main__":

    AdminiStrative = Utils()
    index_url = "http://www.xyhn.gov.cn/"
    # table_name = '�����������ݱ�'
    table_name = '�����������Ա�'
    save_path = "E:\������������\datafolder\����ʡ\���ú���"
    source_library = '����ʡ>���ú���'
    annex_local = source_library.replace("<", '/').replace(">", '/')
    province = source_library[:source_library.find(">")]
    # AdminiStrative.get_index_page_data(index_url)
    res = AdminiStrative.pare_page_data(index_url, table_name, save_path, source_library, province, annex_local)
    # res = AdminiStrative.get_page_data_1(index_url)
    # print(res)