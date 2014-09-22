# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'I:\python_job\yeelink_api_test.ui'
#
# Created: Mon Sep 22 09:25:54 2014
#      by: PyQt4 UI code generator 4.11.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(802, 848)
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 20, 72, 15))
        self.label.setObjectName(_fromUtf8("label"))
        self.ui_text_uapikey = QtGui.QLineEdit(Dialog)
        self.ui_text_uapikey.setGeometry(QtCore.QRect(130, 20, 651, 21))
        self.ui_text_uapikey.setObjectName(_fromUtf8("ui_text_uapikey"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 72, 15))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 100, 81, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.ui_text_file_path = QtGui.QLineEdit(Dialog)
        self.ui_text_file_path.setGeometry(QtCore.QRect(130, 100, 571, 21))
        self.ui_text_file_path.setObjectName(_fromUtf8("ui_text_file_path"))
        self.ui_button_select_file = QtGui.QPushButton(Dialog)
        self.ui_button_select_file.setGeometry(QtCore.QRect(720, 100, 61, 28))
        self.ui_button_select_file.setObjectName(_fromUtf8("ui_button_select_file"))
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 140, 641, 281))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.ui_text_data = QtGui.QPlainTextEdit(self.groupBox)
        self.ui_text_data.setGeometry(QtCore.QRect(10, 20, 621, 251))
        self.ui_text_data.setObjectName(_fromUtf8("ui_text_data"))
        self.ui_button_send_file = QtGui.QPushButton(Dialog)
        self.ui_button_send_file.setGeometry(QtCore.QRect(662, 150, 131, 28))
        self.ui_button_send_file.setObjectName(_fromUtf8("ui_button_send_file"))
        self.ui_button_send_text = QtGui.QPushButton(Dialog)
        self.ui_button_send_text.setGeometry(QtCore.QRect(660, 190, 131, 28))
        self.ui_button_send_text.setObjectName(_fromUtf8("ui_button_send_text"))
        self.ui_button_send_text_hex = QtGui.QPushButton(Dialog)
        self.ui_button_send_text_hex.setEnabled(False)
        self.ui_button_send_text_hex.setGeometry(QtCore.QRect(662, 250, 131, 28))
        self.ui_button_send_text_hex.setCheckable(False)
        self.ui_button_send_text_hex.setObjectName(_fromUtf8("ui_button_send_text_hex"))
        self.ui_button_send = QtGui.QPushButton(Dialog)
        self.ui_button_send.setGeometry(QtCore.QRect(662, 300, 131, 28))
        self.ui_button_send.setObjectName(_fromUtf8("ui_button_send"))
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 430, 641, 411))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.ui_text_output = QtGui.QPlainTextEdit(self.groupBox_2)
        self.ui_text_output.setGeometry(QtCore.QRect(10, 30, 621, 371))
        self.ui_text_output.setObjectName(_fromUtf8("ui_text_output"))
        self.ui_text_url = QtGui.QComboBox(Dialog)
        self.ui_text_url.setGeometry(QtCore.QRect(130, 60, 651, 22))
        self.ui_text_url.setEditable(True)
        self.ui_text_url.setObjectName(_fromUtf8("ui_text_url"))
        self.ui_button_send_delete = QtGui.QPushButton(Dialog)
        self.ui_button_send_delete.setGeometry(QtCore.QRect(660, 430, 131, 28))
        self.ui_button_send_delete.setObjectName(_fromUtf8("ui_button_send_delete"))
        self.ui_button_send_text_put = QtGui.QPushButton(Dialog)
        self.ui_button_send_text_put.setGeometry(QtCore.QRect(660, 480, 131, 28))
        self.ui_button_send_text_put.setObjectName(_fromUtf8("ui_button_send_text_put"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Yeelink API测试", None))
        self.label.setText(_translate("Dialog", "U-ApiKey", None))
        self.label_2.setText(_translate("Dialog", "网址", None))
        self.label_3.setText(_translate("Dialog", "数据文件", None))
        self.ui_button_select_file.setText(_translate("Dialog", "选取", None))
        self.groupBox.setTitle(_translate("Dialog", "数据", None))
        self.ui_button_send_file.setText(_translate("Dialog", "发送文件(POST)", None))
        self.ui_button_send_text.setText(_translate("Dialog", "发送文本(POST)", None))
        self.ui_button_send_text_hex.setText(_translate("Dialog", "发送文本hex(POST)", None))
        self.ui_button_send.setText(_translate("Dialog", "仅发送(GET)", None))
        self.groupBox_2.setTitle(_translate("Dialog", "调试信息", None))
        self.ui_button_send_delete.setText(_translate("Dialog", "仅发送(DELETE)", None))
        self.ui_button_send_text_put.setText(_translate("Dialog", "发送文本(PUT)", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

