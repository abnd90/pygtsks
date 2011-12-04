from oauth2client.client import OAuth2WebServerFlow
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.tools import run
from PyQt4.QtCore import *

from data_backend import Task, TaskList
import httplib2
import json

FLOW = OAuth2WebServerFlow(
        client_id = '440903353654.apps.googleusercontent.com',
        client_secret = 'IEA433WKXc6RdwWbiN0XJV3Y',
        scope='https://www.googleapis.com/auth/tasks',
        user_agent='pygtsks/1.0')


class GtaskApi():

    def authenticate(self):
        try:
            storage = Storage("tasks.dat")
            credentials = storage.get()

            if credentials is None or credentials.invalid == True:
                #Signal auth reqd
                FLOW.step1_get_authorize_url("http://localhost:8080/")
                credentials = run(FLOW, storage)

            http = httplib2.Http()
            http = credentials.authorize(http)
            self.service = build(serviceName='tasks', version='v1', http=http, \
                            developerKey='AIzaSyApuYS1zNEc93L059nwjYdtOWQwVEbg580')
            
        except httplib2.ServerNotFoundError,e:
            print "Connection failed, could not authenticate."


    def getTaskLists(self):
        response = self.service.tasklists().list().execute()
        return response
    
    def getTask(self, tid, tlid='@default'):
        task = service.tasks().get(tasklist=tlid, task=tid).execute()
        return task

    def getTaskList(self, tlid):
        tasklist = service.tasklists().get(tasklist=tlid).execute()
        return tasklist

if __name__ == '__main__':
    g = GtaskApi()
    print g.getTaskLists()

