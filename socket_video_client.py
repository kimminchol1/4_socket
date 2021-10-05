import socket 
import numpy as np
import cv2


HOST = '192.168.0.121'
PORT = 6000


def recv_frame(sock, count):
    buff = b''
    while count:
        new_buffer = sock.recv(count)
        if not new_buffer:
            return None
        buff += new_buffer
        count -= len(new_buffer)
    return buff




client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 

client_socket.connect((HOST, PORT))



# 키보드로 입력한 문자열을 서버로 전송하고 
# 서버에서 에코되어 돌아오는 메시지를 받으면 화면에 출력합니다. 
# quit를 입력할 때 까지 반복합니다. 
while True: 

    # message = input('Enter Message : ')   
    message = '1'
    client_socket.send(message.encode())
    
    length = recv_frame(client_socket, 16)
    
    stringData = recv_frame(client_socket,int(length))
    
    data = np.frombuffer(stringData,dtype='uint8')
    
    decimg=cv2.imdecode(data,1)
    # print(decimg)
    cv2.imshow('image',decimg)
    
    key = cv2.waitKey(1)
    if key == 27:
        break

client_socket.close()