# -*- coding: utf-8 -*-
"""
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
import glob
import os
import threading
from PIL import Image


def create_image(infile, index):
  os.path.splitext(infile)
  im = Image.open(infile)
  # im.save("D:/微信/project1/GHApp/pages/image/webp_" + str(index) + ".webp", "WEBP")
  im.save("D:/微信/project1/GHApp/pages/image/webp_" + str(index) + ".webp", "WEBP")



def start():
  index = 0
  for infile in glob.glob("D:/微信/project1/GHApp/pages/image/*.png"):
    t = threading.Thread(target=create_image, args=(infile, index,))
    t.start()
    t.join()
    index += 1

if __name__ == "__main__":
  start()

