import re
from bs4 import BeautifulSoup
# 全文每一段是由一个p标签包裹着的，可以提取出被处罚人和地址和法人以及书文号 处罚单位 处罚时间

def getNeed(ConetentResponseSoupOld, ConetentResponse, ContentPNum, ContentPNum1, ContentTrNum, ContentTdNum,
                   RSTime,RSTitle,SavePath,header):
    if ContentPNum >10:
        SoupP = BeautifulSoup(ConetentResponseSoupOld,'lxml')
        SoupP = SoupP.find_all('p')
        RSdocumentNum = SoupP[2].text.strip() # 书文号
        RSbePunished = SoupP[3].text.strip().replace("：",'').replace(":",'') # 被处罚人或者机构
        RSprincipal = SoupP[5].text.strip() # 法人
        RSprincipal = re.sub('.*?法定代表人：','',RSprincipal)
        RSlawEnforcement = SoupP[-2].text.strip() #  执法机关
        RSpunishedDate = SoupP[-1].text.strip() #  时间
        RScontent = ConetentResponseSoupOld
        RSagency =RSlawEnforcement #  执法机关
        RSaddress =SoupP[5].text.strip()
        RSaddress = re.findall('地址：(.*?)法定代表人',RSaddress)
        if RSaddress!=[]:
            RSaddress = RSaddress[0]
        else:
            RSaddress = re.findall('<p>地址：(.*?)法定代表人.*?</p>',ConetentResponseSoupOld)
            RSaddress = RSaddress[0]
    else:
        RSdocumentNum = ''
        RSbePunished =''
        RSprincipal =''
        RSlawEnforcement= ''
        RSpunishedDate =''
        RScontent =ConetentResponseSoupOld
        RSagency =''
        RSaddress = ''
    return RSdocumentNum, RSbePunished, RSprincipal, RSlawEnforcement, RSpunishedDate, RScontent, RSagency,RSaddress

