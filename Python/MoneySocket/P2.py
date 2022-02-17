import socket
import multiprocessing

HOST = '127.0.0.1'
PORT = 1234

queue = []
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.connect(('127.0.0.1', 1234))