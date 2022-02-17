from asyncio import tasks
from dataclasses import replace
import socket
import threading
from time import sleep, time

from database import *
import pandas as pd
queue = []
HOST = '127.0.0.1'
PORT1 = 1234
PORT2 = 1235
PORT3 = 1236
df = pd.DataFrame(data={'A':[100], 'B':[100], 'C':[100]})
df.to_csv('database.csv', index=False)
sleep(1)
queue={
    'p1': [],
    'p2': [],
    'p3': []
}

start_time = time()

CS = {'p1':False, 'p2':False, 'p3':False}
connection_list = {}

def CS(func, user, param):
    func(user, param)

def get_curr_time():
    return (time() - start_time)

def message_handler(conn, p_id):
    with conn:
        while True:
            request = conn.recv(2048)
            request = request.decode().split(" ")
            # print(request)
            if request[0] == 'RELEASE':
                queue[p_id] = queue[p_id][1:]
                print("p_id: {}, request: {}".format(p_id, request))
                if len(queue[p_id]) != 0:
                    if queue[p_id][0][1] == p_id[1]:
                        cs_details = queue[p_id][0][2]
                        # print("CS details::::::", cs_details)
                        cs_details[0](cs_details[1], cs_details[2])
                        queue[p_id] = queue[p_id][1:]
                        # queue['p1'] = queue['p1'][1:]
                        # queue['p3'] = queue['p3'][1:]
                        # print("::::::::::::::", connection_list)
                        release(connection_list[p_id][0])
                        release(connection_list[p_id][1])
                        print("release done........")
            elif request[0] == 'REQUEST':
                request = request[1:]
                queue[p_id].append(request)
                queue[p_id].sort()
                # print("server: ", p_id, queue)
                time_stamp = get_curr_time()
                reply_msg = "REPLY {}".format(time_stamp)
                conn.sendall(str.encode(reply_msg))
        # print("sent...", reply_msg, request)
    return 

def make_request(conn, msg):
    msg_str = 'REQUEST {} {}'.format(msg[0], msg[1])
    conn.sendall(str.encode(msg_str))
    reply_msg = conn.recv(2048)
    reply_msg = reply_msg.decode()
    return reply_msg.split(" ")

def release(conn):
    msg_str = 'RELEASE {}'.format(get_curr_time())
    # print("yoyo", conn)
    conn.sendall(str.encode(msg_str))


def socket_server(port, p_id):
    # connection_list[p_id] = []
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, port))
    s.listen()
    for i in range(2):
        conn, addr = s.accept()
        # connection_list[p_id].append([conn, addr])
        # print("connections in {} is {}".format(p_id, [addr for conn, addr in connection_list[p_id]]))
        msg_handler_thread = threading.Thread(target=message_handler, args=(conn, p_id))
        msg_handler_thread.start()
    msg_handler_thread.join()

    return 

def socket_client(port_no):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, port_no))
    return s

def process1():
    server = threading.Thread(target=socket_server, args=(PORT1, 'p1'))
    server.start()
    sleep(2)
    p2_connection = socket_client(PORT2)
    p3_connection = socket_client(PORT3)
    connection_list['p1'] = [p2_connection, p3_connection]
    tasks = [False, False]
    prev_queue = 0
    while(True):
        # if prev_queue is not queue:
        # print(queue)
            # prev_queue = queue
        instant_time = get_curr_time()
        # print(instant_time)
        if instant_time>4 and tasks[0] == False:
            tasks[0] = True
            msg = [str(int(instant_time)), '1', [DepositCash, 'A', 20]]
            queue['p1'].append(msg)
            queue['p1'].sort()
            p2_reply = make_request(p2_connection, msg)
            p3_reply = make_request(p3_connection, msg)
            # print("-------------")
            # print(p2_reply, p3_reply, msg)
            # print("--------------")
            # print(queue)
            if float(p2_reply[1])> float(msg[0]) and float(p3_reply[1])> float(msg[0]):
                if queue['p1'][0][1] == '1':
                        CS(*queue['p1'][0][2])
                        # CheckBalance()
                        queue['p1'] = queue['p1'][1:]
                        release(p2_connection)
                        release(p3_connection)
        elif instant_time>10 and tasks[1] == False:
            tasks[1] = True
            print(queue)
            msg = [str(instant_time), '1', [ApplyInterest, 'C', 10]]
            queue['p1'].append(msg)
            queue['p1'].sort()
            p2_reply = make_request(p2_connection, msg)
            p3_reply = make_request(p3_connection, msg)
            if float(p2_reply[1])> float(msg[0]) and float(p3_reply[1])> float(msg[0]):
                if queue['p1'][0][1] == '1':
                    CS(*queue['p1'][0][2])
                    # ApplyInterest('C', 10)
                    queue['p1'] = queue['p1'][1:]
                    release(p2_connection)
                    release(p3_connection)
        elif instant_time>200:
            CheckBalance()
            break
    
    server.join()
    
    return 

