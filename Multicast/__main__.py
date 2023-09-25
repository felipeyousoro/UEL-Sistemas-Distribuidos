import socket
from Peer import peer as pr
from Client import client as clnt

HOSTNAME = socket.gethostname()
IP = socket.gethostbyname_ex(HOSTNAME)[2][0]
PORT = 3000

# def get_peers(file: str) -> list:
#     peers = []
#     with open(file, 'r') as f:
#         line = f.readline()
#         name, ip = line.split(' ')
#         peers.append(pr.Peer(name, ip))
#
#     return peers


if __name__ == '__main__':
    client = clnt.Client('client')

    # peers = get_peers('peers.txt')
    # for peer in peers:
    #     client.add_peer(peer)

    client.run()