import socket
import threading
import time

from Peer import peer as pr
from Client import client as clnt

HOSTNAME = socket.gethostname()
IP = socket.gethostbyname_ex(HOSTNAME)[2]
PORT = 3000

def get_peers(file: str) -> list:
    peers = []
    with open(file, 'r') as f:
        for line in f.readlines():
            name, ip = line.split(' ')
            ip = ip.replace('\n', '')
            peers.append(pr.Peer(name, ip))

    return peers

def usr1():
    client = clnt.Client(IP[0], 'client1')

    peers = get_peers('test1.txt')

    threading.Thread(target=client.run).start()
    time.sleep(1)

    for peer in peers:
        threading.Thread(target=client.add_peer, args=(peer, 'numero enviado por 1')).start()

if __name__ == '__main__':
    threading.Thread(target=usr1).start()

