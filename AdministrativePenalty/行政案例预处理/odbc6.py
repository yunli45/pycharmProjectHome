# coding:gb18030
import pymssql
import re
import  time
from bs4 import BeautifulSoup

start = time.clock( )
#���ݿ�����
conn=pymssql.connect(host='192.168.31.124\SQLEXPRESS',user='sa',password='123qwe!@#',database='cnlaw2.0')
#���α�
cur=conn.cursor();
if not cur:
    raise Exception('���ݿ�����ʧ�ܣ�')
else:
    print("���ݿ����ӳɹ�")

sql = 'select *  from ��������19157ƪ1 '

#ִ��sql����ȡ��������
cur.execute(sql)

# Python��ѯMysql/SQL SERVER ʹ�� fetchone() ������ȡ��������, ʹ��fetchall() ������ȡ�������ݡ�
# ���ص����ݼ���һ���б��������е�Ԫ����һ��Ԫ�飬ÿ��Ԫ�����һ�����ݿ��е�����
rs = cur.fetchall()
# rs1 = list(rs)
j = 0
for i in rs:
    print(i)
    txt = str(i[7])
    # print(txt)
    j+=1
    # print('���ǵ�' + str(j) + '������' + txt.encode('latin-1').decode('gbk'))
    # print(i[20])
    # ��һ����ȥ��<span> ....</span>  <SPAN> ....</SPAN>
    str1 = re.sub(r'<span .*?>', '', txt,flags=re.I).replace('</span>', '').replace('</SPAN>', '')

    # ��һ����ȥ��<FONT> ....</FONT>
    str1 = re.sub(r'<FONT .*?>', '', str1,flags=re.I).replace('</FONT>', '').replace('</font>', '')

    # ��һ����ȥ��<p style="text-align:center;line-height:38px">...</p>
    str1 = re.sub(r'<p .*?>', '<p>', str1)
    # # ��һ����ȥ��<P style="text-align:center;line-height:38px">...</P>
    str1 = re.sub(r'<P .*?>', '<p>', str1)
    str1 = re.sub(r'</P>', '</p>', str1)

    # # ��һ����ȥ��<img width=  ..... #ddd"/>
    # str1 = re.sub(r'<img .*? solid #ddd"/>', '', str1)

    # ��һ����ȥ��<?xml:namespace prefix = o ns = "urn:schemas-microsoft-com:office:office" /><o:p></o:p>
    str1 = re.sub(r'<?xml:namespace .*?>', '', str1)
    str1 = str1.replace('<o:p></o:p>', '').replace('<o:p>','').replace('</o:p>','')

    # ��һ����ȥ��<<strong>> ....</<strong>>
    str1 = re.sub(r'<strong.*?>', '', str1, flags=re.I).replace('</strong>', '')

    # <st1:chsdate year="2017" month="3" day="30" islunardate="False" isrocdate="False" w:st="on">...</st1:chsdate>
    str1 = re.sub(r'<st1:chsdate .*?>','',str1)
    str1 = re.sub(r'</st1:chsdate>','',str1)
    # print('���ǵ�' + str(j) + '������' + str1.encode('latin-1').decode('gbk'))

    # �������滻��ȥ��ͷ<p><p> =><p>
    str1 = str1.replace(r'<p><p>', '<p>')

    # ������ �滻��<br> Ϊ</p><p>
    str1 = str1.replace('<br>', '</p><p>').replace('</br>', '</p><p>').replace('<br/>','</p><p>')
    str1 = str1.replace('<BR>', '</p><p>').replace('</BR>', '</p><p>')


    # �����Ǵ���<p></p>�������ñ�ǩ�����е�&nbsp;
    str1 = re.sub(r'&nbsp;', '', str1)
    str1 = re.sub(r'<p></p>', '', str1)
    # ���ñ��룬python3
    # str1 = str1.encode('latin-1').decode('gbk')
    # str1 = str1.encode("utf-8").decode("latin1")


    # �����Ǵ������ʱ��ĸ�ʽ
    yy = r'[ �� �� 0 O o �� �� һ �� �� �� �� �� �� �� �� ʮ]{4}��[һ �� �� �� �� �� �� �� �� ʮ ��]{1,2}��[һ �� �� �� �� �� �� �� �� ʮ ��]{1,2}��\s*</p>|<p>\s*\d{4}��\d{1,2}��\d{1,2}��'
    str2 = re.findall(re.compile(yy), str1)
    if len(str2) != 0:
        find1 = str1.find(str2[-1])
        if find1 > 100:
            # ����������ʱ��ͼ��ϸ�<p style="text-align: right;"> ����������ʾ
            str1 = str1.replace(str2[-1], ''.join(['<p style="text-align: right;">', str2[-1], '</p>']))
        else:
            pass
    else:
        pass

    # �����Ǵ�����λ



    yy2 = r'[\u4E00-\u9FA5\uF900-\uFA2D]+[\�� ,\Э��]'
    rs = re.findall(re.compile(yy2), str1)
    if len(rs) != 0 :
        find1 = str1.find(rs[-1])
        if find1 > 100:
            str1 = str1.replace(rs[-1], ''.join(['<p style="text-align: right;">' + rs[-1] + '</p>']))
        else:
            pass

    else:
        pass

    # ����������</p><p><p style="text-align: right;">
    str1 = re.sub(r'</p><p><p style="text-align: right;">','</p><p style="text-align: right;">',str1)
    str1 = re.sub(r'</p></p><p>','</p>',str1)
    str1 = re.sub(r'</p></p></p>','</p>',str1)
    str1 = str1.encode('latin-1').decode('gbk')

    # ȫ��update ����ֶβ���ʱҲ�����룬������ת������
    str2 = str(i[17])
    str2 = str2.encode('latin-1').decode('gbk')


    # ���뵽���ݿ���ȥ ��ΪԴ���еģ����������� i(int)[11]��isDelete(int) i[20] ��updateDate(nvarchar(50)) i[21] �ֶ�����Ϊ��(NULL)python��ȡ��ΪNone���i[11] ��i[20] ���ᱨ���ܽ�Noneת��Ϊvarchar
    # ���ԼӸ��жϵ���������ֵNone�����ݿ���ΪNULLʱֱ�Ӳ����뵽�±�

    if  i[20] or i[21]==None :
        sql2 = "INSERT INTO  ��������19157ƪ(ID,����,�����ĺ�,����������,����,ִ������,��������,ȫ��,Ψһ��־,����,����,����������,����news,����news,����news1,��������,state,ȫ��update,����update,UserName,packid) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
               % (i[0], i[1], i[2], i[3], i[4], i[5], i[6], str1, i[8], i[9], i[10],i[11], i[12], i[13], i[14], i[15], i[16],str2, i[18], i[19])
    else:
        sql2 = "INSERT INTO  table6(ID,����,���������������ĺ�,[��������λ���������ˣ�],[���������ˣ���λ�����ˣ�],ִ������,������������������,ȫ��,Ψһ��־,����,����,����������,����news,����news,����news1,��������,state,ȫ��update,����update,UserName,isDelete,updateDate) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (i[0], i[1], i[2], i[3], i[4], i[5], i[6], str1, i[8], i[9], i[10], i[11], i[12], i[13], i[14], i[15], i[16],str2, i[18], i[19],i[20],i[21])
#     cur.execute(sql2)
# conn.commit()
# conn.close()
end = time.clock( )
print(str(end-start))






