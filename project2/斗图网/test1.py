# coding = utf-8
import threading
import time
import requests

class myThread(threading.Thread):
    def __init__(self, url, q):
        threading.Thread.__init__(self) # 重写写父类的__init__方法
        # super(myThread, self).__init__() # 重写写父类的__init__
        self.url = url
        self.q = q
    def run(self):
        self.parse_page()

    def
