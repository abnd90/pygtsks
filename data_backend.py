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
    def createTables():
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
            conn.execute("insert into %s (tlid, name) values (?, ?)"\
                    % (DB_TASKLIST_NAME),(tl.tlid, tl.name))
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
    hidden=''
    status=''
    deleted=''
    position=''
    completed=''
    parent=''

    def __init__(self, id, title, due, tasklist, notes='', tid=''):
        self.id = id
        self.title = title
        self.due = due
        self.tasklist = tasklist
        self.notes = notes
        self.tid = tid

    def __str__(self):
        return self.title
    
    @staticmethod
    def createTables():
        conn = sqlite3.connect(DB_NAME)
        try:
            conn.execute(DB_TASK_CREAT)
        except sqlite3.OperationalError, e:
            debug(0, str(e) + ", skipping creation.")
        finally:
            conn.close()


if __name__ == '__main__':
    TaskList.createTables()
    Task.createTables()
