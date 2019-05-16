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

def public_down(url, save_path):
    # try:
    r = requests.get(url)
    with open(save_path, "wb") as f:
        f.write(r.content)
    f.close()


# if __name__ == '__main__':
#
#     url = 'http://www.nhc.gov.cn/yzygj/hlykfc/201904/dd54d946806745f6a1df914fe0642ea3/files/be28f522d6d242e38b4926c1e7362549.doc'
#     local_path =r"E:\自收录数据\datafolder\卫计局\卫生计生政策法规解读\be28f522d6d242e38b4926c1e7362549.doc"
#     # local = url.split('/')[-1]
#     # local = os.path.join('E:\行政案例附件\datafolder\海南省', 'P020190114624769074502.xls')
#     # urllib.request.urlretrieve(url, local, Schedule)
#     public_down(url, local_path)