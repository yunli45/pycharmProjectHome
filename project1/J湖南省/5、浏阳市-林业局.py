# coding:gb18030
import re
import requests
from bs4 import BeautifulSoup
from J����ʡ.���߰� import �������ݿ�,�������س���,Ԥ����ģ��, ��ȡ��Ϣ, ��̬����
from J����ʡ.���߰�.�ж�urlǰ��ĵ㷵�������������ַ import returnSRC
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
        else:
            if status_code == 202:
                while True:
                    response = requests.post(url, data=data, headers=self.heders)
                    status_code = response.status_code
                    # print("״̬��2" + str(status_code))
                    if status_code == 200:
                        response = response.content.decode('utf-8')
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
        else:
            if status_code == 202:
                while True:
                    response = requests.get(url, headers=self.heders)
                    status_code = response.status_code
                    # print("״̬��2" + str(status_code))
                    if status_code == 200:
                        response = response.content.decode('utf-8')
                    else:
                        pass

            elif status_code == 400:
                print("���������ַ�Ҳ������鿴��ַ�Ƿ���ȷ" + str(url))

            elif status_code == 404:
                print("���������ַ�Ҳ������鿴��ַ�Ƿ���ȷ" + str(url))
                pass

        print("״̬��3" + str(status_code))
        return response

    def pare_page_data(self, page_url, table_name, save_path, source_library, province):

        # ����17ҳ
        for page_no in range(34, 36):
            src_list, date_list, title_list = [], [], []
            if page_no == 1:
                page_url_1 = page_url
            else:
                page_url_1 = page_url[:page_url.rfind("currentPage=") + 12] + str(page_no)+"&moduleId=edcd26f889f24cae88181e24ce766d08"

            print("# # # # # # # # # # # # # # #���ǵڣ�" + str(page_no) + "ҳ # # # # # # # # # # # # # # # # # # # #")
            # print(page_url_1)

            response = self.get_page_data_1(page_url_1)
            # break
            print(response)
            """
            
            # ��ȡҳ����Ϣ
            
            """
            rs_soup = BeautifulSoup(response, 'lxml')
            rs_soup = rs_soup.find_all('ul', attrs={'class': 'text_neirong'})
            rs_soup = str(rs_soup[0]).replace("\n", '').replace("\r", '').replace("\t", '')
            rs_list = re.findall('<a.*?href="(.*?)".*?>(.*?)</a><span>(.*?)</span></li>', rs_soup)
            if rs_list:
                for i in rs_list:
                    src_list.append(i[0])
                    title_list.append(i[1])
                    date_list.append(i[2])   # ����ʱ�䣨��ʾʱ�䣩
                if src_list:
                    for ids, src in enumerate(src_list):
                        title = title_list[ids]
                        release_time = date_list[ids].replace("(", '').replace(")", '')
                        content_src = returnSRC().returnSrc(page_url_1, src, '')
                        # ע�������-��ҵ�ֵ����ݵ�ȫ��url,��Ҫ�滻�� amp;
                        content_src = content_src.replace("amp;", '')
                        # data_id ���������������ݵ�Ψһ�ԣ�ȡ�������������ַ���һ����б�ܺ�����ַ�����(����ȡ��ַȡ������url)
                        # data_id = content_src[content_src.rfind("/") + 1:]
                        data_id = src
                        # ȥ����������
                        if title.find('ʵʩ���') != -1:
                            pass
                        else:
                            """
                            ��ȡ��ϸ����ҳ��������Ϣ
                            ��ϸ��Ϣ���ڣ�<span class="xilanwb" id="zoom"> �����ǩ��
                            """
                            cont = self.get_page_data_1(content_src)
                            cont_soup = BeautifulSoup(cont, 'lxml')
                            cont_soup_1 = cont_soup.find_all('div', attrs={'class': 'zhengwen'})
                            if cont_soup_1 != []:
                                cont = str(cont_soup_1[0])
                            else:
                                raise Exception(""" �Բ���ȫ��û���ҵ�<div class="zhengwen">�����ǩ����鿴�¾�������""" + str(
                                    title) + "  " + str(content_src))
                            # print(cont)
                            cont = cont.replace("\r", '').replace('\n', '')
                            # ��������ȫ������ȡ��Ϣ����������ȡ��Ϣ���ٴ���ȫ��
                            # book_number, legal_person, punished_people, punished_institution, law_enforcement, area, date
                            info = ��ȡ��Ϣ.extracting_information_3(title, cont)
                            print("���е���Ϣ"+str(info))

                            cont = Ԥ����ģ��.dispose_of_data('', content_src, str(cont), save_path)
                            title = title
                            book_num = info[0]
                            legal_person = info[1]
                            punished_people = info[2]
                            punished_institution = info[3]
                            law_enforcement = info[4]
                            penalty_date = info[6]  # ����ʱ��
                            area = info[5]
                            cont = cont

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
                                insert_sql = "insert into �����������ݿ�.dbo.{0}(����, ���ĺ�, ����������, ��������, ��������λ�����, ִ������, ����ʱ��, �������������ַ, �������������������ַ, �����������ڵڼ�ҳ�ĵڼ���, ģ����ҳ��url, �������Ǹ�ģ��, ʡ��, ����, showid, dataid, �ı�����1, ����ʱ��) VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}') ".format(table_name, title, book_num,  legal_person,  punished_people,  punished_institution,  law_enforcement, penalty_date, content_src, content_src, page_no_position, page_url_1, source_library, province, area, max_show_id, data_id, cont, release_time)

                            elif 30000 < len(cont) < 60000:
                                cont1 = cont[:30000]
                                cont2 = cont[30000:60000]
                                insert_sql = "insert into �����������ݿ�.dbo.{0}(����, ���ĺ�, ����������, ��������, ��������λ�����,ִ������ , ����ʱ��, �������������ַ, �������������������ַ, �����������ڵڼ�ҳ�ĵڼ���, ģ����ҳ��url, �������Ǹ�ģ��, ʡ��, ����, showid, dataid, �ı�����1, �ı�����2, ����ʱ��) VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}') ".format(table_name, title, book_num,  legal_person,  punished_people,  punished_institution,  law_enforcement, penalty_date, src, content_src, page_no_position, page_url_1, source_library, province, area, max_show_id, data_id, cont1, cont2, release_time)
                            elif 60000 < len(cont) < 90000:
                                cont1 = cont[:30000]
                                cont2 = cont[30000:60000]
                                cont3 = cont[60000:90000]

                                insert_sql = "insert into �����������ݿ�.dbo.{0}(����, ���ĺ�, ����������, ��������, ��������λ�����, ִ������, ����ʱ�� , �������������ַ, �������������������ַ, �����������ڵڼ�ҳ�ĵڼ���, ģ����ҳ��url, �������Ǹ�ģ��, ʡ��, ����, showid, dataid, �ı�����1, �ı�����2, �ı�����3, ����ʱ��) VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}','{20}') ".format(table_name, title, book_num,  legal_person,  punished_people,  punished_institution,  law_enforcement, penalty_date, src, content_src, page_no_position, page_url_1, source_library, province, area, max_show_id, data_id, cont1, cont2, cont3, release_time)

                            elif 90000 < len(cont) < 120000:
                                cont1 = cont[:30000]
                                cont2 = cont[30000:60000]
                                cont3 = cont[60000:90000]
                                cont4 = cont[90000:12000]

                                insert_sql = "insert into �����������ݿ�.dbo.{0}(����, ���ĺ�, ����������, ��������, ��������λ�����, ִ������, ����ʱ��, �������������ַ, �������������������ַ, �����������ڵڼ�ҳ�ĵڼ���, ģ����ҳ��url, �������Ǹ�ģ��, ʡ��, ����, showid, dataid, �ı�����1, �ı�����2, �ı�����3, �ı�����4, ����ʱ��) VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}','{20}','{21}') ".format(table_name, title, book_num,  legal_person,  punished_people,  punished_institution,  law_enforcement, penalty_date, src, content_src, page_no_position, page_url_1, source_library, province, area, max_show_id, data_id, cont1, cont2, cont3, cont4, release_time)
                            else:
                                print("�������ݴ���12�����Ѿ��Զ����Ե���,���ı����ǣ�  "+str(title))
                                pass
                            print(insert_sql)
                            �������ݿ�.insert(cursor, insert_sql)
                        �������ݿ�.break_connect(conn)


if __name__ == "__main__":

    # ע�Ȿ��վʹ�õ���post�����ȡҳ����Ϣ����Ϣҳ����Ϣʹ�õ�get��������ַ
    AdminiStrative = Utils()

    index_url = "http://www.liuyang.gov.cn:8081/eportal/ui?pageId=1505856&currentPage=1&moduleId=edcd26f889f24cae88181e24ce766d08"  #
    table_name = '�����������ݱ�'
    # table_name = '�����������Ա�'
    save_path = "E:\������������\datafolder\����ʡ\�����-��ҵ��\%s"
    source_library = '����ʡ>�����-��ҵ��'
    province = source_library[:source_library.find(">")]
    # AdminiStrative.get_index_page_data(index_url)
    res = AdminiStrative.pare_page_data(index_url, table_name, save_path, source_library, province)
    # res = AdminiStrative.get_page_data_1(index_url)
    # print(res)