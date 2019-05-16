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
流程：
    1、数据获取：使用爬虫在相关网站上获取文本内容
    2、数据清洗：按一定格式对文本数据进行清洗和提取（文本分类，贴标签）
    3、数据呈现：多维度呈现和解读数据（计算，做表，画图）

分词：
    所谓分词即是将文本序列按完整的意思切分成一个一个的词儿，方便进行下一步的分析（词频统计，情感分析等）。
    
    由于英文词与词自带空格作为分隔符，相比于中文分词要简单的多。我们在做中文分词时，需要把词语从一整段话中筛出来，困难之处在于，汉语表达博大精深，一段话往往有不同的切分方法。
    
    所幸这不是我们需要担心的，Python中的Jieba库提供了现成的解决方案

编写流程：
    1、中文分词（jieba）：先中文分词 ，结果可能不是很理想；添加自己定义的一些名词：
        特殊名词：程序中定义
        户自定义词典：也可以将特殊用词加入用户自定义词典
    2、文本清洗
        切分之后一些特殊的符号会单独成词，这些词会影响我们之后的分析。这里我们可以使用一个标点符号库 stopwords.txt，将切分出来的特殊符号剔除掉。
        对于“了”，“的”这样长度为一的词，显然对我们分析文本没有任何帮助。处理的方法为将长度为1的词全部剔除掉。

备注：   
    (1)、jieba库概述 
    
             jieba是优秀的中文分词第三方库 
    
             - 中文文本需要通过分词获得单个的词语
             - jieba是优秀的中文分词第三方库，需要额外安装
    
             - jieba库提供三种分词模式，最简单只需掌握一个函数
    
      (2)、jieba分词的原理
    
             Jieba分词依靠中文词库 
    
             - 利用一个中文词库，确定汉字之间的关联概率
             - 汉字间概率大的组成词组，形成分词结果
    
             - 除了分词，用户还可以添加自定义的词组
"""
import jieba
from wordcloud import WordCloud
from string import punctuation
import codecs,sys

if sys.getdefaultencoding() != 'utf-8':
    # reload(sys)
    sys.setdefaultencoding('utf-8')

text = "李小璐给王思聪买了微博热搜"
# 切分之前 定义部分特殊名词
jieba.suggest_freq(('微博'), True)
jieba.suggest_freq(('热搜'), True)
"""
# 假如用户自定义的词典，也可以
jieba.load_userdict("./jieba_user_dict.txt")
"""
# result = jieba.cut(text)
# print("切分结果:  "+",".join(result))

# 文本清洗
# 定义要删除的标点等字符
add_punc='，。、【 】 “”：；（）《》‘’{}？！⑦()、%^>℃：.”“^-——=&#@￥'
all_punc=punctuation+add_punc

line_seg = " ".join(jieba.cut(text))
# print(line_seg)
# 移除标点等需要删除的符号
testline=line_seg.split(' ')
te2=[]
for i in testline:
    te2.append(i)
    if i in all_punc:
        te2.remove(i)
# 返回的te2是个list，转换为string后少了空格，因此需要再次分词
# 第二次在仅汉字的基础上再次进行分词
cloud_text = " ".join(jieba.cut(''.join(te2)))

import numpy as np
from PIL import Image
# 加载背景图
# cloud_mask = np.array(Image.open("./h.png"))

#忽略显示的词
st=set(["东西","这是"])

# 绘制图云
# wordcloud = WordCloud(
#     background_color="white", #背景颜色
#     max_words=200, #显示最大词数
#     # font_path="./font/wb.ttf",  #使用字体
#     min_font_size=15,
#     max_font_size=50,
#     width=400,  #图幅宽度
#     stopwords=st
#     )
# wc.generate(cloud_text)
wordcloud = WordCloud(max_font_size=66).generate(cloud_text)
import matplotlib.pyplot as plt
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
# wc.to_file("pic.png")

