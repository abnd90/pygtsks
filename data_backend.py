import sqlite3
from debug import debug

DB_NAME = 'test'

DB_TASKLIST_NAME = 'TASKLIST'
DB_TASKLIST_CREAT = """create table %s (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                        tlid TEXT UNIQUE, 
                                        name TEXT NOT NULL)""" % DB_TASKLIST_NAME

DB_TASKS_NAME = 'TASKS'
DB_TASKS_CREAT = """create table %s (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                     TASKLIST INTEGER,
                                     TID TEXT UNIQUE,
                                     TITLE TEXT NOT NULL,
                                     NOTES TEXT,
                                     UPDATED TEXT,
                                     DUE TEXT,
                                     HIDDEN INTEGER,
                                     STATUS TEXT,
                                     DETLETED INTEGER,
                                     POSITION TEXT,
                                     COMPLETED TEXT,
                                     PARENT TEXT,
                                     FOREIGN KEY(TASKLIST) REFERENCES TASKLIST(ID))"""  % DB_TASKS_NAME


class TaskList():
    tlid=''
    name=''
    id=0

    def __init__(self, tlid, name, id=0):
        self.name=name
        self.tlid=tlid
        self.id=id

    def __str__(self):
        return self.name
    
    @staticmethod
    def createTable():
        conn = sqlite3.connect(DB_NAME)
        try:
            conn.execute(DB_TASKLIST_CREAT)
        except sqlite3.OperationalError, e:
            debug(0, str(e) + ", skipping creation.")
        finally:
            conn.close()

    @staticmethod
    def getAll():
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("select * from %s" % DB_TASKLIST_NAME)
        list_tl = []
        for row in c:
            tl = TaskList(row[1], row[2], row[0])
            list_tl.append(tl)
        return list_tl
    
    @staticmethod   
    def insert(tl):
        conn = sqlite3.connect(DB_NAME)
        conn.execute("insert into %s (%s,%s) values (?, ?)" \
                % (DB_TASKLIST_NAME, 'tlid', 'name'), (tl.tlid, tl.name))
        conn.commit()
        conn.close()
    
    @staticmethod
    def update(tl):
        conn = sqlite3.connect(DB_NAME)
        conn.execute("update %s set tlid=?, name=? where id=?"\
                % DB_TASKLIST_NAME, (tl.tlid, tl.name, tl.id))
        conn.commit()
        conn.close()

    @staticmethod
    def get(id):
        conn = sqlite3.connect(DB_NAME)
        c = conn.create()
        c.execute("select * from %s where id=?" % DB_TASKLIST_NAME, (id,))
        row = c.fetchone()
        c.close()
        conn.close()
        return TaskList(row[1], row[2], row[0])
    
    @staticmethod
    def insertOrUpdate(tl):
        """ Inserts or updates a tasklist based on whether the google-assigned
            ID already exists in the DB"""

        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("select * from %s where tlid=?" % DB_TASKLIST_NAME, (tl.tlid, ))
        r = cur.fetchone()
        if r:
            conn.execute("update %s set name=? where tlid=?" % (DB_TASKLIST_NAME),\
                    (tl.name, tl.tlid))
        else:
            TaskList.insert(tl)
        conn.commit()
        conn.close()



class Task():
    id=0
    tasklist=0
    tid=''
    title=''
    notes=''
    updated=''
    due='' 
    hidden=0
    status=''
    deleted=0
    position=''
    completed=''
    parent=''

    def __init__(self, title, id=0, due='', tasklist=0, notes='', tid='',\
            completed='', status=''):
        self.id = id
        self.title = title
        self.due = due
        self.tasklist = tasklist
        self.notes = notes
        self.tid = tid
        self.status = status

    def __str__(self):
        return str(self.id)+" "+self.title
    
    @staticmethod
    def createTable():
        conn = sqlite3.connect(DB_NAME)
        try:
            conn.execute(DB_TASKS_CREAT)
        except sqlite3.OperationalError, e:
            debug(0, str(e) + ", skipping creation.")
        finally:
            conn.close()

    @staticmethod
    def insert(task):
        conn = sqlite3.connect(DB_NAME)
        conn.execute("insert into %s (%s,%s,%s,%s,%s,%s,%s) values \
                (?,?,?,?,?,?,?)" \
                % (DB_TASKS_NAME , 'tid', 'title','tasklist', 'notes',\
                'status', 'due','completed'), \
                (task.tid, task.title, task.tasklist, task.notes,\
                task.status, task.due,task.completed))

        conn.commit()
        conn.close()

    @staticmethod
    def get(taskListId):
        """ Returns all tasks in a tasklist. 
        If taskListId == -1, returns tasks of all tasklists. """

        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        if taskListId == -1:
            res = cur.execute("select * from %s" % DB_TASKS_NAME)
        else:
            res = cur.execute("select * from %s where tasklist=?" \
                    % DB_TASKS_NAME, (taskListId, ))
        tasks = []
        for row in res:
            task = Task(id=row[0], tid=row[2], \
                    title=row[3], tasklist=row[1], notes=row[4],\
                    due=row[6], completed=row[11], status=row[8])
            tasks.append(task)
        cur.close()
        conn.close()
        return tasks
    
    @staticmethod
    def insertOrUpdate(task):
        """ Inserts or updates a tasks based on whether the google-assigned
            ID already exists in the DB """

        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("select * from %s where tid=?" % DB_TASKS_NAME, (task.tid, ))
        r = cur.fetchone()
        if r:
            conn.execute("update %s set title=? where tid=?" % (DB_TASKS_NAME),\
                    (task.title, task.tid))
        else:
            Task.insert(task)
        conn.commit()
        conn.close()



TaskList.createTable()
Task.createTable()
