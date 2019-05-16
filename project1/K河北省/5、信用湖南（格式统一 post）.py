# coding:gb18030
import re
import requests
from bs4 import BeautifulSoup
from K�ӱ�ʡ.���߰� import �������ݿ�,�������س���,Ԥ����ģ��, ��ȡ��Ϣ, ��̬����
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
            # response = response.content.decode('utf-8')
            response = response.content.decode('gb18030')
        else:
            if status_code == 202:
                while True:
                    response = requests.post(url, data=data, headers=self.heders)
                    status_code = response.status_code
                    # print("״̬��2" + str(status_code))
                    if status_code == 200:
                        # response = response.content.decode('utf-8')
                        response = response.content.decode('gb18030')
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
            # response = response.content.decode('utf-8')
            response = response.content.decode('gb18030')
        else:
            if status_code == 202:
                while True:
                    response = requests.get(url, headers=self.heders)
                    status_code = response.status_code
                    # print("״̬��2" + str(status_code))
                    if status_code == 200:
                        # response = response.content.decode('utf-8')
                        response = response.content.decode('gb18030')
                    else:
                        pass

            elif status_code == 400:
                print("���������ַ�Ҳ������鿴��ַ�Ƿ���ȷ" + str(url))

            elif status_code == 404:
                print("���������ַ�Ҳ������鿴��ַ�Ƿ���ȷ" + str(url))
                pass
        return response

    def pare_page_data(self, page_url, table_name, save_path, source_library, province, annex_local):

        # ����1771ҳ
        # ��ҳ��ȡ�����ơ�ִ�����š��������ڡ��������ڡ� ������ȡ�������ˡ�����
        for page_no in range(1192, 1772):
            # penalty_date ��������
            # release_date ��������
            src_list, penalty_date_list, release_date_list, title_list, law_enforcement_list = [], [], [], [], []
            # if page_no == 1:
            #     page_url_1 = page_url
            # else:
            #     page_url_1 = page_url[:page_url.rfind("=")+1] + str(page_no)
            """
                ��Ϊ��post������ַ���䣬�����б仯,�����ѧ���õĻ������治���ҳ�����������Ĺ���
            """
            print("# # # # # # # # # # # # # # #���ǵڣ�" + str(page_no) + "ҳ # # # # # # # # # # # # # # # # # # # #")
            # print(page_url_1)
            page_url_1 = "http://www.credithunan.gov.cn:30816/publicity_hn/webInfo/punishmentProxy.do?startrecord="+str((int(page_no)-1)*10+1)+"&endrecord="+str(int(page_no)*10)+"&perpage=10&totalRecord=17707"
            # response = self.get_page_data(page_url_1, parameter)
            response = self.get_page_data_1(page_url_1)
            # break
            print(response)
            """
            
            # ��ȡҳ����Ϣ : 
            
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
                    release_date_list.append(i[4]) # ����ʱ�䣨��ʾʱ�䣩
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
                            cont = self.get_page_data_1(content_src)
                            print(cont)
                            # cont_soup = BeautifulSoup(cont, 'lxml')
                            """
                            �����£� ���ڽ�ȫ���������ڵı�ǩ����ǩ���ԡ���ǩ���Բ�������ʽ����
                            """
                            # ȫ������
                            # Label_name = "td"
                            # Label_class = "valign"
                            # Label_class_val = "top"
                            # cont_soup_1 = cont_soup.find_all('{0}'.format(Label_name), attrs={'{0}'.format(Label_class): '{0}'.format(Label_class_val)})
                            # if cont_soup_1 != []:
                            #     cont_header = str(cont_soup_1[0]).replace("\n", '').replace("\r", '').replace("\t"
                            #                                                   "", '')
                            # else:
                            #     raise Exception(""" �Բ���ȫ��û���ҵ�<{0} {1}="{2}">�����ǩ����鿴�¾�������""".format(Label_name, Label_class, Label_class_val) + str(
                            #         title) + "  " + str(content_src))
                            # cont_header = cont_header.replace("\r", '').replace('\n', '')
                            # info_header_booknum = ��ȡ��Ϣ.extracting_information_table_6(cont_header)
                            # cont = Ԥ����ģ��.dispose_of_data('', content_src, str(cont_cont), save_path, annex_local)

                            # ��ȡ���ĺš����������������ˡ���������������ʱ��
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
                                raise Exception("""ȫ��û���ҵ����ĺŵ���Ϣ��<td.*?class="xzcf_xx".*?>(.*?)</td>""")
                            if cont_c:
                                cont_cc = cont_c[0]
                            else:
                                raise Exception("""ȫ��û���ҵ�ȫ�����ݣ�<td.*?class="xzcf_jds".*?>(.*?)</td>""")

                            cont = '<p>���������������ĺţ�' + book_num + "</p><p>������������ƣ�" + punished_institution + "</p><p>���������ˣ���λ�����ˣ���"+ legal_person + "</p><p>ִ�����ţ�" + law_enforcement + "</p><p>�����������������ڣ�" + penalty_date + "</p><p>�������������飨ȫ�Ļ�ժҪ����"+ str(cont_cc)+"</p>"

                            law_enforcement = law_enforcement
                            penalty_date = penalty_date  # ����ʱ��
                            area = ''

                            # ��ѯ���ݿ������showid,��һ�β�����ָ��Ϊ13300000���Ժ�ÿ�����ݼ�1
                            sql_2 = "select max(showid)  from �����������ݿ�.dbo.{0}".format(table_name)

                            # ��ѯ
                            max_show_id_rs = �������ݿ�.query(cursor, sql_2)
                            if max_show_id_rs[0] is None:
                                max_show_id = 13300000
                            else:
                                max_show_id = max_show_id_rs[0] + 1

                            # �������ݿ�
                            if len(cont) < 30000:
                                insert_sql = "insert into �����������ݿ�.dbo.{0}(����, ���ĺ�, ����������, ��������, ��������λ�����, ִ������, ����ʱ��, �������������ַ, �������������������ַ, �����������ڵڼ�ҳ�ĵڼ���, ģ����ҳ��url, �������Ǹ�ģ��, ʡ��, ����, showid, dataid, �ı�����1, ����ʱ��) VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}') ".format(table_name, title, book_num,  legal_person,  punished_people,  punished_institution,  law_enforcement, penalty_date, content_src, content_src, page_no_position, page_url_1, source_library, province, area, max_show_id, data_id, cont, release_date)

                            elif 30000 < len(cont) < 60000:
                                cont1 = cont[:30000]
                                cont2 = cont[30000:60000]
                                insert_sql = "insert into �����������ݿ�.dbo.{0}(����, ���ĺ�, ����������, ��������, ��������λ�����,ִ������ , ����ʱ��, �������������ַ, �������������������ַ, �����������ڵڼ�ҳ�ĵڼ���, ģ����ҳ��url, �������Ǹ�ģ��, ʡ��, ����, showid, dataid, �ı�����1, �ı�����2, ����ʱ��) VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}') ".format(table_name, title, book_num,  legal_person,  punished_people,  punished_institution,  law_enforcement, penalty_date, src, content_src, page_no_position, page_url_1, source_library, province, area, max_show_id, data_id, cont1, cont2, release_date)
                            elif 60000 < len(cont) < 90000:
                                cont1 = cont[:30000]
                                cont2 = cont[30000:60000]
                                cont3 = cont[60000:90000]

                                insert_sql = "insert into �����������ݿ�.dbo.{0}(����, ���ĺ�, ����������, ��������, ��������λ�����, ִ������, ����ʱ�� , �������������ַ, �������������������ַ, �����������ڵڼ�ҳ�ĵڼ���, ģ����ҳ��url, �������Ǹ�ģ��, ʡ��, ����, showid, dataid, �ı�����1, �ı�����2, �ı�����3, ����ʱ��) VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}','{20}') ".format(table_name, title, book_num,  legal_person,  punished_people,  punished_institution,  law_enforcement, penalty_date, src, content_src, page_no_position, page_url_1, source_library, province, area, max_show_id, data_id, cont1, cont2, cont3, release_date)

                            elif 90000 < len(cont) < 120000:
                                cont1 = cont[:30000]
                                cont2 = cont[30000:60000]
                                cont3 = cont[60000:90000]
                                cont4 = cont[90000:12000]

                                insert_sql = "insert into �����������ݿ�.dbo.{0}(����, ���ĺ�, ����������, ��������, ��������λ�����, ִ������, ����ʱ��, �������������ַ, �������������������ַ, �����������ڵڼ�ҳ�ĵڼ���, ģ����ҳ��url, �������Ǹ�ģ��, ʡ��, ����, showid, dataid, �ı�����1, �ı�����2, �ı�����3, �ı�����4, ����ʱ��) VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}','{20}','{21}') ".format(table_name, title, book_num,  legal_person,  punished_people,  punished_institution,  law_enforcement, penalty_date, src, content_src, page_no_position, page_url_1, source_library, province, area, max_show_id, data_id, cont1, cont2, cont3, cont4, release_date)
                            else:
                                print("�������ݴ���12�����Ѿ��Զ����Ե���,���ı����ǣ�  "+str(title))
                                pass
                            print(insert_sql)
                            �������ݿ�.insert(cursor, insert_sql)
                        �������ݿ�.break_connect(conn)


if __name__ == "__main__":

    # ע�Ȿ��վʹ�õ���post�����ȡҳ����Ϣ����Ϣҳ����Ϣʹ�õ�get��������ַ
    AdminiStrative = Utils()
    index_url = "http://www.credithunan.gov.cn:30816/publicity_hn/webInfo/punishmentList.do"
    table_name = '�����������ݱ�'
    # table_name = '�����������Ա�'
    save_path = "E:\������������\datafolder\����ʡ\���ú���"
    source_library = '����ʡ>���ú���'
    annex_local = source_library.replace("<", '/').replace(">", '/')
    province = source_library[:source_library.find(">")]
    # AdminiStrative.get_index_page_data(index_url)
    res = AdminiStrative.pare_page_data(index_url, table_name, save_path, source_library, province, annex_local)
    # res = AdminiStrative.get_page_data_1(index_url)
    # print(res)