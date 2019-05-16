import re
import openpyxl



rs = re.findall(re.compile(r'[〇 一 二 三 四 五 六 七 八 九 十]{4,5}年[〇 一 二 三 四 五 六 七 八 九 十]{1,2}月[〇 一 二 三 四 五 六 七 八 九 十]{1,3}日'),str1)
# rs = re.findall(re.compile(r'[〇 一 二 三 四 五 六 七 八 九 十]{1,2}月'),str1)
rs = rs[0]
if rs.find("年") and rs.find("月") and rs.find("日"):
    rss = re.split('[年 月 日]',rs)
    time1 = ['〇', '一', '二', '三', '四', '五', '六', '七', '八', '九', ' 十']
    time2= ['0','1' ,'2','3' ,'4' ,'5','6','7' ,'8' , '9' ,' 10']
    YearList = []
    MonthList = []
    DayList = []
    if len(rss[0]) == 4:

        for y in rss[0]:
            if y in time1:
                index = time1.index(y)
                yy = time2[index]
                YearList.append(yy)
        # print(YearList)

        if len(rss[1])<=2:
            for m in rss[1]:
                if m in time1:
                    index1 = time1.index(m)
                    mm = time2[index1]
                    MonthList.append(mm)
        # print(MonthList)
        elif 2< len(rss[1])<=3:
            for m in rss[1]:
                if m in time1:
                    index1 = time1.index(m)
                    mm = time2[index1]
                    MonthList.append(mm)

        if len(rss[2])<=2:
            for d in rss[1]:
                if d in time1:
                    index1 = time1.index(d)
                    dd = time2[index1]
                    DayList.append(dd)
        elif 2< len(rss[2])<=3:
            for d in rss[2]:
                if d in time1:
                    index1 = time1.index(d)
                    dd = time2[index1]
                    DayList.append(dd)
    # print(YearList)
    if   YearList !=[] and MonthList !=[] and DayList!=[]:
        print("yes")
        Year = ''.join(str(i) for i in YearList)
        if len(MonthList)<=2:
            Moth = ''.join(str(i) for i in MonthList)
        elif  len(MonthList) == 3:
            MonthList  =  MonthList[0] + MonthList[-1]
            Moth = ''.join(str(i) for i in MonthList)
        if len(DayList) <=2:
            Day = ''.join(str(i) for i in DayList)
        elif len(DayList) ==3:
            DayList = DayList[0] + DayList[-1]
            Day = ''.join(str(i) for i in DayList)
        Result = Year+"年"+Moth+"月"+Day+"日"

        print(Result)














