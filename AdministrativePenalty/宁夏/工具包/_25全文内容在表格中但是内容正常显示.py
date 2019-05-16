import re
from bs4 import BeautifulSoup
# 全文的内容在表格中，内容正常显示    http://xzzf.spb.gov.cn/SPXzzfApp/base/spBaseXzzfOpenAction_cityOf!toCheckDetails.action?openId=ff8080816059aaa701606cb9d13f5cce&undertakeUnitCode=100100070005

def getNeed(ConetentResponseSoupOld):

    soup = BeautifulSoup(ConetentResponseSoupOld,'lxml')
    soup = soup.find_all('td')
    # 去除前2两个td,包含标题的td
    soup= soup[3:]
    RSdocumentNum = ''
    RSbePunished = re.findall(re.compile('企业（个人）名称：(.*?)法定代表人',flags=re.S|re.M),ConetentResponseSoupOld)
    RSbePunished = RSbePunished[0]
    RSprincipal = re.findall(re.compile('法定代表人：(.*?)住所',flags=re.S|re.M),ConetentResponseSoupOld)
    RSprincipal = RSprincipal[0]
    RSlawEnforcement = soup[-5].text.strip().replace("承办单位：",'')
    RSagency= RSlawEnforcement
    RSpunishedDate = soup[-2].text.strip().replace("公开日期：",'')
    ConetentResponseSoupOld = re.sub('<tr>','<p>',ConetentResponseSoupOld).replace('<td>','').replace('</td>','')
    ConetentResponseSoupOld = re.sub('</tr>','</p>',ConetentResponseSoupOld)
    ConetentResponseSoupOld = re.sub('<table.*?>','',ConetentResponseSoupOld).replace('</table>','')
    RScontent=ConetentResponseSoupOld
    return RSdocumentNum, RSbePunished, RSprincipal, RSlawEnforcement, RSpunishedDate, RScontent, RSagency