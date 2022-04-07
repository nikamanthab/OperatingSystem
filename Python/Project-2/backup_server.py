import socket
import threading
import time
from turtle import back
import sys

HOST = "127.0.0.1"
PORT = int(sys.argv[1])
primary_down = False

def increment_number(num):
    return num+1

def send_heartbeat():
    global primary_down
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                t1 = time.time()
                while True:
                    t2 = time.time()
                    if int(t2 - t1) == 1:
                        t1 = t2
                        try:
                            s.sendall(b'check')
                            data = s.recv(1024)
                            if data.decode() == "available":
                                print("available")
                                continue
                        except:
                            print(t2)
                            print('connection is broken', primary_down)
                            if primary_down == False:
                                primary_down = True
                                handle_from_backup()
                            break
        except:
            continue    

def handle_primary_reboot(ss):
    global primary_down
    conn, addr = ss.accept()
    data = conn.recv(1024)
    data = data.decode()
    print(data)
    if data == "available":
        primary_down = False
        

def handle_client_request(conn):
    global primary_down
    while True:
        if primary_down == False:
            break
        print("hii")
        data = conn.recv(1024)
        print("hii")
        data = int(data)
        print(data)
        data = increment_number(data)
        data = str.encode(str(data))
        print(data)
        conn.sendall(data)

def handle_from_backup():
    print("hihi")
    # time.sleep(4)
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ss.bind((HOST, PORT))
        ss.listen()
        conn, addr = ss.accept()
    except:
        print("error here")
    print(ss)
    thread = threading.Thread(target=handle_primary_reboot, args=(ss, ))
    thread.start()
    print("hey")
    handle_client_request(conn)



backup_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

thread1 = threading.Thread(target=send_heartbeat)
thread2 = threading.Thread(target=handle_client_request, args=(backup_server_socket, ))

thread1.start()
thread2.start()