import socket
import threading
import time
import sys

HOST = "127.0.0.1"
PORT = int(sys.argv[1])

def increment_number(num):
    return num+1

def respond_heartbeat(conn):
    print("running heartbeat")
    while True:
        data = conn.recv(1024)
        if data:
            conn.sendall(b'available')

def handle_client_request(conn):
    while True:
        data = conn.recv(1024)
        data = int(data)
        data = increment_number(data)
        data = str.encode(str(data))
        print(data)
        conn.sendall(data)

def start_process():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    backup_conn, backup_addr = s.accept()
    thread1 = threading.Thread(target=respond_heartbeat, args=(backup_conn, ))
    thread1.start()
    print("hi")
    client_conn, client_addr = s.accept()
    thread2 = threading.Thread(target=handle_client_request, args=(client_conn, ))
    thread2.start()
    print("running...")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((HOST, PORT))
        s.sendall(b"available")
        time.sleep(2)
        start_process()
    except:
        start_process()
    