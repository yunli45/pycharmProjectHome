# coding:utf-8
import re
import openpyxl



str1= """
       <p><p style="TEXT-ALIGN: center; LINE-HEIGHT: 150%"><strong><span style="LINE-HEIGHT: 150%; FONT-FAMILY: 宋体; FONT-SIZE: 29px">玉环县国家税务局稽查局</span></strong></p><h1 style="TEXT-ALIGN: center; LINE-HEIGHT: normal"><a name="_Toc298937935"></a><span style="FONT-FAMILY: 宋体; FONT-SIZE: 35px">税务行政处罚决定书</span></h1><p style="TEXT-ALIGN: center; LINE-HEIGHT: 33px; TEXT-INDENT: 43px"><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">玉国税稽罚〔2015〕86号</span></p><p><span style="TEXT-DECORATION: underline"><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">浙江维拉利家具有限公司</span></span><span style="TEXT-DECORATION: underline"><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">：</span></span><span style="TEXT-DECORATION: underline"><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">（</span></span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">纳税人识别号：</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">331021770742916</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">）</span></p><p style="LINE-HEIGHT: 150%"><span style="LINE-HEIGHT: 150%; FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">&nbsp;&nbsp;&nbsp;&nbsp; </span><span style="LINE-HEIGHT: 150%; FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">我局于</span><span style="LINE-HEIGHT: 150%; FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">2015</span><span style="LINE-HEIGHT: 150%; FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">年6月17日</span><span style="LINE-HEIGHT: 150%; FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">至2015年8月10日对你单位2013年1月1日至2014年12月31日</span><span style="LINE-HEIGHT: 150%; FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">期间的纳税</span><span style="LINE-HEIGHT: 150%; FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">情况进行了检查，违法事实及处罚决定如下：</span></p><p style="LINE-HEIGHT: 150%; TEXT-INDENT: 43px"><span style="LINE-HEIGHT: 150%; FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">一、违法事实</span></p><p style="LINE-HEIGHT: 35px; TEXT-INDENT: 43px"><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">经查你单位</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">2013</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">年1月至2014年12月期间：</span></p><p style="TEXT-INDENT: 53px"><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">1</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">、2013年1月至12月份期间，销售货物取得<span style="COLOR: black">应税销售收入</span></span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">95811.98</span><span style="FONT-FAMILY: 仿宋_GB2312; COLOR: black; FONT-SIZE: 21px">元，未入账未申报纳税：</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">造成少缴增值税16288.02元；应调增2013年度应纳税所得额95811.98元</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">。</span></p><p style="TEXT-INDENT: 53px"><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">2</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">、2014年1月至12月份期间，销售货物取得<span style="COLOR: black">应税销售收入</span></span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">122222.24</span><span style="FONT-FAMILY: 仿宋_GB2312; COLOR: black; FONT-SIZE: 21px">元，未入账未申报纳税：</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">造成少缴增值税20777.76元；应调增2014年度应纳税所得额122222.24</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">元。</span></p><p style="TEXT-INDENT: 53px"><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">3</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">、</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">2014</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">年10月份向客户无偿赠送外购的月饼计金额9,204.33元，未作视同销售申报纳税：造成少缴增值税1564.72元；应调减2014年度应纳税所得额1564.72</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">元</span></p><p style="TEXT-INDENT: 53px"><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">以上共计：应补增值税38630.50元；应调增2013年度应纳税所得额95811.98</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">元，应补2013年度企业所得税</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">23953.00</span><span style="FONT-FAMILY: 仿宋_GB2312; COLOR: black; FONT-SIZE: 21px">元</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">；</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">应调增2014年度应纳税所得额</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">120657.52</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">元，应补2014年度企业所得税</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">30164.38</span><span style="FONT-FAMILY: 仿宋_GB2312; COLOR: black; FONT-SIZE: 21px">元。</span></p><p style="LINE-HEIGHT: 32px; TEXT-INDENT: 43px"><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">二、处罚决定</span></p><p style="LINE-HEIGHT: 31px; TEXT-INDENT: 43px"><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">根据</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">《中华人民共和国税收征收管理法》第六十三条</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">第一款</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">规定：你单位取得</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">应税销售收入及视同销售未申报纳税</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">，</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">造成少缴</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">增值税38630.50元</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">的行为属偷税，处少缴增值税款金额的百分之六十的罚款，</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">计金额</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">23178.30</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">元；你单位取得</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">营业收入未申报纳税</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">，</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">造成少缴</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">企业所得税54117.38<span style="COLOR: black">元</span>的行为属偷税，处少缴企业所得税款金额的百分之六十的罚款，</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">计金额</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">32470.43</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">元。</span></p><p style="LINE-HEIGHT: 37px; TEXT-INDENT: 43px"><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">以上应缴款项共计</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">55648.73</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">元，限你单位自本决定书送达之日起</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">十五</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">日内到</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">玉环县国家税务局稽查局</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">缴纳入库。到期不缴纳罚款，我局将依照《中华人民共和国行政处罚法》第五十一条第（一）项规定，每日按罚款数额的百分之三加处罚款。</span></p><p style="TEXT-INDENT: 43px"><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">如对本决定不服，可以自收到本决定书之日起六十日内依法向</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">玉环县国家税务局</span><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">申请行政复议，或者自收到本决定书之日起六个月内依法向人民法院起诉。如对处罚决定逾期不申请复议也不向人民法院起诉、又不履行的，我局将采取《中华人民共和国税收征收管理法》第四十条规定的强制执行措施，或者申请人民法院强制执行。</span></p><p style="TEXT-INDENT: 43px"><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; </span></p><p style="TEXT-INDENT: 43px"><span style="FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">&nbsp;</span></p><p style="LINE-HEIGHT: 150%"><span style="LINE-HEIGHT: 150%; FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">&nbsp;</span></p><p style="LINE-HEIGHT: 150%"><span style="LINE-HEIGHT: 150%; FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; </span><span style="LINE-HEIGHT: 150%; FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">二</span><span style="LINE-HEIGHT: 150%; FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">○</span><span style="LINE-HEIGHT: 150%; FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">一五年十月二十<span style="DISPLAY: none">二</span></span><span style="LINE-HEIGHT: 150%; FONT-FAMILY: 仿宋_GB2312; FONT-SIZE: 21px">日</span></p><p></p></p>      

"""
rs = re.findall(
    re.compile(r'>二.*?○.*?[○ 0 O o 〇 Ｏ 一 二 三 四 五 六 七 八 九 十 ]{2}.*?年[〇 一 二 三 四 五 六 七 八 九 十]{1,2}月'),
    str(str1))
# rs = re.findall(re.compile(r'[〇 一 二 三 四 五 六 七 八 九 十]{1,2}月'),str1)
# print(type(rowK_va))
print(rs)
if rs != []:
    startIndex = str1.find(rs[0])
    endIndex = startIndex + len(rs[0])
    print(str(startIndex))
    rs = rs[0]
    if rs.find("年") and rs.find("月") and rs.find("日"):
        rss = re.split('[年 月 日]', rs)
        print(rss[0])
        time1 = ['○','0', 'O', 'o', '〇', 'Ｏ', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
        time2 = ['0','0', '0', '0', '0', '0' ,'1', '2', '3', '4', '5', '6', '7', '8', '9', ' 10']
        YearList = []
        MonthList = []
        DayList = []
        print(len(rss[0]))
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
            if len(Moth) >2 :
                Moth = Moth[0] + Moth[-1]
            if len(Day) >2:
                Day = Day[0] + Day[-1]
            Result = Year + "年" + Moth + "月" + Day + "日"
            print(Result)

else:
    pass





