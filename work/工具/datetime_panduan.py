import datetime
import time

def is_flag():
    current=datetime.datetime.now()
    current2=datetime.datetime.now()
    print(current)
    Today=datetime.datetime.today()
    print(Today)
    t=datetime.time(hour=19,minute=0,second=0)
    result=datetime.datetime.combine(current2.date(),t)
    print(result)
    timestamp1=time.mktime(current.timetuple())
    timestamp2=time.mktime(result.timetuple())
    print(timestamp1)
    print(timestamp2)
    return timestamp1>timestamp2
print(is_flag())
