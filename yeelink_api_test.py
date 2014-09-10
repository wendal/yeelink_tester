# -*- coding: utf-8 -*-

"""
Module implementing YeelinkTestDialog.
"""

from PyQt4.QtGui import QDialog
from PyQt4.QtCore import pyqtSignature

from Ui_yeelink_api_test import Ui_Dialog
import PyQt4.QtGui
import urllib2
import traceback
import os

handler=urllib2.HTTPHandler(debuglevel=1)
opener = urllib2.build_opener(handler)
#urllib2.install_opener(opener)

class YeelinkTestDialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        
    def send(self, data, method=None):
        url = str(self.ui_text_url.currentText())
        self.ui_text_output.clear()
        def log(msg):
            self.ui_text_output.appendPlainText(msg)
            #self.ui_text_output.append("\n")
        if method :
            url += "?method=" + method
        log("URL: " + url)
        req = urllib2.Request(url, data)
        req.add_header("U-ApiKey", str(self.ui_text_uapikey.text()))
        if data :
            req.add_header("Content-Length", str(len(data)))
        try :
            resp = urllib2.urlopen(req)
            log("Resp Code " + str(resp.code))
            log("---------------------------------")
            log(str(resp.read()))
        except:
            log(traceback.format_exc())
    
    @pyqtSignature("")
    def on_ui_button_select_file_pressed(self):
        """
        Slot documentation goes here.
        """
        p = PyQt4.QtGui.QFileDialog.getOpenFileName()
        if p :
            self.ui_text_file_path.setText(p)
    
    @pyqtSignature("")
    def on_ui_button_send_file_pressed(self):
        """
        Slot documentation goes here.
        """
        if os.path.getsize(str(self.ui_text_file_path.text())) > 1024*1024 :
            pass
        with open(str(self.ui_text_file_path.text()), "rb") as f :
            self.send(f.read())
    
    @pyqtSignature("")
    def on_ui_button_send_text_pressed(self):
        """
        Slot documentation goes here.
        """
        self.send(self.ui_text_data.toPlainText().toUtf8().data())
    
    @pyqtSignature("")
    def on_ui_button_send_text_hex_pressed(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSignature("")
    def on_ui_button_send_pressed(self):
        """
        Slot documentation goes here.
        """
        self.send(None)

    
    @pyqtSignature("")
    def on_ui_button_send_delete_released(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.send(None, method="DELETE")
    
    @pyqtSignature("")
    def on_ui_button_send_text_put_released(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.send(self.ui_text_data.toPlainText().toUtf8().data(), method="PUT")
