import socket
import pickle
import time
import struct
import cv2
#import BinaryRCNN

# client_socket.connect(('192.168.0.114', 2222))
# connection = client_socket.makefile('wb')
print("start")
is_working = False
'''
SYS - set your status 
RRD - be ready to recive data
SBD - send back data 
'''
flag1 = True
while True:

    if flag1:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('192.168.0.114', 2222))
        connection = client_socket.makefile('wb')
        starter = pickle.dumps("ready")
        print("123")
        client_socket.send(starter)
        flag1 = False

    orders = client_socket.recv(4096)
    orders = pickle.loads(orders)
    print(orders)

    if orders == "RRD":
        '''
        while len(data) < payload_size:
            print("Recv: {}".format(len(data)))
            data += client_socket.recv(4096)

        number_frame = data[:struct.calcsize(">L")]
        number_frame = struct.unpack(">L",number_frame)
        print(number_frame)
        data = pickle.loads(data[struct.calcsize(">L"):])
        print("recived data:{}".format(pickle.loads(data)))
        client_socket.send(pickle.dumps("RC"))

        print("order RC send to host")
'''

    if orders == "SBD":
        client_socket.sendall(struct.pack(">L",number_frame)+pickle.dumps(data))
        print("Data send to host")
        client_socket.close()
        flag1 = True

    if orders == "END":
        break


