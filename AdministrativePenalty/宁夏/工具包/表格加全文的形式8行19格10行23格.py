import re
from  bs4 import BeautifulSoup
import requests

# 这种表格是8行19格或者是10行23格形式的，全文可能除了表格还有全文到时候再说
# 8行19格是因为没有处罚机构和处罚时间
#  http://www.ngsh.gov.cn/2017/10/23/62760.html    http://www.ngsh.gov.cn/2017/10/17/62698.html
def TableN(ConetentResponseSoupOld,ConetentResponse,ContentPNum,ContentPNum1,ContentTrNum,ContentTdNum,RSTime,RSTitle,SavePath,header):

    if ConetentResponseSoupOld.find("<table")!=-1:
        print("包含表格")
        ConetentResponseSoupOld = re.sub("\n", '', ConetentResponseSoupOld)
        SoupTable = BeautifulSoup(ConetentResponseSoupOld, 'lxml')
        TDList = []
        if (ContentTrNum== 8 and ContentTdNum==19):
            print("这种表格是比较标准形式的"+str(ContentTrNum)+"行"+str(ContentTdNum)+"格的表格")
            for ids, tr in enumerate(SoupTable.find_all("tr")):
                tds = tr.find_all('td')
                TDList.append(tds)

            RSdocumentNum = TDList[0][-1].text.strip()  # s书文号
            RSbePunished = TDList[1][-1].text.strip()  # 被处罚人或机构
            RSlawEnforcement = TDList[3][-1].text.strip()  # 被处罚机构
            RSprincipal = TDList[5][-1].text.strip()  # 法人
            违法行为类型 = TDList[6][-1].text.strip()  # 违法行为类型
            行政处罚内容 = TDList[7][-1].text.strip()  # 行政处罚内容
            RSagency = ''
            RSpunishedDate = ''
            RScontent ="<p>违法行为类型："+违法行为类型+"</p><p>行政处罚内容："+行政处罚内容+"</p>"+ConetentResponse
        elif  (ContentTrNum== 10 and ContentTdNum==23):
            print("这种表格是比较标准形式的" + str(ContentTrNum) + "行" + str(ContentTdNum) + "格的表格")
            for ids, tr in enumerate(SoupTable.find_all("tr")):
                tds = tr.find_all('td')
                TDList.append(tds)
            RSdocumentNum = TDList[0][-1].text.strip()  # 书文号
            RSbePunished = TDList[1][-1].text.strip()  # 被处罚人或机构
            RSlawEnforcement = TDList[3][-1].text.strip()  # 被处罚机构
            RSprincipal = TDList[5][-1].text.strip()  # 法人
            违法行为类型 = TDList[6][-1].text.strip()  # 违法行为类型
            行政处罚内容 = TDList[7][-1].text.strip()  # 行政处罚内容
            RSagency = TDList[8][-1].text.strip()  # 作出行政处罚决定机关名称
            RSpunishedDate = TDList[9][-1].text.strip()  # 作出行政处罚决定日期
            RScontent ="<p>违法行为类型："+违法行为类型+"</p><p>行政处罚内容："+行政处罚内容+"</p><p>作出行政处罚决定机关名称："+RSagency+"</p><p>作出行政处罚决定日期："+RSpunishedDate+"</p>"+ConetentResponse
        # 全文是一个7格tr的表格，内容没有
        else:
            print("这里是出除开8行19格或者是10行23格形式的")
            RSdocumentNum = ''  # 书文号
            RSagency = ''
            RSbePunished = ""  # 被处罚人或机构
            RSlawEnforcement = ""  # 被处罚单位
            RSprincipal = ""  # 法定代表人
            RSpunishedDate =RSTime  # 受处罚时间
            RScontent =ConetentResponse
    elif ContentPNum1 == ContentPNum :
        print("这里是不含有表格的,只有文章内容")
        ConetentNoTable = ConetentResponse
        # 全文还可能是一个图片的形式
        RSimgFind = re.findall(re.compile(r'<img.*?src="(.*?)".*?>'), ConetentResponse)

        print(ConetentNoTable)
        ConetentNOW = BeautifulSoup(ConetentNoTable, 'lxml')
        ConetentNOWp = ConetentNOW.find_all('p')
        print(ConetentNOWp)
        if 0 <= len(ConetentNOWp) <= 8:
            RSdocumentNum = ''  # 书文号
            RSagency = ''
            RSbePunished = ""  # 被处罚人或机构
            RSlawEnforcement = ""  # 被处罚单位
            RSprincipal = ""  # 法定代表人
            RSpunishedDate = RSTime  # 受处罚时间


        else:

            RSdocumentNum = ConetentNOWp[2].text.strip() # 书文号
            RSagency = ConetentNOWp[-2].text.strip()
            RSbePunished = ConetentNOWp[4].text.strip().replace("当事人",'').replace(':','').replace("：",'').replace("当 事 人",'')# 被处罚人或机构
            RSlawEnforcement = RSbePunished # 被处罚单位
            RSprincipal = ConetentNOWp[7].text.strip().replace("法定代表人",'').replace(':','').replace("：",'').replace("（负责人）",'')  # 法定代表人
            RSpunishedDate = ConetentNOWp[-1].text.strip()  # 受处罚时间



            if RSimgFind:
                print(RSTitle)
                print(RSimgFind)
                print(ConetentResponse)
                ConetentResponse = "这可能是一个图片形式的，请查看本地是否有相应的标题图片" + ConetentResponse
                RSdocumentNum = ''  # 书文号
                imgSrc = RSimgFind[0]
                RSbePunished = ''  # 被处罚人或者单位
                RSlawEnforcement = ''  # 被处罚单位
                RSprincipal = ''  # 法人
                RSpunishedDate = RSTime  # 受处罚时间

                try:
                    imgSrc = imgSrc
                    for TitleNum in enumerate(RSimgFind):
                        imgTitle = RSTitle + str(TitleNum[0]) + ".jpg"
                        SavePath1 = SavePath % (imgTitle)
                        r = requests.get(imgSrc, headers=header, timeout=3)
                        with open(SavePath1, "wb") as f:
                            f.write(r.content)
                        f.close()
                except:
                    print("这条数据的网址出错了")

                    pass
            else:
                ConetentResponse = ConetentResponse

        RScontent = ConetentResponse
    else:
        print("")




    return RSdocumentNum, RSbePunished, RSprincipal, RSlawEnforcement, RSpunishedDate, RScontent, RSagency