import socket
import threading
import cv2
import numpy as np
from queue import Queue


class ReadVideo(threading.Thread):
    def __init__(self,conn=None,addr=None):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.cap = None
        
        self.buff = b''
        self.frame = None
        self.new_buff = None
        # self.decoded_frame = None
        
        

    def run(self):
        while True:
            length = self.decode_video(16)
            stringData = self.decode_video(int(length))
            data = np.frombuffer(stringData,dtype='uint8')
            # th_server.server_socket.close()

            decoded_frame = cv2.imdecode(data,1)
            cv2.imshow('server',decoded_frame)
            print("영상 불러오기 완료")
            if cv2.waitKey(10) & 0xFF == 27:
                break

            
        
    def decode_video(self,count):
        while count:
            self.newbuff = self.conn.recv(count)
            if not self.newbuff:
                return None
            self.buff += self.newbuff
            count -= len(self.newbuff)
            return self.buff
            
class TcpManager(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST,PORT))
        self.server_socket.listen()

    def run(self):
        print("영상 불러오는중..")
        while True:
            conn, addr = self.server_socket.accept()
            
            th_read = ReadVideo(conn,addr)
            th_read.start()
            
            
        # self.server_socket.close()
            


# class DecodeVideo(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)

#     def run(self):
#         pass


if __name__ == '__main__':
    HOST = '192.168.0.121'
    PORT = 6000

    th_server = TcpManager()
    th_server.start()

    