import socket
import threading
import time

from Peer import peer as pr
from Client import client as clnt

HOSTNAME = socket.gethostname()
IP = socket.gethostbyname_ex(HOSTNAME)[2][1]
print(IP)
if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((IP, 3001))

    #start listening and print
    while True:
        print('cade a msg')
        msg, addr = sock.recvfrom(1024)
        print(f'[{time.strftime("%H:%M:%S", time.localtime(time.time()))}] {msg.decode("utf-8")}')



