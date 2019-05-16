# from wand.image import Image
from PIL import Image
import pyocr.builders
import pyocr.libtesseract
import io
import pyocr
import pytesseract
import sys


tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
# The tools are returned in the recommended order of usage
tool = tools[0]
print("will use tool '%s'"%(tool.get_name()))
# Ex: Will use tool 'libtesseract'
# # tool = pyocr.libtesseract
langs = tool.get_available_languages()
print("Available languages ：%s"%",".join(langs))
# i have langs : chi_sim,eng,equ,osd ,so we will use chi_sim
lang = langs[0]
print("Will use lang '%s'"%(lang))

filename =r"E:\Python\PyCharm\project\project1\0.png"
word_boxes = tool.image_to_string(
    Image.open(filename),
    lang="eng",
    builder=pyocr.builders.WordBoxBuilder()
)

for item in word_boxes:
    print(item)







req_image = []
final_text = []




# image_pdf = Image(filename=r"E:\Python\PyCharm\project\project1\0.png",resolution=300)
# image_jepg = image_pdf.convert('jpeg')
# # print("image_jepg"+str(image_jepg))
# for img in image_jepg.sequence:
#     img_page = Image(image=img)
#     req_image.append(img_page.make_blob('jpeg'))
#
# # 为每个图像运行OCR，识别图像中的文本
# for img in req_image:
#     # print(img)
#     # txt = pytesseract.image_to_string(
#     #     PI.open(io.BytesIO(img)),
#     #     lang=lang, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'
#     # )
#     txt = tool.image_to_string(
#         PI.open(io.BytesIO(img)),
#         lang=lang,
#         builder=pyocr.builders.WordBoxBuilder()
#     )
#
#     final_text.append(txt)
# print(final_text)