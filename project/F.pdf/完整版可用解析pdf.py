from wand.image import Image
from PIL import Image as PI
import PIL
import pyocr
import pyocr.builders
import io
import pytesseract

tool = pyocr.get_available_tools()[0]
lang = tool.get_available_languages()[0]

req_image = []
fianl_text  = []

image_pdf = Image(filename=r"F:\环保局\标准文本\1741.pdf",resolution=200)
image_jpeg = image_pdf.convert('jpeg')

for img in image_jpeg.sequence:
    image_page = Image(image=img)
    req_image.append(image_page.make_blob('jpeg'))
for img in req_image:
    txt = pytesseract.image_to_string(PI.open(io.BytesIO(img)),lang=lang )
    # txt = tool.image_to_string(PI.open(io.BytesIO(img)),lang=lang,builder=pyocr.builders.TextBuilder())
    fianl_text.append(txt)
print(fianl_text)