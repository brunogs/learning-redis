import time
import threading
import redis

conn = redis.Redis()

def notrans():
    pipeline = conn.pipeline()
    pipeline.incr('trans:')
    time.sleep(.1)
    pipeline.incr('trans:', -1)
    print pipeline.execute()[0]

if 1:
    for i in xrange(3):
        threading.Thread(target=notrans).start()
    time.sleep(.5)
