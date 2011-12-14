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
        if hasattr(self, "_getTaskListThread"):
            if self._getTaskListThread.isRunning():
                self._getTaskListThread.terminate()
        else:
            self._getTaskListThread = QThread()

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
                    
                if callback:
                    callback(tls)

        self._getTaskListThread.run = run
        self._getTaskListThread.start()


    def getTask(self, tid, tlid='@default'):
        task = service.tasks().get(tasklist=tlid, task=tid).execute()
        return task

    def getTaskList(self, tlid):
        tasklist = service.tasklists().get(tasklist=tlid).execute()
        return tasklist

