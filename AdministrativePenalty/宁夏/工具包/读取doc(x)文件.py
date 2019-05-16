from win32com import client
def doc2docx(doc_name,docx_name):
    """
    :doc转docx
    """
    try:
        # 首先将doc转换成docx
        word = client.Dispatch("Word.Application")
        doc = word.Documents.Open(doc_name)
        #使用参数16表示将doc转换成docx
        doc.SaveAs(docx_name,16)
        doc.Close()
        word.Quit()
    except:
        pass
# if __name__ == '__main__':
#     doc2docx('E:\Python\PyCharm\project\AdministrativePenalty\宁夏\ggs.doc','E:\Python\PyCharm\project\AdministrativePenalty\宁夏\ggs.docx')
#coding:utf-8
import docx
from docx2html import convert
import HTMLParser
def  docx2html(docx_name,new_name):
    """
    :docx转html
    """
    try:
        #读取word内容
        doc = docx.Document(docx_name,new_name)
        data = doc.paragraphs[0].text
        # 转换成html
        html_parser = HTMLParser.HTMLParser()
        #使用docx2html模块将docx文件转成html串，随后你想干嘛都行
        html = convert(new_name)
        #docx2html模块将中文进行了转义，需要将生成的字符串重新转义
        return html_parser.enescape(html)
    except:
        pass
if __name__ == '__main__':
    docx2html('f:/test.docx','f:/test1.docx')