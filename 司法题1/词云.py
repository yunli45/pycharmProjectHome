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
"""
Minimal Example
===============
使用默认参数生成方形的词云

"""
from wordcloud import WordCloud
from os import path

d = path.dirname(__file__)

# 读取整个文本
text = open(path.join(d, "Alice.txt")).read()

# 生成词云图像
# wordcloud = WordCloud.generate(text)

# matplotlib的方式展示生成的词云图像
import matplotlib.pyplot as plt
# plt.imshow(wordcloud, interpolation="bilinear")  # 展示
# plt.axis("off")

#max_font_size设定生成词云中的文字最大大小
#width,height,margin可以设置图片属性
# generate 可以对全部文本进行自动分词,但是他对中文支持不好

wordcloud = WordCloud(max_font_size=66).generate(text)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

#保存到本地
wordcloud.to_file(path.join(d, "alice.png"))

# pil方式展示生成的词云图像（如果你没有matplotlib）
# image = wordcloud.to_image()
# image.show()
