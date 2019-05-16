# -*- coding=gbk -*-
import re
import openpyxl
from bs4 import BeautifulSoup


data = openpyxl.load_workbook(r'E:\Python\PyCharm\project\AdministrativePenalty\处理广西行政案例数据提取关键字\重庆行政处罚案例数据8.31.xlsx')
active = data.active
table = data['Sheet1']
rows = table.max_row

for row in range(2,rows+1) :
    # rowH = 'H%s'%(row)
    rowK = 'K%s'%(row)
    rowK_va = table[rowK].value
    rowJ = 'J%s'%(row)
    print(type(rowK_va))

    #   I 正文， H 修改后


    "正则提取，条件判断，插入对应的值"
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
    #     # print("正在处理第" + str(row) + "行的数据")
    #     # print(soup)
    #
    # if soup[-1].find("年")!=-1 and  soup[-1].find("月")!=-1 and soup[-1].find("日")!=-1 and len(soup[-1])<30:
    #     print("yes")
    #     print(soup[-1])
    #     table[rowJ] = str(soup[-1]).replace("<p>",'').replace("</p>",'')
    # else:
    #     pass
    # print(rowI_va)
    #  替换中文时间
    # rs = re.findall(re.compile(r'[○ 0 O o 〇 Ｏ 一 二 三 四 五 六 七 八 九 十]{4}年[〇 一 二 三 四 五 六 七 八 九 十]{1,2}月[〇 一 二 三 四 五 六 七 八 九 十]{1,3}日'), str(rowH_va))
    #     # rs = re.findall(re.compile(r'[〇 一 二 三 四 五 六 七 八 九 十]{1,2}月'),str1)
    # # print(type(rowK_va))
    # print(rs)
    # if rs!=[]:
    #     print(rs[0])
    #     print("正在处理第："+str(row)+"行的数据")
    #     startIndex = rowH_va.find(rs[0])
    #     endIndex = startIndex + len(rs[0])
    #     print(str(startIndex) )
    #     NowRow = "正在处理第" + str(row) + "行的数据"
    #     print(NowRow)
    #     rs  = rs[0]
    #     # with open("E:\\替换时间.txt",'a') as f:
    #     #     f.write(NowRow+"\n")
    #     if rs.find("年") and rs.find("月") and rs.find("日"):
    #         rss = re.split('[年 月 日]', rs)
    #         time1 = ['○', '0', 'O', 'o', '〇', 'Ｏ', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
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
    #             Result = Year + "年" + Moth + "月" + Day + "日"
    #             print(Result)
    #             table[rowH] = rowH_va.replace(rowH_va[startIndex:endIndex],Result)
    #             print("处理后的数据")
    #             print(rowH_va.replace(rowH_va[startIndex:endIndex],Result))
    #             with open("E:\\替换时间.txt", 'a') as f:
    #                 f.write(str(NowRow)+"\n"+"时间为"+str(rs)+"年"+str(YearList)+"月"+str(MonthList)+"日"+str(DayList)+"\n"+str(Result)+"\n")
    # else:
    #     pass

    str1 = re.sub(r'<span.*?>', '', str(rowK_va), flags=re.I).replace('</span>', '').replace('</SPAN>', '')

    # 这一组是去除<FONT> ....</FONT>
    str1 = re.sub(r'<FONT.*?>', '', str1, flags=re.I).replace('</FONT>', '').replace('</font>', '')

    # 这一组是去除<p style="text-align:center;line-height:38px">...</p>
    str1 = re.sub(r'<p.*?>', '<p>', str1)
    # # 这一组是去除<P style="text-align:center;line-height:38px">...</P>
    str1 = re.sub(r'<P.*?>', '<p>', str1)
    str1 = re.sub(r'</P>', '</p>', str1)

    # # 这一组是去除<img width=  ..... #ddd"/>
    # str1 = re.sub(r'<img .*? solid #ddd"/>', '', str1)

    # 这一组是去除<?xml:namespace prefix = o ns = "urn:schemas-microsoft-com:office:office" /><o:p></o:p>
    str1 = re.sub(r'<?xml:namespace .*?>', '', str1)
    str1 = str1.replace('<o:p></o:p>', '').replace('<o:p>', '').replace('</o:p>', '')

    # 这一组是去除<<strong>> ....</<strong>>
    str1 = re.sub(r'<strong.*?>', '', str1, flags=re.I).replace('</strong>', '')

    # <st1:chsdate year="2017" month="3" day="30" islunardate="False" isrocdate="False" w:st="on">...</st1:chsdate>
    str1 = re.sub(r'<st1:chsdate .*?>', '', str1)
    str1 = re.sub(r'</st1:chsdate>', '', str1)
    # print('这是第' + str(j) + '条数据' + str1.encode('latin-1').decode('gbk'))

    # 这组是替换掉去开头<p><p> =><p>
    str1 = str1.replace(r'<p><p>', '<p>')

    # 这组是 替换掉<br> 为</p><p>
    str1 = str1.replace('<br>', '</p><p>').replace('</br>', '</p><p>').replace('<br/>', '</p><p>')
    str1 = str1.replace('<BR>', '</p><p>').replace('</BR>', '</p><p>')

    # 这组是处理<p></p>这种无用标签和所有的&nbsp;
    str1 = re.sub(r'&nbsp;', '', str1)
    str1 = re.sub(r'<p></p>', '', str1)
    # 设置编码，python3
    # str1 = str1.encode('latin-1').decode('gbk')
    # str1 = str1.encode("utf-8").decode("latin1")
    #
    str1 = re.sub(r'<td.*?>', '<p>', str1).replace("</td>",'</p>')
    str1 = re.sub(r'<aname=.*?>', '', str1).replace("</a>",'')
    str1 = re.sub(r'\u3000', '', str1)





    # 处理标题
    title = re.findall(re.compile(r'<p>.*?[监 罚 处].*?\d号</p>'),str1)
    if title!=[]:
        ti = str1.find(title[-1])
        if ti<100  and len(title[-1]) <20:
            title[0] = title[0].replace("<p>",'').replace("</p>",'')
            str1 = str1.replace(title[0],''.join(['<p style="text-align: center;">'+title[-1]+'</p>']))

    # 这组是处理落款时间的格式
    yy = r'<p>\s*[ 零 ○ 0 O o 〇 Ｏ 一 二 三 四 五 六 七 八 九 十]{4}年[一 二 三 四 五 六 七 八 九 十 〇]{1,2}月[一 二 三 四 五 六 七 八 九 十 〇]{1,2}日\s*</p>|<p>\s*\d{4}年\d{1,2}月\d{1,2}日</p>'
    str2 = re.findall(re.compile(yy), str1)
    print("找到的结果"+str(str2))
    if len(str2) != 0 :
        find1 = str1.find(str2[-1])
        if find1 > 100  and len(str2[-1])<20 :
            str2[-1] = str2[-1].replace("<p>", '').replace("</p>", '')
            print("str2[-1]"+str2[-1])
            rss = re.split('[年 月 日]', str2[-1])
            print(rss)

            time1 = ['零','○', '0', 'O', 'o', '〇', 'Ｏ', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
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
                Time1 = Year + "年" + Moth + "月" + Day + "日"
                print("中文时间"+str2[-1])
            # 如果存在落款时间就加上个<p style="text-align: right;"> 让它居右显示
                print("noe"+str2[-1])
                if Time1:
                    str1 = str1.replace(str2[-1], ''.join(['<p style="text-align: right;">' + Time1 + '</p>']))
            else:
                str1 = str1.replace(str2[-1], ''.join(['<p style="text-align: right;">' + str2[-1] + '</p>']))

    # 这组是处理落款单位
    yy2 = r'<p>[\u4E00-\u9FA5\uF900-\uFA2D]+[\局 ,\协会,\厅]</p>'
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

data.save(r'E:\Python\PyCharm\project\AdministrativePenalty\处理广西行政案例数据提取关键字\重庆行政处罚案例数据8.31.xlsx')

