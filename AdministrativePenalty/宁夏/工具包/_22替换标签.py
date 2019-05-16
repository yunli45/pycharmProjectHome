import re


#  在取出全文后提前去掉一部分不需要的标签，如果存在表格计算出去掉表格前后p标签的个数，用来判断全文的类型（3种）：是否含有表格 全文是一个表格、全文没有表格、全文包含表格(因为这种类型表格中的内容在全文已经包含了，所以在处理的时候会提前去掉表格)
#  返回去除掉部分标签的全文、返回去掉标签前原来的tr 和td的个数 、返回去掉表格前后p标签的个数
def replaceLable(ConetentResponseSoupOld):
    ConetentResponseSoupOld = re.sub("<strong.*?>", '', str(ConetentResponseSoupOld)).replace("</strong>", '')
    ConetentResponseSoupOld = re.sub("<u.*?>", '', ConetentResponseSoupOld, flags=re.S | re.M).replace("</u>",
                                                                                                       '')
    ConetentResponseSoupOld = re.sub("<b.*?>", '', ConetentResponseSoupOld, flags=re.S | re.M).replace("</b>",
                                                                                                       '')
    # <tr class="firstRow"
    ConetentResponseSoupOld = re.sub('<tr class="firstRow".*?>.*?</tr>','',ConetentResponseSoupOld, flags=re.S | re.M)
    ConetentResponseSoupOld  =re.sub('<tr.*?>.*?<td.*?>序号.*?</tr>','',ConetentResponseSoupOld, flags=re.S | re.M)



    ConetentResponseSoupOld = re.sub('<p.*?>','<p>',ConetentResponseSoupOld, flags=re.S | re.M)
    ConetentResponseSoupOld = re.sub('<span.*?>', '', ConetentResponseSoupOld, flags=re.S | re.M).replace(
        '</span>', '').replace(r'<a name="TCSignMonth"></a>', '').replace('<a name="TCSignDay"></a>', '')
    ConetentResponseSoupOld = re.sub('<div class="suspension">.*?</div>','',ConetentResponseSoupOld,flags=re.S | re.M)
    ConetentResponseSoupOld = re.sub('<div class="userControl">.*?</div>','',ConetentResponseSoupOld,flags=re.S | re.M)
    ConetentResponseSoupOld = re.sub('<div class="copy">.*?</div>','',ConetentResponseSoupOld, flags=re.S | re.M)
    ConetentResponseSoupOld = re.sub('<div class="others">.*?</div>','',ConetentResponseSoupOld, flags=re.S | re.M)
    ConetentResponseSoupOld = re.sub('<div class="bdsharebuttonbox">.*?</div>','',ConetentResponseSoupOld, flags=re.S | re.M)
    ConetentResponseSoupOld = re.sub('<div class="footerNav">.*?</div>','',ConetentResponseSoupOld, flags=re.S | re.M)
    ConetentResponseSoupOld = re.sub('<div id="footer">.*?</div>','',ConetentResponseSoupOld, flags=re.S | re.M)
    ConetentResponseSoupOld = re.sub('<script.*?>.*?</script>','',ConetentResponseSoupOld, flags=re.S | re.M)
    ConetentResponseSoupOld = re.sub('<a class="a".*?title="打印文章">【打印文章】</a>','',ConetentResponseSoupOld)
    ConetentResponseSoupOld = re.sub('<center></center></td>.*?</div>','',ConetentResponseSoupOld, flags=re.S | re.M)
    ConetentResponseSoupOld = re.sub('<v:line.*?>','',ConetentResponseSoupOld, flags=re.S | re.M).replace("</v:line>",'').replace("<p><?</p>",'').replace("<p></p>",'').replace("<p> </p>",'')
    # ConetentResponseSoupOld = ConetentResponseSoupOld.replace(" ",'')

    ConetentResponseSoupOld = str(ConetentResponseSoupOld)

    from bs4 import BeautifulSoup
    ContentNum = BeautifulSoup(str(ConetentResponseSoupOld), 'lxml')
    ContentTrNum = len(ContentNum.findAll('tr'))
    ContentTdNum = len(ContentNum.findAll('td'))
    ContentPNum = len(ContentNum.findAll('p'))

    print("这条数据原来有：" + str(ContentPNum) + "个P")
    print("这条数据原来一共有：" + str(ContentTrNum) + "个tr")
    print("这条数据原来一共有：" + str(ContentTdNum) + "个td")
    # 先尝试着找到到table，如果存在就删除再去找p标签的个数,
    if ConetentResponseSoupOld.find("<table") != -1:
        ConetentResponseSoupOld1 = re.sub('<table.*?>.*?</table>', '', ConetentResponseSoupOld,
                                          flags=re.S | re.M)
    else:
        ConetentResponseSoupOld1 = ConetentResponseSoupOld

    ContentNum1 = BeautifulSoup(str(ConetentResponseSoupOld1), 'lxml')
    ContentPNum1 = len(ContentNum1.findAll('p'))
    print("这条数据去掉表格后有：" + str(ContentPNum1) + "个P")
    print("这条数据去掉表格后的全文"+ConetentResponseSoupOld1)
    ConetentResponseTable = re.sub('<span.*?>', '', str(ConetentResponseSoupOld)).replace('</span>', '')
    ConetentResponseTable = re.sub('<p.*?>', '<p>', str(ConetentResponseTable))
    ConetentResponseTable = re.sub('<font.*?>', '', str(ConetentResponseTable)).replace('</font>', '')

    # 替换标签
    ConetentResponseTable = re.sub('<col.*?>', '', ConetentResponseTable).replace('</colgroup>', '')
    ConetentResponseTable = re.sub('<td.*?>', '<td>', ConetentResponseTable)
    ConetentResponseSoupOld = re.sub('<tr.*?>', '<tr>', ConetentResponseTable).replace("<td><td>", "<td>").replace("<o:p>",'').replace("</o:p>",'')
    ConetentResponseSoupOld = re.sub(r'\xa0','',ConetentResponseSoupOld).replace("<p></p>",'').replace("<p><!--EndFragment--></p>",'')
    # <?xml:namespaceprefix =ons="urn:schemas-microsoft-com:office:office"/>
    ConetentResponseSoupOld = re.sub('<?xml:name.*?>','',ConetentResponseSoupOld).replace("<v:linefrom>",'').replace("</v:linefrom>",'')
    print("除去和替换部分标签后的原来的全文："+ConetentResponseSoupOld)

    return ConetentResponseSoupOld,ContentTrNum,ContentTdNum,ContentPNum,ContentPNum1


# 全文类型为全文没有表格、全文包含表格的时候，去掉这些标签。全文是一个表格的时候所有字段内容均在表格中取
def  replaceLableNow(ConetentResponseSoupOld):
    # print("333")
    # print(ConetentResponseSoupOld)
    ConetentResponse = re.sub('<table.*?>.*?</table>','',ConetentResponseSoupOld,flags=re.S|re.M)
    ConetentResponse = re.sub(r'<p.*?><o:p> </o:p></p>', '', str(ConetentResponse)).replace('<o:p></o:p>', '')
    ConetentResponse = re.sub(r'<st1:.*?>', '', str(ConetentResponse)).replace('</st1:chsdate>', '').replace(
        '<a name="TCSignYear"></a>', '')
    ConetentResponse = re.sub(r'<o:p>\xa0</o:p>', '', str(ConetentResponse))
    ConetentResponse = re.sub(r'<p.*?>', '<p>', str(ConetentResponse), flags=re.S | re.M)
    ConetentResponse = ConetentResponse.replace("'", "''").replace('<b>', '').replace('</b>', '').replace(
        "2312>'，", '')
    # print("修改后i的全文")
    return  ConetentResponse