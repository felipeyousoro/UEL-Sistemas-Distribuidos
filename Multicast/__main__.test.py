import socket
import time

HOSTNAME = socket.gethostname()
IP = socket.gethostbyname_ex(HOSTNAME)[2][1]

if __name__ == '__main__':
    print('IP: ', IP)
    list_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    list_sock.bind((IP, 3000))
    list_sock.listen()

    send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send_sock.connect((socket.gethostbyname_ex(HOSTNAME)[2][0], 3000))
    send_sock.send('start'.encode('utf-8'))

    while True:
        conn, addr = list_sock.accept()
        break
    print('conectado')

    while True:
        data = conn.recv(1024)

        if not data:
            print('aguardando')
            break

        print(data.decode('utf-8'))
