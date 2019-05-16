#  coding:utf-8
from bs4 import BeautifulSoup
import  re
import requests
str1 = """<divclass="news_content">
<p> </p><pstyle="TEXT-ALIGN:center;LINE-HEIGHT:39px">天津市市场和质量监督管理</p><pstyle="TEXT-ALIGN:center;LINE-HEIGHT:39px">行政处罚决定书</p><pstyle="TEXT-ALIGN:right;LINE-HEIGHT:13px"> </p><pstyle="TEXT-ALIGN:center;LINE-HEIGHT:29px;MARGIN:0px2px0px0px">津市场监管青竞罚〔2018〕17号</p><pstyle="TEXT-ALIGN:center;LINE-HEIGHT:37px"> </p><pstyle="LINE-HEIGHT:37px;TEXT-INDENT:43px">当事人姓名或者单位名称:天津市西青区金福家乐食品店（黄子强）</p><pstyle="LINE-HEIGHT:37px;TEXT-INDENT:43px">主体资格证件名称及号码:营业执照120111600435901</p><pstyle="LINE-HEIGHT:37px;TEXT-INDENT:43px">住所(经营场所)或者住址:天津市西青区赤龙南街佳和康庭12号楼101配建</p><pstyle="LINE-HEIGHT:37px;TEXT-INDENT:43px">法定代表人（负 责 人）:黄子强</p><pstyle="LINE-HEIGHT:37px;TEXT-INDENT:43px">违法事实：当事人自2017年5月在未经当地烟草专卖部门核准登记的情况下，在天津市西青区赤龙南街佳和康庭12号楼101配建从事烟草制品零售活动 。当事人共收购红梅等8个品牌9种规格35条卷烟用于销售，至查处之日止尚未销售出烟草制品。当事人的经营额为2051.94元，没有违法所得。  </p><pstyle="LINE-HEIGHT:37px;TEXT-INDENT:43px">主要证据：</p><pstyle="LINE-HEIGHT:37px;TEXT-INDENT:43px">1、西青区烟草专卖局案件移送函一份；</p><pstyle="LINE-HEIGHT:37px;TEXT-INDENT:43px">2、西青区烟草专卖局移送财务清单一份；</p><pstyle="LINE-HEIGHT:37px;TEXT-INDENT:43px">3、西青区烟草专卖局检查（勘验）笔录复印件一份；</p><pstyle="LINE-HEIGHT:37px;TEXT-INDENT:43px">4、西青区烟草专卖局询问笔录复印件一份；</p><pstyle="LINE-HEIGHT:37px;TEXT-INDENT:43px">5、现场照片两张；</p><pstyle="LINE-HEIGHT:37px;TEXT-INDENT:43px">6、天津市烟草公司西青分公司出具的涉烟案件违法卷烟价格认定意见书一份，证明涉案烟草制品的价格；</p><pstyle="LINE-HEIGHT:37px;TEXT-INDENT:43px">7、2018年4月25日对当事人的询问笔录1份，共2页，证明当事人无证零售烟草制品的事实和经营情况；</p><pstyle="LINE-HEIGHT:37px;TEXT-INDENT:43px">8、当事人的身份证复印件及营业执照复印件各1份，证明当事人的身份情况及主体资格。</p><pstyle="LINE-HEIGHT:37px;TEXT-INDENT:43px">以上证据和笔录均由当事人签名或案源提供者盖章认可。</p><pstyle="TEXT-ALIGN:left;LINE-HEIGHT:37px;TEXT-INDENT:36px;MARGIN:0px0px0px7px">对当事人陈述、申辩或者听证意见的采纳情况及理由：当事人在法定期限内未提出陈述申辩意见，也未要求举行听证。 </p><pstyle="LINE-HEIGHT:37px;TEXT-INDENT:43px">从轻、减轻、从重处罚的理由：当事人违法行为一般，没有《行政处罚法》和《天津市市场和质量监督管理委员会行政处罚裁量适用规则（试行）》规定的从轻、减轻、从重处罚的情形，选择适中处罚。</p><pstyle="LINE-HEIGHT:37px;TEXT-INDENT:43px">当事人的上述行为违反了《中华人民共和国烟草专卖法实施条例》第六条“从事烟草专卖品的生产、批发、零售业务，以及经营烟草专卖品进出口业务和经营外国烟草制品购销业务的，必须依照《烟草专卖法》和本条例的规定，申请领取烟草专卖许可证。”的规定，构成了无证从事烟草制品零售业务的违法行为。 </p><pstyle="LINE-HEIGHT:37px;TEXT-INDENT:43px">依据《中华人民共和国烟草专卖法实施条例》第五十七条“无烟草专卖零售许可证经营烟草制品零售业务的，由工商行政管理部门或者由工商行政管理部门根据烟草专卖行政主管部门的意见，责令停止经营烟草制品零售业务，没收违法所得，处以违法经营总额20％以上50％以下的罚款。”的规定，责令当事人停止经营烟草制品零售业务，并作出行政处罚如下：</p><pstyle="LINE-HEIGHT:37px;TEXT-INDENT:43px">罚款600元整。</p><pstyle="LINE-HEIGHT:37px;TEXT-INDENT:43px">当事人应当自收到本处罚决定书之日起十五日内将罚款交至市场和质量监督管理机关罚款代收机构（代收机构名称：中国工商银行天津西青支行，地址：天津市西青区杨柳青镇新华道77号）。逾期不缴纳罚款的，依据《中华人民共和国行政处罚法》第五十一条第一项的规定，每日按罚款数额的百分之三加处罚款，并将依法申请人民法院强制执行。</p><pstyle="LINE-HEIGHT:37px;TEXT-INDENT:43px">如不服本处罚决定，可自收到本处罚决定书之日起六十日内向天津市市场和质量监督管理委员会申请行政复议；也可以在六个月内依法向人民法院提起诉讼。当事人对处罚决定不服申请行政复议或者提起行政诉讼的，行政处罚不停止执行，法律另有规定的除外。</p><pstyle="LINE-HEIGHT:37px;TEXT-INDENT:43px">依据《企业信息公示暂行条例》等有关规定，本机关将通过市场主体信用信息公示系统、门户网站、专业网站等公示行政处罚信息。如公示的行政处罚信息不准确，当事人可以申请本机关予以更正。</p><pstyle="LINE-HEIGHT:37px;TEXT-INDENT:43px"> </p><pstyle="LINE-HEIGHT:37px;TEXT-INDENT:43px"> </p><pstyle="TEXT-ALIGN:right;LINE-HEIGHT:37px">天津市西青区市场和质量监督管理局   </p><pstyle="LINE-HEIGHT:37px;TEXT-INDENT:352px">                  2018年7月9日</p><p> </p><p> </p><p> </p>
</div>
"""
# # print(re.findall(re.compile(r'法定代表人（负责人）|（负 责 人）(.*?)<'),str1))
# # print(re.findall(re.compile(r'>(.*?[天]津市.*?局)'),str1))
# # print(re.findall(re.compile(r'>(.*?年.*?月.*?日)'),str1))
# # # print(re.findall(re.compile(r'<img src="(.*?)".*? title="(.*?)".*>'),str1))
# #
# url = "http://scjg.tj.gov.cn/binhaixinqu/zwgk/xzcfxx/28642.html"
# header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
# response = requests.get(url,headers = header)
# response = response.content.decode('UTF-8')
# # # print(response)
# homePageSoup = BeautifulSoup(response,'lxml')
# homePageSoup = homePageSoup.findAll('div',attrs={'class':'news_content'})
# # print(homePageSoup)
# # srcListFind = re.findall(re.compile(r'<a href="(.*?)".*?title="(.*?)">.*?</a>.*?<span>(.*?)</span>', re.S),str(homePageSoup))
# # print(srcListFind)
# RS = re.sub('<span.*?>', '', str(homePageSoup), flags=re.S | re.M).replace('</span>', '')
# RS = re.sub(r'</p></p><p><p','</p><p',RS).replace('</p></p>','</p>')
# RS = re.sub(r'<td.*?>','<td>',RS)
# rs = re.sub(r'<p.*?>','',str(RS)).replace('</p>','')
# rs = re.sub(r'<span.*?>','',str(rs)).replace('</span>','')
# rs = BeautifulSoup(rs,'lxml')
# #
# ContentTrNum = len(rs.findAll('tr'))
#
# for idx, tr in enumerate(rs.find_all('tr')):
#     if idx != 0:
#         tds = tr.find_all('td')
#         print(tds)
#         RSdocumentNum = tds[5].text.strip()
#         RSbePunished = tds[1].text.strip()  # 被处罚人或机构
#         RSprincipal = tds[4].text.strip()  # 法定代表人
#         RSlawEnforcement = tds[1].text.strip()  # 被处罚单位
#         RSpunishedDate = tds[11].text.strip()  # 受处罚时间
#         RScontent = "主要违法事实：" + tds[6].text.strip() + "。\n 处罚种类:" + tds[7].text.strip() + "。\n 处罚依据：" + \
#                     tds[8].text.strip() + "。\n 行政处罚的履行方式和期限:" + tds[9].text.strip()
#         RSagency = tds[10].text.strip()
# print(RSpunishedDate)
    # # print(ContentTrNum)
#
#
# if rs.find("table")!=-1  and ContentTrNum == (3 or 4):
#     print("laji")
# else:
#     print("m美哟")








# for idx,tr in  enumerate(rs.find_all('tr')):
#     tds = tr.find_all('td')
#     if idx !=0:
# #         tds = tr.find_all('td')
#         title = tds[5].text.strip()
#         # print(tds)
#         # RScontent = "主要违法事实：" + tds[6].contents[0] + "。\n 处罚种类:" + tds[7].contents[0] + "。\n 处罚依据：" + \
#         #                      tds[8].contents[0] + "。\n 行政处罚的履行方式和期限:" + tds[9].contents[0]
# print(title)

str2 = """
<table>
 <tr>dfsdf</tr>
 <tr>sdfasdfasd</tr>
 <tr>dfasdfad</tr>
"""
num = BeautifulSoup(str2,'lxml')
num =len(num.findAll('tr'))
print(num)
if str2.find("table")!=-1 and num==(3 or 4):
    print("gg")
else:
    print("mmp")




