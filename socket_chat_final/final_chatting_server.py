import socket
import threading
import time
from queue import Queue
import numpy as np


class User_Manager(threading.Thread):
    def __init__(self,conn=None, addr=None):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.username = None
        
    def run(self):
        self.register_user()
        self.recv_msg()
        self.remove_user()

    def register_user(self):
        check = True
        while check:
            self.conn.send('로그인ID:'.encode())
            self.username = self.conn.recv(1024).decode().strip()
            
            for user in th2.userlist:
                if user == self.username:
                    self.conn.send("이미 등록된 사용자입니다.".encode())
                    break
            else:
                check=False
                th2.userlist.append(self)
                self.send_msg_all('%s 님 입장'%self.username)
        
    def remove_user(self):
        th2.userlist.remove(self)
        self.send_msg_all('%s 님 퇴장'%self.username)

    def send_msg_all(self,msg):
        
        for user in th2.userlist:
            user.conn.send(msg.encode())

    def recv_msg(self):
        while True:
            msg = self.conn.recv(1024).decode()
            if not msg:
                break
            msg = '[%s] :'%self.username + msg
            self.send_msg_all(msg)
            
                
class TCP_Manager(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen(5)
        self.userlist = []
        
    def run(self):
        print('연결중 ..')
        while True:
            
            conn, addr = self.server_socket.accept()
            print('연결됨')
            th1 = User_Manager(conn,addr)
            th1.start()
            
        # self.server_socket.close()
        # user.remove_user(username)
            
if __name__=='__main__':
    HOST = '192.168.0.121'
    PORT = 6000
    # Q = Queue()
    
    
    th2 = TCP_Manager()
    th2.start()

    
    
        
        # server_socket.close()
    

    
    
    

