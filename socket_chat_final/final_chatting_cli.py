import socket
import threading
import time

HOST = '192.168.0.121'
PORT = 6000

def recv_all(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            print(data.decode())
        except Exception as e:
            print(e)

def send_msg(client_socket):
    th_recv = threading.Thread(target=recv_all,args=(client_socket,))
    th_recv.daemon = True
    th_recv.start()
    while True: 
        message = input()
        if message == 'quit':
            client_socket.send(message.encode())
            break
        client_socket.send(message.encode())


if __name__ == '__main__':
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_socket.connect((HOST,PORT))
    # while True:
    th_send = threading.Thread(target=send_msg, args=(client_socket,))
    th_send.start()
    
        
    
    # while True:
    #     time.sleep(0.001)
    #     pass
    


# client_socket.close()
