from PyQt4.QtGui import *
from PyQt4.QtCore import *

import mainwindowui
import controller

class TasksMainWindow(mainwindowui.Ui_MainWindow):
    def __init__(self):
        super(TasksMainWindow, self).__init__()
        self.controller = controller.Controller()
     
    def setupUi(self, MainWindow):
        super(TasksMainWindow, self).setupUi(MainWindow)
        
        self.splitter = QSplitter()
        self.splitter.setHandleWidth(1)
        self.splitter.setChildrenCollapsible(False)
        self.listView = QListView()
        self.listView.setStyleSheet("QListView{background: #dedede;border: 0px;}")
        self.listView.setMinimumWidth(160)
        self.listView.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.listView.setModel(self.controller.taskListModel)

        self.tableView = QTableView()
        self.splitter.addWidget(self.listView)
        self.splitter.addWidget(self.tableView)
        self.splitter.setSizes([160, 99999999])
        MainWindow.setCentralWidget(self.splitter)

        self.toolBar.addAction(self.actionNew_Task)
        self.toolBar.addAction(self.actionNew_Task_List)
        self.toolBar.addAction(self.actionSync)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionPreferences)

        self.statusLabel = QLabel("Ready")
        self.statusProgress = QProgressBar()
        MainWindow.statusBar().addWidget(self.statusLabel)
        MainWindow.statusBar().addWidget(self.statusProgress)
        self.statusProgress.hide()

        self.connectActions()

        index = self.controller.taskListModel.createIndex(0,0)
        self.listView.setCurrentIndex(index)

    def connectActions(self):
        self.actionQuit.triggered.connect(qApp.quit)
        self.actionSync.triggered.connect(self.controller.sync)