def process2():
    server = threading.Thread(target=socket_server, args=(PORT2, 'p2'))
    server.start()
    sleep(2)
    p1_connection = socket_client(PORT1)
    p3_connection = socket_client(PORT3)
    connection_list['p2'] = [p1_connection, p3_connection]

    tasks = [False, False]
    while(True):
        instant_time = get_curr_time()
        # print(instant_time)
        if instant_time>4 and tasks[0] == False:
            tasks[0] = True
            msg = [str(int(instant_time)), '2', [WithdrawCash, 'C', 30]]
            queue['p2'].append(msg)
            queue['p2'].sort()
            p1_reply = make_request(p1_connection, msg)
            p3_reply = make_request(p3_connection, msg)
            # print("-------------")
            # print(p1_reply, p3_reply, msg)
            # print("--------------")
            # print(queue)
            if float(p1_reply[1])> float(msg[0]) and float(p3_reply[1])> float(msg[0]):
                if queue['p2'][0][1] == '2':
                        CS(*queue['p2'][0][2])
                        # WithdrawCash('C', 30)
                        # print("after withdrawal")
                        # CheckBalance()
                        queue['p2'] = queue['p2'][1:]
                        release(p1_connection)
                        release(p3_connection)
        elif instant_time>12 and tasks[1] == False:
            tasks[1] = True
            msg = [str(instant_time), '2', [DepositCash, 'B', 40]]
            queue['p2'].append(msg)
            queue['p2'].sort()
            p1_reply = make_request(p1_connection, msg)
            p3_reply = make_request(p3_connection, msg)
            if float(p1_reply[1])> float(msg[0]) and float(p3_reply[1])> float(msg[0]):
                if queue['p2'][0][1] == '2':
                    CS(*queue['p2'][0][2])
                    # DepositCash('B', 40)
                    queue['p2'] = queue['p2'][1:]
                    release(p1_connection)
                    release(p3_connection)
        elif instant_time>200:
            CheckBalance()
            break
    server.join()
    return 

def process3():
    server = threading.Thread(target=socket_server, args=(PORT3, 'p3'))
    server.start()
    sleep(2)
    p1_connection = socket_client(PORT1)
    p2_connection = socket_client(PORT2)
    connection_list['p3'] = [p1_connection, p2_connection]

    tasks = [False, False]
    while(True):
        instant_time = get_curr_time()
        # print(instant_time)
        if instant_time>2 and tasks[0] == False:
            tasks[0] = True
            msg = [str(int(instant_time)), '3', [ApplyInterest, 'B', 10]]
            queue['p3'].append(msg)
            queue['p3'].sort()
            p2_reply = make_request(p2_connection, msg)
            p1_reply = make_request(p1_connection, msg)
            # print("-------------")
            # print(p2_reply, p1_reply, msg)
            # print("--------------")
            if float(p2_reply[1])> float(msg[0]) and float(p1_reply[1])> float(msg[0]):
                if queue['p3'][0][1] == '3':
                        CS(*queue['p3'][0][2])
                        # ApplyInterest('B', 10)
                        queue['p3'] = queue['p3'][1:]
                        # print("after p3, 2")
                        release(p2_connection)
                        release(p1_connection)
                        # print(queue)
        elif instant_time>15 and tasks[1] == False:
            tasks[1] = True
            msg = [str(instant_time), '3', [WithdrawCash, 'A', 10]]
            queue['p3'].append(msg)
            queue['p3'].sort()
            p2_reply = make_request(p2_connection, msg)
            p1_reply = make_request(p1_connection, msg)
            if float(p2_reply[1])> float(msg[0]) and float(p1_reply[1])> float(msg[0]):
                if queue['p3'][0][1] == '3':
                    CS(*queue['p3'][0][2])
                    # WithdrawCash('A', 10)
                    queue['p3'] = queue['p3'][1:]
                    release(p2_connection)
                    release(p1_connection)
        elif instant_time>200:
            CheckBalance()
            break
    server.join()
    return 

if __name__ == '__main__':

    p1 = threading.Thread(target=process1, args=())
    p2 = threading.Thread(target=process2, args=())
    p3 = threading.Thread(target=process3, args=())

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()