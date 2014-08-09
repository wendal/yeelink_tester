# -*- coding: utf-8 -*-


import sys
from PyQt4 import QtCore, QtGui
from main_window import MainWindow


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MainWindow()
    myapp.show()
    sys.exit(app.exec_())
