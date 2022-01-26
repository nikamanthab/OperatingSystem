from threading import Semaphore
import threading
from threading import Thread
from time import sleep
buffer = [""]*25
in_file = open('input.txt','r')
out_file = open('output.txt', 'w')
head_ptr = 0
tail_ptr = 0
mutex = Semaphore()
sem_p = Semaphore(25)
sem_c = Semaphore(0)
length = 0
counter = 0
# with open(r"input.txt", 'r') as fp:
#     length = len(fp.readlines())
# print(length)
# function to create threads
def producer():
    global buffer
    global head_ptr
    string = in_file.readline()
    while(string):
        # sem_p.acquire()
        x = mutex.acquire()
        print(x)
        buffer[head_ptr] = string
        string = in_file.readline()
        print(threading.get_ident())
        print("reading: ", string)
        head_ptr+=1
        head_ptr = head_ptr%25
        mutex.release()
        # sem_c.release()
    print("err:", string)
    return

def consumer():
    global buffer
    global tail_ptr
    global counter
    while(counter < length):
        sem_c.acquire()
        mutex.acquire()
        counter+=1
        print("writing to file")
        # out_file.writelines([buffer[tail_ptr]])
        buffer[tail_ptr] = ""
        tail_ptr+=1
        tail_ptr = tail_ptr%16
        mutex.release()
        sem_p.release()
        print(buffer)

    return
    

if __name__ == '__main__':
    thread1 = Thread(target = producer)
    thread3 = Thread(target = producer)
    # thread2 = Thread(target = consumer)

    # thread4 = Thread(target = consumer)

    thread1.start()
    # thread2.start()
    thread3.start()
    # thread4.start()
    thread1.join()
    # thread2.join()
    thread3.join()
    # thread4.join()
    print("thread finished...a=", buffer)