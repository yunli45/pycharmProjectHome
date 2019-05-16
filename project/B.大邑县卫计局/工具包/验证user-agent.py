'''

判断user-agent,判断是否是正常浏览器访问
'''
from urllib import request

base_url = "http://www.langlang2017.com"

headers = {
    "connnction":"keep-alive",
    "USer_Agent":"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36"
}
req = request.Request(base_url,headers=headers)
#req在封装的时候，每个浏览器对键的书写进行规范，

user_agent  = req.get_header("User_agent")
#有时候若无法取出键值对的值，看req.headers里面的键是怎么写的，各浏览器可能有区别
conn=req.get_header('Connnction')
print(req.headers)
# print(headers['USer_Agent'])
print(conn)

if user_agent:
    print("是浏览器访问")
else:
    print("不是浏览请求！")

