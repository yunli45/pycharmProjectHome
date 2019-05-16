# -*- coding: utf-8 -*-
"""
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
import re
from bs4 import BeautifulSoup
from 工具包 import 移动文件, 字符串查找方法, 读写xlsx文件
import openpyxl


class Discussion(object):
    def __init__(self):
        self.name = "Discussion"

    # 第一步：先读取一个文件下的文件，判断每一个文件是选择题还是 做答题（论述题）
    def open_file(self, file_path_1, excel_file_path_1):
        # 罗列出所有文件，并读取每一个文件
        file_list = 移动文件.seachFile(file_path_1)
        for file_1 in file_list:
            with open(file_1, 'r', encoding='utf-8', errors='ignore') as f:
                s = f.read()

                # 提取全部内容
                label_name = "div"
                label_class = "class"
                label_val = "examPaper"
                all_cont_soup = BeautifulSoup(s, 'lxml')
                all_cont = all_cont_soup.find_all(label_name, attrs={label_class: label_val})

                if all_cont is not []:
                    # 2、提取全部题型、以及每种题型对应：题干、答案、描述到一个集合中
                    label_name_1 = "div"
                    label_class_1 = "class"
                    label_val_1 = "SubType"
                    all_qes_types = all_cont_soup.find_all(label_name_1,
                                                           attrs={label_class_1: label_val_1})  # len = 2

                    if all_qes_types is not []:
                        # 分别提取每种题型 、 以及每种题型下的每道题
                        # 循环遍历每种题型，并提取该题型下的内容
                        for qes_types_before in all_qes_types:

                            # 3、提取题型
                            qes_types_name = "div"
                            qes_types_class = "class"
                            qes_types_val = "SubTypeDesc"  # 题型描述
                            qes_types_before_soup = BeautifulSoup(str(qes_types_before), 'lxml')
                            qes_type_descs = qes_types_before_soup.find_all(qes_types_name,
                                                                            attrs={qes_types_class: qes_types_val})
                            print(len(qes_type_descs))
                            if qes_type_descs is not []:
                                for qes_type_desc in qes_type_descs:
                                    题型 = str(qes_type_desc.string).replace("\t", '').replace("\n", '')
                                    print("题型：" + 题型)
                            else:
                                raise Exception(
                                    """3、：提取具体的题型描述的出现问题，题型的描述不在<{0} {1}="{2}">标签中""".format(qes_types_name,
                                                                                             qes_types_class,
                                                                                             qes_types_val))
                    else:
                        raise Exception(
                            """2、：提取所有的题型的时候出现问题，题型不在<{0} {1}="{2}">标签中""".format(label_name_1, label_class_1,
                                                                                  label_val_1))


    # 读取系统文件:罗列出一个目录下的所有文件
    def open_file_1(self, file_path_1, excel_file_path_1):
        # 罗列出所有文件，并读取每一个文件
        file_list = 移动文件.seachFile(file_path_1)
        for file_1 in file_list:
            with open(file_1, 'r', encoding='utf-8', errors='ignore') as f:
                s = f.read()
                # 论述题所有的内容全部在一个 <div class="examPaper">中, 又分别由两个相同的div包含着1、分析题  2、论述题 （<div class='SubTypeDesc'>
                # 	2. 论述题</div>)
                #  每道题由 <div class='Sub'> 包括

                # 提取全部内容
                label_name = "div"
                label_class = "class"
                label_val = "examPaper"
                all_cont_soup = BeautifulSoup(s, 'lxml')
                all_cont = all_cont_soup.find_all(label_name, attrs={label_class: label_val})

                # 提取文件名字（标题）包含了：考试种类、知识点、来源、(出处还有待考虑)
                if all_cont is not []:

                     # 1、提取文件名字（标题）
                    title_la_name = "div"
                    title_la_class = "class"
                    title_la_val = "mTitle"
                    title_info = all_cont_soup.find_all(title_la_name, attrs={title_la_class: title_la_val})
                    if title_info is not [] and len(title_info) == 1:
                            title = title_info[0].string

                            #  考试种类
                            test_type = ["国家司法考试", "司法考试模拟题"]
                            for type in test_type:
                                if title.find(type) != -1:
                                    考试种类 = type
                                    break
                                else:
                                    考试种类 = ""

                            # 知识点从这里面选取
                            points_list = ["法理学", "法制史", "国际法", "国际经济法", "国际私法", "经济法", "民法", "民事诉讼法与仲裁制度", "商法",
                                           "司法制度和法律职业道德", "宪法", "刑法", "刑事诉讼法", "行政法与行政诉讼法"]
                            for point in points_list:
                                if title.find(point) != -1:
                                    知识点 = point
                                    break
                                else:
                                    知识点 = ''

                            # 来源
                            source_list = ['真题', '模拟题']
                            for source in source_list:
                                if title.find(source) != -1:
                                    来源 = source
                                    break
                                else:
                                    来源 = '未知'
                    else:
                        raise Exception(
                            """sorry,该文件的标题不在这个标签中<{0} {1} "{2}">，或者不止一个该标签""".format(title_la_name, title_la_class, title_la_val))

                    # 2、提取全部题型、以及每种题型对应：题干、答案、描述到一个集合中
                    label_name_1 = "div"
                    label_class_1 = "class"
                    label_val_1 = "SubType"
                    all_qes_types = all_cont_soup.find_all(label_name_1,
                                                           attrs={label_class_1: label_val_1})  # len = 2

                    if all_qes_types is not []:
                        # 分别提取每种题型 、 以及每种题型下的每道题
                        # 循环遍历每种题型，并提取该题型下的内容
                        大题干的长度 = len(all_qes_types)
                        for qes_types_before in all_qes_types:

                            # 3、提取题型
                            qes_types_name = "div"
                            qes_types_class = "class"
                            qes_types_val = "SubTypeDesc"  # 题型描述
                            qes_types_before_soup = BeautifulSoup(str(qes_types_before), 'lxml')
                            qes_type_descs = qes_types_before_soup.find_all(qes_types_name,
                                                                            attrs={qes_types_class: qes_types_val})
                            print(len(qes_type_descs))
                            if qes_type_descs is not []:
                                # 循环每种题型（题型描述），并提取每日中题型下的内容
                                for qes_type_desc in qes_type_descs:
                                    题型 = str(qes_type_desc.string).replace("\t", '').replace("\n", '')
                            else:
                                raise Exception(
                                    """3、：提取具体的题型描述的出现问题，题型的描述不在<{0} {1}="{2}">标签中""".format(qes_types_name,
                                                                                             qes_types_class,
                                                                                             qes_types_val))

                            # 4、提取该题型的每一道题大题干(包含了大题干、小题干、答案、描述)到一个集合中
                            qes_cont_name = "div"
                            qes_cont_class = "class"
                            qes_cont_val = "Sub"
                            ques_conts = qes_types_before_soup.find_all(qes_cont_name,
                                                                        attrs={qes_cont_class: qes_cont_val})
                            # 提取该题型下的：大题干、小题干
                            if ques_conts is not []:
                                # 没到题型的下的题目数
                                ques_conts_lent = len(ques_conts)

                                # 循环每个大题干下，提取其下的：小题干、答案、描述、分值
                            #     for ques_cont in ques_conts:
                            #         # 大题干
                            #         ques_cont_soup = BeautifulSoup(str(ques_cont), 'lxml')
                            #         big_ques_desc_name = "div"
                            #         big_ques_desc_class = "class"
                            #         big_ques_desc_val = "SubDesc"  # 大题干的描述
                            #         big_ques_descs = ques_cont_soup.find_all(big_ques_desc_name,
                            #                                              attrs={big_ques_desc_class: big_ques_desc_val})
                            #         # 大题干
                            #         if big_ques_descs is not []:
                            #             ques_list = []
                            #             for ques_desc in big_ques_descs:
                            #                 ques_desc = re.sub('<div.*?>', '', str(ques_desc)).replace("<pre>",
                            #                                                                            '').replace(
                            #                     "</pre>", '').replace("</div>", '')
                            #                 ques_desc = ques_desc.replace("【", '\n【')
                            #                 ques_list.append(ques_desc)
                            #
                            #         else:
                            #             Exception("""提取{0}这一题型具体的某一题，题描述的具体内容不在<{1} {2}="{3}">标签中""".format(题型,
                            #                                                                                 big_ques_desc_name,
                            #                                                                                 big_ques_desc_class,
                            #                                                                                 big_ques_desc_val))
                            #
                            #         # 小题干(具体的问题)
                            #         small_ques_desc_name = "div"
                            #         small_ques_desc_class = "class"
                            #         small_ques_desc_val = "Qst"
                            #         ques = ques_cont_soup.find_all(small_ques_desc_name, attrs={
                            #             small_ques_desc_class: small_ques_desc_val})
                            #         if ques is not []:
                            #             samll_que_len = len(ques)
                            #             que_list = []
                            #             for que in ques:
                            #                 print(que)
                            #                 # 提取每个小题干
                            #                 QstDesc_name = "div"
                            #                 QstDesc_class = "class"
                            #                 QstDesc_val = "QstDesc"
                            #                 QstDesc_soup = BeautifulSoup(str(que),'lxml')
                            #                 QstDesc = QstDesc_soup.find(QstDesc_name, attrs={QstDesc_class: QstDesc_val})
                            #
                            #                 if QstDesc is not []:
                            #                     QstDesc_len = len(QstDesc)
                            #                     小题干 =  str(QstDesc[0])
                            #                     小题干 = re.sub("<div.*?>", '', 小题干).replace("</div>", '').replace("<pre>", '').replace("</pre>", '')
                            #                 else:
                            #                     raise Exception("""提取小题干的描述的时候出现问题，内容不在<{0} {1}="{2}">这个标签中""".format(QstDesc_name, QstDesc_class, QstDesc_val))
                            #
                            #                 # 分值
                            #                 score_list = re.findall("该问题分值:(.*?)<", str(ques_cont))
                            #
                            #                 # 答案Answer
                            #                 answer_name = "div"
                            #                 answer_class = "class"
                            #                 answer_val = "Answer"
                            #                 answers = QstDesc_soup.find_all(answer_name,
                            #                                                   attrs={answer_class: answer_val})
                            #                 if answers is not []:
                            #                     answers_list = []
                            #                     for answer in answers:
                            #                         answer = re.sub("<div.*?>", '', str(answer)).replace(
                            #                             "</div>",
                            #                             '').replace(
                            #                             "<pre>", '').replace("</pre>", '').replace("\n", '')
                            #                         answer = re.sub("<span.*?>", '', str(answer)).replace(
                            #                             "</span>",
                            #                             '').replace(
                            #                             "<br/>", '')
                            #                         answers_list.append(answer)
                            #                 else:
                            #                     raise Exception(
                            #                         """提取{0}这一题型出现问题，答案中的具体内容不在<{1} {2}="{3}">标签中""".format(题型,
                            #                                                                                 answer_name,
                            #                                                                                 answer_class,
                            #                                                                                 answer_val))
                            #         else:
                            #             raise Exception("""具体的问题不在，<{0} {1}="{2}">""".format(small_ques_desc_name,
                            #                                                                  small_ques_desc_class,
                            #                                                                  small_ques_desc_val))
                            #
                            #
                            #
                            #
                            #
                            #         # print(题型)
                            #         # print("考试种类:" + str(考试种类))
                            #         # print(知识点)
                            #         # print("大体干"+ str(ques_list))
                            #         # print("小题干" + str(que_list))
                            #         # print("分值" + str(score_list))
                            #
                            #         # 注意 分析题是一个大题干，下有很多小题干，论述题是一个题干，一个答案
                            #         count_id = 1;
                            #         if 题型.find("分析题") != -1 and len(que_list) ==len(score_list):
                            #             data_table_rows = 读写xlsx文件.open_excel_file(excel_file_path_1)
                            #             data = data_table_rows[0]
                            #             table = data_table_rows[1]
                            #             rows = data_table_rows[2]
                            #             count_len = len(ques_list) # 大题干
                            #             print()
                            #             for ques  in ques_list:
                            #
                            #                 for row in range(2,100):
                            #
                            #                     table['A%s'%(row)] = 考试种类
                            #                     table['B%s'%(row)] = 知识点
                            #                     table['D%s'%(row)] = 题型
                            #                     table['G%s'%(row)] = 题型
                            else:
                                raise Exception(
                                    """提取{0}这一题型出现问题，题型中的具体内容不在<{1} {2}="{3}">标签中""".format(题型, label_name_1,
                                                                                            label_class_1,
                                                                                            label_val_1))
                    else:
                        raise Exception(
                            """2、：提取所有的题型的时候出现问题，题型不在<{0} {1}="{2}">标签中""".format(label_name_1, label_class_1,
                                                                                  label_val_1))

                else:
                    raise Exception("""1、：sorry,该文件的全文内容不在这个标签中<{0} {1} "{2}">""".format(label_name, label_class, label_val))


            # break

    # 选择题：
    def open_file_2(self, file_path_1, excel_file_path_1):
        # 罗列出所有文件，并读取每一个文件
        file_list = 移动文件.seachFile(file_path_1)
        for file_1 in file_list:
            # 题型_list
            with open(file_1, 'r', encoding='utf-8', errors='ignore') as f:
                s = f.read()

                # 提取全部内容
                label_name = "div"
                label_class = "class"
                label_val = "examPaper"
                all_cont_soup = BeautifulSoup(s, 'lxml')
                all_cont = all_cont_soup.find_all(label_name, attrs={label_class: label_val})

                if all_cont is not []:
                    # 2、提取全部题型、以及每种题型对应：题干、答案、描述到一个集合中
                    label_name_1 = "div"
                    label_class_1 = "class"
                    label_val_1 = "SubType"
                    all_qes_types = all_cont_soup.find_all(label_name_1,
                                                           attrs={label_class_1: label_val_1})  # len = 2
                    题型_list = []
                    Qst_list = []  # 每道题型下的小题干集合
                    if all_qes_types is not []:
                        # 分别提取每种题型 、 以及每种题型下的每道题
                        # 循环遍历每种题型，并提取该题型下的内容
                        for qes_types_before in all_qes_types:

                            # 3、提取题型
                            qes_types_name = "div"
                            qes_types_class = "class"
                            qes_types_val = "SubTypeDesc"  # 题型描述
                            qes_types_before_soup = BeautifulSoup(str(qes_types_before), 'lxml')
                            qes_type_descs = qes_types_before_soup.find_all(qes_types_name,
                                                                            attrs={qes_types_class: qes_types_val})
                            print(len(qes_type_descs))
                            if qes_type_descs is not []:

                                题型长度 = len(qes_type_descs)
                                for qes_type_desc in qes_type_descs:
                                    题型 = str(qes_type_desc.string).replace("\t", '').replace("\n", '')

                                    题型_list.append(题型)
                                # print("题型_list:" + str(题型_list))
                                # 4、提取该题型的每一道题大题干(包含了大题干、小题干、答案、描述)到一个集合中



                                qes_cont_name = "div"
                                qes_cont_class = "class"
                                qes_cont_val = "Sub"
                                ques_conts = qes_types_before_soup.find_all(qes_cont_name,
                                                                            attrs={qes_cont_class: qes_cont_val})
                                # 提取该题型下一共有几道题
                                if ques_conts is not []:
                                    # len = len(ques_conts)

                                    for ques_cont in ques_conts:
                                        Qst_list.append(ques_cont)

                                else:
                                    raise Exception(
                                        """提取{0}这一题型出现问题，题型中的具体内容不在<{1} {2}="{3}">标签中""".format(题型, label_name_1,
                                                                                                label_class_1,
                                                                                                label_val_1))
                            else:
                                raise Exception(
                                    """3、：提取具体的题型描述的出现问题，题型的描述不在<{0} {1}="{2}">标签中""".format(qes_types_name,
                                                                                             qes_types_class,
                                                                                             qes_types_val))
                    else:
                        raise Exception(
                            """2、：提取所有的题型的时候出现问题，题型不在<{0} {1}="{2}">标签中""".format(label_name_1, label_class_1,
                                                                                  label_val_1))

            print("题型_list的长度:"+str(len(题型_list)))
            print("题型_list: "+str(题型_list))
            print("Qst_list的长度："+str(len(Qst_list)))
            print("Qst_list："+str(Qst_list))

if __name__ == '__main__':
    user = Discussion()
    file_path = r"C:\Users\ASUS\Desktop\司法题\选择题"
    excel_file_path = r"C:\Users\ASUS\Desktop\司法题\2017年司法考试真题--卷4.xlsx"
    user.open_file_2(file_path, excel_file_path)