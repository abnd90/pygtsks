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
        self.api.authenticate()
