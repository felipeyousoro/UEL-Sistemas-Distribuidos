import socket
import threading
import time

from Peer import peer as pr
from Client import client as clnt

HOSTNAME = socket.gethostname()
IP = '191.52.64.120'

def get_peers(file: str) -> list:
    peers = []
    with open(file, 'r') as f:
        for line in f.readlines():
            ip, name = line.split(' ')
            ip = ip.replace('\n', '')
            peers.append(pr.Peer(name, ip))

    return peers

if __name__ == '__main__':
    client = clnt.Client(IP, 'client')

    peers = get_peers('peers.txt')

    threading.Thread(target=client.run).start()

    for peer in peers:
        client.add_peer(peer)


