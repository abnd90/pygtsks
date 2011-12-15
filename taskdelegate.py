from PyQt4.QtGui import *
from PyQt4.QtCore import *

import tablewidgetui

class TaskDelegate(QItemDelegate):
    def paint(self, painter, option, index):
        view = self.parent()
        
        if index.column() == 1:
            if not view.indexWidget(index):
                widget = QWidget()
                ui = tablewidgetui.Ui_Form()
                ui.setupUi(widget)
                view.setIndexWidget(index, widget)
        elif index.column() == 0:
            if not view.indexWidget(index):
                view.setIndexWidget(index, QCheckBox())

        super(TaskDelegate, self).paint(painter, option, index)
