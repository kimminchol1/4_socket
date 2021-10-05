import socketserver
import threading
from flask import Flask,render_template

HOST = '192.168.0.121'
PORT = 6000
# app = Flask(__name__)
# @app.route('/')
# def web_chat():
#     return render_template('index.html')

class User_Manage:
    def __init__(self):
        self.users = {}

    def add_user(self, username, conn, addr):
        if username in self.users:
            conn.send("이미 등록된 사용자입니다.".encode())
            return None
        self.users[username] = (conn,addr) # users = {username:(conn,addr), ....}
        self.send_message_all('[%s]님이 입장하셨습니다.'%username)
        

        return username

    def remove_user(self,username):
        del self.users[username]
        self.send_message_all('[%s] 님이 퇴장하셨습니다.'%username)

    def send_message_all(self,message):
        for conn,addr in self.users.values():
            conn.send(message.encode())

class TCP_Manager(socketserver.BaseRequestHandler):
    
    user = User_Manage()#이렇게 정의하면 self.userman으로 클래스접근가능

    def handle(self): #클라이언트 접속시 클라이언트 주소 출력
        
        # print('[%s] 연결됨'%self.client_address[0])
        try:
            username = self.register_user()
            print('[%s] 연결됨'%self.client_address[0])
            message = self.request.recv(1024)
            while message:
                print('[%s] '%username + message.decode())
                message = self.request.recv(1024)
        except Exception as e:
            print(e)

        
        self.user.remove_user(username)
        print('[%s] 연결끊김'%self.client_address[0])

    def register_user(self):
        while True:
            self.request.send('로그인ID:'.encode())
            username = self.request.recv(1024)
            username = username.decode().strip()
            if self.user.add_user(username, self.request, self.client_address[0]):
                return username

class ChatServer_Manager(socketserver.ThreadingMixIn,socketserver.TCPServer):
    pass

def run_server():
    # app.run(host='192.168.0.121', debug = False, port=6000)
    try:
        print("채팅을 시작합니다.")
        print('끝내려면 Ctrl-C를 누르세요.')
        serv = ChatServer_Manager((HOST,PORT),TCP_Manager)
        serv.serve_forever()
    except KeyboardInterrupt:
        print('채팅을 종료합니다.')
        serv.shutdown()
        serv.server_close()

run_server()

        

