import cv2
import threading
import socket
from cv2 import data
import numpy as np


class ReadAndEncode(threading.Thread):
    def __init__(self,url=None, sock=None):
        threading.Thread.__init__(self)
        self.cap = None
        self.frame = None
        self.sock = sock
        # self.string_result = None
        if url is not None:
            self.cap = cv2.VideoCapture(url)
            self.cap.set(3,640)
            self.cap.set(4,480)

    def run(self):
        # th_send.start_check = True
        while True:
            ret, frame = self.cap.read()
            
            if ret:
                self.frame = frame
                self.frame = cv2.resize(self.frame, dsize=(640,480), interpolation=cv2.INTER_AREA)
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY),80]
                data, encoded_frame = cv2.imencode('.jpg', self.frame, encode_param)
                if data:

                    string_data = np.array(encoded_frame).tostring()
                    self.sock.send(str(len(string_data)).encode().ljust(16))
                    self.sock.send(string_data)
                    # decimg=cv2.imdecode(string_data,1)
                    cv2.imshow('CLIENT',self.frame)
                    if cv2.waitKey(1) & 0xFF == 27:
                        break

class SendEncode(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client_socket.connect((HOST,PORT))
        self.start_check = False
        
    def run(self):
        th_enc = ReadAndEncode(url,self.client_socket)
        th_enc.start()
        self.start_check=True
            
            # self.client_socket.send(str(len(th_enc.string_result)).ljust(24))
            # self.client_socket.send(th_enc.string_result)
            # self.client_socket.close()
if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 6000
    url = 'rtsp://admin:4ind331%23@192.168.0.242/profile2/media.smp'
    # url = 0

    th_send = SendEncode()
    th_send.start()