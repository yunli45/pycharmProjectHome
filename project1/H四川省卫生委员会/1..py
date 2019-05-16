# coding:gb18030
import re
import requests
from bs4 import BeautifulSoup
from H�Ĵ�ʡ����ίԱ��.���߰� import �������ݿ�,�������س���,Ԥ����ģ��, ��ȡ��Ϣ, ��̬����
from H�Ĵ�ʡ����ίԱ��.���߰�.�ж�urlǰ��ĵ㷵�������������ַ import returnSRC
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


# ������ַ��get
    def get_page_data(self, url):
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

    def pare_page_data(self, index_url, table_name, save_path, source_library, province):

        pro_list = {}
        for page_no in range(12, 15):
            src_list,  title_list, publicity_time_list = [], [], []   #Publicity  ��ʾʱ��   release_list ����ʱ��
            if page_no == 1:
                page_url = index_url
            else:
                page_url = index_url[:index_url.rfind(".")] + "_" + str(page_no - 1) + index_url[index_url.rfind("."):]

            print("# # # # # # # # # # # # # # #���ǵڣ�" + str(page_no) + "ҳ # # # # # # # # # # # # # # # # # # # #")
            print(page_url)

            page_response = self.get_page_data(page_url)
            # page_response = ��̬����.get_index_page_1(page_url)
            page_response_soup = BeautifulSoup(page_response, 'lxml')
            page_response_soup = page_response_soup.find_all('div', attrs={'class': r'wy_contMain fontSt'})
            # print("page_response_soup"+str(page_response_soup))
            # ��Ϣ��ȡ
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
                    publicity_time = publicity_time_list[ids]  # �������ݹ�ʾʱ�䣨��������ַ�ϵ�ʱ�䣩
                    # data_id ���������������ݵ�Ψһ�ԣ�ȡ�������������ַ���һ����б�ܺ�����ַ�����
                    data_id = content_src[content_src.rfind("/") + 1:]
                    # cont = self.get_page_data(content_src)
                    cont = ��̬����.get_index_page(content_src)
                    cont_soup = BeautifulSoup(cont, 'lxml')
                    cont_1 = cont_soup.find_all('div', attrs={'class': 'wy_contMain fontSt'})  # ����ȫ�Ĳ���
                    cont_2 = cont_soup.find_all('div', attrs={'class': 'TRS_Editor'})  # ����ȫ�Ĳ���
                    cont_1_num = ��ȡ��Ϣ.word_count(str(cont_1))
                    cont_2_num = ��ȡ��Ϣ.word_count(str(cont_2))
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
                    # annex_info_1 = cont_soup.find_all('div', attrs={'id': 'fujian'})  # ���Ǹ�������
                    annex_info_1 = cont_soup.find_all('div', attrs={'class': 'wy_wj_more'})  # ���Ǹ�������
                    annex_info_2 = cont_soup.find_all('div', attrs={'class': 'contMain fontSt'})  # ���Ǹ�������
                    annex_1_num = ��ȡ��Ϣ.word_count(str(annex_info_1))
                    annex_2_num = ��ȡ��Ϣ.word_count(str(annex_info_2))

                    if annex_info_1 and annex_1_num > 50:
                        annex_info = annex_info_1[0]
                    elif annex_info_1==[] and annex_info_2 and annex_2_num > 50:
                        annex_info = annex_info_2[0]
                    else:
                        annex_info = ''
                    # cont_info1 = Ԥ����ģ��.dispose_of_data_sc(page_url, content_src, cont1, save_path)
                    cont_info2 = Ԥ����ģ��.dispose_of_data_sc(page_url, content_src, cont, save_path)
                    # cont_info = cont_info1+cont_info2
                    cont_info = cont_info2
                    cont_annex = Ԥ����ģ��.dispose_of_data_sc(page_url, content_src, str(annex_info), save_path)
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


                    info = ��ȡ��Ϣ.extracting_information_sc(whole_content)  # ��ȡ���ĺ�, ����ʱ��, ��������
                    book_num = info[0]
                    publisher = info[1].replace("?", '')
                    # print("��������"+publisher)
                    release_time = info[2].replace("?", '')
                    # print("����ʱ��dd"+release_time)
                    # ���ڿ�ʼ����ȫ�ĵ����ݴ��ڲ��������ھ���һ����������ʽ
                    num = ��ȡ��Ϣ.word_count(cont_info)




                    # ��ѯ���ݿ��Ƿ������һ�����ݣ������ھͲ������ݿ�
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
                        # ��ͳ�Ƴ���С��50���ַ���ʱ��ȫ�ľ���һ����������ʽ
                    else:
                        if num < 50 and cont_annex.find(".pdf") != -1:
                            print("ȫ����һ��pdf��������ʽ")
                            insert_sql = "insert into �����������ݿ�.dbo.{0}([����]  ,[�������� ] ,[����ʱ�� ] ,[�������������ַ] ,[�������������������ַ] ,[�����������ڵڼ�ҳ�ĵڼ���] ,[ģ����ҳ��url] ,[�������Ǹ�ģ��] ,[ʡ��],[�ı�����1] ,[����ʱ��] ,[���ĺ�] ,[ȫ���Ƿ���һ��pdf]) VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}')".format(table_name, title, publisher, release_time, src, content_src, page_no_position, index_url, source_library, province, whole_content, publicity_time, book_num, '��')

                        elif num < 50 and cont_annex.find(".pdf") == -1:
                            print("����һ�������Ҳ���pdf")
                            insert_sql = "insert into �����������ݿ�.dbo.{0}([����]  ,[�������� ] ,[����ʱ�� ] ,[�������������ַ] ,[�������������������ַ] ,[�����������ڵڼ�ҳ�ĵڼ���] ,[ģ����ҳ��url] ,[�������Ǹ�ģ��] ,[ʡ��],[�ı�����1] ,[����ʱ��] ,[���ĺ�] ,[ȫ���Ƿ���һ��pdf])  VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}')".format(
                                table_name, title, publisher, release_time, src, content_src, page_no_position,
                                index_url, source_library, province, whole_content, publicity_time, book_num, 'ȫ����һ������,�Ҳ���pdf��ʽ��')
                        else:
                            print("ȫ����һ������+���»��߾���Ҫ�����µ���ʽ")
                            insert_sql = "insert into �����������ݿ�.dbo.{0}([����]  ,[�������� ] ,[����ʱ�� ] ,[�������������ַ] ,[�������������������ַ] ,[�����������ڵڼ�ҳ�ĵڼ���] ,[ģ����ҳ��url] ,[�������Ǹ�ģ��] ,[ʡ��],[�ı�����1] ,[����ʱ��] ,[���ĺ�])  VALUES ('{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}')".format(
                                table_name, title, publisher, release_time, src, content_src, page_no_position, index_url,
                                source_library, province, whole_content, publicity_time, book_num)

                        print(insert_sql)
                        �������ݿ�.insert(cursor, insert_sql)
                    �������ݿ�.break_connect(conn)
        print("����������   "+ str(pro_list))

if __name__ =="__main__":

    # ע�Ȿ��վʹ�õ���post�����ȡҳ����Ϣ����Ϣҳ����Ϣʹ�õ�get��������ַ
    AdminiStrative = Utils()
    index_url = "http://www.scwst.gov.cn/wj/zcwjjjd/zcwj/index.html"  #
    table_name = '[�Ĵ�ʡ����ίԱ��]'
    save_path = "E:\������������\�Ĵ�ʡ����ίԱ�������ļ�\%s"
    source_library = '�Ĵ�ʡ>�Ĵ�ʡ����ίԱ�������ļ�'
    province = source_library[:source_library.find(">")]
    res = AdminiStrative.pare_page_data(index_url, table_name, save_path, source_library, province)
