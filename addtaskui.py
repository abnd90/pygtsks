# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addtask.ui'
#
# Created: Wed Dec 28 12:24:26 2011
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_EditDialog(object):
    def setupUi(self, EditDialog):
        EditDialog.setObjectName(_fromUtf8("EditDialog"))
        EditDialog.resize(463, 307)
        EditDialog.setWindowTitle(QtGui.QApplication.translate("EditDialog", "Create new task", None, QtGui.QApplication.UnicodeUTF8))
        self.verticalLayout = QtGui.QVBoxLayout(EditDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(EditDialog)
        self.label.setText(QtGui.QApplication.translate("EditDialog", "Title", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.task_name = QtGui.QLineEdit(EditDialog)
        self.task_name.setObjectName(_fromUtf8("task_name"))
        self.horizontalLayout.addWidget(self.task_name)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_2 = QtGui.QLabel(EditDialog)
        self.label_2.setText(QtGui.QApplication.translate("EditDialog", "Notes", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_2.addWidget(self.label_2)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        spacerItem2 = QtGui.QSpacerItem(31, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.textEdit = QtGui.QTextEdit(EditDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.horizontalLayout_2.addWidget(self.textEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.checkBox = QtGui.QCheckBox(EditDialog)
        self.checkBox.setEnabled(True)
        self.checkBox.setText(QtGui.QApplication.translate("EditDialog", "Time", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.horizontalLayout_3.addWidget(self.checkBox)
        self.dateTimeEdit = QtGui.QDateTimeEdit(EditDialog)
        self.dateTimeEdit.setEnabled(False)
        self.dateTimeEdit.setObjectName(_fromUtf8("dateTimeEdit"))
        self.horizontalLayout_3.addWidget(self.dateTimeEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.buttonBox = QtGui.QDialogButtonBox(EditDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(EditDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), EditDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), EditDialog.reject)
        QtCore.QObject.connect(self.checkBox, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.dateTimeEdit.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(EditDialog)

    def retranslateUi(self, EditDialog):
        pass

