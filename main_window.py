# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from Ui_main_window import Ui_MainWindow
import urllib2
import json
import traceback

sensor_type_map = {
                   "0" : u"数值型",
                   "9" : u"图像型",
                   "5" : u"开关型",
                   "6" : u"GPS型",
                   "8" : u"泛型"
                   }

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.ui_table_sensors
        
    def apikey(self):
        return self.ui_text_uapikey.text()
    
    def devid(self):
        return unicode(self.ui_combo_devid.currentText()).split(" ")[0]
        
    def yeelink_send(self,  uri,  data):
        url = "http://api.yeelink.net/v1.1" + uri
        req = urllib2.Request(url, data)
        req.add_header("U-ApiKey", self.apikey())
        resp = urllib2.urlopen(req)
        if resp.code == 200 :
            return str(resp.read())
        raise UserWarning("bad resp code = %d" % resp.code)
        
    
    @pyqtSignature("")
    def on_ui_button_help_pressed(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        QMessageBox.about(self,  u"帮助",  "http://wendal.net")
    
    @pyqtSignature("")
    def on_ui_button_check_api_pressed(self):
        """
        Slot documentation goes here.
        """
        try :
            re = json.loads(self.yeelink_send("/devices", None))
            if not re :
                QMessageBox.about(self,  u"无可用设备",  u"该密钥下的帐号无任何设备")
                return
            self.ui_combo_devid.clear()
            for dev in re :
                print dev
                self.ui_combo_devid.addItem(QString("%s %s" % (dev["id"], dev["title"])))
            self.ui_button_get_sensors.setEnabled(True)
            self.ui_button_start_read.setEnabled(True)
            self.ui_button_check_api.setEnabled(False)
            self.ui_text_uapikey.setEnabled(False)
        except:
            traceback.print_exc()
            QMessageBox.about(self,  u"密钥错误",  u"密钥不对: " + self.apikey())
    
    @pyqtSignature("")
    def on_ui_button_get_sensors_pressed(self):
        """
        Slot documentation goes here.
        """
        try :
            print self.devid()
            sensors = json.loads(self.yeelink_send("/device/%s/sensors" % self.devid(), None))
            self.ui_table_sensors.setRowCount(len(sensors))
            index = 0
            for sensor in sensors :
                print sensor
                self.ui_table_sensors.setItem(index, 0, QTableWidgetItem(sensor["id"]))
                self.ui_table_sensors.setItem(index, 1, QTableWidgetItem(sensor["title"]))
                sensor_type = sensor_type_map.get(str(sensor["type"]))
                if not sensor_type :
                    sensor_type = "其他类型"
                self.ui_table_sensors.setItem(index, 2, QTableWidgetItem(sensor_type))
                index += 1
                if sensor["type"] == "5" :
                    self.ui_button_start_mqtt.setEnabled(True)
            self.ui_button_get_sensors.setEnabled(False)
            self.ui_combo_devid.setEnabled(False)
        except:
            traceback.print_exc()
            self.msgbox_err(u"获取失败" + self.apikey())

    def msgbox_err(self, msg):
        QMessageBox.about(self,  u"出错了!!",  msg)
        
    def msgbox(self, title, msg):
        QMessageBox.about(self,  title,  msg)
    
    @pyqtSignature("")
    def on_ui_button_clear_debug_pressed(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.ui_debug_console.clear()
