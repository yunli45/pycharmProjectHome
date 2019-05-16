# coding:utf-8
import requests
import re
import time
from bs4 import BeautifulSoup
import pymssql

class Utils(object):
    def __init__(self):
        self.header = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Cache - Control': 'max - age = 0',
'Connection':'keep-alive',
'Cookie': 'JSESSIONID=73824732C6B0980D2FFE441E8C19D9DA',
'Host': 'www.linhe.gov.cn',
# 'Referer':'http://www.linhe.gov.cn/sites/lhqzf/list.jsp?ColumnID=88&SiteID=lhqzf',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}
        self.OnlyID = 1
        self.showId = 12335200


    def getPage(self,url=None):
        response = requests.get(url,headers=self.header)
        print(response.encoding)
        response =  response.content.decode('gb18030')
        return response

    def parsePage(self,url=None,pageNo=None,baseUrl="http://www.linhe.gov.cn",path="F:\行政处罚数据\内蒙古\巴彦淖尔市_临河区\%s"):

        if pageNo =="1":
            response = self.getPage("http://www.linhe.gov.cn/sites/lhqzf/list.jsp?ColumnID=88&SiteID=lhqzfhttps://www.hao123.com/?tn=94993071_hao_pg")
            # response = self.getPage(url+pageNo)
            # print(url)
        else:
            response =  self.getPage(url+pageNo)


        print("+++++++++++++++++++这是第："+pageNo+"页++++++++++++++++")
        print(response)
        response = response.replace("\n",'').replace("\r",'').replace("\t",'')
        # 注意这里数据提取出来不完整，只有src是完整的其他的信息去详细页面提取

        responseList = BeautifulSoup(response,'lxml')
        responseList = responseList.find_all('div',attrs={'class':'zwxw_news_list_nr'})
        # print(responseList)
        RSlist = re.findall(re.compile(r'<a href="(.*?)"><span.*?>(.*?)</span></a><span.*?>(.*?)</span>',re.S|re.M),str(responseList))
        # print("这也是mmp")
        print(RSlist)
        urlF = baseUrl + "/sites/lhqzf"
        #  复制一个新的集合
        RSlist1=[]
        for m in RSlist:
            RSlist1.append(m)

        for n in RSlist1:
            src = n[0]
            KeyID = re.findall(re.compile(r'KeyID=.*'), str(src))
            ColumnID = re.findall(re.compile(r'(ColumnID=.*?)&amp'), str(src))
            print("KeyID" + str(KeyID))
            ContentSrc = urlF + "/" + "detail.jsp?" + KeyID[0] + "&" + ColumnID[0]
            print(ContentSrc)
            ConetentResponse = requests.get(ContentSrc, headers=self.header)
            ConetentResponse = ConetentResponse.content.decode('gb18030')
            ConetentResponseSoup = BeautifulSoup(ConetentResponse, 'lxml')
            ConetentResponseSoupOld = ConetentResponseSoup.find('div', attrs={'class': 'zwxw_nr_title2'})
            # print(n[1])
            if str(ConetentResponseSoupOld).find("许可机关") !=-1:
                RSlist.remove(n)
            else:
                print("需要提取的文章")
                print(n[1])
        print("最终版的")
        print(RSlist)
        SrcList = []
        TitleList =[]
        for i in RSlist:
            SrcList.append(i[0])
            TitleList.append(i[1])
        for src in SrcList:
            RSTitle = TitleList[SrcList.index(src)]
            # ('/cms/info/preview.jsp?SiteID=lhqzf&amp;ColumnID=88&amp;KeyID=20180816105720502428983'
            # http://www.linhe.gov.cn/sites/lhqzf/  +  detail.jsp?KeyID=20180816105720502428983&ColumnID=88
            KeyID = re.findall(re.compile(r'KeyID=.*'),str(src))
            ColumnID = re.findall(re.compile(r'(ColumnID=.*?)&amp'),str(src))
            print("KeyID"+str(KeyID))
            RSdataId = ColumnID[0]
            ContentSrc = urlF+ "/"+"detail.jsp?"+KeyID[0]+"&"+ColumnID[0]
            print(ContentSrc)
            # print(ContentSrc)
            # 提取整个页面 在提取标题 时间   全文
            ConetentResponse = requests.get(ContentSrc, headers=self.header)
            ConetentResponse = ConetentResponse.content.decode('gb18030')
            ConetentResponseSoup = BeautifulSoup(ConetentResponse, 'lxml')
            ConetentResponseSoupOld = ConetentResponseSoup.find('div', attrs={'class': 'zwxw_nr_title2'})

            ConetentResponseSoupOld = re.sub("<strong.*?>", '', str(ConetentResponseSoupOld)).replace("</strong>", '')
            ConetentResponseSoupOld = re.sub("<u.*?>", '', ConetentResponseSoupOld, flags=re.S | re.M).replace("</u>",
                                                                                                               '')
            ConetentResponseSoupOld = re.sub("<b.*?>", '', ConetentResponseSoupOld, flags=re.S | re.M).replace("</b>",
                                                                                                               '')
            ConetentResponseSoupOld = re.sub('<span.*?>', '', ConetentResponseSoupOld, flags=re.S | re.M).replace(
                '</span>', '').replace("<h4>人体胎盘倒卖事件经报道后，北京妇产医院立即成立调查小组对医院胎盘管理情况进行了调查管理情况进行了调查管理情况进行了调查</h4>",'').replace("""<img src="/sites/lhqzf/images/img_11.jpg" style="text-align:center">""",'')
            ConetentResponseSoupOld = str(ConetentResponseSoupOld)

            ContentNum = BeautifulSoup(str(ConetentResponseSoupOld), 'lxml')
            print("这条数据一共有：" + str(len(ContentNum.findAll('tr'))) + "个tr")
            print("这条数据有：" + str(len(ContentNum.findAll('p'))) + "个P")
            print("还没修改完全的全文+" + ConetentResponseSoupOld)
            #   #  #  #  #  #  #  #  #  #  #  #  #  #  #
            #
            #           替换掉表格的所有的格式为p标签
            #
            #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
            ConetentResponse = re.sub('<col.*?>', '', ConetentResponseSoupOld)
            ConetentResponse = re.sub('<tr.*?>', '<p>', ConetentResponse).replace("</tr>","</p>")
            ConetentResponse = re.sub('<td.*?>', '<p>', ConetentResponse).replace("</td>","</p>")
            ConetentResponse = re.sub('<table.*?>', '', ConetentResponse).replace("</table>","")
            ConetentResponse = re.sub('<tbody.*?>', '', ConetentResponse).replace("</tbody>","")
            ConetentResponse = re.sub(r'<p.*?><o:p> </o:p></p>', '', str(ConetentResponse)).replace('<o:p></o:p>', '')
            ConetentResponse = re.sub(r'<st1:.*?>', '', str(ConetentResponse)).replace('</st1:chsdate>', '').replace(
                '<a name="TCSignYear"></a>', '')
            ConetentResponse = re.sub(r'<o:p>\xa0</o:p>', '', str(ConetentResponse))
            ConetentResponse = re.sub(r'<p.*?>', '<p>', str(ConetentResponse), flags=re.S | re.M)
            ConetentResponse = ConetentResponse.replace("'", "''").replace('<b>', '').replace('</b>', '').replace(
                "2312>'，", '')
            ConetentResponse = str(ConetentResponse)

            # print("修改后i的全文")
            # print(ConetentResponse)

            # 全文是表格 含有行政处罚决定文书号
            if ConetentResponseSoupOld.find("<table")!=-1 and ConetentResponseSoupOld.find("行政处罚决定文书号")!=-1:
                print("这是表格")
                ConetentResponseNow = re.sub('<table.*?>','',ConetentResponseSoupOld , flags=re.S | re.M).replace("</table>",'')
                ConetentResponseNow = re.sub('<tbody.*?>','',ConetentResponseNow, flags=re.S | re.M).replace("</tbody>",'')
                ConetentResponseNow = re.sub('<colgroup.*?>','',ConetentResponseNow, flags=re.S | re.M).replace("</colgroup>",'')
                ConetentResponseNow = re.sub('<col.*?>','',ConetentResponseNow, flags=re.S | re.M).replace("</col>",'')
                ConetentResponseNow = re.sub('<tr.*?>','<p>',ConetentResponseNow, flags=re.S | re.M).replace("</tr>",'</p>')
                ConetentResponseNow = re.sub('<td.*?>','',ConetentResponseNow, flags=re.S | re.M).replace("</td>",'')
                ConetentResponseNow = re.sub('<th.*?>','',ConetentResponseNow, flags=re.S | re.M).replace("</th>",'')
                ConetentResponseNow = re.sub('<div.*?>','',ConetentResponseNow, flags=re.S | re.M).replace("</div>",'')
                print(ConetentResponseNow)
                RSdocumentNumFind = re.findall(re.compile(r'<p>行政处罚决定文书号[：：](.*?)</p>'),ConetentResponseNow)
                RSbePunishedFind1 = re.findall(re.compile(r'<p>信用主体名称[: ：](.*?)</p>'),ConetentResponseNow)
                RSbePunishedFind2 = re.findall(re.compile(r'<p>企业名称/个人姓名[: ：](.*?)</p>'),ConetentResponseNow)
                if RSbePunishedFind1!=[]:
                    RSbePunishedFind = RSbePunishedFind1
                elif RSbePunishedFind2!=[]:
                    RSbePunishedFind = RSbePunishedFind2
                RSprincipalFind = re.findall(re.compile(r'<p>法定代表.*?[: ：](.*?)</p>'),ConetentResponseNow)
                RSlawEnforcementFind1 = re.findall(re.compile(r'<p>信用主体名称[: ：](.*?)</p>'),ConetentResponseNow)
                RSlawEnforcementFind2 = re.findall(re.compile(r'<p>企业名称/个人姓名[: ：](.*?)</p>'), ConetentResponseNow)
                if RSlawEnforcementFind1 !=[]:
                    RSlawEnforcementFind =RSlawEnforcementFind1
                elif RSlawEnforcementFind2!=[]:
                    RSlawEnforcementFind= RSlawEnforcementFind2
                RSpunishedDateFind = re.findall(re.compile(r'<p>处罚生效期[: ：](.*?)</p>'),ConetentResponseNow)
                RSagencyFind = re.findall(re.compile(r'<p>处罚机关[: ：](.*?)</p>'),ConetentResponseNow)
                RSdocumentNum = RSdocumentNumFind[0]# 书文号
                RSbePunished = RSbePunishedFind[0]# 被处罚人或机构
                RSprincipal = RSprincipalFind[0] # 法定代表人
                RSlawEnforcement = RSlawEnforcementFind[0]# 被处罚单位
                RSpunishedDate = RSpunishedDateFind[0] # 受处罚时间
                RScontent = ConetentResponseNow  # 全文RScontent
                RSagency = RSagencyFind[0]# 处罚机构

            if ConetentResponseSoupOld.find("<table") ==-1:
                print("这不是表格")
                RSdocumentNum =""
                RSbePunished =""
                RSprincipal = ""
                RSlawEnforcement=""
                RSpunishedDate =""
                RScontent = ConetentResponse
                RSagency = ""
            #  文中可能含有图片，进行下载
            JpgContent = re.findall(re.compile(r'<img.*?src="(.*?)".*?>'),str(ConetentResponseSoupOld))
            print("tupianList"+str(JpgContent))
            if JpgContent!=[]:
                for num in JpgContent:
                    print("tup地址"+num)
                    rsJpgName =  RSTitle+ str(JpgContent.index(num))+".jpg"
                    print(rsJpgName)
                    if num.find("http")== -1:
                        rsJpgSrc =  baseUrl+num
                    else:
                        rsJpgSrc =num

                    print("图片地址"+rsJpgSrc)
                    path1 = path % (rsJpgName)
                    r = requests.get(rsJpgSrc, headers=self.header, timeout=1)
                    with open(path1, "wb") as f:
                        f.write(r.content)
                    f.close()


            """"
            表中的字段 公共部分插入到数据库
            """

            #  来源处的id，没有就以src最后的数字为准
            dataId = RSdataId
            title = RSTitle
            documentNum = RSdocumentNum  # 书文号
            bePunished = RSbePunished  # 被处罚人或机构
            principal = RSprincipal  # 法定代表人
            lawEnforcement = RSlawEnforcement  # 被处罚单位
            punishedDate = RSpunishedDate  # 受处罚时间
            content = RScontent  # 全文RScontent
            uniqueSign = ContentSrc  # url地址
            address = '内蒙古自治区'  # 省份  RSagency
            area = "巴彦淖尔市"  # 地区
            agency = RSagency   # 处罚机构
            if len(content) <= 100:
                grade = -1  # 级别
            elif 100 < len(content) <= 200:
                grade = 1  # 级别
            elif 200 < len(content) <= 1500:
                grade = 2  # 级别
            elif len(content) > 1500:
                grade = 0  # 级别
            showId = self.showId  # 系统ID


            #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
            #
            #        附件下载部分
            #
            #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
            adjunct = re.findall(re.compile(r'<a.*?href="(.*?)".*?>(.*?)</a>', re.I | re.S), str(ConetentResponseSoupOld))

            if ConetentResponse:
                conn = pymssql.connect(host='(local)', user='sa', password='123456', database='AdministrativePunNeiM')
                # 打开游标
                cur = conn.cursor();
                if not cur:
                    raise Exception('数据库连接失败！')
                else:
                    print("数据库链接成功")
                sql1 = " INSERT INTO  crawlDataNeiM22(dataId,title,documentNum,bePunished,principal,lawEnforcement,punishedDate,content,uniqueSign,address,area,agency,grade,showId) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " % (dataId, title, documentNum, bePunished,principal,lawEnforcement,punishedDate,content,uniqueSign,address, area, agency,grade,showId)


                print(sql1)
                if adjunct:
                    print("这条数据存在附件，可能会很大，请稍等，已经自动开始下载.....")
                    for xiaZai in adjunct:
                        print(xiaZai)
                        rsDocuniqueSign = xiaZai[0]
                        rsDocName = xiaZai[1]
                        xiaZai = str(xiaZai)
                        rsDoc1 = re.findall(re.compile(r'.*?.doc', re.I), xiaZai)
                        rsDoc2 = re.findall(re.compile(r'.*?.docx', re.I), xiaZai)
                        rsPdF = re.findall(re.compile(r'.*?.pdf', re.I), xiaZai)
                        rsXlsx = re.findall(re.compile(r'.*?.xlsx|xls', re.I), xiaZai)
                        rsZip = re.findall(re.compile(r'.*?.zip', re.I), xiaZai)
                        rsRar = re.findall(re.compile(r'.*?.rar', re.I), xiaZai)
                        reJpg = re.findall(re.compile(r'.*?.jpg', re.I), xiaZai)
                        if rsDoc1 or rsDoc2:
                            rsDocName = rsDocName + ".doc"
                            rsDocName = rsDocName.replace("/", '_')

                            path1 = path % (rsDocName)

                            if rsDocuniqueSign.find("http") == -1:
                                rsDocuniqueSign = "%s" % (baseUrl) + rsDocuniqueSign
                            else:
                                rsDocuniqueSign = rsDocuniqueSign
                            # print(rsDocuniqueSign)
                            r = requests.get(rsDocuniqueSign, headers=self.header, timeout=30)
                            with open(path1, "wb") as f:
                                f.write(r.content)
                            f.close()
                        elif rsPdF:
                            rsDocName = rsDocName + ".PDF"
                            rsDocName = rsDocName.replace("/", '_')
                            path1 = path % (rsDocName)

                            if rsDocuniqueSign.find("http") == -1:
                                rsDocuniqueSign = baseUrl + rsDocuniqueSign
                            else:
                                rsDocuniqueSign = rsDocuniqueSign
                            # print(rsDocuniqueSign)
                            r = requests.get(rsDocuniqueSign, headers=self.header)
                            with open(path1, "wb") as f:
                                f.write(r.content)
                            f.close()
                        elif rsXlsx:
                            rsDocName = rsDocName + ".xlsx"
                            rsDocName = rsDocName.replace("/", '_')
                            path1 = path % (rsDocName)

                            if rsDocuniqueSign.find("http") == -1:
                                rsDocuniqueSign = baseUrl + rsDocuniqueSign
                            else:
                                rsDocuniqueSign = rsDocuniqueSign

                            # print(rsDocuniqueSign)
                            r = requests.get(rsDocuniqueSign, headers=self.header)
                            with open(path1, "wb") as f:
                                f.write(r.content)
                            f.close()
                        elif rsZip:
                            rsDocName = rsDocName + ".zip"
                            rsDocName = rsDocName.replace("/", '_')
                            path1 = path % (rsDocName)

                            if rsDocuniqueSign.find("http") == -1:
                                rsDocuniqueSign = baseUrl + rsDocuniqueSign
                            else:
                                rsDocuniqueSign = rsDocuniqueSign

                            # print(rsDocuniqueSign)
                            r = requests.get(rsDocuniqueSign, headers=self.header)
                            with open(path1, "wb") as f:
                                f.write(r.content)
                            f.close()
                        elif rsRar:
                            rsDocName = rsDocName + ".rar"
                            rsDocName = rsDocName.replace("/", '_')
                            path1 = path % (rsDocName)

                            if rsDocuniqueSign.find("http") == -1:
                                rsDocuniqueSign = baseUrl + rsDocuniqueSign
                            else:
                                rsDocuniqueSign = rsDocuniqueSign

                            # print(rsDocuniqueSign)
                            r = requests.get(rsDocuniqueSign, headers=self.header)
                            with open(path1, "wb") as f:
                                f.write(r.content)
                            f.close()
                        elif reJpg:
                            rsDocName = rsDocName + ".jpg"
                            rsDocName = rsDocName.replace("/", '_')
                            path1 = path % (rsDocName)

                            if rsDocuniqueSign.find("http") == -1:
                                rsDocuniqueSign = "%s" % (baseUrl) + rsDocuniqueSign
                            else:
                                rsDocuniqueSign = rsDocuniqueSign
                            # print(rsDocuniqueSign)
                            r = requests.get(rsDocuniqueSign, headers=self.header, timeout=30)
                            with open(path1, "wb") as f:
                                f.write(r.content)
                            f.close()

                cur.execute(sql1)
                self.OnlyID += 1
                self.showId += 1
            conn.commit()
            conn.close()
        print("下一页开始的id是" + str(self.OnlyID))
        print("这一夜爬取成功相关数据和文件，文件保存的目录在" + path)

#######     执行    ########
if __name__ =="__main__":
    # 共计353页
    url ="http://www.linhe.gov.cn/sites/lhqzf/list.jsp?page="
    AdminiStrative =Utils()
    for i in range(1,16):
        AdminiStrative.parsePage(url,str(i))
        time.sleep(3)



























