# coding:UTF-8
import requests

url = "http://www.nhfpc.gov.cn/zwgk/jdjd/ejlist.shtml"
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
data = {'Host':'www.nhfpc.gov.cn',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
'Accept-Encoding':'gzip, deflate',
'Cookie':'FSSBBIl1UgzbN7N80T=3.H2Ia5ajF2W9MN4MexaHbwzbRdo6Ibvothnjv26zdIEPzIbEFAGKUVrSeldMhLRaR6UT4DHRuAezjJ6umYAblrR1.UgqzGaQSIqxA2OuZfb_OVHuCepRlcDvsUFFbW8Zc9OpYa_5oCK1KHUwdodoVHSReJB7XCoVkjOSYSlT49Q0QbYU8FGG_QNJY2cUU1o9n48WRP9i3JO9UscicJdzYWcvLCk32L_kXcm1Z4tqhC3zySwryE2qmAkRWa30lR0JUJvfYkk60tpcNtPMrYYQhxGoaNkhqmvJ3HF1SfyRlle.PQ6VpaLtJF_WUWHWgcdWWOccWDNSVTnW9Eg8hG2WOvNZz98sAFWkkAS4koeD3wjEpq; FSSBBIl1UgzbN7N80S=BBmhTOmn80_slbXvAdgknuzSr9K7.OSGjcCmvc7kS.n2MmVwnx9JETg1JYLxoKCk; _gscu_170533903=39059502zmsxsa12; gwdshare_firstime=1539059514384; _gscu_773881060=39059514dcaa0s11; banggoo.nuva.cookie=1|W7xsf|W7xi6; _gscbrs_170533903=1',
'Connection':'keep-alive',
'Upgrade-Insecure-Requests':'1',
'Cache-Control':'max-age=0'}

response = requests.get(url,headers=headers)
# print(response.status_code)
# print(response.encoding)
response1 = response.content.decode('UTF-8')
print(response1)




# print(response.text)
# response = response.content.decode('utf-8', errors='ignore')

# response = response.text.encode('iso-8859-1').decode('utf-8')
# response = response.text.encode('gbk2312').decode('utf-8')

