from PyQt4.QtGui import *
from PyQt4.QtCore import *

import addtaskui

class TaskDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        view = self.parent()
        task = index.data(Qt.UserRole).toPyObject()
        
        if index.column() == 0:
            widget = view.indexWidget(index)
            if not widget:
                widget = QCheckBox()
                widget.setStyleSheet("QCheckBox{ padding: 5px;}")
                view.setIndexWidget(index, widget)
        
        if index.column() == 1:
            textRect = option.rect.adjusted(0,6,0,0)
            painter.save()

            if option.state & QStyle.State_Selected:
                painter.fillRect(option.rect, option.palette.highlight())
                painter.setPen(QPalette().color(QPalette.HighlightedText))
            
            painter.drawText(textRect, Qt.AlignTop, task.title)
            painter.drawText(textRect.adjusted(5,0,0,0), Qt.AlignBottom, "status")
            painter.restore()
        else:
            super(TaskDelegate, self).paint(painter, option, index)

    def createEditor(self, parent, option, index):
        widget = TaskDialog(parent)
        ui = addtaskui.Ui_EditDialog()
        ui.setupUi(widget)
        widget.ui = ui

        return widget

    def setEditorData(self, editor, index):
        task = index.data(Qt.UserRole).toPyObject()
        editor.ui.task_name.setText(task.title)

    def setModelData(self, editor, model, index):
        if editor.result() == QDialog.Accepted:
            pass


class TaskDialog(QDialog):

    def accept(self):
        self.setResult(QDialog.Accepted)
        QDialog.accept(self)

    def cancel(self):
        self.setResult(QDialog.Rejected)
        QDialog.cancel(self)
