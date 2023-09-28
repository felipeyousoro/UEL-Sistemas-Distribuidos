import socket
import threading
import time

from Peer import peer as pr
from Client import client as clnt

HOSTNAME = socket.gethostname()
IP = socket.gethostbyname_ex(HOSTNAME)[2][0]

def get_peers(file: str) -> list:
    peers = []
    with open(file, 'r') as f:
        for line in f.readlines():
            name, ip = line.split(' ')
            ip = ip.replace('\n', '')
            peers.append(pr.Peer(name, ip))

    return peers

def usr1():
    client = clnt.Client(IP, 'client1')

    peers = get_peers('test1.txt')

    threading.Thread(target=client.run).start()

    for peer in peers:
        client.add_peer(peer)

def usr2():
    client = clnt.Client(socket.gethostbyname_ex(HOSTNAME)[2][1], 'client2')

    peers = get_peers('test2.txt')

    threading.Thread(target=client.run).start()

    for peer in peers:
        client.add_peer(peer)

if __name__ == '__main__':
    usr1()
    # time.sleep(1)
    # usr2()

