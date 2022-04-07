import socket
import threading
import time
import sys

HOST = "127.0.0.1"
PORT = int(sys.argv[1])
connected = False

value = 0
while True:
    socket_obj =  None
    while connected == False:
        try:
            socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_obj.connect((HOST, PORT))
            print(socket_obj)
            connected = True
            break
        except:
            continue
    while True:
        try:
            value = str.encode(str(value))
            print(value)
            socket_obj.sendall(value)
            data = socket_obj.recv(1024)
            value = int(data.decode())
            print("value:", value)
            time.sleep(1)
        except:
            value = int(value)
            print(value)
            connected = False
            break
    