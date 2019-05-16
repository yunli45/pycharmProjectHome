# coding :utf-8
import requests
import re
from bs4 import BeautifulSoup


n = 3

for i in range(1,n):
    if i ==1:
        print("dfsdfsdf")
    else:
        print(i)

list1 = [(1,'w'),(2,'e')]
list2 = [(3,'r'),(4,'t')]
list3 =[]
for i in range(1,3):
    if i==1:
        list3.append(list1)
        # for y in list1:
        #     list3.append(y)
    else:
        # for z in list2:
        #     list3.append(z)
        list3.append(list2)
# print(list3)
# print(list3[0][0][0])
list4 ,list5 =[],[]
for i in list1:
    list4.append(i[0]),list5.append(i[1])
print(list4)

str1 = """

`<div class="index_art_con" id="printContent">`
<table width="100%" cellspacing="0" cellpadding="0" border="0">
	<tbody><tr>
		<td>

<p>　　9月19日，国务院总理李克强在天津梅江会展中心出席2018年夏季达沃斯论坛开幕式并发表特别致辞。李克强在致辞中表示，中国近年对外支付的知识产权使用费位居世界前列。中国政府坚决依法保护知识产权。这不仅是履行国际规则，也是中国创新发展的内在需要。李克强强调，中国将实施更加严格的知识产权保护制度，对侵害中外知识产权的行为坚决依法打击，加倍惩罚。让侵权者付出难以承受的代价，让创新者放心大胆去创造。（综合中国政府网消息）</p>

<p>　<strong>　李克强总理致辞摘编</strong></p>

<p>　　在新产业革命中，没有谁能包打天下。各方应优势互补，共育创新、共推创新、共享创新，在严格保护知识产权的基础上，支持企业基于市场原则和商业规则开展创新合作，协力加速新产业革命进程。</p>

<p>　　对谋财害命、坑蒙拐骗、假冒伪劣、侵犯知识产权的，不管是新业态还是传统业态，不管是线上还是线下，都坚决依法予以打击。正是由于这样的监管，网上购物、移动支付、共享经济等新兴产业迅速崛起，成为中国经济发展新动能蓬勃成长的显著标志。</p>

<p>　　过去五年，中国有效发明专利拥有量增加了2倍，年度技术交易额翻了一番。前不久，世界知识产权组织等机构发布2018年全球创新指数排名，中国列第17位，较2013年上升了18位。</p>

<p>　　我们将继续全面深化改革，加强基础性关键领域改革，深入推进简政放权、放管结合、优化服务改革，进一步放宽市场准入，提高政策透明度，实行公平公正监管，为各类所有制企业、内外资企业打造一视同仁、公平竞争的市场环境。落实和完善支持民营经济的政策措施，消除民营企业投资的各种隐形障碍。严格保护各类产权，激励企业家创业创新。</p>

<p>　　以更大力度激励创新。提高创新能力是一个系统工程。我们将强化创新生态体系建设，支持基础研究和应用基础研究，鼓励企业增加研发投入，加快创新成果转化应用。我们将完善政策、创新机制，提升众创空间、孵化器、创新平台的市场化专业化水平，打造线上线下结合、产学研用贯通、各类主体协同的融通创新格局。</p>

<p>　　保护知识产权就是保护和激励创新。中国要实现创新发展，离不开一个尊重知识、保护产权的环境。中国已建立起完整的知识产权法律保护体系，成立了专门的知识产权法院。中国加入世贸组织以来，企业对外支付的知识产权费增长14倍。我们将进一步加强执法力量，实施更加严格、更有威慑力的侵权惩罚性赔偿制度，为各方面创新提供更加牢靠的保护。</p>
 


<p>

<!--
</p>
<p style="color:#3248C0;">
<a href=""></a>
</p>
-->

		</p></td>
	</tr>
</tbody></table>

				</div>
"""
# ContentResponse = BeautifulSoup(str1, 'lxml')
# ContentResponse = ContentResponse.find_all("div", attrs={'class', 'index_art_con'})
# print(ContentResponse[0])
# str2 = "/images/content/2018-08/20180827075011376131.jpg"
# print(str2[str2.rfind("/"):])
# str3 = "/images/content/2018-08/20180827075011376131.jpg"
# print(str3[str2.rfind("/"):])
# str4 = """
# sdfsdfs
# <img src="../images/content/2018-08/20180827075011376131.jpg" class="index_bor01">
# <img src="../images/content/2018-08/20180.jpg" class="index_bor01">
# <img src="../images/content/2018-08/20181.jpg" class="index_bor01">
# <img src="../images/content/2018-08/20182.jpg" class="index_bor01">
# sdfsdf
# """
# imgList = re.findall(re.compile(r'<img.*?src="(.*?)".*?>'),str4)
# imgList1 = re.findall(re.compile(r'<img.*?src=".*?".*?>'),str4)
# savePath = "F:\知识产权\%s"
#
# for img1 in imgList1:
#
#     for img in imgList:
#         print(img)
#         imgSrc = img.replace("../", '').replace("./", '')
#         imgName = imgSrc[imgSrc.rfind("/") + 1:]
#         savePath1 = savePath%(imgName)
#         print(savePath1)
#         str4 = str4.replace(img1,'<img src="'+"%s"%(savePath1)+'">')
#         print(str4)
#
# str2 = "http://www.cnipa.gov.cn/tz/2017nqgzldlrzgkscjwtjd.pdf"
# Rs1 = re.findall(re.compile(r'.*?.(doc|DOC|docx|DOCX|xlsx|XLSX|xls|XLS|pdf|PDF)'), str2)
# print(Rs1)
# print(str2[:str2.rfind(".")])

list4 =['1132300.htm', '1132364.htm', '1132363.htm', '1132362.htm', '1132361.htm', '1132407.htm', '1132360.htm', '1132299.htm', '1132297.htm', '1132295.htm', '1132219.htm', '1132216.htm', '1132214.htm', '1132096.htm', '1132092.htm', '1132087.htm', '1132019.htm', '1132017.htm', 'http://www.gov.cn/zhengce/2018-09/11/content_5320979.htm', '1131876.htm', '1131895.htm', '1131894.htm', '1131866.htm', '1131862.htm', '1131861.htm', '1131792.htm', '1131828.htm', '1131791.htm', '1131807.htm', '1131788.htm', '1131787.htm', '1131733.htm', '1131732.htm', '1131613.htm', '1131612.htm', '1131610.htm', '1131609.htm', '1131607.htm', '1131605.htm', '1131601.htm']
tt = "1131788.htm"
id = 256
print(list4[28])
for ids ,src in enumerate(list4):
    if src != tt:
        # print("haha")
        id+=1
        完整的url = "http://www."+src
    else:
        break
print(完整的url)
# print(ids)
# print(id)
# import datetime
# RS插入时间 = datetime.datetime.now().strftime('%Y-%m-%d')
# print(RS插入时间)