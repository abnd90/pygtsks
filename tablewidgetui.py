# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tablewidget.ui'
#
# Created: Tue Dec 20 11:28:07 2011
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(168, 50)
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.verticalLayout_2 = QtGui.QVBoxLayout(Form)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(5, -1, -1, -1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.check = QtGui.QCheckBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.check.sizePolicy().hasHeightForWidth())
        self.check.setSizePolicy(sizePolicy)
        self.check.setText(_fromUtf8(""))
        self.check.setCheckable(True)
        self.check.setObjectName(_fromUtf8("check"))
        self.horizontalLayout_2.addWidget(self.check)
        self.title = QtGui.QLabel(Form)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setText(QtGui.QApplication.translate("Form", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.title.setMargin(5)
        self.title.setObjectName(_fromUtf8("title"))
        self.horizontalLayout_2.addWidget(self.title)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(24, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.statusLabel = QtGui.QLabel(Form)
        self.statusLabel.setStyleSheet(_fromUtf8("margin-top: -8px;"))
        self.statusLabel.setText(QtGui.QApplication.translate("Form", "Due on:", None, QtGui.QApplication.UnicodeUTF8))
        self.statusLabel.setObjectName(_fromUtf8("statusLabel"))
        self.horizontalLayout.addWidget(self.statusLabel)
        self.status = QtGui.QLabel(Form)
        self.status.setStyleSheet(_fromUtf8("margin-top: -8px;"))
        self.status.setText(QtGui.QApplication.translate("Form", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.status.setMargin(0)
        self.status.setObjectName(_fromUtf8("status"))
        self.horizontalLayout.addWidget(self.status)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        pass

