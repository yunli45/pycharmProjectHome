import re
from bs4 import BeautifulSoup
import requests
# 全文的内容在表格中，key在左边value在右边   http://www.nxszs.gov.cn/zwgk/hangzhengchufa.htm

def getNeed(ConetentResponseSoupOld, ConetentResponse, ContentPNum, ContentPNum1, ContentTrNum, ContentTdNum,
                   RSTime,RSTitle,SavePath,header,RSdataId,RSdocumentNum,RSlawEnforcement):
    fj = re.findall('<a.*?href="(.*?)".*?>.*?.doc|docx|PDF|pdf|jpg</a>',ConetentResponseSoupOld)
    if  fj!=[] and ContentPNum <6:
        print("全文是附件")
        RSdocumentNum = RSdocumentNum
        RSlawEnforcement=RSlawEnforcement
        RSbePunished = ''
        RSprincipal = ''
        RSpunishedDate = RSTime
        RScontent = ConetentResponseSoupOld
        RSagency = RSlawEnforcement
        pass
    else:
        pass
        print("全文不是以附件")
        Soup =BeautifulSoup(ConetentResponseSoupOld,'lxml')
        Soup = Soup.find_all('p')
        if ContentPNum >10:
            RSdocumentNum = RSdocumentNum
            RSbePunished = Soup[3].text.strip().replace("：",'').replace(":",'')
            if Soup[6].text.strip().find("法定代表人")!=-1:
                RSprincipal = Soup[6].text.strip().replace("法定代表人（负责人）姓名：",'').replace(":",'')
            else:
                RSprincipal = Soup[7].text.strip().replace("法定代表人（负责人）姓名：", '').replace(":", '')
            RSlawEnforcement = RSlawEnforcement
            RSpunishedDate = Soup[-1].text.strip()
            RScontent = ConetentResponseSoupOld
            RSagency = RSlawEnforcement
        else:
            RSdocumentNum = RSdocumentNum
            RSbePunished = ''
            RSprincipal = ''
            RSlawEnforcement = RSlawEnforcement
            RSpunishedDate = RSTime
            RScontent = ConetentResponseSoupOld
            RSagency  = RSlawEnforcement
    return RSdocumentNum, RSbePunished, RSprincipal, RSlawEnforcement, RSpunishedDate, RScontent, RSagency
