from PyQt4.QtGui import *
from PyQt4.QtCore import *

import mainwindowui
import controller
from taskdelegate import TaskDelegate

class TasksMainWindow(mainwindowui.Ui_MainWindow):
    def __init__(self):
        super(TasksMainWindow, self).__init__()
        self.controller = controller.Controller()
     
    def setupUi(self, MainWindow):
        super(TasksMainWindow, self).setupUi(MainWindow)
        
        self.splitter = QSplitter()
        
        # Construct Sidebar
        self.listView = QListView(self.splitter)
        _bgcolor = QPalette().color(QPalette.Window)
        self.listView.setStyleSheet("""
            QListView{ background: %s;border: 5px; margin: 9px 0px;} 
            QListView::item{padding: 3px}""" % _bgcolor.name())
        self.listView.setMinimumWidth(160)
        self.listView.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.listView.setModel(self.controller.taskListModel)
        # Set default task list
        self.setTaskList(0)
        self.listView.setUniformItemSizes(True)
        
        # Create a placeholder widget encapsulating the authorization and taskview widget
        _placeWidget = QWidget(self.splitter)
        _placeVbox = QVBoxLayout()
        _placeVbox.setMargin(0)
        _placeVbox.setSpacing(0)
        _placeWidget.setLayout(_placeVbox)
       
        # Construct bottom-right authorization widget
        self.authWidget = QWidget(_placeWidget)
        vbox = QVBoxLayout()
        self.authWidget.setLayout(vbox)
        self.authWidget.setStyleSheet("""
            QTextEdit{color: black; background: #FFDCDC; border:0px} 
            .QWidget{ background: #FFDCDC;}""")
        textEdit = QTextEdit()
        textEdit.setReadOnly(True)
        textEdit.setTextInteractionFlags(Qt.LinksAccessibleByMouse 
                | Qt.LinksAccessibleByKeyboard)
        textEdit.setFixedHeight(50)
        hbox = QHBoxLayout()
        hbox.addStretch()
        button = QPushButton()
        hbox.addWidget(button)
        vbox.addWidget(textEdit)
        vbox.addLayout(hbox)
        self.authWidget.textEdit = textEdit
        self.authWidget.button = button
        self.authWidget.hide()
        self.authWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Create a tree widget that displays the tasks
        self.treeView = QTreeView(_placeWidget)
        self.treeView.setItemDelegate(TaskDelegate(self.treeView))
        self.treeView.setModel(self.controller.taskModel)
        self.treeView.setHeaderHidden(True)
        self.treeView.setRootIsDecorated(False)
        self.treeView.setUniformRowHeights(True)
        self.treeView.setAlternatingRowColors(True)
        self.treeView.setColumnWidth(0,35)
        
        _placeVbox.addWidget(self.treeView)
        _placeVbox.addWidget(self.authWidget)

        # Create the central splitter widget
        self.splitter.setHandleWidth(1)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.addWidget(self.listView)
        self.splitter.addWidget(_placeWidget)
        self.splitter.setSizes([160, 99999999])
        MainWindow.setCentralWidget(self.splitter)

        self.toolBar.addAction(self.actionNew_Task)
        self.toolBar.addAction(self.actionNew_Task_List)
        self.toolBar.addAction(self.actionSync)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionPreferences)

        self.actionPreferences.setIcon(QIcon.fromTheme("preferences-system"))
        self.actionNew_Task.setIcon(QIcon.fromTheme("document-new"))
        self.actionNew_Task_List.setIcon(QIcon.fromTheme("folder-new"))
        self.actionSync.setIcon(QIcon.fromTheme("emblem-synchronized"))

        self.statusLabel = QLabel("Ready.")
        self.statusProgress = QProgressBar()
        self.statusBar = MainWindow.statusBar()
        self.statusBar.addWidget(self.statusLabel)
        self.statusBar.addWidget(self.statusProgress)
        self.statusProgress.setMaximum(0)
        self.statusProgress.hide()

        self.connectActions()
        self.connectSignals()

    def connectActions(self):
        self.actionQuit.triggered.connect(qApp.quit)
        self.actionSync.triggered.connect(self.controller.sync)
        self.controller.syncing[bool,str].connect(self.syncing)

    def connectSignals(self):
        self.controller.api.needsAuthentication[str].connect(\
                self.authRequired)
        self.controller.api.authenticationDone.connect(self.authDone)

        selectionModel = self.listView.selectionModel()
        selectionModel.currentChanged[QModelIndex, QModelIndex]\
                .connect(self.controller.taskListModel.taskListChanged)
        selectionModel.currentChanged[QModelIndex, QModelIndex]\
                .connect(self.controller.taskModel.taskListChanged)
        self.controller.taskListModel.setViewRow[int].connect(self.setTaskList)

    def setTaskList(self, row):
        index = self.controller.taskListModel.createIndex(row,0)
        self.listView.setCurrentIndex(index)
        self.controller.taskModel.taskListChanged(index, QModelIndex())

    def authRequired(self, url):
        self.setStatus("Authentication required.")
        self.authWidget.button.setText("Open Link in default browser")
        text = """Authorization with google required. Open <a href="%s">this link</a>
        in your web browser or press the button to open 
        your web browser to continue.""" % url
        
        self.authWidget.textEdit.setHtml(text)
        self.authWidget.show()

        def openBrowser():
            QDesktopServices.openUrl(QUrl.fromEncoded(str(url)))
        self.authWidget.button.clicked.connect(openBrowser)

    def authDone(self):
        self.statusLabel.setStatus()
        self.setStatus("Authentication successful.", 3000)
        self.authWidget.hide()

    def setStatus(self, text='', time=0):
        if text == '':
            text="Ready."

        if time:
            self.statusBar.showMessage(text, time)
        else:
            self.statusLabel.setText(text)

    def syncing(self, status, text=''):
        if status:
            if text == '':
                self.setStatus("Syncing")
            else:
                self.statusLabel.setText(text)
            self.statusProgress.show()
        else:
            self.setStatus()
            self.statusProgress.hide()


