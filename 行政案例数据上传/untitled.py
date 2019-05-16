# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setEnabled(True)
        Form.resize(781, 521)
        font = QtGui.QFont()
        font.setPointSize(10)
        Form.setFont(font)
        Form.setToolTip("")
        self.textEdit = QtWidgets.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(50, 50, 671, 241))
        self.textEdit.setObjectName("textEdit")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(100, 340, 111, 51))
        self.pushButton.setCheckable(False)
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "温馨提示"))
        self.textEdit.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'宋体\'; font-size:14pt; color:#f8f8f2;\">  </span><span style=\" font-family:\'宋体\'; font-size:14pt; color:#000000;\"> </span><span style=\" font-family:\'宋体\'; color:#000000;\">这是第一次检查并处理数据表中的标签问题，并将预处理后的全文保存会原数据表，对于本次检查出有关附件的问题全都保存到相关excel中了，请手动处理表格中的问题，处理完了，再次运行</span><span style=\" font-family:\'Consolas\'; font-size:9.4pt; color:#a6e22e;\">upload_to_database</span><span style=\" font-family:\'Consolas\'; font-size:9.4pt; color:#000000;\">函数就好了</span><span style=\" font-family:\'宋体\'; font-size:14pt; color:#f8f8f2;\"><br />附件不在链接修改了<br />附件存在链接没改</span></p></body></html>"))
        self.pushButton.setText(_translate("Form", "OK"))
        pushButton()


def main():
    import sys
    from PyQt5.QtGui import QIcon
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(widget)
    widget.setWindowIcon(QIcon('smail.png'))  # 增加icon图标，如果没有图片可以没有这句
    widget.show()
    sys.exit(app.exec_())

if __name__=="__main__":
    main()
