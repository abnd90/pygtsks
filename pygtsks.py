#!/usr/bin/python2

import sys
from PyQt4.QtGui import *

import mainwindow

def main():
    qapp = QApplication(sys.argv)

    ui = mainwindow.TasksMainWindow()
    mw = QMainWindow()
    ui.setupUi(mw)
    mw.show()
    trayIcon = QSystemTrayIcon()
    trayIcon.show()
    sys.exit(qapp.exec_())

if __name__ == '__main__':
    main()
