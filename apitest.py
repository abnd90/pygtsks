from oauth2client.client import OAuth2WebServerFlow
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.tools import run

import httplib2
import gflags

FLOW = OAuth2WebServerFlow(
        client_id = '440903353654.apps.googleusercontent.com',
        client_secret = 'IEA433WKXc6RdwWbiN0XJV3Y',
        scope='https://www.googleapis.com/auth/tasks',
        user_agent='pygtsks/1.0')

storage = Storage("tasks.dat")
credentials = storage.get()
if credentials is None or credentials.invalid == True:
    print FLOW.step1_get_authorize_url("http://localhost:8080/")
    credentials = run(FLOW, storage)

http = httplib2.Http()
http = credentials.authorize(http)

service = build(serviceName='tasks', version='v1', http=http,
        developerKey='AIzaSyApuYS1zNEc93L059nwjYdtOWQwVEbg580')

print service.tasklists().list().execute()
