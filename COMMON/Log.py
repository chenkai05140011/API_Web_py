from __future__ import unicode_literals
from CONFIG.Define import LogLevel
import time

def LogOutput(level=LogLevel.INFO, message=""):
    currentTime = time.strftime('%Y-%m-%d %H:%M:%S')
    if(level == LogLevel.INFO):
        print("[%s][INFO][%s]" % (currentTime,message))
    elif(level == LogLevel.DEBUG):
        print("[%s][DEBUG][%s]" % (currentTime,message))
    elif(level == LogLevel.ERROR):
        print("[%s][ERROR][%s]" % (currentTime,message))
    elif(level == LogLevel.WARN):
        print("[%s][WARN][%s]" % (currentTime,message))
    else:
        print('log level set error!')


