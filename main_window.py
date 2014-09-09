# -*- coding: utf-8 -*-

"""
Yeelink Tester by wendal.net
"""

# 修正windows UTF-8控制台下报错
import codecs
codecs.register(lambda name: codecs.lookup('utf-8') if name == 'cp65001' else None)

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
import socket

#日志头部的标签
TAG_SELF = "SELF"
TAG_API  = "API"
TAG_MQTT = "MQTT"
TAG_MOCK = "MOCK"

#传感器表格每列的含义
SENSOR_COLUMN_ID = 0
SENSOR_COLUMN_NAME = 1
SENSOR_COLUMN_TYPE = 2
SENSOR_COLUMN_VALUE = 3
SENSOR_COLUMN_DATA_WRITE = 4
SENSOR_COLUMN_DATA_READ = 5
SENSOR_COLUMN_UPDATE_TIME = 6

#传感器类型
SENSOR_TYPE_NUMBER = "0"
SENSOR_TYPE_GPS = "6"
SENSOR_TYPE_IMAGE = "9"
SENSOR_TYPE_SWITCH = "5"
SENSOR_TYPE_RAW = "8"

# 读数据的key
READ_KEY = "r_key"
# 上传数据的前缀
WRITE_KEY = "w_key"

# 传感器类型的中文对应
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
        
        # 初始化日志输出timer, 因为Qt的UI更新不能在子线程中执行
        self.log_timer = QTimer()
        self.logs = []
        self.log_timer.setInterval(1)
        self.log_timer.start(1)
        self.connect(self.log_timer, SIGNAL("timeout()"), self.append_log)
        
        # 初始化传感器表格更新timer
        self.table_data = []
        self.table_timer = QTimer()
        self.table_timer.setInterval(1)
        self.table_timer.start(1)
        self.connect(self.table_timer, SIGNAL("timeout()"), self.table_update)
        
        # 启动完成, 自然卖卖广告咯...
        self.D(TAG_SELF, u"启动完成 . Power by wendal http://wendal.net")
        
    def apikey(self):
        """全局获取API KEY的帮助方法"""
        return unicode(self.ui_text_uapikey.text())
    
    def devid(self):
        """当前的设计只允许一个设备,所以全局来吧"""
        return unicode(self.ui_combo_devid.currentText()).split(" ")[0]
        
    def yeelink_send(self,  uri,  data):
        url = "http://api.yeelink.net/v1.1" + uri
        req = urllib2.Request(url, data)
        req.add_header("U-ApiKey", self.apikey())
        if data :
            self.D(TAG_API+".W", u"POST " + url)
            try :
                self.D(TAG_API+".W", str(data))
            except:
                self.D(TAG_API+".W", u"...")
        else :
            self.D(TAG_API+".W", u"GET " + url)
        try :
            resp = urllib2.urlopen(req)
            self.D(TAG_API + ".R", u"code=%d" % resp.code)
            return resp.read()
        except:
            self.D(TAG_API, u"FAIL" + traceback.format_exc())
            raise
    
    def D(self, TAG, msg):
        """日志方法"""
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
        
        """MQTT监听"""
        try :
            mqttc = mqtt.Client()
            def on_message(client, userdata, msg):
                self.D(TAG_SELF, "MQTT sensor update %s %s > %s" % (sensor["id"], sensor["title"], str(msg.payload)))
                try :
                    re = json.loads(msg.payload)
                    s = "%s%s" % (sensor[WRITE_KEY], re["value"])
                    self.D(self.ser.port, s)
                    self.ser.write(s + "\n")
                except:
                    traceback.print_exc()
            def on_connect(client, userdata, flags, rc):
                self.D(TAG_SELF, "MQTT Connected with result code "+str(rc))
                topic = "u/%s/v1.1/device/%s/sensor/%s/datapoints" % (self.apikey(), self.devid(), sensor["id"])
                #print topic
                mqttc.subscribe([(str(topic), 0), ])
            mqttc.on_message = on_message
            mqttc.on_connect = on_connect
            mqttc.connect("mqtt.yeelink.net")
            
            mqttc.loop_forever()
        except:
            self.D(TAG_SELF, u"MQTT 启动失败 : " + traceback.format_exc())
    
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
                #print dev
                self.ui_combo_devid.addItem(QString("%s %s" % (dev["id"], dev["title"])))
            self.ui_button_get_sensors.setEnabled(True)
            self.ui_button_start_read.setEnabled(True)
            self.ui_button_check_api.setEnabled(False)
            self.ui_text_uapikey.setEnabled(False)
            
            if len(re) == 1 :
                self.D(TAG_SELF, u"只有一个设备,自动加载传感器")
                self.on_ui_button_get_sensors_pressed()
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
                
                it = self.ui_table_sensors.item(index, SENSOR_COLUMN_DATA_WRITE)
                if not it :
                    self.ui_table_sensors.setItem(index, SENSOR_COLUMN_DATA_WRITE, QTableWidgetItem("w"+sensor["id"]+":"))
                it = self.ui_table_sensors.item(index, SENSOR_COLUMN_DATA_READ)
                if not it :
                    self.ui_table_sensors.setItem(index, SENSOR_COLUMN_DATA_READ, QTableWidgetItem("r"+sensor["id"]))
                    
                sensor["w_key"] = str(self.ui_table_sensors.item(index, SENSOR_COLUMN_DATA_WRITE).text())
                sensor["r_key"] = str(self.ui_table_sensors.item(index, SENSOR_COLUMN_DATA_READ).text())
                
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
            self.D(TAG_SELF, "出错啦 " + traceback.format_exc())
    
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
                self.D(ser.port+".R", line)
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
        line = str(line).strip()
        if not line :
            return
        
        if line[0] == '[' or line[0] == '{' :
            try :
                try :
                    j = json.loads(line)
                except:
                    self.D(ser.port, u"非法的json字符串")
                    return
                if not j :
                    self.D(ser.port, u"没有包含任何数据")
                    return
                if line[0] == '[' :
                    for d in j :
                        if d.get("sensor_id") :
                            self.D(ser.port, u"数据是列表,且包含sensor_id,所以这是'多数据点(同一设备)', 执行上传")
                            try :
                                self.yeelink_send("/device/%s/datapoints" % self.devid(), line)
                            except:
                                self.D(ser.port, u"上传失败")
                            return
                    self.D(ser.port, u"数据是列表,但不包含sensor_id,所以这是'多数据点(单个设备)', 查找'数据上传'键为空字符的传感器")
                    for sensor in self.sensors :
                        if sensor[WRITE_KEY] == "" :
                            self.D(ser.port, u"作为传感器[id=%s,name=%s]的数据进行上传")
                            self.yeelink_send("/device/%s/sensor/%s/datapoints" % (self.devid(), sensor["id"]), line)
                            return
                    self.D(ser.port, u"没有找到'数据上传'键为空字符的传感器,忽略数据")
                    return
                if len(self.sensors) == 1 :
                    self.D(ser.port, u"只有一个传感器, 而且数据看上去ok, 那就上传吧")
                    self.yeelink_send("/device/%s/sensor/%s/datapoints" % (self.devid(), sensor["id"]), line)
                    return
                for sensor in self.sensors :
                    if sensor[WRITE_KEY] == "" :
                        self.D(ser.port, u"作为传感器[id=%s,name=%s]的数据进行上传")
                        self.yeelink_send("/device/%s/sensor/%s/datapoints" % (self.devid(), sensor["id"]), line)
                        return
                self.D(ser.port, u"没有找到'数据上传'键为空字符的传感器,忽略数据")
                return
            except:
                self.D(ser.port, u"出错了")
                
        for sensor in self.sensors :
            if line.startswith(sensor[READ_KEY]) :
                self.D(ser.port, u"与传感器[id=%s, name=%s]的'数据读取'键匹配" % (sensor["id"], sensor["title"]))
                try :
                    re = self.yeelink_send("/device/%s/sensor/%s/datapoints" % (self.devid(), sensor["id"]), None)
                    re = json.loads(re)
                    if re.get("key") :
                        msg = sensor[WRITE_KEY] + json.dumps(re) + "\n"
                    else :
                        msg = sensor[WRITE_KEY] + json.dumps(re.get("value")) + "\n"
                    self.D(ser.port + ".W", msg)
                    ser.write(msg)
                except:
                    self.D(ser.port, u"出错了" + traceback.format_exc())
                return
        
        for sensor in self.sensors :
            if line.startswith(sensor[WRITE_KEY]) :
                data = line[len(sensor[WRITE_KEY]):]
                if not data :
                    self.D(ser.port, u"没数据")
                    return
                if data[0] == ":" :
                    data = data[1:]
                if data[0] == '{' :
                    try :
                        try :
                            re = json.loads(data)
                        except:
                            self.D(ser.port, u"非法的JSON字符串" + traceback.format_exc(2))
                            return
                        if re and re.get("value") :
                            self.yeelink_send("/device/%s/sensor/%s/datapoints" % (self.devid(), sensor["id"]), data)
                            return
                    except:
                        self.D(ser.port, "Bad Bad")
                self.yeelink_send("/device/%s/sensor/%s/datapoints" % (self.devid(), sensor["id"]), """{"value":%s}""" % data)
                return
        self.D(ser.port, u"没匹配任何传感器")
        
    @pyqtSignature("")
    def on_ui_button_start_read_pressed(self):
        """
        Slot documentation goes here.
        """
        try :
            self.D(TAG_SELF, u"尝试打开串口 ... ")
            ser = serial.Serial()
            ser.baudrate = int(str(self.ui_text_com_bitrate.currentText()))
            ser.bytesize = int(str(self.ui_text_com_databit.currentText()))
            ser.stopbits = int(str(self.ui_text_com_stopbit.currentText()))
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
            t = Thread(name="yeelink api proxy", target=self.yeelink_api_proxy)
            t.setDaemon(True)
            t.start()
            
            self.ui_button_mock_stop.setEnabled(True)
            self.ui_button_mock_start.setEnabled(False)
            self.mock_running = True
            self.D(TAG_MOCK, u"启动成功")
        except:
            self.D(TAG_MOCK, u"启动失败" + traceback.format_exc())
    
    @pyqtSignature("")
    def on_ui_button_mock_stop_pressed(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.mock_running = False
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
        try :
            t.ui_text_url.clear()
            for sensor in self.sensors :
                t.ui_text_url.addItem(QString("http://api.yeelink.net/v1.1/device/%s/sensor/%s/datapoints" % (self.devid(), sensor["id"])))
        except:
            pass
        t.show()
        
    def yeelink_api_proxy(self):
        PORT = int(str(self.ui_spin_mock_port.text()))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #s.settimeout(3)
        s.bind(("", PORT))
        s.listen(PORT)
        while self.mock_running :
            conn = None
            _out = None
            try:
                conn, addr = s.accept()
                self.D(TAG_MOCK, "Connected by " + str(addr))
                _in = conn.makefile()
                _out = conn.makefile("w")
                
                try :
                    #读取请求头
                    data = _in.read(4)
                    if str(data) != "POST" :
                        self.D(TAG_MOCK, u"不是POST请求,拒绝之.")
                        continue
                    data = _in.read(1)
                    if str(data) != " " :
                        self.D(TAG_MOCK, u"POST之后的不是空格,非法请求")
                        continue
                    #开始读取URI
                    data = ""
                    for i in xrange(1024) :
                        d = _in.read(1)
                        if d == ' ' :
                            self.D(TAG_MOCK, u"读取到URI之后的空格, 识别URI为 " + data)
                            break
                        else :
                            data += str(d)
                        if i == 1023 :
                            self.D(TAG_MOCK, u"读取1024字节之后还没结束, URI太长了,拒绝")
                            data = None
                    if data == None :
                        continue
                    if data == "" :
                        self.D(TAG_MOCK, u"URI以空格开头,肯定是多输入了一个空格导致的,拒绝")
                        continue
                    #然后就是HTTP/1.1或者HTTP/1.0,然后接\r\n
                    data = _in.read(len("HTTP/1.0\r\n"))
                    #print data
                    if not str(data).startswith("HTTP/1.0") and not str(data).startswith("HTTP/1.1") :
                        self.D(TAG_MOCK, u"请求行不包含HTTP/1.0或HTTP/1.1,拒绝")
                        continue
                    if not str(data).endswith("\r\n") :
                        self.D(TAG_MOCK, u"请求行不是以\\r\\n结束,拒绝")
                        continue
                    key_ok = False
                    cnt_len = 0
                    while 1 :
                        header_line = ""
                        while 1 :
                            d = _in.read(1)
                            if d == '\n' :
                                break
                            header_line += str(d)
                        if header_line == "" :
                            self.D(TAG_MOCK, u"检测到非法的Header,拒绝")
                            break
                        if header_line == "\r" :
                            self.D(TAG_MOCK, u"检测到Header结束")
                            break
                        header_line = header_line.strip()
                        self.D(TAG_MOCK, "Read Header --> " + str(header_line))
                        if header_line.startswith("U-ApiKey: ") :
                            self.D(TAG_MOCK, u"检测到U-ApiKey,对比本地数据中");
                            _key = header_line.split(" ", 2)[1]
                            if _key == self.apikey() :
                                self.D(TAG_MOCK, u"U-ApiKey合法")
                                key_ok = True
                            else :
                                self.D(TAG_MOCK, u"U-ApiKey不合法 [%s] [%s]" % (_key, self.apikey()))
                                break
                        elif header_line.startswith("Content-Length: ") :
                            self.D(TAG_MOCK, u"检测到Content-Length: ")
                            try :
                                cnt_len = int(header_line.split(" ", 2)[1])
                                self.D(TAG_MOCK, u"获取到请求主体的长度为" + str(cnt_len))
                            except:
                                self.D(TAG_MOCK, u"Content-Length 不是合法的整数值")
                                break
                    if not key_ok :
                        self.D(TAG_MOCK, u"没有在Header里面找到合法U-ApiKey,拒绝")
                        continue
                    if cnt_len < 5 :
                        self.D(TAG_MOCK, u"请求体太小,肯定不合法")
                        continue
                    #开始读取body
                    try :
                        body = _in.read(cnt_len)
                        j = json.loads(body)
                        self.D(TAG_MOCK, u"请求中的JSON数据(经过格式化) --> "  + json.dumps(j))
                        if not j.get("value") :
                            self.D(TAG_MOCK, u"数据里面没有名为value的键,肯定非法")
                            break
                        
                        if j.get("key") :
                            self.D(TAG_MOCK, u"看来是泛型数据,放行")
                        elif j.get("value") :
                            if json.dumps(j.get("value")).startswith("{") :
                                self.D(TAG_MOCK, u"看上去是GPS数据,分析里面的key")
                                gps = j.get("value")
                                if not gps.get("lat") :
                                    self.D(TAG_MOCK, u"缺失lan值")
                                    continue
                                if not gps.get("lng") :
                                    self.D(TAG_MOCK, u"缺失lng值")
                                    continue
                                if str(gps.get("speed")) == "None" :
                                    self.D(TAG_MOCK, u"缺失speed值")
                                    continue
                                self.D(TAG_MOCK, u"GPS数据 看上去合法")
                            else :
                                self.D(TAG_MOCK, u"看来不是GPS,那只能是数值型数据了,校验之")
                                if isinstance(j.get("value"), float) :
                                    self.D(TAG_MOCK, u"看来是合法的数值")
                                else :
                                    self.D(TAG_MOCK, u"不是JSON格式中的数值,拒绝")
                                    break
                        else :
                            self.D(TAG_MOCK, u"数据里面没有名为key或timestamp的键,肯定非法")
                            break
                        
                        # 看来是合法的哦, 返回个赞
                        _out.write("HTTP/1.1 200 OK\r\nPower: wendal\r\nContent-Length: 0\r\n\r\n")
                        _out.flush()
                        conn.shutdown(1)
                        conn.close()
                        conn = None
                    except:
                        self.D(TAG_MOCK, u"yeelink上传的数据必然是json格式,然后它报错了,所以,你的数据不是合法JSON!!" + traceback.format_exc())
                        break
                except:
                    self.D(TAG_MOCK, u"出错了!!" + traceback.format_exc())
                
            except:
                traceback.print_exc()
            finally:
                if conn != None :
                    try :
                        self.D(TAG_MOCK, u"关闭连接 " + str(conn))
                        _out.write("HTTP/1.1 403 Error\r\nPower: wendal\r\nContent-Length: 0\r\n\r\n")
                        _out.flush()
                        conn.shutdown(1)
                        conn.close()
                    except:
                        self.D(TAG_MOCK, u"关闭连接失败!!" + traceback.format_exc())
        s.close()
    
    @pyqtSignature("QTableWidgetItem*")
    def on_ui_table_sensors_itemChanged(self, item):
        """
        Slot documentation goes here.
        """
        try :
            _ = self.sensors
        except:
            return
        sensor = self.sensors[item.row()]
        if item.column() == SENSOR_COLUMN_DATA_READ :
            sensor[READ_KEY] = str(item.text())
            self.D(TAG_SELF, u"传感器[id=%s, name=%s]的'数据读取'键修改为%s" % (sensor["id"], sensor["title"], sensor[READ_KEY]))
            return
        if item.column() == SENSOR_COLUMN_DATA_WRITE :
            sensor[WRITE_KEY] = str(item.text())
            self.D(TAG_SELF, u"传感器[id=%s, name=%s]的'数据上传'键修改为%s" % (sensor["id"], sensor["title"], sensor[WRITE_KEY]))
            return
        # TODO 如果修改的是值, 发请求更新服务器的值
        