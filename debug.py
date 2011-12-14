import sys

DEBUG = True
DEBUG_LEVEL = 0
APP_NAME = "PyGtsks"

_dl = { 0: "Info",
        1: "Warning",
        2: "Error",
        3: "Critical"
        }

def debug(level, msg):
    if level >= DEBUG_LEVEL:
        _slevel = _dl[level]
        sys.stderr.write(APP_NAME+"."+_slevel +"::"+msg+"\n")

