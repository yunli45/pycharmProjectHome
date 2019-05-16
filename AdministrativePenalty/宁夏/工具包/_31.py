import re
from bs4 import BeautifulSoup
import requests
import xlrd
from 宁夏.工具包 import 附件下载程序
import time
#

def getNeed(ConetentResponseSoupOld, RSTime,RSTitle):


    if RSTitle.find("号")!=-1:
        RSdocumentNum= re.sub('号.*?书','',RSTitle )+"号"
    else:
        RSdocumentNum = ''
    DSR1 = re.findall(re.compile(r'>被行政处理单位：(.*?)<',flags=re.S|re.M),ConetentResponseSoupOld)
    DSR2 =re.findall(re.compile(r'>当事人：(.*?)<'),ConetentResponseSoupOld)
    if DSR1!=[]:
        RSbePunished = DSR1[0]
    elif DSR2!=[]:
        RSbePunished = DSR2[0]
    else:
        RSbePunished = ''
    RSprincipal = ''
    Soup = BeautifulSoup(ConetentResponseSoupOld,'lxml')
    Soup = Soup.find_all('p')

    RSpunishedDate = Soup[-1].text.strip()
    if RSpunishedDate =='':
        RSpunishedDate =RSTime
    RSlawEnforcement= Soup[-2].text.strip()
    RScontent = ConetentResponseSoupOld
    RSagency = Soup[-2].text.strip()

    return RSdocumentNum, RSbePunished, RSprincipal, RSlawEnforcement, RSpunishedDate, RScontent, RSagency