import re
import requests
import json
from L河南.工具包 import 链接数据库,附件下载程序,预处理模块, 提取信息, 动态访问


class jrtt(object):
    def __init__(self, index_url,table_name, key_find, reg_abstract, reg_title, reg_open_url, reg_source, reg_behot_time):
        self.index_url = index_url
        self.table_name = table_name
        self.key_find = key_find
        self.reg_abstract = reg_abstract
        self.reg_title = reg_title
        self.reg_open_url = reg_open_url
        self.reg_source = reg_source
        self.reg_behot_time = reg_behot_time

    def getReq(self,url):
        response = requests.get(url)
        response = response.content.decode("utf-8")
        return response

    def pare_page(self):
        rs = self.getReq(self.index_url)
        json_text = rs.strip('() \n\t\r')
        obj = json.loads(json_text)
        data_list = obj['data']
        # 简述、标题、地址（需要拼接）、作者、时间戳
        abstract_list, title_list, open_url_list, source_list, behot_time_list, group_id_list = [], [], [], [], [],[]
        if data_list:
            for ids,i in enumerate(data_list):
                # 当有简述的时候才是一条数据，不然就是一条广告 source
                try :
                    abs = re.findall(self.reg_abstract, str(data_list[ids]), flags=re.M)
                    if abs:
                        # tlt = re.findall(self.reg_title, str(data_list[ids]), flags=re.M)[1]
                        tlt = data_list[ids]['title']
                        gro_id = data_list[ids]['group_id']
                        open_ul = data_list[ids]['open_url']
                        # open_ul =  re.findall(self.reg_open_url, str(data_list[ids]), flags=re.M)
                        sou = data_list[ids]['source']
                        be_time =  data_list[ids]['behot_time']
                        # be_time = re.findall(self.reg_behot_time, str(data_list[ids]), flags=re.M)
                        abstract_list.append(abs)
                        title_list.append(tlt)
                        group_id_list.append(gro_id)
                        open_url_list.append(open_ul)
                        source_list.append(sou)
                        behot_time_list.append(be_time)
                except:
                    pass
        else:
            pass

        if abstract_list:
            for ids1, abstract_sql in enumerate(abstract_list):
                abstract_data = abstract_sql[0].replace("'",'')
                title_data = title_list[ids1].replace("'",'')
                # if open_url_list[ids1] and  open_url_list[ids1][0]:
                #     open_url_data = str(open_url_list[ids1][0].replace("'",''))
                # else:
                #     open_url_data = str(open_url_list[ids1]).replace("'",'')

                open_url_data = str(open_url_list[ids1]).replace("'", '')

                source_data = source_list[ids1].replace("'",'')
                # if behot_time_list[ids1] and behot_time_list[ids1][0]:
                #     behot_tim_data = str(behot_time_list[ids1][0].replace("'",''))
                # else:
                #     behot_tim_data = str(behot_time_list[ids1]).replace("'",'')
                behot_tim_data = str(behot_time_list[ids1]).replace("'",'')
                group_id_data = str(group_id_list[ids1])
                print(group_id_data)
                sql_1= "select *  from 行政案例数据库.dbo.{0} where group_id='{1}'".format(self.table_name, group_id_data)
                connect_cursor = 链接数据库.get_connect_cursor()
                conn = connect_cursor[0]
                cursor = connect_cursor[1]
                # 查询
                data_id_rs = 链接数据库.query(cursor, sql_1)
                if data_id_rs is not None:
                    print("这条数据在已有的数据库中已存在，现在已经paa掉了，依据的原则是这条数据完整的请求地址,标题为： " + str(title_data))
                    pass
                else:
                    insert_sql = "insert into 行政案例数据库.dbo.{0}(title, open_url, source, behot_time,abstract, group_id, key_find) values ('{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}')".format(self.table_name, title_data, open_url_data, source_data, behot_tim_data, abstract_data, group_id_data, self.key_find)
                    print(insert_sql)
                    链接数据库.insert(cursor, insert_sql)
                链接数据库.break_connect(conn)


def main():

    """
        参数说明：
            key_list : 保存的是我们需要查询的关键字
            table_name：是我们需要保存的数据表表名
            reg_* : 是可以用于正则去匹配取数据的时候使用，但是现在使用的json来解析更加方便准确
            num: 因为不知道具体有多少数据，我们只能去官网一直往下拉刷新查看，初始值是100，能查看到 2000条数据（实际上都没有那么多），可根据实际情况来填写
    :return:
    """
    key_list = ["公安+执法资格+考试", "行政执法+教育+培训+考试", "行政执法监督+双随机", "法律职业资格+考试"]
    table_name = 'jrtt'
    reg_abstract = """'abstract':.'(.*?)'"""
    reg_title = """'title':.'(.*?)'"""
    reg_open_url = """'open_url':.'(.*?)'"""
    reg_source = """'source':.'(.*?)'"""
    reg_behot_time = """'behot_time':.'(.*?)'"""
    num = 100
    for key_fin in key_list:
        key_find = key_fin
        for i in range(0,num):
            index_url = "https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset={0}&format=json&keyword={1}&autoload=true&count={1}&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis".format(i*20, key_find, 20)

            jrtt(index_url, table_name, key_find, reg_abstract, reg_title, reg_open_url, reg_source, reg_behot_time).pare_page()


if __name__ == '__main__':
    main()