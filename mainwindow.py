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
        
        # Construct Sidebar
        self.listView = QListView()
        color = QPalette().color(QPalette.Window).name()
        self.listView.setStyleSheet("QListView{background: %s;border: 0px;}" % color)
        self.listView.setMinimumWidth(160)
        self.listView.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.listView.setModel(self.controller.taskListModel)
        index = self.controller.taskListModel.createIndex(0,0)
        self.listView.setCurrentIndex(index)
        
        # Construct bottom-right authorization widget
        self.authWidget = QWidget()
        vbox = QVBoxLayout()
        self.authWidget.setLayout(vbox)
        self.authWidget.setStyleSheet("""QTextEdit{color: black; background: #FFDCDC; border:0px} .QWidget{ background: #FFDCDC;}""")
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

        # Create a tree widget that displays the tasks
        self.treeView = QTreeView()
        self.treeView.setItemDelegate(TaskDelegate(self.treeView))
        self.treeView.setModel(self.controller.taskModel)
        self.treeView.setHeaderHidden(True)
        self.treeView.setRootIsDecorated(False)
        self.treeView.setUniformRowHeights(True)

        # Create a placeholder widget encapsulating the authorization and taskview widget
        widget = QWidget()
        vbox = QVBoxLayout()
        vbox.setMargin(0)
        vbox.setSpacing(0)
        widget.setLayout(vbox)
        vbox.addWidget(self.treeView)
        vbox.addWidget(self.authWidget)

        # Create the central splitter widget
        self.splitter = QSplitter()
        self.splitter.setHandleWidth(1)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.addWidget(self.listView)
        self.splitter.addWidget(widget)
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
                .connect(self.controller.taskModel.taskListChanged)

    def authRequired(self, url):
        self.setStatus("Authentication required.")
        self.authWidget.button.setText("Open Link in default browser")
        text = """Authorization with google required. Open <a href="%s">this link</a> in your web
                browser or press the button to open your web browser to continue.""" % url
        self.authWidget.textEdit.setHtml(text)
        self.authWidget.show()
        self.authWidget.setFixedHeight(80)
        
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


