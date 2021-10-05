import socket
import threading 
import numpy as np
import cv2
from queue import Queue


HOST = '192.168.0.121'
PORT = 6000


Q = Queue()
# class threadA(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)


#     def recv_frame(self, sock, count):
#         buff = b''
#         while count:
#             new_buffer = sock.recv(count)
            
#             if not new_buffer:
#                 return None
#             buff += new_buffer
#             count -= len(new_buffer)
#             # print(count)
#         return buff



# class threadB(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
    
#     def run(self):
#         while True: 

#             # message = input('Enter Message : ')
#             self.message = '1'
#             client_socket.send(self.message.encode())
            
#             self.length = th_recv.recv_frame(client_socket, 16)
            
#             self.stringData = th_recv.recv_frame(client_socket,int(self.length))
            
#             self.data = np.frombuffer(self.stringData,dtype='uint8')
            
#             decimg=cv2.imdecode(self.data,1)
#             cv2.imshow('image',decimg)
            
#             key = cv2.waitKey(1)
#             if key == 27:
#                 break

#         client_socket.close()

class threadC(threading.Thread):
    def __init__(self, url = None):
        threading.Thread.__init__(self)
        self.cap = None
        # self.name = name
        self.frame = None
        if url is not None:
            self.cap = cv2.VideoCapture(url)
            self.cap.set(3,640)
            self.cap.set(4,480)

    def run(self):
        while True:
            ret,frame = self.cap.read()
            frame = cv2.resize(frame, dsize=(640,480), interpolation=cv2.INTER_AREA)
            if ret:
                self.frame = frame
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY),90]
                result, img_encode = cv2.imencode('.jpg',frame,encode_param)

                data = np.array(img_encode)
                stringData = data.tostring
                Q.put(stringData)
                cv2.imshow('frame',frame)
                if cv2.waitKey(10) & 0xFF ==27:
                    break


if __name__ == '__main__':
    
    cctv = 'rtsp://admin:4ind331%23@192.168.0.242/profile2/media.smp'
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    client_socket.connect((HOST, PORT))

    # th_recv = threadA()
    # th_recv.start()

    # th_read_buff = threadB()
    # th_read_buff.start()

    th_send_frame = threadC(url=cctv)
    th_send_frame.start()