import socket
import threading


HOST = '192.168.0.121'
PORT = 6000
def recieve_msg(sock):

    while True:
        
        try:
            data = sock.recv(1024)
            if not data:
                break
            print(data.decode())
        except Exception as e:
            print(e)


def run_chat():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    t = threading.Thread(target=recieve_msg,args=(sock,))
    t.daemon = True
    t.start()
    while True:
        message = input()
        if message == 'quit':
            sock.send(message.encode())
            break
        sock.send(message.encode())
        # data = sock.recv(1024)

        # print('Received from the server : {}'.format(data)) 
run_chat()
