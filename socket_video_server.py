from collections import UserList
import queue
import socket
import cv2
import numpy as np
from _thread import *
# from collections import deque
import time
from queue import Queue
stream_deque = Queue()
## 이미지 스트리밍
## 쓰레드 두개 생성 - 클라이언트가 접속하면 큐에서 이미지를 꺼내어 클라이언트에 전송하는 쓰레드,
#                  - 웹캠으로부터 캡처한 이미지를 큐에 삽입하는 쓰레드
def threaded(client_socket, addr, stream_deque):
    print('connected by:', addr[0], ':', addr[1])

    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print('disconnected')
                break
            # if len(stream_deque) >= 2:
            stringData = stream_deque.get() ## 큐에서 이미지 꺼냄
           
            client_socket.send(str(len(stringData)).ljust(16).encode()) ##클라이언트에게 전송
            client_socket.send(stringData) 
            # time.sleep(0.001)
        


        except ConnectionResetError as e:
            print('disconnected by'+ addr[0],':', addr[1])
            break
    client_socket.close()

def video_stream(stream_deque):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if ret:
                encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
                result, img_encode = cv2.imencode('.jpg', frame, encode_param)

                data = np.array(img_encode)
                stringData = data.tostring()

                stream_deque.put(stringData)
                cv2.imshow('image', frame)
                if cv2.waitKey(10) & 0xFF == 27:
                    cv2.destroyAllWindows()
                    exit()


HOST = '192.168.0.121'
PORT = 6000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# 포트 사용중이라 연결할 수 없다는 
# WinError 10048 에러 해결를 위해 필요합니다. 
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind 함수는 소켓을 특정 네트워크 인터페이스와 포트 번호에 연결하는데 사용됩니다.
# HOST는 hostname, ip address, 빈 문자열 ""이 될 수 있습니다.
# 빈 문자열이면 모든 네트워크 인터페이스로부터의 접속을 허용합니다.
server_socket.bind((HOST, PORT))

# 서버가 클라이언트의 접속을 허용하도록 합니다. 
server_socket.listen()

print('server start')
print('%d번 포트로 접속 대기중...'%PORT)
start_new_thread(video_stream, (stream_deque,))

while True: 
# 클라이언트가 접속하면 accept 함수에서 새로운 소켓을 리턴 
    client_socket, addr = server_socket.accept() 
    start_new_thread(threaded, (client_socket, addr, stream_deque,)) 

server_socket.close()