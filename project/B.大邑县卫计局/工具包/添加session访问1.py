import requests

from fake_useragent import UserAgent
url = "http://www.nhfpc.gov.cn//zwgk/jdjd/201809/9eb3f794162046a3a9305f5bd1fe9cc4.shtml"
# url = 'http://www.nhfpc.gov.cn/zwgk/jdjd/ejlist.shtml'
# cookie_jar = RequestsCookieJar()
# cookie_jar.set("banggoo.nuva.cookie", "3|W71Pw|W71MH", domain="http://61.49.18.66:80", path='/')
# res = requests.get(url, cookies=cookie_jar)
# print(res.text)
# print (res.status_code)

ua = UserAgent()
header  =  {"User-Agent": ua.random}
jar = requests.cookies.RequestsCookieJar()
# 不加cookie会返回202状态吗
jar.set(name='banggoo.nuva.cookie', value='1|W71xc|W71xb', path='/', domain='www.nhfpc.gov.cn')
cookies = jar
response = requests.get(url,headers= header,cookies= cookies)
response = response.content.decode('utf-8', errors='ignore')
print(response)