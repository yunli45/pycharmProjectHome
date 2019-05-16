# encoding=utf-8
import urllib
import  os
import requests
"""
    方法一：
    使用 urllib 模块提供的 urlretrieve() 函数。urlretrieve() 方法直接将远程数据下载到本地。
	
urlretrieve(url, [filename=None, [reporthook=None, [data=None]]])
"""
def Schedule(a,b,c):
    '''''
        a:已经下载的数据块
        b:数据块的大小
        c:远程文件的大小
       '''
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print('%.2f%%' % per)

def requestDwon(url, local_path):

    r = requests.get(url)
    with open(local_path, "wb") as code:
        code.write(r.content)



if __name__ == '__main__':

    url = 'http://xxgk.hainan.gov.cn/qhxxgk/wtj/201901/P020190114624769074502.xls'
    local_path = "E:\行政案例附件\datafolder\海南省\P020190114624769074502.xls"
    # local = url.split('/')[-1]
    # local = os.path.join('E:\行政案例附件\datafolder\海南省', 'P020190114624769074502.xls')
    # urllib.request.urlretrieve(url, local, Schedule)
    requestDwon(url, local_path)