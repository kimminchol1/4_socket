import cv2
import threading
import socket
from cv2 import data
import numpy as np



class ReadAndEncode(threading.Thread):
    def __init__(self,url=None):
        threading.Thread.__init__(self)
        self.cap = None
        self.frame = None
        # self.string_result = None
        if url is not None:
            self.cap = cv2.VideoCapture(url)
            self.cap.set(3,640)
            self.cap.set(4,480)

    def run(self):
        
        while True:
            ret, frame = self.cap.read()
            if ret:
                self.frame = frame
                encoding = [int(cv2.IMWRITE_JPEG_QUALITY),90]
                data, encoded_frame = cv2.imencode('.jpg', self.frame, encoding)

                result = np.array(encoded_frame)
                string_result = result.tostring()
                th_send.client_socket.send(str(len(string_result)).ljust(16))
                th_send.client_socket.send(string_result)
                th_send.client_socket.close()
                decimg=cv2.imdecode(data,1)
                cv2.imshow('CLIENT',decimg)
                if cv2.waitKey(10) & 0xFF == 27:
                    break

class SendEncode(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client_socket.connect((HOST,PORT))
        
    def run(self):
        while True:
            th_enc = ReadAndEncode(url)
            th_enc.start()
            
            # self.client_socket.send(str(len(th_enc.string_result)).ljust(24))
            # self.client_socket.send(th_enc.string_result)
            # self.client_socket.close()
            



if __name__ == '__main__':
    HOST = '192.168.0.121'
    PORT = 6000
    url = 'rtsp://admin:4ind331%23@192.168.0.242/profile2/media.smp'

    th_send = SendEncode()
    th_send.start()