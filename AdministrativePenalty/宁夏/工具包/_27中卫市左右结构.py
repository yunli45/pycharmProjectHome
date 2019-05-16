import re
from bs4 import BeautifulSoup
# 全文的内容在表格中，key在左边value在右边   http://www.nxszs.gov.cn/zwgk/hangzhengchufa.htm

def getNeed(ConetentResponseSoupOld):

    SoupTable = BeautifulSoup(ConetentResponseSoupOld, 'lxml')
    SoupTable1 = SoupTable.find('table', attrs={'class': 'companydetails'})
    SoupTable1 = BeautifulSoup(str(SoupTable1), 'lxml')
    SoupTable1 = SoupTable1.find_all('td')
    print("表格"+str(SoupTable1))
    RSdocumentNum = SoupTable1[0].text.strip() # 书文号
    RSbePunished = SoupTable1[5].text.strip() # 被处罚人或者单位
    RSprincipal = SoupTable1[11].text.strip() # 法人
    RSlawEnforcement =  SoupTable1[14].text.strip() # 处罚单位
    RSagency = RSlawEnforcement
    RSpunishedDate = SoupTable1[13].text.strip() # 时间
    RScontent= "<p>处罚类别："+ SoupTable1[2].text.strip()+"</p>\n<p>处罚事由："+SoupTable1[3].text.strip()+"</p>\n<p>处罚依据："+SoupTable1[4].text.strip()+"</p>\n<p>处罚结果："+SoupTable1[12].text.strip()+"</p>\n<p>处罚生效期："+SoupTable1[13].text.strip()+"</p>"
    RStitle = SoupTable1[1].text.strip() # 书文号
    print("第一个td"+str(SoupTable1[1].text.strip()))
    if RStitle =='':
        RStitle = RSdocumentNum

    print("第一个标题"+RStitle)
    return RSdocumentNum, RSbePunished, RSprincipal, RSlawEnforcement, RSpunishedDate, RScontent, RSagency,RStitle
