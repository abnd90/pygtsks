from PyQt4.QtGui import *
from PyQt4.QtCore import *

from data_backend import TaskList, Task
from debug import debug

class TaskListModel(QAbstractListModel):

    taskList = [] 
    currentRow = 0
    setViewRow = pyqtSignal(int)

    def __init__(self):
        super(TaskListModel, self).__init__()
        self.readTaskLists()

    def readTaskLists(self):
        self.taskLists = TaskList.getAll()
        #First row is a pseudo "ALL TASKS" row
        self.taskLists.insert(0, TaskList("", "All Tasks", id=-1))

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
           self.taskLists[index.row()] = tl
           self.dataChanged.emit(index, index)
           return True
        else:
           return False

    def insertOrUpdate(self, l): 
        """ Inserts or updates a whole list of tasklists """
        for t in l:
            debug(0, "Inserting (or updating) tasklist into DB: " + str(t))
            TaskList.insertOrUpdate(t)
        self.beginResetModel()
        self.readTaskLists()
        self.endResetModel()
        self.setViewRow.emit(self.currentRow)

    def taskListForTlid(self, tlid):
        for tl in self.taskLists:
            if tl.tlid == tlid:
                return tl
            
    def taskListChanged(self, curr, prev):
        self.currentRow = curr.row()

    
class TaskModel(QAbstractTableModel):
    
    tasks = []

    def __init__(self):
        super(TaskModel, self).__init__()

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled

        return  super(TaskModel, self).flags(index) | Qt.ItemIsEditable

    def setData(self, index, value, role):
        self.dataChanged.emit(index, index)
        return True

    def taskListChanged(self, curr, prev):
        tl = curr.data(Qt.UserRole).toPyObject()
        self.currentList = tl.id
        self.beginResetModel()
        self.refreshTasks()
        self.endResetModel()
 
    def insertOrUpdate(self, l): 
        """ Inserts or updates a whole list of tasks """
        for t in l:
            debug(0, "Inserting (or updating) task into DB: " + str(t))
            Task.insertOrUpdate(t)
        self.beginResetModel()
        self.refreshTasks()
        self.endResetModel()
    
    def refreshTasks(self):
        self.tasks = Task.get(self.currentList)

    def rowCount(self, parent=QModelIndex()):
        if not parent.isValid():
            return len(self.tasks)
        else:
            return 0

    def columnCount(self, parent=QModelIndex()):
        return 2

    def data(self, index, role):
        row = index.row()
        col = index.column()
        task = self.tasks[row]
        if role == Qt.UserRole:
            return task
        elif role == Qt.EditRole:
            if col == 1:
                return task.title
        elif role == Qt.SizeHintRole:
            return QSize(0,35)

