# -*- coding=gbk -*-
import re
import openpyxl
from bs4 import BeautifulSoup


data = openpyxl.load_workbook(r'E:\Python\PyCharm\project\AdministrativePenalty\���������������������ȡ�ؼ���\��������������������8.31.xlsx')
active = data.active
table = data['Sheet1']
rows = table.max_row

for row in range(2,rows+1) :
    # rowH = 'H%s'%(row)
    rowK = 'K%s'%(row)
    rowK_va = table[rowK].value
    rowJ = 'J%s'%(row)
    print(type(rowK_va))

    #   I ���ģ� H �޸ĺ�


    "������ȡ�������жϣ������Ӧ��ֵ"
    # if table[rowJ].value ==None :
    #     # rowK_va = re.sub(r'<b>', '', rowK_va).replace('</b>', '')
    #     # rowK_va = re.sub(r'<font.*?>', '', rowK_va).replace('</font>', '').replace('</FONT>', '')
    #     # rowK_va = re.sub(r'<span.*?>', '', rowK_va).replace('</span>', '')
    #     # rowK_va = re.sub(r'<a.*?>', '', rowK_va).replace('</a>', '')
    #     # rowK_va = re.sub(r'<td.*?>', '<p>', rowK_va).replace('</td>', '</p>')
    #     # rowK_va = re.sub(r'<tr.*?>', ' ', rowK_va).replace('</tr>', ' ')
    #     # rowK_va = re.sub(r'<p.*?>', '<p>', rowK_va).replace('</tr>', ' ')
    #     # rowK_va = re.sub(r'<strong.*?>', '', rowK_va).replace('</strong>', '').replace('</u>', '').replace('<u>',
    #     #                                                                                                    '').replace(
    #     #     " ", '').replace("<o:p>",'').replace("</o:p>",'')
    #     # soup = BeautifulSoup(rowK_va,'lxml')
    #     # soup = soup.find_all("p")
    #     # print("���ڴ����" + str(row) + "�е�����")
    #     # print(soup)
    #
    # if soup[-1].find("��")!=-1 and  soup[-1].find("��")!=-1 and soup[-1].find("��")!=-1 and len(soup[-1])<30:
    #     print("yes")
    #     print(soup[-1])
    #     table[rowJ] = str(soup[-1]).replace("<p>",'').replace("</p>",'')
    # else:
    #     pass
    # print(rowI_va)
    #  �滻����ʱ��
    # rs = re.findall(re.compile(r'[�� 0 O o �� �� һ �� �� �� �� �� �� �� �� ʮ]{4}��[�� һ �� �� �� �� �� �� �� �� ʮ]{1,2}��[�� һ �� �� �� �� �� �� �� �� ʮ]{1,3}��'), str(rowH_va))
    #     # rs = re.findall(re.compile(r'[�� һ �� �� �� �� �� �� �� �� ʮ]{1,2}��'),str1)
    # # print(type(rowK_va))
    # print(rs)
    # if rs!=[]:
    #     print(rs[0])
    #     print("���ڴ���ڣ�"+str(row)+"�е�����")
    #     startIndex = rowH_va.find(rs[0])
    #     endIndex = startIndex + len(rs[0])
    #     print(str(startIndex) )
    #     NowRow = "���ڴ����" + str(row) + "�е�����"
    #     print(NowRow)
    #     rs  = rs[0]
    #     # with open("E:\\�滻ʱ��.txt",'a') as f:
    #     #     f.write(NowRow+"\n")
    #     if rs.find("��") and rs.find("��") and rs.find("��"):
    #         rss = re.split('[�� �� ��]', rs)
    #         time1 = ['��', '0', 'O', 'o', '��', '��', 'һ', '��', '��', '��', '��', '��', '��', '��', '��', 'ʮ']
    #         time2 = ['0', '0', '0', '0', '0', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' 10']
    #         YearList = []
    #         MonthList = []
    #         DayList = []
    #         # print(rss[2])
    #         print(len(rss[2]))
    #         if len(rss[0]) == 4:
    #             for y in rss[0]:
    #                 if y in time1:
    #                     index = time1.index(y)
    #                     yy = time2[index]
    #                     YearList.append(yy)
    #             # print(YearList)
    #
    #             if len(rss[1]) <= 2:
    #                 for m in rss[1]:
    #                     if m in time1:
    #                         index1 = time1.index(m)
    #                         mm = time2[index1]
    #                         MonthList.append(mm)
    #             # print(MonthList)
    #             elif 2 < len(rss[1]) <= 3:
    #                 for m in rss[1]:
    #                     if m in time1:
    #                         index1 = time1.index(m)
    #                         mm = time2[index1]
    #                         MonthList.append(mm)
    #             print(MonthList)
    #             if len(rss[2]) <= 2:
    #                 print(rss[2])
    #                 for d in rss[2]:
    #                     if d in time1:
    #                         index1 = time1.index(d)
    #                         dd = time2[index1]
    #                         DayList.append(dd)
    #             elif 2 < len(rss[2]) <= 3:
    #                 for d in rss[2]:
    #                     if d in time1:
    #                         index1 = time1.index(d)
    #                         dd = time2[index1]
    #                         DayList.append(dd)
    #         print(DayList)
    #         if YearList != [] and MonthList != [] and DayList != []:
    #             print("yes")
    #             Year = ''.join(str(i) for i in YearList).replace(" ",'')
    #             Moth = ''.join(str(i) for i in MonthList).replace(" ",'')
    #             Day = ''.join(str(i) for i in DayList).replace(" ", '')
    #             if len(Moth) > 2:
    #                 Moth = Moth[0] + Moth[-1]
    #             if len(Day) > 2:
    #                 Day = Day[0] + Day[-1]
    #             Result = Year + "��" + Moth + "��" + Day + "��"
    #             print(Result)
    #             table[rowH] = rowH_va.replace(rowH_va[startIndex:endIndex],Result)
    #             print("����������")
    #             print(rowH_va.replace(rowH_va[startIndex:endIndex],Result))
    #             with open("E:\\�滻ʱ��.txt", 'a') as f:
    #                 f.write(str(NowRow)+"\n"+"ʱ��Ϊ"+str(rs)+"��"+str(YearList)+"��"+str(MonthList)+"��"+str(DayList)+"\n"+str(Result)+"\n")
    # else:
    #     pass

    str1 = re.sub(r'<span.*?>', '', str(rowK_va), flags=re.I).replace('</span>', '').replace('</SPAN>', '')

    # ��һ����ȥ��<FONT> ....</FONT>
    str1 = re.sub(r'<FONT.*?>', '', str1, flags=re.I).replace('</FONT>', '').replace('</font>', '')

    # ��һ����ȥ��<p style="text-align:center;line-height:38px">...</p>
    str1 = re.sub(r'<p.*?>', '<p>', str1)
    # # ��һ����ȥ��<P style="text-align:center;line-height:38px">...</P>
    str1 = re.sub(r'<P.*?>', '<p>', str1)
    str1 = re.sub(r'</P>', '</p>', str1)

    # # ��һ����ȥ��<img width=  ..... #ddd"/>
    # str1 = re.sub(r'<img .*? solid #ddd"/>', '', str1)

    # ��һ����ȥ��<?xml:namespace prefix = o ns = "urn:schemas-microsoft-com:office:office" /><o:p></o:p>
    str1 = re.sub(r'<?xml:namespace .*?>', '', str1)
    str1 = str1.replace('<o:p></o:p>', '').replace('<o:p>', '').replace('</o:p>', '')

    # ��һ����ȥ��<<strong>> ....</<strong>>
    str1 = re.sub(r'<strong.*?>', '', str1, flags=re.I).replace('</strong>', '')

    # <st1:chsdate year="2017" month="3" day="30" islunardate="False" isrocdate="False" w:st="on">...</st1:chsdate>
    str1 = re.sub(r'<st1:chsdate .*?>', '', str1)
    str1 = re.sub(r'</st1:chsdate>', '', str1)
    # print('���ǵ�' + str(j) + '������' + str1.encode('latin-1').decode('gbk'))

    # �������滻��ȥ��ͷ<p><p> =><p>
    str1 = str1.replace(r'<p><p>', '<p>')

    # ������ �滻��<br> Ϊ</p><p>
    str1 = str1.replace('<br>', '</p><p>').replace('</br>', '</p><p>').replace('<br/>', '</p><p>')
    str1 = str1.replace('<BR>', '</p><p>').replace('</BR>', '</p><p>')

    # �����Ǵ���<p></p>�������ñ�ǩ�����е�&nbsp;
    str1 = re.sub(r'&nbsp;', '', str1)
    str1 = re.sub(r'<p></p>', '', str1)
    # ���ñ��룬python3
    # str1 = str1.encode('latin-1').decode('gbk')
    # str1 = str1.encode("utf-8").decode("latin1")
    #
    str1 = re.sub(r'<td.*?>', '<p>', str1).replace("</td>",'</p>')
    str1 = re.sub(r'<aname=.*?>', '', str1).replace("</a>",'')
    str1 = re.sub(r'\u3000', '', str1)





    # �������
    title = re.findall(re.compile(r'<p>.*?[�� �� ��].*?\d��</p>'),str1)
    if title!=[]:
        ti = str1.find(title[-1])
        if ti<100  and len(title[-1]) <20:
            title[0] = title[0].replace("<p>",'').replace("</p>",'')
            str1 = str1.replace(title[0],''.join(['<p style="text-align: center;">'+title[-1]+'</p>']))

    # �����Ǵ������ʱ��ĸ�ʽ
    yy = r'<p>\s*[ �� �� 0 O o �� �� һ �� �� �� �� �� �� �� �� ʮ]{4}��[һ �� �� �� �� �� �� �� �� ʮ ��]{1,2}��[һ �� �� �� �� �� �� �� �� ʮ ��]{1,2}��\s*</p>|<p>\s*\d{4}��\d{1,2}��\d{1,2}��</p>'
    str2 = re.findall(re.compile(yy), str1)
    print("�ҵ��Ľ��"+str(str2))
    if len(str2) != 0 :
        find1 = str1.find(str2[-1])
        if find1 > 100  and len(str2[-1])<20 :
            str2[-1] = str2[-1].replace("<p>", '').replace("</p>", '')
            print("str2[-1]"+str2[-1])
            rss = re.split('[�� �� ��]', str2[-1])
            print(rss)

            time1 = ['��','��', '0', 'O', 'o', '��', '��', 'һ', '��', '��', '��', '��', '��', '��', '��', '��', 'ʮ']
            time2 = ['0','0', '0', '0', '0', '0', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' 10']
            YearList = []
            MonthList = []
            DayList = []
            if len(rss[0]) == 4:
                for y in rss[0]:
                    if y in time1:
                        index = time1.index(y)
                        yy = time2[index]
                        YearList.append(yy)
                print(YearList)
                if len(rss[1]) <= 2:
                    for m in rss[1]:
                        if m in time1:
                            index1 = time1.index(m)
                            mm = time2[index1]
                            MonthList.append(mm)
                # print(MonthList)
                elif 2 < len(rss[1]) <= 3:
                    for m in rss[1]:
                        if m in time1:
                            index1 = time1.index(m)
                            mm = time2[index1]
                            MonthList.append(mm)
                print(MonthList)
                if len(rss[2]) <= 2:
                    print(rss[2])
                    for d in rss[2]:
                        if d in time1:
                            index1 = time1.index(d)
                            dd = time2[index1]
                            DayList.append(dd)
                elif 2 < len(rss[2]) <= 3:
                    for d in rss[2]:
                        if d in time1:
                            index1 = time1.index(d)
                            dd = time2[index1]
                            DayList.append(dd)
            print(DayList)
            if YearList != [] and MonthList != [] and DayList != []:
                print("yes")
                Year = ''.join(str(i) for i in YearList).replace(" ", '')
                Moth = ''.join(str(i) for i in MonthList).replace(" ", '')
                Day = ''.join(str(i) for i in DayList).replace(" ", '')
                if len(Moth) > 2:
                    Moth = Moth[0] + Moth[-1]
                if len(Day) > 2:
                    Day = Day[0] + Day[-1]
                Time1 = Year + "��" + Moth + "��" + Day + "��"
                print("����ʱ��"+str2[-1])
            # ����������ʱ��ͼ��ϸ�<p style="text-align: right;"> ����������ʾ
                print("noe"+str2[-1])
                if Time1:
                    str1 = str1.replace(str2[-1], ''.join(['<p style="text-align: right;">' + Time1 + '</p>']))
            else:
                str1 = str1.replace(str2[-1], ''.join(['<p style="text-align: right;">' + str2[-1] + '</p>']))

    # �����Ǵ�����λ
    yy2 = r'<p>[\u4E00-\u9FA5\uF900-\uFA2D]+[\�� ,\Э��,\��]</p>'
    rs = re.findall(re.compile(yy2), str1)
    if len(rs) != 0:
        find1 = str1.find(rs[-1])
        if find1 > 100 and len(rs[-1])<20:
            rs[-1] = rs[-1].replace("<p>",'').replace("</p>",'')
            str1 = str1.replace(rs[-1], ''.join(['<p style="text-align: right;">' + rs[-1] + '</p>']))
        else:
            pass

    else:
        pass
    table[rowJ] = str1

data.save(r'E:\Python\PyCharm\project\AdministrativePenalty\���������������������ȡ�ؼ���\��������������������8.31.xlsx')

