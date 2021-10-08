import socket
import threading
import cv2
import numpy as np
from collections import deque
import time

from darknet.yolo_python import net

class ReceiveVideoManager(threading.Thread):
    def __init__(self,conn=None,addr=None):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        
        self.decoded_frame = None
        self.frame_count = 0
        self.results = []
        

    def run(self):
        while th_server.start_check:
            try:
                length = self.decode_video(16)
                stringData = self.decode_video(int(length))
                data = np.fromstring(stringData, dtype='uint8')
                self.decoded_frame = cv2.imdecode(data,cv2.IMREAD_COLOR)
                self.frame_count +=1
                
                # cv2.imshow('SERVER', self.decoded_frame)
                # cv2.waitKey(1)

                if (self.frame_count%3 == 0) & len(th_server.stream_deque) < 30:
                    th_server.stream_deque.append([self, self.decoded_frame])
                
                
            except Exception as e:
                print(e)
                th_server.start_check = False

            
    def decode_video(self,count):
        buf = b''
        while count:
            if count >0:
                newbuff = self.conn.recv(count)
            if not newbuff:
                return None
            buf += newbuff
            count -= len(newbuff)
        return buf


class TcpManager(threading.Thread):
    # global get_frame
    def __init__(self):
        threading.Thread.__init__(self)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((HOST,PORT))
        self.server_socket.listen()
        
        self.stream_deque = deque()
        self.thread_list = []
        self.start_check = False

    def run(self):
        print("영상 불러오는중..")
        while True:
            conn, addr = self.server_socket.accept()
            print("연결됨")
            self.start_check = True
            
            th_read = ReceiveVideoManager(conn,addr)
            self.thread_list.append(th_read)
            for thr in self.thread_list:
                thr.start()
            time.sleep(1)
            if len(self.stream_deque) > 0 :
                th_A, get_frame = self.stream_deque.popleft()

                results= net.detect(get_frame,0.5,0.5)
                th_A.results = results
                # cv2.imshow('server',get_frame)
                # cv2.waitKey(1)
            time.sleep(0.0001)
                
            
            

class DetectManager(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        time.sleep(0.0001)
        
        while True:
            for just_one in th_server.thread_list:
                if just_one.decoded_frame is not None:
                    frame = just_one.decoded_frame.copy()
                    
                    for detection in just_one.results:
                        label = detection[0]
                        confidence = detection[1]
                        x,y,w,h = detection[2]
                        xmin = int(round(x - (w / 2)))
                        xmax = int(round(x + (w / 2)))
                        ymin = int(round(y - (h / 2)))
                        ymax = int(round(y + (h / 2)))

                        labelText = label + ": " + str(np.rint(100 * confidence)) +"%"

                        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0,0,255), 2)
                        cv2.putText(frame, labelText, (xmin,ymin-12), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0,0,255), 1)
                        
                    
                    cv2.imshow('SERVER', frame)
                    # get_frame[th_A.name] = frame

            if cv2.waitKey(1) & 0xff == 27:
                cv2.destroyAllWindows()
                exit()

            time.sleep(1/30)

            
if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 6000

    
    # thread_list.append(th_read)
    # for thr in self.thread_list:
    #     thr.start()

    th_detect = DetectManager()
    th_detect.start()
    th_server = TcpManager()
    th_server.start()
    
    

    