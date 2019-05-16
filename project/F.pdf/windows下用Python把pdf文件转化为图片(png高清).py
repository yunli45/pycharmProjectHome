# -*- coding: utf-8 -*-
"""
1、安装库  pip install pymupdf
2、直接运行
3 、来源  https://blog.csdn.net/qq_43145035/article/details/83270501
"""
import fitz

#  打开PDF文件，生成一个对象
doc = fitz.open(r'F:\环保局\标准文本\1741.pdf')

for pg in range(doc.pageCount):
    page = doc[pg]
    rotate = int(0)
    # 每个尺寸的缩放系数为2，这将为我们生成分辨率提高四倍的图像。
    zoom_x = 2.0
    zoom_y = 2.0
    trans = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
    pm = page.getPixmap(matrix=trans, alpha=False)
    pm.writePNG('%s.png' % pg)
