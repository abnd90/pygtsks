from PyQt4.QtCore import *

import api_backend
import taskmodel

class Controller():

    def __init__(self):
        self.taskListModel = taskmodel.TaskListModel()
        self.api = api_backend.GtaskApi()

        self.connectSignals()
    
    def connectSignals(self):
        pass

    def sync(self):
        def cb(response):
            #Callback after tasklist was retrived
            tl = response
            self.taskListModel.insert(tl)
        self.api.getTaskLists(cb)
