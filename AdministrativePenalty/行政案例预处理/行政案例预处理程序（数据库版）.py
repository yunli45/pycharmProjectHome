# coding:utf-8
import pyodbc
import re
from bs4 import BeautifulSoup
import datetime
from 行政案例预处理.工具包 import 链接数据库

class Utils(object):
    def __init__(self):
        # 没有啥可以初始化的啊，玩一玩
        self.id = 1
    def readTable(self,sql):
        con = 链接数据库.getConnect(sql)
        conn = con[0]
        cursor = con[1]
        row = cursor.fetchone()
        链接数据库.breakConnect(conn)
        return row

    def witeTable(self,sql):
        con = 链接数据库.getConnect(sql)
        conn = con[0]
        链接数据库.breakConnect(conn)
    # 核心，处理过程
    def dispose(self):
        # 查询统计一共有多少条数据
        sql1 = """
         select  count(*)  from [AdministrativeCase]
              """
        print(sql1)
        totalNumber = self.readTable(sql1)[0]# 总行数 int:2082600
        print(totalNumber)
        # for row in range(1,totalNumber+1):
        # for row in range(411000,1411000):
        # for row in range(711000,1011000):
        # for row in range(816552,1011000):
        # for row in range(1010999,1310999):
        # for row in range(1248483,1410999):
        # for row in range(1710998,2010999):
        for row in range(2375700,2376700):
            print(row)
            try :
                print(row)
                sql2 ="""
                    select  全文update  from [AdministrativeCase]  where ID= '%s'
                      """%(row)
                print(sql2)
                待处理全文 = self.readTable(sql2)[0]
                if 待处理全文 ==None:
                    sql3 = """
                                    select 全文  from [AdministrativeCase]  where ID= '%s'
                                      """ % (row)
                    待处理全文 = self.readTable(sql3)[0]

                处理格式后1 = self.disposeFormat1(待处理全文)
                处理格式后2 = self.disposeFormat2(处理格式后1)
                替换中文时间后 = self.reoalceTimeToNum(处理格式后2,row)
                处理标题后 = self.disposeTitle(替换中文时间后)
                处理落款格式后 = self.disposeInscriber(处理标题后)
                最终全文= 处理落款格式后

                sql4 = """
                update [cnlaw2.0].[dbo].[AdministrativeCase] set 预处理后 = '%s' where ID='%s'
                """%(最终全文,int(row))
                self.witeTable(sql4)
            except Exception:
                pass
    # 处理文中部分格式
    def disposeFormat1 (self,conent):
        处理中的全文 = conent
        处理中的全文 = re.sub(r'<b>', '', 处理中的全文).replace('</b>', '')
        处理中的全文 = re.sub(r'<span.*?>', '', str(处理中的全文), flags=re.I).replace('</span>', '').replace('</SPAN>', '')
        # 这一组是去除<FONT> ....</FONT>
        处理中的全文 = re.sub(r'<font.*?>', '', 处理中的全文, flags=re.I).replace('</FONT>', '').replace('</font>', '')
        处理中的全文 = re.sub(r'<?xml:namespace .*?>', '', 处理中的全文, flags=re.I)
        处理中的全文 = re.sub(r'<o:p.*?>', '', 处理中的全文, flags=re.I)
        处理中的全文 = re.sub(r'</o:p>', '', 处理中的全文, flags=re.I)
        # 表格处理：保留表格但不保留样式
        处理中的全文 = re.sub(r'<tr.*?>', '<tr>', 处理中的全文, flags=re.S | re.I).replace('</TR>', '</tr>')
        处理中的全文 = re.sub(r'<td.*?>', '<tr>', 处理中的全文, flags=re.S | re.I).replace('</TD>', '</td>')
        处理中的全文 = re.sub(r'<th.*?>', '<tr>', 处理中的全文, flags=re.S | re.I).replace('</TH>', '</th>')

        # 处理中的全文 = re.sub(r'<a.*?>', '', 处理中的全文).replace('</a>', '')
        处理中的全文 = re.sub("<style.*?>.*?</style>",'',处理中的全文, flags=re.I | re.S)
        处理中的全文 = re.sub('<script>.*?</script>', '', 处理中的全文, flags=re.I | re.S)
        # 这一组是去除<strong> ..../<strong>
        处理中的全文 = re.sub(r'<strong.*?>', '', 处理中的全文, flags=re.I)
        处理中的全文 = re.sub(r'</strong>', '', 处理中的全文, flags=re.I)
        处理中的全文 = 处理中的全文.replace('</u>', '').replace('<u>','')

        # <st1:chsdate year="2017" month="3" day="30" islunardate="False" isrocdate="False" w:st="on">...</st1:chsdate>
        处理中的全文 = re.sub(r'<st1:chsdate .*?>', '', 处理中的全文, flags=re.I)
        处理中的全文 = re.sub(r'</st1:chsdate>', '', 处理中的全文, flags=re.I)

        # 处理<div style="TEXT-ALIGN: center; LINE-HEIGHT: 150%; FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 16pt" id="allStyleDIV">
        处理中的全文 = re.sub(r'<div.*?id="allStyleDIV".*?>', '', 处理中的全文, flags=re.S | re.I)

        # <v:line></v:line> 什么鬼的直接链接符啥？啥玩意儿这是，一脸懵逼
        处理中的全文 = re.sub(r'<v:line.*?>.*?</v:line>', '', 处理中的全文, flags=re.S | re.I)

        return  处理中的全文
    # 替换文中的中文时间为阿拉伯数字格式
    def  reoalceTimeToNum(self,content,row):
        处理中的全文 = content
        #  替换中文时间
        rs = re.findall(re.compile(
            r'[○ 0 O o 〇 Ｏ 一 二 三 四 五 六 七 八 九 十]{4}年[〇 一 二 三 四 五 六 七 八 九 十]{1,2}月[〇 一 二 三 四 五 六 七 八 九 十]{1,3}日'),
                        str(处理中的全文))
        print(rs)
        if rs != []:
            print(rs[0])
            print("正在处理第：" + str(row) + "行的数据")
            startIndex = 处理中的全文.find(rs[0])
            endIndex = startIndex + len(rs[0])
            print(str(startIndex))
            NowRow = "正在处理第" + str(row) + "行的数据"
            print(NowRow)
            rs = rs[0]
            # with open(r"E:\Python\PyCharm\project\AdministrativePenalty\行政案例预处理\行政案例数处理时间记录.txt",'a') as f:
            #     f.write(NowRow+"\n")
            if rs.find("年") and rs.find("月") and rs.find("日"):
                rss = re.split('[年 月 日]', rs)
                time1 = ['○', '0', 'O', 'o', '〇', 'Ｏ', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
                time2 = ['0', '0', '0', '0', '0', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' 10']
                YearList = []
                MonthList = []
                DayList = []
                # print(rss[2])
                print(len(rss[2]))
                if len(rss[0]) == 4:
                    for y in rss[0]:
                        if y in time1:
                            index = time1.index(y)
                            yy = time2[index]
                            YearList.append(yy)
                    # print(YearList)

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
                    Result = Year + "年" + Moth + "月" + Day + "日"
                    print(Result)
                    处理中的全文 = 处理中的全文.replace(处理中的全文[startIndex:endIndex], Result)
                    print("处理后的数据")
                    print(处理中的全文.replace(处理中的全文[startIndex:endIndex], Result))
                    with open(r"E:\Python\PyCharm\project\AdministrativePenalty\行政案例预处理\行政案例数处理时间记录.txt", 'a') as f:
                        f.write(str(NowRow) + "\n" + "时间为" + str(rs) + "年" + str(YearList) + "月" + str(
                            MonthList) + "日" + str(DayList) + "\n" + str(Result) + "\n")
        else:
            pass

        return 处理中的全文
    # 处理文中部分格式
    def disposeFormat2(self, conent):
        处理中的全文 = conent
        处理中的全文 = re.sub(r'<span.*?>', '', str(处理中的全文), flags=re.I).replace('</span>', '').replace('</SPAN>', '')

        # 这一组是去除<FONT> ....</FONT>
        处理中的全文 = re.sub(r'<FONT.*?>', '', 处理中的全文, flags=re.I).replace('</FONT>', '').replace('</font>', '')

        # 这一组是去除<p style="text-align:center;line-height:38px">...</p>
        处理中的全文 = re.sub(r'<p.*?>', '<p>', 处理中的全文)
        # # 这一组是去除<P style="text-align:center;line-height:38px">...</P>
        处理中的全文 = re.sub(r'<P.*?>', '<p>', 处理中的全文)
        处理中的全文 = re.sub(r'</P>', '</p>', 处理中的全文)

        # # 这一组是去除<img width=  ..... #ddd"/>
        # 处理中的全文 = re.sub(r'<img .*? solid #ddd"/>', '', 处理中的全文)

        # 这一组是去除<?xml:namespace prefix = o ns = "urn:schemas-microsoft-com:office:office" /><o:p></o:p>
        处理中的全文 = re.sub(r'<?xml:namespace .*?>', '', 处理中的全文)
        处理中的全文 = 处理中的全文.replace('<o:p></o:p>', '').replace('<o:p>', '').replace('</o:p>', '')

        # 这一组是去除<<strong>> ....</<strong>>
        处理中的全文 = re.sub(r'<strong.*?>', '', 处理中的全文, flags=re.I).replace('</strong>', '')

        # <st1:chsdate year="2017" month="3" day="30" islunardate="False" isrocdate="False" w:st="on">...</st1:chsdate>
        处理中的全文 = re.sub(r'<st1:chsdate .*?>', '', 处理中的全文)
        处理中的全文 = re.sub(r'</st1:chsdate>', '', 处理中的全文)
        # print('这是第' + str(j) + '条数据' + 处理中的全文.encode('latin-1').decode('gbk'))

        # 这组是替换掉去开头<p><p> =><p>
        处理中的全文 = 处理中的全文.replace(r'<p><p>', '<p>')

        # 这组是 替换掉<br> 为</p><p>
        处理中的全文 = 处理中的全文.replace('<br>', '</p><p>').replace('</br>', '</p><p>').replace('<br/>', '</p><p>')
        处理中的全文 = 处理中的全文.replace('<BR>', '</p><p>').replace('</BR>', '</p><p>')

        # 这组是处理<p></p>这种无用标签和所有的&nbsp;
        处理中的全文 = re.sub(r'&nbsp;', '', 处理中的全文)
        处理中的全文 = re.sub(r'<p></p>', '', 处理中的全文)
        # 设置编码，python3
        # 处理中的全文 = 处理中的全文.encode('latin-1').decode('gbk')
        # 处理中的全文 = 处理中的全文.encode("utf-8").decode("latin1")
        #
        处理中的全文 = re.sub(r'<td.*?>', '<p>', 处理中的全文).replace("</td>", '</p>')
        处理中的全文 = re.sub(r'<aname=.*?>', '', 处理中的全文).replace("</a>", '')
        处理中的全文 = re.sub(r'\u3000', '', 处理中的全文)
        return 处理中的全文
    # 处理标题
    def disposeTitle(self,content):
            处理中的全文 = content
            title = re.findall(re.compile(r'<p>.*?[监 罚 处 环  局].*?\d号</p>'), 处理中的全文)
            行政处罚决定书 = re.findall(re.compile(r'<p>行政处罚决定书</p>'), 处理中的全文)
            执法局 = r'<p>[\u4E00-\u9FA5\uF900-\uFA2D]+[\局 ,\协会,\厅]</p>'
            执法局 = re.findall(re.compile(执法局), 处理中的全文)
            if title != []:
                ti = 处理中的全文.find(title[-1])
                if ti < 100 and len(title[-1]) < 20:
                    title[0] = title[0].replace("<p>", '').replace("</p>", '')
                    处理中的全文 = 处理中的全文.replace(title[0], ''.join(['<p style="text-align: center;">' + title[-1] + '</p>']))
            if 行政处罚决定书 !=[]:
                ti1 = 处理中的全文.find(行政处罚决定书[-1])
                if ti1 < 100 and len(行政处罚决定书[-1]) < 20:
                    行政处罚决定书[0] = 行政处罚决定书[0].replace("<p>", '').replace("</p>", '')
                    处理中的全文 = 处理中的全文.replace(行政处罚决定书[0], ''.join(['<p style="text-align: center;">' + 行政处罚决定书[-1] + '</p>']))
            if len(执法局) != 0:
                find1 = 处理中的全文.find(执法局[-1])
                if find1 > 100 and len(执法局[-1]) < 20:
                    执法局[-1] = 执法局[-1].replace("<p>", '').replace("</p>", '')
                    处理中的全文 = 处理中的全文.replace(执法局[-1], ''.join(['<p style="text-align: center;">' + 执法局[-1] + '</p>']))
                else:
                    pass


            # 这组是处理落款时间的格式
            yy = r'<p>\s*[ 零 ○ 0 O o 〇 Ｏ 一 二 三 四 五 六 七 八 九 十]{4}年[一 二 三 四 五 六 七 八 九 十 〇]{1,2}月[一 二 三 四 五 六 七 八 九 十 〇]{1,2}日\s*</p>|<p>\s*\d{4}年\d{1,2}月\d{1,2}日</p>'
            str2 = re.findall(re.compile(yy), 处理中的全文)
            print("找到的结果" + str(str2))
            if len(str2) != 0:
                find1 = 处理中的全文.find(str2[-1])
                if find1 > 100 and len(str2[-1]) < 20:
                    str2[-1] = str2[-1].replace("<p>", '').replace("</p>", '')
                    print("str2[-1]" + str2[-1])
                    rss = re.split('[年 月 日]', str2[-1])
                    print(rss)

                    time1 = ['零', '○', '0', 'O', 'o', '〇', 'Ｏ', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
                    time2 = ['0', '0', '0', '0', '0', '0', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' 10']
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
                        print("中文时间" + str2[-1])
                        # 如果存在落款时间就加上个<p style="text-align: right;"> 让它居右显示
                        print("noe" + str2[-1])
                        if Time1:
                            处理中的全文 = 处理中的全文.replace(str2[-1], ''.join(['<p style="text-align: right;">' + Time1 + '</p>']))
                    else:
                        处理中的全文 = 处理中的全文.replace(str2[-1], ''.join(['<p style="text-align: right;">' + str2[-1] + '</p>']))
            return  处理中的全文
    # 处理落款格式
    def disposeInscriber(self,content):
        处理中的全文 = content
        yy2 = r'<p>[\u4E00-\u9FA5\uF900-\uFA2D]+[\局 ,\协会,\厅]</p>'
        rs = re.findall(re.compile(yy2), 处理中的全文)
        if len(rs) != 0:
            find1 = 处理中的全文.find(rs[-1])
            if find1 > 100 and len(rs[-1]) < 20:
                rs[-1] = rs[-1].replace("<p>", '').replace("</p>", '')
                处理中的全文 = 处理中的全文.replace(rs[-1], ''.join(['<p style="text-align: right;">' + rs[-1] + '</p>']))
            else:
                pass
        else:
            pass
        return 处理中的全文

if __name__ =="__main__":
    AdminiStrative = Utils()
    AdminiStrative.dispose()







