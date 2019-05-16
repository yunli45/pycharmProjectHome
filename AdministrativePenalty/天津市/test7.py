# coding:utf-8
# from urllib import request
#
import requests
url = 'http://scjg.tj.gov.cn/heping/zwgk/xzcfxx/index.html'
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
# 需要使用url和headers生成一个Request对象，然后将其传入urlopen方法中

response = requests.get(url, headers=headers)
response = response.content.decode('UTF-8')
print(response)

# from urllib import request
#
# url = 'http://ly.tj.gov.cn/UploadedFiles/image/20150113/709_%E9%A1%B5%E9%9D%A2_1.jpg'
# request.urlretrieve(url, 'pytho.jpg')