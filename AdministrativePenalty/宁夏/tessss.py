from win32com import client as wc
word = wc.Dispatch('Word.Application')
doc = word.Documents.Open('e:\\P020171211353795931931.docx')
doc.SaveAs('e:\\test.text', 2)
doc.Close()
word.Quit()