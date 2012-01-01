from PyQt4.QtGui import *
from PyQt4.QtCore import *

import addtaskui

TIME_PRINT_FMT = "%c"

class TaskDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        super(TaskDelegate, self).paint(painter, option, index)
        view = self.parent()
        task = index.data(Qt.UserRole).toPyObject()
        
        painter.save()

        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())
            painter.setPen(QPalette().color(QPalette.HighlightedText))

        if index.column() == 0:
            widget = view.indexWidget(index)
            if not widget:
                widget = QCheckBox()
                widget.setStyleSheet("QCheckBox{ padding: 5px;}")
                view.setIndexWidget(index, widget)
            if task.status == 'completed':
                widget.setChecked(True)

        
        if index.column() == 1:
            textRect = option.rect.adjusted(0,6,0,0)

            status = self.taskStatusStr(task) 

            if task.status == 'completed':
                font = QFont()
                font.setStrikeOut(True)
                painter.setFont(font)
                        
            painter.drawText(textRect, Qt.AlignTop, task.title)
            painter.setFont(QFont())
            painter.drawText(textRect.adjusted(5,0,0,0), Qt.AlignBottom, status)
        
        painter.restore()

    def taskStatusStr(self, task):
        status = 'Due'
        if task.due != '':
            status += " on " + task.due.strftime(TIME_PRINT_FMT)

        if task.status == 'completed':
            status = "Completed"
            
            if task.completed != '':
                status += " on " + task.completed.strftime(TIME_PRINT_FMT)
                        
        status += "."
        return status

    def createEditor(self, parent, option, index):
        widget = TaskDialog(parent)
        ui = addtaskui.Ui_EditDialog()
        ui.setupUi(widget)
        widget.ui = ui
        widget.setModal(True)
        return widget

    def setEditorData(self, editor, index):
        task = index.data(Qt.UserRole).toPyObject()
        editor.ui.task_name.setText(task.title)
        editor.ui.statusLabel.setText(task.status)
        editor.ui.textEdit.setText(task.notes)
        editor.ui.statusLabel.setText(self.taskStatusStr(task))
        editor.ui.dateEdit.setMinimumDate(QDate.currentDate())
       
        if task.due != '':
            editor.ui.groupBox.setChecked(True)
            date = QDate(task.due.year, task.due.month, task.due.day)
            editor.ui.dateEdit.setDate(date)

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
