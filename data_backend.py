import sqlite3

conn = sqlite3.connect('test')

DB_TASKLIST_NAME = 'TASKLIST'
DB_TASKLIST_CREAT = """create table %s (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                        tlid TEXT, 
                                        name TEXT NOT NULL)""" % DB_TASKLIST_NAME

DB_TASK_NAME = 'TASK'
DB_TASK_CREAT = """create table %s (
                                    """ % DB_TASK_NAME

class TaskList():
    tlid=''
    name=''
    id=0

    def __init__(self, tlid, name, id=0):
        self.name=name
        self.tlid=tlid
        self.id=id

class Task():
    id=''
    tid=''
    title=''
    notes=''
    updated=''
    due='' 
    hidden=''
    status=''
    deleted=''
    eTag=''
    position=''
    completed=''

    def __init__(self, tid, title, notes, updated, due, hidden):
        pass

def createTables():
    try:
        c = conn.cursor()
        c.execute(DB_TASKLIST_CREAT)
    except sqlite3.OperationalError, e:
        print str(e) + ", skipping creation."
    finally:
        c.close()

def getTaskLists():
    c = conn.cursor()
    c.execute("select * from %s" % DB_TASKLIST_NAME)
    list_tl = []
    for row in c:
        tl = TaskList(row[1], row[2], row[0])
        list_tl.append(tl)
    return list_tl
    
def insertTaskList(tl):
    conn.execute("insert into %s (%s,%s) values (?, ?)" % (DB_TASKLIST_NAME, 'tlid', 'name'), (tl.tlid, tl.tlname))
    conn.commit()

def getTaskList(id):
    c = conn.create()
    c.execute("select * from %s where id=?" % DB_TASKLIST_NAME, (id,))
    row = c.fetchone()
    return TaskList(row[1], row[2], row[0])

if __name__ == '__main__':
    createTables()
    insertTaskList(TaskList('TESTID', 'TESTNAME'))


