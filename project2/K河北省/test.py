import requests
'''代理IP地址（高匿）'''
proxy = {
    'http': 'http://95.179.135.66:3128',
    # 'http': 'http://120.77.247.147:80',


}
'''head 信息'''
head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
             'Connection': 'keep-alive'}
'''http://icanhazip.com会返回当前的IP地址'''
p = requests.get('http://www.tangshan.gov.cn/zhuzhan/rdxyxxxzcf/', headers=head, proxies=proxy)
gg = p.status_code
print(gg)
# print(p.text)