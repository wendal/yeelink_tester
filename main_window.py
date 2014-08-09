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
import serial.tools.list_ports
from threading import Thread
import time
import paho.mqtt.client as mqtt

TAG_SELF = "SELF"
TAG_API  = "API"
TAG_MQTT = "MQTT"
TAG_MOCK = "MOCK"

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
        
        self.log_timer = QTimer()
        self.logs = []
        self.log_timer.setInterval(1)
        self.log_timer.start(1)
        self.connect(self.log_timer, SIGNAL("timeout()"), self.append_log)
        
        self.table_data = []
        self.table_timer = QTimer()
        self.table_timer.setInterval(1)
        self.table_timer.start(1)
        self.connect(self.table_timer, SIGNAL("timeout()"), self.table_update)
        
        self.D(TAG_SELF, u"启动完成 . Power by wendal http://wendal.net")
        
    def apikey(self):
        return self.ui_text_uapikey.text()
    
    def devid(self):
        return unicode(self.ui_combo_devid.currentText()).split(" ")[0]
        
    def yeelink_send(self,  uri,  data):
        url = "http://api.yeelink.net/v1.1" + uri
        req = urllib2.Request(url, data)
        req.add_header("U-ApiKey", self.apikey())
        if data :
            self.D(TAG_API, u"POST " + url)
            try :
                self.D(TAG_API, str(data))
            except:
                self.D(TAG_API, u"...")
        else :
            self.D(TAG_API, u"GET " + url)
        try :
            resp = urllib2.urlopen(req)
            self.D(TAG_API, u"resp > %d" % resp.code)
            return resp.read()
        except:
            self.D(TAG_API, u"FAIL" + traceback.format_exc())
            raise
    
    def D(self, TAG, msg):
        self.logs.append(QString("%-5s > %s\r\n" % (TAG, msg)))
        
    def append_log(self):
        tmp = self.logs
        self.logs = []
        if not tmp :
            return
        for p in tmp :
            self.ui_debug_console.moveCursor(QTextCursor.End)
            self.ui_debug_console.insertPlainText(p)
        sb = self.ui_debug_console.verticalScrollBar()
        sb.setValue(sb.maximum())
        
    def table_update(self):
        tmp = self.table_data
        self.table_data = []
        if not tmp :
            return
        for row,column,s in tmp :
            self.ui_table_sensors.setItem(row, column, QTableWidgetItem(s))
    
    def mqtt_sensor_run(self, sensor):
        
        try :
            mqttc = mqtt.Client()
            def on_message(client, userdata, msg):
                self.D(TAG_SELF, "MQTT sensor update %s %s > %s" % (sensor["id"], sensor["title"], str(msg.payload)))
            def on_connect(client, userdata, flags, rc):
                self.D(TAG_SELF, "MQTT Connected with result code "+str(rc))
                topic = "u/%s/v1.1/device/%s/sensor/%s/datapoints" % (self.apikey(), self.devid(), sensor["id"])
                print topic
                mqttc.subscribe([(str(topic), 0), ])
            mqttc.on_message = on_message
            mqttc.on_connect = on_connect
            mqttc.connect("mqtt.yeelink.net")
            
            mqttc.loop_forever()
        except:
            self.D(TAG_SELF, "MQTT FAIL : " + traceback.format_exc())
    
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
                if sensor.get("last_data_gen") :
                    self.ui_table_sensors.setItem(index, 4, QTableWidgetItem(sensor["last_data_gen"]))
                elif sensor.get("last_data") :
                    self.ui_table_sensors.setItem(index, 4, QTableWidgetItem(sensor["last_data"]))
                if sensor.get("last_update") :
                    self.ui_table_sensors.setItem(index, 5, QTableWidgetItem(sensor["last_update"]))
                
                index += 1
                if sensor["type"] == "5" :
                    self.D(TAG_SELF, u"启动MQTT监听 sensor id=%s name=%s" % (sensor["id"], sensor["title"]))
                    t = Thread(target=self.mqtt_sensor_run, name=("Yeelink MQTT id=" + sensor["id"]), args=[sensor])
                    t.setDaemon(True)
                    t.start()
            self.ui_button_get_sensors.setEnabled(False)
            self.ui_combo_devid.setEnabled(False)
            
            coms = sorted(serial.tools.list_ports.comports())
            if coms :
                self.ui_text_com_number.clear()
            for port, _, _ in  coms:
                self.ui_text_com_number.addItem(QString(port))
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
        self.ui_debug_console.clear()
        
    def com_run(self, ser):
        while self.com_reading :
            try :
                line = ser.readline()
                if not line :
                    continue
                line = str(line).strip()
                self.D(ser.port, line)
                self.handle_com_line(ser, line)
            except:
                traceback.print_exc()
            time.sleep(1)
        try :
            if ser.isOpen():
                ser.close()
        except:
            traceback.print_exc()
        self.ui_button_stop_read.setEnabled(False)
        self.ui_button_start_read.setEnabled(True)
        
    def handle_com_line(self, ser, line):
        if not ":" in line :
            self.D(ser.port, "Not match for any sensors")
            return
        tmp = line.split(":", 2)
        if len(tmp) != 2 :
            self.D(ser.port, "Not match for any sensors")
            return
        count = self.ui_table_sensors.rowCount()
        if not count :
            self.D(ser.port, "no sensor at all !!")
            return
        for row_index in range(count) :
            item = self.ui_table_sensors.item(row_index, 3) #匹配数据前缀
            if not item :
                continue
            p = str(item.text())
            if not p or p != str(tmp[0]) :
                self.D(ser.port, "NOT Match %s %s" % (p, tmp[0]))
                continue
            
            item = self.ui_table_sensors.item(row_index, 5) #匹配最后更新时间
            if item :
                t = float(str(item.text()))
                if time.time() - t < 30 :
                    self.D(TAG_API, "Upload Too fast, skip")
                    return
            
            item = self.ui_table_sensors.item(row_index, 0)
            if not item :
                continue
            sensor_id = str(item.text())
            self.yeelink_send("/device/%s/sensor/%s/datapoints" % (self.devid(), sensor_id), """{"value":%s}""" % tmp[1])
            self.table_data.append([row_index, 5, str(time.time())])
            self.table_data.append([row_index, 4, str(tmp[1])])
            return
        self.D(ser.port, "Not match for any sensors")
        
    
    @pyqtSignature("")
    def on_ui_button_start_read_pressed(self):
        """
        Slot documentation goes here.
        """
        try :
            self.D(TAG_SELF, u"尝试打开串口 ... ")
            ser = serial.Serial()
            ser.baudrate = int(str(self.ui_text_com_bitrate.currentText()))
            #ser.bytesize = int(str(self.ui_text_com_databit.currentText()))
            #ser.stopbits = int(str(self.ui_text_com_stopbit.currentText()))
            ser.port = str(self.ui_text_com_number.currentText())
            ser.timeout = 3
            ser.open()
            self.D(TAG_SELF, u"打开串口成功")
            self.ui_button_start_read.setEnabled(False)
            self.ui_button_stop_read.setEnabled(True)
            t = Thread(target=self.com_run, args=[ser], name="Yeelink COM Listener", )
            t.setDaemon(True)
            self.com_reading = True
            t.start()
        except:
            traceback.print_exc()
            self.D(TAG_SELF, u"串口打开识别!!" + traceback.format_exc())

    
    @pyqtSignature("")
    def on_ui_button_stop_read_pressed(self):
        """
        Slot documentation goes here.
        """
        self.D(TAG_SELF, u"触发串口关闭")
        self.com_reading = False
