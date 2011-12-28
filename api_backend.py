from oauth2client.client import OAuth2WebServerFlow
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.tools import run as _run
from PyQt4.QtCore import *

from data_backend import Task, TaskList
import httplib2
import json
from debug import debug

FLOW = OAuth2WebServerFlow(
        client_id = '440903353654.apps.googleusercontent.com',
        client_secret = 'IEA433WKXc6RdwWbiN0XJV3Y',
        scope='https://www.googleapis.com/auth/tasks',
        user_agent='pygtsks/1.0')


class GtaskApi(QObject):
    authenticated = False

    needsAuthentication = pyqtSignal(str)
    authenticationDone = pyqtSignal()
    gotTaskLists = pyqtSignal(list)

    _taskRefreshQueue = []

    def authenticate(self):
        # if self.authenticated == True:
        #     return
        # if hasattr(self, '_authThread'):
        #     if self._authThread.isRunning():
        #         debug(1, "Authentication already in progress")
        #         return
        # self._authThread = QThread()
        
        try:
            storage = Storage("tasks.dat")
            credentials = storage.get()

            if credentials is None or credentials.invalid == True:
                self.needsAuthentication.emit(\
                        FLOW.step1_get_authorize_url("http://localhost:8080/"))
                credentials = _run(FLOW, storage)
                self.authenticationDone.emit()

            http = httplib2.Http()
            http = credentials.authorize(http)
            self.service = build(serviceName='tasks', version='v1', http=http, \
                            developerKey='AIzaSyApuYS1zNEc93L059nwjYdtOWQwVEbg580')
            self.authenticated = True
        
        except httplib2.ServerNotFoundError,e:
            debug(2,"Connection failed, could not authenticate.")

        # self._authThread.run = run
        # self._authThread.start()


    def getTaskLists(self, callback=None):
        if hasattr(self, "_getTaskListsThread"):
            if self._getTaskListsThread.isRunning():
                self._getTaskListsThread.terminate()
        else:
            self._getTaskListsThread = QThread()

        def run():
            if not self.authenticated:
                self.authenticate()
            
            if self.authenticated:
                response = self.service.tasklists().list().execute()
                lists = response['items']
                tls = []

                for l in lists:
                    # Convert into internal data sructures
                    tl = TaskList(l['id'], l['title'])
                    tls.append(tl)
                
                self.gotTaskLists.emit(tls)
                if callback:
                    callback(tls)

        self._getTaskListsThread.run = run
        self._getTaskListsThread.start()

    def addToRefreshQueue(self, taskList, cb=None):
        self._taskRefreshQueue.append(taskList.tlid)
        
        if not hasattr(self, "_getSingleListThread"):
            self._getSingleListThread = QThread()
            
            def run():
                if not self.authenticated:
                    self.authenticate()
                
                if self.authenticated:
                    while len(self._taskRefreshQueue):
                        tlid = self._taskRefreshQueue.pop()
                        res = self.service.tasks().list(tasklist=tlid).execute()
                        res = res['items']
                        tasks = []
                        for task in res:
                            t = Task(title=task['title'], tid=task['id'])
                            tasks.append(t)
                        if cb:
                            cb(tlid, tasks)

            self._getSingleListThread.run = run

        if not self._getSingleListThread.isRunning():
            self._getSingleListThread.start()


