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

SENSOR_COLUMN_ID = 0
SENSOR_COLUMN_NAME = 1
SENSOR_COLUMN_TYPE = 2
SENSOR_COLUMN_VALUE = 3
SENSOR_COLUMN_DATA_READ = 4
SENSOR_COLUMN_DATA_WRITE = 5
SENSOR_COLUMN_UPDATE_TIME = 6

SENSOR_TYPE_NUMBER = "0"
SENSOR_TYPE_GPS = "6"
SENSOR_TYPE_IMAGE = "9"
SENSOR_TYPE_SWITCH = "5"
SENSOR_TYPE_RAW = "8"

sensor_type_map = {
                   SENSOR_TYPE_NUMBER : u"数值型",
                   SENSOR_TYPE_IMAGE : u"图像型",
                   SENSOR_TYPE_SWITCH : u"开关型",
                   SENSOR_TYPE_GPS : u"GPS型",
                   SENSOR_TYPE_RAW : u"泛型"
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
                try :
                    re = json.loads(msg.payload)
                    s = "m:%s:%s" % (re["sensor_id"], re["value"])
                    self.D(self.ser.port, s)
                    self.ser.write(s + "\n")
                except:
                    traceback.print_exc()
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
            #print self.devid()
            sensors = json.loads(self.yeelink_send("/device/%s/sensors" % self.devid(), None))
            self.ui_table_sensors.setRowCount(len(sensors))
            index = 0
            for sensor in sensors :
                sensor["row_index"] = index
                self.ui_table_sensors.setItem(index, SENSOR_COLUMN_ID, QTableWidgetItem(sensor["id"]))
                self.ui_table_sensors.setItem(index, SENSOR_COLUMN_NAME, QTableWidgetItem(sensor["title"]))
                sensor_type = sensor_type_map.get(str(sensor["type"]))
                if not sensor_type :
                    sensor_type = "其他类型"
                self.ui_table_sensors.setItem(index, SENSOR_COLUMN_TYPE, QTableWidgetItem(sensor_type))
                if sensor.get("last_data_gen") :
                    self.ui_table_sensors.setItem(index, SENSOR_COLUMN_VALUE, QTableWidgetItem(sensor["last_data_gen"]))
                elif sensor.get("last_data") :
                    self.ui_table_sensors.setItem(index, SENSOR_COLUMN_VALUE, QTableWidgetItem(sensor["last_data"]))
                if sensor.get("last_update") :
                    self.ui_table_sensors.setItem(index, SENSOR_COLUMN_UPDATE_TIME, QTableWidgetItem(sensor["last_update"]))
                
                index += 1
                if sensor["type"] == SENSOR_TYPE_SWITCH :
                    self.D(TAG_SELF, u"启动MQTT监听 sensor id=%s name=%s" % (sensor["id"], sensor["title"]))
                    t = Thread(target=self.mqtt_sensor_run, name=("Yeelink MQTT id=" + sensor["id"]), args=[sensor])
                    t.setDaemon(True)
                    t.start()
                    
            self.sensors = sensors #保存起来,这样就能快捷访问了
                    
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
        line = str(line)
        if not ":" in line :
            self.D(ser.port, "Not command")
            return
        tmp = line.split(":", 2)
        if len(tmp) != 2 or len(tmp[1]) == 0 :
            self.D(ser.port, "Not command")
            return
        if tmp[0] == "r" :
            sensor_id = None
            for sensor in self.sensors :
                if tmp[1] == sensor["id"] :
                    sensor_id = sensor["id"]
                    break
                item = self.ui_table_sensors.item(sensor["row_index"], SENSOR_COLUMN_DATA_READ)
                if item and str(item.text()) == tmp[1] :
                    sensor_id = sensor["id"]
                    break
            if not sensor_id :
                self.D(ser.port, "not match sensor")
                return
            re = self.yeelink_send("/device/%s/sensor/%s/datapoints" % (self.devid(), sensor_id), None)
            re = json.loads(re)
            if sensor["type"] == SENSOR_TYPE_RAW :
                re = json.dumps(re)
            else :
                re = json.dumps(re["value"])
            self.D(ser.port +".W", re)
            ser.write("r:%s:%s\n" % (tmp[1], re))
            return
                    
        count = self.ui_table_sensors.rowCount()
        if not count :
            self.D(ser.port, "no sensor at all !!")
            return
        for row_index in range(count) :
            #泛匹配
            
            item = self.ui_table_sensors.item(row_index, SENSOR_COLUMN_DATA_WRITE) #匹配数据前缀
            if not item :
                continue
            p = str(item.text())
            if not p or p != str(tmp[0]) :
                self.D(ser.port, "NOT Match %s %s" % (p, tmp[0]))
                continue
            
            item = self.ui_table_sensors.item(row_index, SENSOR_COLUMN_UPDATE_TIME) #匹配最后更新时间
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
            self.table_data.append([row_index, SENSOR_COLUMN_UPDATE_TIME, str(time.time())])
            self.table_data.append([row_index, SENSOR_COLUMN_VALUE, str(tmp[1])])
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
            self.ser = ser
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

    
    @pyqtSignature("")
    def on_ui_button_mock_start_pressed(self):
        """
        Slot documentation goes here.
        """
        try :
            import bottle
            bottle.debug(True)
            self.mock_app = bottle.Bottle()
            
            def before_req():
                self.D(TAG_MOCK, "before req " + str(bottle.request))
                if bottle.request.method == "GET" :
                    return
                key = bottle.request.headers().get("U-ApiKey")
                if not key :
                    self.D(TAG_MOCK, "U-ApiKey not in header!")
                    raise bottle.HTTPError(403)
                if key != self.apikey() :
                    self.D(TAG_MOCK, "U-ApiKey NOT match %s %s" % (key, self.apikey()))
                    raise bottle.HTTPError(403)
                
            def after_req():
                self.D(TAG_MOCK, "after req  " + str(bottle.request))
            
            self.mock_app.add_hook("before_request", before_req)
            self.mock_app.add_hook("after_request", after_req)
            
            @bottle.post("/v1.1/device/<dev_id>/sensor/<sensor_id>/datapoints")
            def data_upload(dev_id, sensor_id):
                if dev_id != self.devid() :
                    self.D(TAG_MOCK, "device_id NOT match %s %s" % (dev_id, self.devid()))
                    raise bottle.HTTPError(403)
                index = -1
                for sensor in self.sensors:
                    index += 1
                    if sensor_id == sensor["id"] :
                        if sensor["type"] == "0" or sensor["type"] == "6" or sensor["type"] == "6":
                            try :
                                p = json.load(bottle.request)
                                if sensor["type"] == "0" or sensor["type"] == "6" :
                                    t = p.get("timestamp")
                                    if t :
                                        self.D(TAG_MOCK, "timestamp = " + str(t))
                                    v = p.get("value")
                                    if not v :
                                        self.D(TAG_MOCK, "NO value!! " + json.dumps(p))
                                        raise bottle.HTTPError(406)
                                    if sensor["type"] == "0" :
                                        try :
                                            v = int(v)
                                        except:
                                            self.D(TAG_MOCK, "NOT number value!! " + json.dumps(p))
                                            raise bottle.HTTPError(406)
                                    elif sensor["type"] == "6" :
                                        try :
                                            _ = v["lat"]
                                            _ = v["lng"]
                                            _ = v["speed"]
                                        except:
                                            self.D(TAG_MOCK, "NOT gps value!! " + json.dumps(p))
                                            raise bottle.HTTPError(406)
                                    
                                    self.D(TAG_MOCK, "value ok, update it")
                                    self.table_data.append([index, SENSOR_COLUMN_VALUE, str(v)])
                                    self.table_data.append([index, SENSOR_COLUMN_UPDATE_TIME, str(time.time())])
                                    return
                                elif sensor["type"] == "8" :
                                    try :
                                        _ = p["key"]
                                        _ = p["value"]
                                    except:
                                        self.D(TAG_MOCK, "NOT raw value!! " + json.dumps(p))
                                        raise bottle.HTTPError(406)
                                    self.D(TAG_MOCK, "value ok, update it")
                                    self.table_data.append([index, SENSOR_COLUMN_VALUE, str(p)])
                                    self.table_data.append([index, SENSOR_COLUMN_UPDATE_TIME, str(time.time())])
                                return
                            except bottle.HTTPError:
                                raise
                            except:
                                self.D(TAG_MOCK, "Bad req : " + traceback.format_exc())
                                raise bottle.HTTPError(406)
                        else :
                            self.D(TAG_MOCK, "Not updateable " + sensor["id"])
                            raise bottle.HTTPError(406)
                self.D(TAG_MOCK, "No match any sensor")
                raise bottle.HTTPError(406)
            
            @bottle.get("/v1.1/device/<dev_id>/sensor/<sensor_id>/datapoints")
            def data_get(dev_id, sensor_id):
                if dev_id != self.devid() :
                    self.D(TAG_MOCK, "device_id NOT match %s %s" % (dev_id, self.devid()))
                    raise bottle.HTTPError(403)
                index = -1
                for sensor in self.sensors:
                    index += 1
                    if sensor_id != sensor["id"] :
                        continue
                    if sensor["type"] != "0" and sensor["type"] != "6" and sensor["type"] != "6":
                        self.D(TAG_MOCK, "NOT getable" + sensor_id)
                        raise bottle.HTTPError(403)
                    item = self.ui_table_sensors.item(index, SENSOR_COLUMN_VALUE)
                    if not item :
                        self.D(TAG_MOCK, "NO value!!")
                        raise bottle.HTTPError(403)
                    if sensor["type"] == "0" or  sensor["type"] == "6" :
                        return """{"value":%s}""" % str(item.text())
                    else :
                        return str(item.text())
                self.D(TAG_MOCK, "No match any sensor")
                raise bottle.HTTPError(406)
            
            def run():
                self.mock_app.run(host="0.0.0.0", port=int(str(self.ui_spin_mock_port.text())))
            t = Thread(target=run, name="Yeelink Mock server")
            t.setDaemon(True)
            t.start()
            
            self.ui_button_mock_stop.setEnabled(True)
            self.ui_button_mock_start.setEnabled(False)
            self.D(TAG_MOCK, u"启动成功")
        except:
            self.D(TAG_MOCK, u"启动失败" + traceback.format_exc())
    
    @pyqtSignature("")
    def on_ui_button_mock_stop_pressed(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.mock_app.close()
        self.D(TAG_MOCK, u"关闭")
        self.ui_button_mock_start.setEnabled(True)
        self.ui_button_mock_stop.setEnabled(False)
    
    @pyqtSignature("")
    def on_ui_button_api_test_pressed(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        import yeelink_api_test
        t = yeelink_api_test.YeelinkTestDialog(self)
        t.ui_text_uapikey.setText(self.ui_text_uapikey.text())
        t.show()
