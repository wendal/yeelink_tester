# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'I:\python_job\main_window.ui'
#
# Created: Wed Sep 10 13:02:56 2014
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1160, 843)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.groupBox = QtGui.QGroupBox(self.centralWidget)
        self.groupBox.setGeometry(QtCore.QRect(870, 10, 281, 351))
        self.groupBox.setAutoFillBackground(True)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.ui_text_com_bitrate = QtGui.QComboBox(self.groupBox)
        self.ui_text_com_bitrate.setGeometry(QtCore.QRect(100, 90, 87, 22))
        self.ui_text_com_bitrate.setEditable(True)
        self.ui_text_com_bitrate.setObjectName(_fromUtf8("ui_text_com_bitrate"))
        self.ui_text_com_bitrate.addItem(_fromUtf8(""))
        self.ui_text_com_checkbit = QtGui.QComboBox(self.groupBox)
        self.ui_text_com_checkbit.setGeometry(QtCore.QRect(100, 130, 87, 22))
        self.ui_text_com_checkbit.setObjectName(_fromUtf8("ui_text_com_checkbit"))
        self.ui_text_com_checkbit.addItem(_fromUtf8(""))
        self.ui_text_com_checkbit.addItem(_fromUtf8(""))
        self.ui_text_com_checkbit.addItem(_fromUtf8(""))
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(30, 130, 72, 15))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.ui_button_stop_read = QtGui.QPushButton(self.groupBox)
        self.ui_button_stop_read.setEnabled(False)
        self.ui_button_stop_read.setGeometry(QtCore.QRect(30, 280, 181, 31))
        self.ui_button_stop_read.setObjectName(_fromUtf8("ui_button_stop_read"))
        self.ui_text_com_number = QtGui.QComboBox(self.groupBox)
        self.ui_text_com_number.setGeometry(QtCore.QRect(100, 50, 87, 22))
        self.ui_text_com_number.setEditable(True)
        self.ui_text_com_number.setObjectName(_fromUtf8("ui_text_com_number"))
        self.ui_text_com_number.addItem(_fromUtf8(""))
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(30, 170, 72, 15))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.ui_text_com_databit = QtGui.QComboBox(self.groupBox)
        self.ui_text_com_databit.setGeometry(QtCore.QRect(100, 170, 87, 22))
        self.ui_text_com_databit.setObjectName(_fromUtf8("ui_text_com_databit"))
        self.ui_text_com_databit.addItem(_fromUtf8(""))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(30, 50, 72, 15))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.ui_text_com_stopbit = QtGui.QComboBox(self.groupBox)
        self.ui_text_com_stopbit.setGeometry(QtCore.QRect(100, 210, 87, 22))
        self.ui_text_com_stopbit.setObjectName(_fromUtf8("ui_text_com_stopbit"))
        self.ui_text_com_stopbit.addItem(_fromUtf8(""))
        self.ui_text_com_stopbit.addItem(_fromUtf8(""))
        self.label_7 = QtGui.QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(30, 210, 72, 15))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.ui_button_start_read = QtGui.QPushButton(self.groupBox)
        self.ui_button_start_read.setEnabled(False)
        self.ui_button_start_read.setGeometry(QtCore.QRect(30, 240, 181, 31))
        self.ui_button_start_read.setObjectName(_fromUtf8("ui_button_start_read"))
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(30, 90, 72, 15))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.groupBox_2 = QtGui.QGroupBox(self.centralWidget)
        self.groupBox_2.setGeometry(QtCore.QRect(870, 380, 281, 251))
        self.groupBox_2.setAutoFillBackground(True)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.comboBox = QtGui.QComboBox(self.groupBox_2)
        self.comboBox.setGeometry(QtCore.QRect(60, 60, 87, 22))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.ui_spin_mock_port = QtGui.QSpinBox(self.groupBox_2)
        self.ui_spin_mock_port.setGeometry(QtCore.QRect(60, 30, 50, 22))
        self.ui_spin_mock_port.setMinimum(80)
        self.ui_spin_mock_port.setMaximum(9999)
        self.ui_spin_mock_port.setObjectName(_fromUtf8("ui_spin_mock_port"))
        self.label_12 = QtGui.QLabel(self.groupBox_2)
        self.label_12.setGeometry(QtCore.QRect(10, 30, 72, 15))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.label_13 = QtGui.QLabel(self.groupBox_2)
        self.label_13.setGeometry(QtCore.QRect(10, 60, 72, 15))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.ui_button_mock_start = QtGui.QPushButton(self.groupBox_2)
        self.ui_button_mock_start.setGeometry(QtCore.QRect(30, 110, 181, 28))
        self.ui_button_mock_start.setObjectName(_fromUtf8("ui_button_mock_start"))
        self.ui_button_mock_stop = QtGui.QPushButton(self.groupBox_2)
        self.ui_button_mock_stop.setEnabled(False)
        self.ui_button_mock_stop.setGeometry(QtCore.QRect(30, 150, 181, 28))
        self.ui_button_mock_stop.setObjectName(_fromUtf8("ui_button_mock_stop"))
        self.groupBox_3 = QtGui.QGroupBox(self.centralWidget)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 10, 851, 351))
        self.groupBox_3.setAutoFillBackground(True)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.ui_text_uapikey = QtGui.QLineEdit(self.groupBox_3)
        self.ui_text_uapikey.setGeometry(QtCore.QRect(110, 30, 461, 21))
        self.ui_text_uapikey.setObjectName(_fromUtf8("ui_text_uapikey"))
        self.ui_button_save_config = QtGui.QPushButton(self.groupBox_3)
        self.ui_button_save_config.setEnabled(False)
        self.ui_button_save_config.setGeometry(QtCore.QRect(720, 30, 101, 31))
        self.ui_button_save_config.setObjectName(_fromUtf8("ui_button_save_config"))
        self.ui_button_get_sensors = QtGui.QPushButton(self.groupBox_3)
        self.ui_button_get_sensors.setEnabled(False)
        self.ui_button_get_sensors.setGeometry(QtCore.QRect(590, 70, 121, 31))
        self.ui_button_get_sensors.setObjectName(_fromUtf8("ui_button_get_sensors"))
        self.ui_button_check_api = QtGui.QPushButton(self.groupBox_3)
        self.ui_button_check_api.setGeometry(QtCore.QRect(590, 30, 121, 31))
        self.ui_button_check_api.setStyleSheet(_fromUtf8(""))
        self.ui_button_check_api.setCheckable(False)
        self.ui_button_check_api.setObjectName(_fromUtf8("ui_button_check_api"))
        self.label_8 = QtGui.QLabel(self.groupBox_3)
        self.label_8.setGeometry(QtCore.QRect(10, 100, 81, 16))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.label_10 = QtGui.QLabel(self.groupBox_3)
        self.label_10.setGeometry(QtCore.QRect(10, 70, 72, 15))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.ui_table_sensors = QtGui.QTableWidget(self.groupBox_3)
        self.ui_table_sensors.setGeometry(QtCore.QRect(10, 130, 831, 201))
        self.ui_table_sensors.setShowGrid(True)
        self.ui_table_sensors.setCornerButtonEnabled(True)
        self.ui_table_sensors.setRowCount(5)
        self.ui_table_sensors.setColumnCount(7)
        self.ui_table_sensors.setObjectName(_fromUtf8("ui_table_sensors"))
        item = QtGui.QTableWidgetItem()
        self.ui_table_sensors.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.ui_table_sensors.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.ui_table_sensors.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.ui_table_sensors.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.ui_table_sensors.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.ui_table_sensors.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.ui_table_sensors.setHorizontalHeaderItem(6, item)
        self.ui_table_sensors.verticalHeader().setVisible(False)
        self.label_2 = QtGui.QLabel(self.groupBox_3)
        self.label_2.setGeometry(QtCore.QRect(10, 30, 72, 15))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.ui_combo_devid = QtGui.QComboBox(self.groupBox_3)
        self.ui_combo_devid.setGeometry(QtCore.QRect(110, 70, 291, 22))
        self.ui_combo_devid.setObjectName(_fromUtf8("ui_combo_devid"))
        self.ui_button_api_test = QtGui.QPushButton(self.groupBox_3)
        self.ui_button_api_test.setGeometry(QtCore.QRect(720, 70, 101, 28))
        self.ui_button_api_test.setObjectName(_fromUtf8("ui_button_api_test"))
        self.groupBox_4 = QtGui.QGroupBox(self.centralWidget)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 380, 851, 451))
        self.groupBox_4.setAutoFillBackground(True)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.ui_debug_console = QtGui.QTextEdit(self.groupBox_4)
        self.ui_debug_console.setGeometry(QtCore.QRect(30, 60, 801, 381))
        self.ui_debug_console.setObjectName(_fromUtf8("ui_debug_console"))
        self.ui_button_clear_debug = QtGui.QPushButton(self.groupBox_4)
        self.ui_button_clear_debug.setGeometry(QtCore.QRect(650, 20, 181, 28))
        self.ui_button_clear_debug.setObjectName(_fromUtf8("ui_button_clear_debug"))
        self.ui_button_help = QtGui.QPushButton(self.centralWidget)
        self.ui_button_help.setGeometry(QtCore.QRect(950, 720, 93, 28))
        self.ui_button_help.setObjectName(_fromUtf8("ui_button_help"))
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Yeelink API调试工具 v1.1 by wendal.net", None))
        self.groupBox.setTitle(_translate("MainWindow", "串口", None))
        self.ui_text_com_bitrate.setItemText(0, _translate("MainWindow", "9600", None))
        self.ui_text_com_checkbit.setItemText(0, _translate("MainWindow", "NONE", None))
        self.ui_text_com_checkbit.setItemText(1, _translate("MainWindow", "ODD", None))
        self.ui_text_com_checkbit.setItemText(2, _translate("MainWindow", "NDD", None))
        self.label_5.setText(_translate("MainWindow", "校验位", None))
        self.ui_button_stop_read.setText(_translate("MainWindow", "停止读取", None))
        self.ui_text_com_number.setItemText(0, _translate("MainWindow", "COM2", None))
        self.label_6.setText(_translate("MainWindow", "数据位", None))
        self.ui_text_com_databit.setItemText(0, _translate("MainWindow", "8", None))
        self.label_3.setText(_translate("MainWindow", "端口", None))
        self.ui_text_com_stopbit.setItemText(0, _translate("MainWindow", "1", None))
        self.ui_text_com_stopbit.setItemText(1, _translate("MainWindow", "2", None))
        self.label_7.setText(_translate("MainWindow", "停止位", None))
        self.ui_button_start_read.setText(_translate("MainWindow", "开始读取", None))
        self.label_4.setText(_translate("MainWindow", "波特率", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "API调试服务器", None))
        self.comboBox.setItemText(0, _translate("MainWindow", "标准服务", None))
        self.comboBox.setItemText(1, _translate("MainWindow", "仅显示", None))
        self.label_12.setText(_translate("MainWindow", "端口", None))
        self.label_13.setText(_translate("MainWindow", "类型", None))
        self.ui_button_mock_start.setText(_translate("MainWindow", "开始", None))
        self.ui_button_mock_stop.setText(_translate("MainWindow", "停止", None))
        self.groupBox_3.setTitle(_translate("MainWindow", "Yeelink信息", None))
        self.ui_text_uapikey.setText(_translate("MainWindow", "Your-ApiKey", None))
        self.ui_button_save_config.setText(_translate("MainWindow", "保存配置", None))
        self.ui_button_get_sensors.setText(_translate("MainWindow", "获取传感器列表", None))
        self.ui_button_check_api.setText(_translate("MainWindow", "检查密钥", None))
        self.label_8.setText(_translate("MainWindow", "传感器列表", None))
        self.label_10.setText(_translate("MainWindow", "设备id", None))
        item = self.ui_table_sensors.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "传感器id", None))
        item = self.ui_table_sensors.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "传感器名称", None))
        item = self.ui_table_sensors.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "类型", None))
        item = self.ui_table_sensors.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "最新值", None))
        item = self.ui_table_sensors.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "数据上传", None))
        item = self.ui_table_sensors.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "数据读取", None))
        item = self.ui_table_sensors.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "最后更新时间", None))
        self.label_2.setText(_translate("MainWindow", "U-ApiKey", None))
        self.ui_button_api_test.setText(_translate("MainWindow", "API测试", None))
        self.groupBox_4.setTitle(_translate("MainWindow", "调试信息", None))
        self.ui_button_clear_debug.setText(_translate("MainWindow", "清空调试信息", None))
        self.ui_button_help.setText(_translate("MainWindow", "帮助", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

