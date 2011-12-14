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
        color = QPalette().color(QPalette.Window).name()
        self.listView.setStyleSheet("QListView{background: %s;border: 0px;}" % color)
        self.listView.setMinimumWidth(160)
        self.listView.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.listView.setModel(self.controller.taskListModel)

        self.authWidget = QWidget()
        vbox = QVBoxLayout()
        self.authWidget.setLayout(vbox)
        self.authWidget.setStyleSheet("""QTextEdit{color: black; background: #FFDCDC; border:0px}
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

        widget = QWidget()
        vbox = QVBoxLayout()
        vbox.setMargin(0)
        vbox.setSpacing(0)
        widget.setLayout(vbox)
        self.tableView = QTableView()
        vbox.addWidget(self.tableView)
        vbox.addWidget(self.authWidget)
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

        self.statusLabel = QLabel("Ready")
        self.statusProgress = QProgressBar()
        self.statusBar = MainWindow.statusBar()
        self.statusBar.addWidget(self.statusLabel)
        self.statusBar.addWidget(self.statusProgress)
        self.statusProgress.hide()

        index = self.controller.taskListModel.createIndex(0,0)
        self.listView.setCurrentIndex(index)

        self.connectActions()
        self.connectSignals()

    def connectActions(self):
        self.actionQuit.triggered.connect(qApp.quit)
        self.actionSync.triggered.connect(self.controller.sync)

    def connectSignals(self):
        self.controller.api.needsAuthentication[str].connect(\
                self.authRequired)
        self.controller.api.authenticationDone.connect(self.authDone)

    def authRequired(self, url):
        self.statusLabel.setText("Authentication required.")
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
        self.statusLabel.setText("Ready.")
        self.statusBar.showMessage("Authentication successful.", 3000)
        self.authWidget.hide()
