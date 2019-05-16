# coding:gb18030
import pymssql
import re
import  time
from bs4 import BeautifulSoup

start = time.clock( )
#数据库连接
conn=pymssql.connect(host='192.168.31.124\SQLEXPRESS',user='sa',password='123qwe!@#',database='cnlaw2.0')
#打开游标
cur=conn.cursor();
if not cur:
    raise Exception('数据库连接失败！')
else:
    print("数据库链接成功")

sql = 'select *  from 财政数据19157篇1 '

#执行sql，获取所有数据
cur.execute(sql)

# Python查询Mysql/SQL SERVER 使用 fetchone() 方法获取单条数据, 使用fetchall() 方法获取多条数据。
# 返回的数据集是一个列表，但是其中的元素是一个元组，每个元组包含一条数据库中的数据
rs = cur.fetchall()
# rs1 = list(rs)
j = 0
for i in rs:
    print(i)
    txt = str(i[7])
    # print(txt)
    j+=1
    # print('这是第' + str(j) + '条数据' + txt.encode('latin-1').decode('gbk'))
    # print(i[20])
    # 这一组是去除<span> ....</span>  <SPAN> ....</SPAN>
    str1 = re.sub(r'<span .*?>', '', txt,flags=re.I).replace('</span>', '').replace('</SPAN>', '')

    # 这一组是去除<FONT> ....</FONT>
    str1 = re.sub(r'<FONT .*?>', '', str1,flags=re.I).replace('</FONT>', '').replace('</font>', '')

    # 这一组是去除<p style="text-align:center;line-height:38px">...</p>
    str1 = re.sub(r'<p .*?>', '<p>', str1)
    # # 这一组是去除<P style="text-align:center;line-height:38px">...</P>
    str1 = re.sub(r'<P .*?>', '<p>', str1)
    str1 = re.sub(r'</P>', '</p>', str1)

    # # 这一组是去除<img width=  ..... #ddd"/>
    # str1 = re.sub(r'<img .*? solid #ddd"/>', '', str1)

    # 这一组是去除<?xml:namespace prefix = o ns = "urn:schemas-microsoft-com:office:office" /><o:p></o:p>
    str1 = re.sub(r'<?xml:namespace .*?>', '', str1)
    str1 = str1.replace('<o:p></o:p>', '').replace('<o:p>','').replace('</o:p>','')

    # 这一组是去除<<strong>> ....</<strong>>
    str1 = re.sub(r'<strong.*?>', '', str1, flags=re.I).replace('</strong>', '')

    # <st1:chsdate year="2017" month="3" day="30" islunardate="False" isrocdate="False" w:st="on">...</st1:chsdate>
    str1 = re.sub(r'<st1:chsdate .*?>','',str1)
    str1 = re.sub(r'</st1:chsdate>','',str1)
    # print('这是第' + str(j) + '条数据' + str1.encode('latin-1').decode('gbk'))

    # 这组是替换掉去开头<p><p> =><p>
    str1 = str1.replace(r'<p><p>', '<p>')

    # 这组是 替换掉<br> 为</p><p>
    str1 = str1.replace('<br>', '</p><p>').replace('</br>', '</p><p>').replace('<br/>','</p><p>')
    str1 = str1.replace('<BR>', '</p><p>').replace('</BR>', '</p><p>')


    # 这组是处理<p></p>这种无用标签和所有的&nbsp;
    str1 = re.sub(r'&nbsp;', '', str1)
    str1 = re.sub(r'<p></p>', '', str1)
    # 设置编码，python3
    # str1 = str1.encode('latin-1').decode('gbk')
    # str1 = str1.encode("utf-8").decode("latin1")


    # 这组是处理落款时间的格式
    yy = r'[ 零 ○ 0 O o 〇 Ｏ 一 二 三 四 五 六 七 八 九 十]{4}年[一 二 三 四 五 六 七 八 九 十 〇]{1,2}月[一 二 三 四 五 六 七 八 九 十 〇]{1,2}日\s*</p>|<p>\s*\d{4}年\d{1,2}月\d{1,2}日'
    str2 = re.findall(re.compile(yy), str1)
    if len(str2) != 0:
        find1 = str1.find(str2[-1])
        if find1 > 100:
            # 如果存在落款时间就加上个<p style="text-align: right;"> 让它居右显示
            str1 = str1.replace(str2[-1], ''.join(['<p style="text-align: right;">', str2[-1], '</p>']))
        else:
            pass
    else:
        pass

    # 这组是处理落款单位



    yy2 = r'[\u4E00-\u9FA5\uF900-\uFA2D]+[\局 ,\协会]'
    rs = re.findall(re.compile(yy2), str1)
    if len(rs) != 0 :
        find1 = str1.find(rs[-1])
        if find1 > 100:
            str1 = str1.replace(rs[-1], ''.join(['<p style="text-align: right;">' + rs[-1] + '</p>']))
        else:
            pass

    else:
        pass

    # 处理多出来的</p><p><p style="text-align: right;">
    str1 = re.sub(r'</p><p><p style="text-align: right;">','</p><p style="text-align: right;">',str1)
    str1 = re.sub(r'</p></p><p>','</p>',str1)
    str1 = re.sub(r'</p></p></p>','</p>',str1)
    str1 = str1.encode('latin-1').decode('gbk')

    # 全文update 这个字段插入时也会乱码，必须先转码如下
    str2 = str(i[17])
    str2 = str2.encode('latin-1').decode('gbk')


    # 插入到数据库中去 因为源表中的：文章字数量 i(int)[11]、isDelete(int) i[20] 、updateDate(nvarchar(50)) i[21] 字段允许为空(NULL)python读取后为None针对i[11] 和i[20] ，会报错能将None转化为varchar
    # 所以加个判断当这三个的值None即数据库中为NULL时直接不插入到新表

    if  i[20] or i[21]==None :
        sql2 = "INSERT INTO  财政数据19157篇(ID,标题,处罚文号,被处罚主体,法人,执法部门,处罚日期,全文,唯一标志,区域,机构,文章字数量,区域news,机构news,区域news1,处罚对象,state,全文update,标题update,UserName,packid) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
               % (i[0], i[1], i[2], i[3], i[4], i[5], i[6], str1, i[8], i[9], i[10],i[11], i[12], i[13], i[14], i[15], i[16],str2, i[18], i[19])
    else:
        sql2 = "INSERT INTO  table6(ID,标题,行政处罚决定书文号,[被处罚单位（被处罚人）],[法定代表人（或单位负责人）],执法部门,作出行政处罚的日期,全文,唯一标志,区域,机构,文章字数量,区域news,机构news,区域news1,处罚对象,state,全文update,标题update,UserName,isDelete,updateDate) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (i[0], i[1], i[2], i[3], i[4], i[5], i[6], str1, i[8], i[9], i[10], i[11], i[12], i[13], i[14], i[15], i[16],str2, i[18], i[19],i[20],i[21])
#     cur.execute(sql2)
# conn.commit()
# conn.close()
end = time.clock( )
print(str(end-start))






