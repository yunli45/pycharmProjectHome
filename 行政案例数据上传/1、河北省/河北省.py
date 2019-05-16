# coding = utf-8
import re
from 工具包 import 各种处理, 链接数据库
from tkinter import *
import tkinter.messagebox
import time

# 第一步先处理各种标签问题，并检查附件问题
def check_hyper_link(table_name, excel_file_path, adj_file_path, adj_orr_excel_path):
    """
    :param table_name: 需要传入到数据库（已经固定了不需要修改）下具体的那张表（其实不传也可以，只是为了提醒下你看下是否是传到你想要的具体的表）
    :param excel_file_path: EXCEL文件所在的位置
    :param adj_file_path: 本地附件保存的父级目录  (E:\行政案例附件\datafolder\历史\河北省)
    :param adj_orr_excel_path: 本地附件保问题保存的excel文件名 （../附件情况.xlsx）
    :return:
    对应行政案例数据库 自收录数据 字段：
         标题、全文、 区域、类别、机构、文号、被处罚主体、法人、处罚对象、处罚日期、文章字数、附件
    """
    start_time = time.time()
    root = Tk()
    root.withdraw()  # ****实现主窗口隐藏
    tkinter.messagebox.showinfo("温馨提示", "       注意本程序至少需要运行三次：第一次、处理标签问题，检查附件问题，并把附件问题写入本地相应excel文件中；第二次、将已经处理过标签和附件情况（手动修改存在问题的数据）的数据，开始文中附件在本地（我的电脑上面）以及放入到服务器上面的位置（E:\datafolder\）；第三次、在已经处理了附件、标签、附件名的情况下，已经是预处理后的数据了，开始上传到数据库中")

    wb_ws_rows = 各种处理.open_excel_file(excel_file_path)
    wb = wb_ws_rows[0]
    ws = wb_ws_rows[1]
    rows = wb_ws_rows[2]

    """
        第一次处理： 处理标签问题，检查附件问题，写入本地相应excel文件中
    """
    ans = tkinter.messagebox.askquestion("温馨提示", "开始第一次运行程序，本次主要完成：处理标签问题、附件问题检查并写入本地的excel文件中.......,是否继续运行？")
    if ans == "yes":
        ws['v1'] = '字数'
        ws['w1'] = '附件'
        ws['X1'] = '附件(本地)'
        for row in range(2, rows+1):
            print("正在读取,并处理第："+str(row)+"行的数据")
            title = ws['B%s' % (row)].value  # 标题
            if title == None:
                break
            else:
                cont = str(ws['Q%s' % (row)].value) + str(ws['R%s' % (row)].value) + str(ws['S%s' % (row)].value)  # 全文，后边处理后的，传入数据库的字段为：content
                cont = cont.replace("None", '')

                source_url =  ws['I%s' % (row)].value                        # 这条数据的完整请求地址

                # 处理文中的标签问题，没有处理 a 、img 标签，由 check_adj 方法来处理
                content = 各种处理.processing_text(str(cont))

                # 检查附件情况，并写入本地相应的excel文件中，
                cont_end = 各种处理.check_adj(title, adj_file_path, content, source_url, adj_orr_excel_path, row)
                char_num = len(re.sub('</？[^>]*>', '', content))               # 文章字数

                # 现在开始将处理标签后的数据存入原数据表，注意 a 、img 标签，如果出现链接没改，请自行修改，只处理这两种标签跳转的情况，以及其他的标签
                if 0 < len(cont_end) <30000:
                    ws['Q%s' % (row)] = cont_end
                    ws['V%s' % (row)] = char_num
                elif 30000 <= len(cont_end) < 60000:
                    ws['Q%s' % (row)] = cont_end[:30000]
                    ws['R%s' % (row)] = cont_end[30000:]
                    ws['V%s' % (row)] = char_num
                elif 60000 <= len(cont_end) < 90000:
                    ws['Q%s' % (row)] = cont_end[:30000]
                    ws['R%s' % (row)] = cont_end[30000:60000]
                    ws['S%s' % (row)] = cont_end[60000:]
                    ws['V%s' % (row)] = char_num
        wb.save(excel_file_path)
        tkinter.messagebox.showinfo("温馨提示", "第一次运行已经结束，本次已经处理了标签和检查出附件的问题已经存在本地的:{0} 文件中了，请先自行查看，并手动解决附件问题！！！".format(
            adj_orr_excel_path))
        end_time = time.time()
        print("本次运行时间为："+str(end_time - start_time)+" S")


    """
        第二次处理：将已经处理过标签和附件情况的数据，将文中附件在本地（我的电脑上面）以及放入到服务器上面的位置（E:\datafolder\）写入到源数据表格中
    """

    # ans = tkinter.messagebox.askokcancel("警告", "开始第二次运行程序，本次主要任务是：将文中附件在本地（我的电脑上面）以及放入到服务器上面的位置（E:\datafolder\）写入到源数据表格; 本次运行的前提是：已经将附件问题全部修改了，没有的话后期忘了会出现附件问题很麻烦的，你是否已经处理好了之前检查出的附件问题？")
    #
    # if ans == True:
    #     for row in range(2, rows+1):
    #         print("正在读取,并处理第：" + str(row) + "行的数据")
    #         title = ws['B%s' % (row)].value  # 标题
    #         if title == None:
    #             pass
    #         else:
    #             cont = str(ws['Q%s' % (row)].value) + str(ws['R%s' % (row)].value) + str(ws[
    #                                                                                          'S%s' % (
    #                                                                                              row)].value)  # 全文，后边处理后的，传入数据库的字段为：content
    #             cont = cont.replace("None", '')
    #             save_path_local = adj_file_path
    #             save_path_father_server = "E:"  # 服务器上面附件保存位置，现在统一是在E:\datafolder\省份（北京市或者模块：环保局），因为是记录位置需要拼接服务器上面完整的位置，只需要 E：就行了，datafolder这些是通过文中链接来提取的，且已经将/转义为了\
    #             adj_list = 各种处理.check_adj_name(title, cont, save_path_father_server, save_path_local)
    #             the_server_adj_list = adj_list[0]
    #             the_local_adjlist = adj_list[1]
    #             ws['w{0}'.format(row)] = the_server_adj_list
    #             ws['x{0}'.format(row)] = the_local_adjlist
    #     wb.save(excel_file_path)
    #     tkinter.messagebox.showinfo("温馨提示", "第二次处理已经完成，将已处理附件问题后的每条数据的附件在本地和服务器上本地位置已经写入到源数据：{0} 中了".format(excel_file_path))
    # else:
    #     tkinter.messagebox.showwarning("警告", "请先手动处理之前检测出的附件问题，本地附件问题保存文件是：{0}".format(adj_orr_excel_path))
    # end_time = time.time()
    # print("本次运行的时间是：" + str(end_time - start_time) + " S")


    """
        第三次处理，在已经处理了附件、标签、附件名的情况下，已经是预处理后的数据了，开始长传到数据库中
    """
    # answer = tkinter.messagebox.askquestion("温馨提示框", "这是第三次运行本程序了，本次的主要任务是：将已经处理了标签和附件问题的数据上传到数据库，请先确认下是否进行了前两次的运行并解决了相应的问题。是否继续进行，点击“是”的就会直接将数据传入到数据库中！！！".format(adj_orr_excel_path))
    # if answer == "yes":
    #     ins_sql = ""
    #     connect_cursor = 链接数据库.get_connect_cursor()
    #     connect = connect_cursor[0]
    #     cursor = connect_cursor[1]
    #     for row in range(2, rows+1):
    #         title = ws['B%s' % (row)].value  # 标题
    #         if title == None:
    #             break
    #         else:
    #             book_num = str(ws['C%s' % (row)].value).replace("None", '')              # 文号
    #             legal_person = str(ws['D%s' % (row)].value).replace("None", '')          # 法人
    #             punished_person = str(ws['E%s' % (row)].value).replace("None", '')       # 被处罚主体
    #             law_organ = str(ws['F%s' % (row)].value).replace("None", '')             # 执法机构（自收录数据库中没有这个字段）
    #             penalty_time = str(ws['G%s' % (row)].value).replace("None", '').replace(" 00:00:00", '').replace("-", '')          # 处罚日期
    #             law = str(ws['L%s' % (row)].value).replace("None", '')                   # 机构
    #             region = str(ws['M%s' % (row)].value).replace("None", '')                # 区域
    #             category = str(ws['N%s' % (row)].value).replace("None", '')              # 类别
    #             Objectofpunishment = str(ws['U%s' % (row)].value).replace("None", '')    # 处罚对象
    #             cont = str(ws['Q%s' % (row)].value) + str(ws['R%s' % (row)].value) + str(ws[
    #                 'S%s' % (row)].value)  # 全文，后边处理后的，传入数据库的字段为：content
    #             cont = cont.replace("None", '')
    #             char_num = len(re.sub('</？[^>]*>', '', cont))  # 文章字数
    #             adj = str(ws['W{0}'.format(row)].value).replace("None", '').replace(' ','')        # 附件
    #
    #             # 先根据标题和书文号查询这条数据在数据库是否存在这条数据，不存在的话再拼接
    #             select_sql = "select *  from {0} where 标题='{1}' and 文号='{2}'".format(table_name, title, book_num)
    #             select_res = 链接数据库.query(cursor, select_sql)
    #             if select_res == None:
    #                 ins_sql += "insert into {0} (标题, 全文, 区域, 类别, 机构, 文号, 被处罚主体, 法人, 处罚对象, 处罚日期, 文章字数, 附件) values ('{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}');\n".format(table_name, title, cont, region, category, law, book_num, punished_person, legal_person, Objectofpunishment, penalty_time, char_num, adj)
    #                 print(ins_sql)
    #                 print("\n\n")
    #                 if row % 100 == 0 or row == rows:
    #                     connect_cursor1 = 链接数据库.get_connect_cursor()
    #                     connect1 = connect_cursor1[0]
    #                     cursor1 = connect_cursor1[1]
    #                     链接数据库.insert(cursor1, ins_sql)
    #                     链接数据库.break_connect(connect1)
    #                     ins_sql = " "
    # else:
    #     tkinter.messagebox.showwarning("温馨提示框", "你选择了“否”,请先查看第一次和第二次运行的结果是否和预期一致，如果一致的话，再次运行本程序点击“是”就好了........")


"""
    程序的入口
"""
if __name__ == '__main__':

    table_name = "[自收录数据].dbo.[AdministrativeCase-行政执法案例] "
    check_hyper_link(table_name, "./河北省【校对上传版】.xlsx", 'E:\行政案例附件\datafolder\历史\河北省', './河北省附件情况.xlsx')