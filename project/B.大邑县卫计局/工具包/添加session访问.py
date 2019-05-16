import requests
from fake_useragent import UserAgent
ua = UserAgent()
print(ua.random)
headers = {"User-Agent": ua.random}

url = 'http://www.nhfpc.gov.cn/zwgk/jdjd/ejlist.shtml'

jar = requests.cookies.RequestsCookieJar()
# 不加cookie会返回202状态吗
jar.set(name='banggoo.nuva.cookie', value='1|W71xc|W71xb',path='/', domain='www.nhfpc.gov.cn')
r = requests.get(url, headers=headers, cookies=jar)
print(r.status_code)
print(r.encoding)
# 修改编码
r.encoding = 'utf-8'
print(r.text)
print(r.encoding)


