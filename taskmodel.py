from PyQt4.QtGui import *
from PyQt4.QtCore import *

import data_backend

class TaskListModel(QAbstractListModel):
    def __init__(self):
        super(TaskListModel, self).__init__()
        self.taskLists = data_backend.getTaskLists()

    def rowCount(self, parent=QModelIndex()):
        return len(self.taskLists) + 1

    def data(self, index, role = Qt.DisplayRole):
        row = index.row()
        if role == Qt.DisplayRole:
        #First row is a pseudo "ALL TASKS" row
            if row == 0:
                return "All Tasks"
            else:
                taskList = self.taskLists[row - 1]
                return taskList.name

    def headerData(self, selection, orientation, role = Qt.DisplayRole):
        if selection == 0:
                return "Task List"
