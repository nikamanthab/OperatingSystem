import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 1234        # Port to listen on (non-privileged ports are > 1023)
counter = 0

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(s)
    while counter<1:
        conn, addr = s.accept()
        counter+=1
    print("hi")
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)