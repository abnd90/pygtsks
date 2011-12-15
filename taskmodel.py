from PyQt4.QtGui import *
from PyQt4.QtCore import *

from data_backend import TaskList
from debug import debug

class TaskListModel(QAbstractListModel):
    def __init__(self):
        super(TaskListModel, self).__init__()
        self.readTaskLists()

    def readTaskLists(self):
        self.taskLists = TaskList.getAll()
        #First row is a pseudo "ALL TASKS" row
        self.taskLists.insert(0, TaskList("", "All Tasks"))

    def rowCount(self, parent = QModelIndex()):
        return len(self.taskLists) 

    def data(self, index, role = Qt.DisplayRole):
        row = index.row()
        taskList = self.taskLists[row]
        if role == Qt.UserRole:
            return taskList
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return str(taskList)

    def headerData(self, selection, orientation, role):
        if selection == 0:
                return "Task List"

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        elif index.row() == 0:
            return super(TaskListModel, self).flags(index)

        return  super(TaskListModel, self).flags(index) | Qt.ItemIsEditable

    def setData(self, index, value, role):
        if index.isValid and role == Qt.EditRole:
           tl = self.taskLists[index.row()]
           tl.name = str(value.toString())
           TaskList.update(tl)
           self.dataChanged.emit(index, index)
           self.readTaskLists()
           return True
        else:
           return False

    def insertOrUpdate(self, l): 
        for t in l:
            debug(0, "Inserting (or updating) tasklist into DB: " + str(t))
            TaskList.insertOrUpdate(t)
        self.readTaskLists()
        self.dataChanged.emit(self.createIndex(0, 0), \
                self.createIndex(self.rowCount()-1, 0))

class TaskModel(QAbstractTableModel):

    def taskListChanged(self, curr, prev):
        tl = curr.data(Qt.UserRole).toPyObject()

    def rowCount(self, parent):
        return 5

    def columnCount(self, parent):
        return 2

    def data(self, index, role):
        pass
