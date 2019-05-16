# coding = utf-8
from queue import Queue
# from threading import Thread
import threading
import time
import requests
from bs4 import BeautifulSoup
from lxml import etree

class DouBanSpider(threading.Thread):
    def __init__(self, url, q):
        # 重写父类的 __init__ 方法
        super(DouBanSpider, self).__init__()
        self.url = url
        self.q = q
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36'
        }

    def run(self):
        self.parse_page()

    def send_request(self, url):
        '''
        用来发送请求的方法
        :return: 返回网页源码
        '''
        # 请求出错时，重复请求３次,
        i = 0
        while i <= 3:
            try:
                print(u"[INFO]请求url:" + url)
                html = requests.get(url=url, headers=self.headers).content
            except Exception as e:
                print(u'[INFO] %s%s' % (e, url))
                i += 1
            else:
                return html

    def parse_page(self):
        response = self.send_request(self.url)
        html = etree.HTML(response)
        node_list = html.xpath("//div[@class='info']")
        for move in node_list :
            # 电影名称
            title = move.xpath('.//a/span/text()')[0]
            # 评分
            score = move.xpath('.//div[@class="bd"]//span[@class="rating_num"]/text()')[0]
            # 将每一部电影的名称跟评分加入到队列
            self.q.put(score + "\t" + title)
def main():
    # 创建一个队列用来保存进程获取到的数据
    q = Queue()
    base_url = 'https://movie.douban.com/top250?start='
    # 构造所有ｕｒｌ
    url_list = [base_url + str(num) for num in range(0, 225 + 1, 25)]
    # 保存线程
    Thread_list = []
    # 创建新的并启动线程 （根据每一页来创建一个新的线程）
    for url in url_list:
        thread  = DouBanSpider(url, q)
        thread.start()
        Thread_list.append(thread )
    print("线程："+str(len(Thread_list)))
    # 让主线程等待子线程执行完成
    for i in Thread_list:
        i.join()
    while not q.empty():
        print(q.get())


if __name__ == "__main__":
    start = time.time()
    main()
    print('[info]耗时：%s' % (time.time() - start))