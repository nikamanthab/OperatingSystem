import threading
from threading import Thread
from time import sleep
lock = threading.Lock()
a = 0
# function to create threads
def increment1(arg):
    global a
    for i in range(arg):
        lock.acquire()
        a=a+1
        print("a in 1 ->", a)
        lock.release()

def increment2(arg):
    global a
    for i in range(arg):
        lock.acquire()
        a=a+1
        print("a in 2 ->", a)
        lock.release()
 
thread1 = Thread(target = increment1, args=(10, ))
thread2 = Thread(target = increment2, args=(10, ))

thread1.start()
thread2.start()
thread1.join()
thread2.join()
print("thread finished...a=", a)