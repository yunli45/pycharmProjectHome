import requests
from requests.cookies import RequestsCookieJar

url = "http://www.nhfpc.gov.cn/zwgk/jdjd/ejlist.shtml"
# url = "https://fanyi.baidu.com"
# res = requests.get(url)
# print(res.cookies)

cookie_jar = RequestsCookieJar()
cookie_jar.set("banggoo.nuva.cookie", "1|W8AJX|W8AJX", domain="www.nhfpc.gov.cn")

res = requests.get(url, cookies=cookie_jar)
print(res.content.decode('utf-8', errors='ignore'))
print(res.status_code)















