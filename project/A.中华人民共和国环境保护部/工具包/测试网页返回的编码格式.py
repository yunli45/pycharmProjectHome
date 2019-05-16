# coding:UTF-8
import requests

url = 'http://kjs.mee.gov.cn/hjbhbz/bzwb/jcffbz/200703/t20070316_101690.shtml'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10-12.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}
response = requests.get(url,headers=headers,timeout=1)
print(response.status_code)
# print(response.text)
# print(response.status_code)
# print(response.encoding)
print(response.content.decode('utf-8'))
# print(response)





# print(response.text)


# response = response.text.encode('iso-8859-1').decode('utf-8')
# response = response.text.encode('gbk2312').decode('utf-8')

