import socket
import threading

def Send(client_sock):
    while True:
        send_data = bytes(input().encode())
        client_sock.send(send_data)

def Recv(client_sock):
    while True:
        recv_data = client_sock.recv(1024).decode()
        print(recv_data)


if __name__ == '__main__':
    client_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    HOST = '192.168.0.121'
    PORT = 6000
    client_sock.connect((HOST,PORT))
    print('Connecting to', HOST, PORT)


    thread1 = threading.Thread(target=Send, args=(client_sock,))
    thread1.start()

    thread2 = threading.Thread(target=Recv, args=(client_sock,))
    thread2.start()