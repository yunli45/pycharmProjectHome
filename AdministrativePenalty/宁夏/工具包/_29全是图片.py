import re
from bs4 import BeautifulSoup
import requests
# 全文的内容在表格中，key在左边value在右边   http://www.nxszs.gov.cn/zwgk/hangzhengchufa.htm

def getNeed(ConetentResponseSoupOld, ConetentResponse, ContentPNum, ContentPNum1, ContentTrNum, ContentTdNum,
                   RSTime,RSTitle,SavePath,header,ContentSrc):

    if ContentPNum == ContentPNum1 and ContentPNum1<10:
        RSdocumentNum = '这是图片形式的无法提取'
        RSbePunished = ''
        RSprincipal = ''
        RSlawEnforcement = ''
        RSpunishedDate= RSTime
        RScontent = ConetentResponseSoupOld
        RSagency = ''
        adjunct2 = re.findall(re.compile(r'<img.*?src="(.*?)".*?>', re.I | re.S),
                              str(ConetentResponseSoupOld))

        if adjunct2:
            baseUrl =ContentSrc[:ContentSrc.rfind("/")+1]
            i = 1
            for src in adjunct2:
                rsDocuniqueSign = baseUrl+ src
                SavePath1 = SavePath % (RSTitle)+str(i)+".jpg"
                if rsDocuniqueSign.find("http") == -1:
                    rsDocuniqueSign = baseUrl + rsDocuniqueSign
                else:
                    rsDocuniqueSign = rsDocuniqueSign

                # print(rsDocuniqueSign)
                r = requests.get(rsDocuniqueSign, header)
                with open(SavePath1, "wb") as f:
                    f.write(r.content)
                f.close()
                i+=1


    return RSdocumentNum, RSbePunished, RSprincipal, RSlawEnforcement, RSpunishedDate, RScontent, RSagency
