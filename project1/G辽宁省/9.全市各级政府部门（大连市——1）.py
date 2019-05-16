# coding:gb18030
import re
import requests
from bs4 import BeautifulSoup
from G����ʡ.���߰� import �������ݿ�,�������س���,Ԥ����ģ��, ��ȡ��Ϣ, ��̬����
from G����ʡ.���߰�.�ж�urlǰ��ĵ㷵�������������ַ import returnSRC
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

        # for page_no in range(1, 1213):
        for page_no in range(585, 1213):
            src_list,  company_list, title_list = [], [], []
            if page_no == 1:
                page_url_1 = page_url
            else:
                page_url_1 = page_url

            print("# # # # # # # # # # # # # # #���ǵڣ�" + str(page_no) + "ҳ # # # # # # # # # # # # # # # # # # # #")
            # print(page_url_1)
            data_1 = {
                'pageNO': '%s'%(page_no),
                'pageSize': '10',

            }
            response = self.get_page_data(page_url_1, data=data_1)

            response_soup = BeautifulSoup(response, 'lxml')
            response_soup_1 = response_soup.find_all(self.page_label_type,attrs={self.page_label_selector: self.page_label_selector_name})
            response_soup_1 = str(response_soup_1).replace("\r", '').replace("\n", '')
            # print(response_soup_1)
            # �����ֻ��ȡ�����Ӿ��У���������Ϣ����ϸҳ��ȥ��ȡ
            rs_list = re.findall(self.page_regular_expression, str(response_soup_1), flags=re.S)
            # print(rs_list)
            if rs_list:
                for info in rs_list:
                    src_list.append(info[0])
                    company_list.append(info[1])
                    title_list.append(info[2])

            if src_list:
                # print(src_list)
                for ids, src in enumerate(src_list):
                    # �������������ַ
                    src = "http://credit.dl.cn"+src
                    title_1= title_list[ids]
                    conpany = company_list[ids]

                    # ��Ϊ�еĵı���ֻ�У� Υ��˰�չ��� �ȼ򵥵�������������Ҫ�鿴��ȡ�����ı����Ƿ���ڶ�Ӧ�ı�������λ��û�еĻ������Ϊ�� ��������λ+����

                    title = str(title_1).replace("\n", '').replace("\r", '').replace(" ", '')


                    # data_id ���������������ݵ�Ψһ�ԣ�ȡ�������������ַ���һ����б�ܺ�����ַ�����
                    data_id = src[src.rfind("/")+1:]

                    content_src = src

                    # cont_response = self.get_page_data(content_src)
                    cont_response = self.get_page_data_1(content_src)
                    # print(cont_response)
                    # print(cont_response)
                    cont_soup = BeautifulSoup(cont_response, 'lxml')
                    cont_soup_1 = cont_soup.find_all(self.cont_label_type, attrs={self.cont_label_selector: self.cont_label_selector_name})
                    # print(cont_soup_1)
                    # �ⲿ���Ǵ���ϸ���ݵ�ҳ��ȡʱ��
                    # cont_soup_2 = cont_soup.find_all('div', attrs={'class': 'news-info'})
                    # if cont_soup_2:
                    #     date_find = re.findall(r'\d{4}-\d{1,2}-\d{1,2}', str(cont_soup_2[0]))
                    #     if date_find:
                    #         date = date_find[0].replace("-", '')
                    #     else:
                    #         date = ''
                    # else:
                    #     date = ''
                    # ȥ����������
                    if title == '�й�֤ȯ�ල����ίԱ������������֤����':
                        pass

                    else:

                        cont_1 = str(cont_soup_1[0])
                        # print(cont_1)
                        # ������������ڱ�ʾ�����������ڵڼ�ҳ�ĵڼ���������
                        page_no_position = "���ǵ�" + str(page_no) + "ҳ�ĵ�" + str(ids + 1) + "��������"
                        # page_url, content_src, content, save_path
                        # ����Ҫȥ�����ʽ���⣬ֱ����ȡ��Ҫ ����Ϣ�ͺ���
                        # cont_1 = Ԥ����ģ��.dispose_of_data_table(str(cont_1))

                        cont = cont_1
                        print(cont)

                        need_table_infor = ��ȡ��Ϣ.extracting_information_table_2(title, str(cont))
                        # print(need_table_infor)
                        book_num = need_table_infor[0]
                        legal_person = need_table_infor[1]
                        punished_people = ''
                        punished_institution = need_table_infor[3]
                        law_enforcement = need_table_infor[4]
                        area = ''
                        cont = need_table_infor[7]
                        date = need_table_infor[6]

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
                                insert_sql = "insert into �����������ݿ�.dbo.{0}(����, ���ĺ�, [���������� ], ��������, ��������λ�����, [ִ������ ], [����ʱ�� ], �������������ַ, �������������������ַ, �����������ڵڼ�ҳ�ĵڼ���, ģ����ҳ��url, �������Ǹ�ģ��, ʡ��, ����, showid, dataid, �ı�����1) VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}') ".format(table_name, title, book_num,  legal_person,  punished_people,  punished_institution,  law_enforcement, date, src, content_src, page_no_position, page_url_1, source_library, province, area, max_show_id, data_id, cont)

                            elif 30000 < len(cont) < 60000:
                                cont1 = cont[:30000]
                                cont2 = cont[30000:60000]
                                insert_sql = "insert into �����������ݿ�.dbo.{0}(����, ���ĺ�, [���������� ], ��������, ��������λ�����, [ִ������ ], [����ʱ�� ], �������������ַ, �������������������ַ, �����������ڵڼ�ҳ�ĵڼ���, ģ����ҳ��url, �������Ǹ�ģ��, ʡ��, ����, showid, dataid, �ı�����1, �ı�����2) VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}') ".format(table_name, title, book_num,  legal_person,  punished_people,  punished_institution,  law_enforcement, date, src, content_src, page_no_position, page_url_1, source_library, province, area, max_show_id, data_id, cont1, cont2)
                            elif 60000 < len(cont) < 90000:
                                cont1 = cont[:30000]
                                cont2 = cont[30000:60000]
                                cont3 = cont[60000:90000]

                                insert_sql = "insert into �����������ݿ�.dbo.{0}(����, ���ĺ�, [���������� ], ��������, ��������λ�����, [ִ������ ], [����ʱ�� ], �������������ַ, �������������������ַ, �����������ڵڼ�ҳ�ĵڼ���, ģ����ҳ��url, �������Ǹ�ģ��, ʡ��, ����, showid, dataid, �ı�����1, �ı�����2, �ı�����3) VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}') ".format(table_name, title, book_num,  legal_person,  punished_people,  punished_institution,  law_enforcement, date, src, content_src, page_no_position, page_url_1, source_library, province, area, max_show_id, data_id, cont1, cont2, cont3)

                            elif 90000 < len(cont) < 120000:
                                cont1 = cont[:30000]
                                cont2 = cont[30000:60000]
                                cont3 = cont[60000:90000]
                                cont4 = cont[90000:12000]

                                insert_sql = "insert into �����������ݿ�.dbo.{0}(����, ���ĺ�, [���������� ], ��������, ��������λ�����, [ִ������ ], [����ʱ�� ], �������������ַ, �������������������ַ, �����������ڵڼ�ҳ�ĵڼ���, ģ����ҳ��url, �������Ǹ�ģ��, ʡ��, ����, showid, dataid, �ı�����1, �ı�����2, �ı�����3, �ı�����4) VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}','{20}') ".format(table_name, title, book_num,  legal_person,  punished_people,  punished_institution,  law_enforcement, date, src, content_src, page_no_position, page_url_1, source_library, province, area, max_show_id, data_id, cont1, cont2, cont3, cont4)
                            else:
                                print("�������ݴ���12�����Ѿ��Զ����Ե���,���ı����ǣ�  "+str(title))
                                pass
                            print(insert_sql)
                            �������ݿ�.insert(cursor, insert_sql)
                        �������ݿ�.break_connect(conn)


if __name__ =="__main__":

    # ע�Ȿ��վʹ�õ���post�����ȡҳ����Ϣ����Ϣҳ����Ϣʹ�õ�get��������ַ
    AdminiStrative = Utils()

    index_url = "http://credit.dl.cn/sgs/punish.jsp"  #
    # index_url = "http://credit.dl.cn/sgs/punish-view.jsp?id=e896b6fd87f741dabcf6921eeaf26637"  #
    table_name = '�����������ݱ�'
    # table_name = '�����������Ա�'
    save_path = "E:\������������\datafolder\����ʡ\������\%s"
    source_library = '����ʡ>������'
    province = source_library[:source_library.find(">")]
    # AdminiStrative.get_index_page_data(index_url)
    res = AdminiStrative.pare_page_data(index_url, table_name, save_path, source_library, province)
    # res = AdminiStrative.get_page_data_1(index_url)
    # print(res)