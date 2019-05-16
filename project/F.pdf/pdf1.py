# coding:utf-8
from PIL import Image
import pytesser3
im = Image.open(r"E:\234.png")
print(pytesser3.image_to_string(im))
