import cv2
from PIL import Image
import sys

import pyocr
import pyocr.builders
import pyocr.libtesseract

filename = r"E:\Python\PyCharm\project\project1\0.png"

tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
# The tools are returned in the recommended order of usage
tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))
# Ex: Will use tool 'libtesseract'

langs = tool.get_available_languages()
print("Available languages: %s" % ", ".join(langs))
lang = langs[0]
print("Will use lang '%s'" % (lang))

word_boxes = pyocr.libtesseract.image_to_string(Image.open(filename),lang='eng',builder=pyocr.builders.WordBoxBuilder())
# word_boxes = tool.image_to_string(
#     Image.open(filename),
#     lang="eng",
#     builder=pyocr.builders.WordBoxBuilder()
# )

for item in word_boxes:
    print(item)