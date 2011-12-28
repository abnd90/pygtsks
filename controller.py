from PyQt4.QtCore import *

import api_backend
import taskmodel
from debug import debug

class Controller(QObject):

    syncing = pyqtSignal(bool, str)

    def __init__(self):
        super(Controller, self).__init__()
        self.taskListModel = taskmodel.TaskListModel()
        self.taskModel = taskmodel.TaskModel()
        self.api = api_backend.GtaskApi()

        self.connectSignals()
    
    def connectSignals(self):
        self.api.gotTaskLists[list].connect(self.refreshTasks)

    def sync(self):
        def cb(response):
            #Callback after list(TaskList) was retrived
            tls = response
            self.taskListModel.insertOrUpdate(tls)
        
        self.syncing.emit(True, "Fetching task lists")
        self.api.getTaskLists(cb)

    def refreshTasks(self, tls):
        self.syncing.emit(True, "Refreshing tasks")
        def callback(tlid, res):
            # Update tasks with the internal tasklist id
            for t in res:
                tl = self.taskListModel.taskListForTlid(tlid)
                t.tasklist = tl.id
            self.taskModel.insertOrUpdate(res)
            self.syncing.emit(False, '')

        for tl in tls:
            self.api.addToRefreshQueue(tl, callback)
         

