import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new
import zlib
import threading
from queue import Queue
import os
import hashlib
import time
#import BinaryRCNN
'''
Purpose of this function is getting frames from video and returning it in fifo que
It can by developed for capturing video from camera
Attributes: none 
Returns: fifo queue


'''

def frame_from_video():
    fifo_frames = Queue()
    cap = cv2.VideoCapture("1234.mp4")

   # while (cap.isOpened()):
    for i in range(100):
        ret, frame = cap.read()
        fifo_frames.put(frame)

    return fifo_frames
'''
This function manages connections with slaves.
When slave is connected it sends "ready". After that master send to slave RRD order and frame data. 
It stands for be Ready to Receive Data. Slave will send RC(received).
Next master will send SBD(Send Back Data) and the work of slave will start.
When work is finished slave will send data to master.

Attributes : conn - Connection from socket
           : addr - Adders from socket
           : frame - Frame 
Returns: none 


'''
def job_for_hosts(conn,addr,frame,fr_num):
    while 1:
        ##print("123")
        data = conn.recv(90456)
        data = data.decode()
        #print("Recived:{}".format(data))
        if data == "ready":
            print("sending data to:{}".format(addr))
            conn.send("RRD".encode())

            data = cv2.imencode('.jpg', frame)[1].tostring()
            #z1 = hashlib.md5()
            #z1.update(data)

            ##print(z1.hexdigest())
            x1 = str(len(data))
            x1 = x1.encode()
            size_of_buffor = int(len(data) / 4096)
            conn.send(x1)
            reply = conn.recv(1024)
            ##print(reply)

            for i in range(size_of_buffor + 1):
                conn.sendall(data[4096 * i:4096 + 4096 * i])
                ##print(4096 + 4096 * i)

            #conn.sendall(data)
        if data == "RC":
            #print("Order SBD send to slave")
            conn.send("SBD".encode())
            rc_data = conn.recv(90456)
            print("Recived from {}".format(addr))
            while len(rc_data)< int(x1):
                rc_data += conn.recv(90456)
            o1 = hashlib.md5()
            o1.update(rc_data)
            #print(o1.hexdigest())
            #number_frame = rc_data[:struct.calcsize(">L")]
            #number_frame = struct.unpack(">L", number_frame)
            ##print(number_frame)
            #rc_data = rc_data[struct.calcsize(">L"):]
            nparr = np.fromstring(rc_data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            cv2.imshow('ImageWindow', frame)
            cv2.waitKey(1)
            break
    conn.close()
    return
def end_jobs(conn,addr):
    #print("closing: {}".format(addr))
    conn.send("END".encode())
    return

HOST='192.168.0.114'
PORT=2222
proto = socket.getprotobyname('tcp')
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM,proto)
#print('Socket created')
s.bind((HOST,PORT))
#print('Socket bind complete')
s.listen(10) #max number of slaves
#print('Socket now listening')

list_of_workers = []
q_f = frame_from_video()
#q = Queue()
#q.put(cv2.imread("123.jpg"))
i = 0
#print("TAK")
while 1:
    conn, addr = s.accept()
    #job_for_hosts(conn,addr,pickle.dumps("penis"))
    #_thread.start_new_thread(job_for_hosts,(conn,addr,pickle.dumps("penis")))
    if(q_f.empty()):
        threading.Thread(end_jobs(conn,addr)).start()
        break
    tmp = q_f.get_nowait()
    tmp2 = struct.pack(">L",i)
    i= i+1
    threading.Thread(job_for_hosts(conn, addr,tmp,tmp2)).start()


    #end_jobs(conn,addr)

#print("end")

#frame = pickle.loads(data, fix_imports=True, encoding="bytes")
#frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
#cv2.imshow('ImageWindow',frame)
#cv2.waitKey(1)
'''
frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
        cv2.imshow('ImageWindow', frame)
        cv2.waitKey(1)

frame = conn.recv(8192)
data = b""
payload_size = struct.calcsize(">L")

cv2.imshow('ImageWindow',frame)
cv2.waitKey(1)

data = b""
payload_size = struct.calcsize(">L")
#print("payload_size: {}".format(payload_size))
while True:
    while len(data) < payload_size:
        #print("Recv: {}".format(len(data)))
        data += conn.recv(8192)

    #print("Done Recv: {}".format(len(data)))
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    #print("msg_size: {}".format(msg_size))
    while len(data) < msg_size:
        data += conn.recv(8192)
    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    cv2.imshow('ImageWindow',frame)
    cv2.waitKey(1)
    '''