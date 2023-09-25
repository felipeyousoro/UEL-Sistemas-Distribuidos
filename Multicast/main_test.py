import socket
import time

HOSTNAME = socket.gethostname()
IP = socket.gethostbyname(HOSTNAME)
PORT = 3000

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((IP, PORT))

    while True:
        sock.send('Teste'.encode('utf-8'))
        time.sleep(2)
