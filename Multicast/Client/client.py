import socket
import threading
from Multicast.Peer import peer as pr


class Client:
    def __init__(self, name: str, port: int):
        self.name = name
        self.port = port
        self.ip = socket.gethostbyname(socket.gethostname())
        self.peer_list = []

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.ip, self.port))

    def __str__(self):
        return f'Client: {self.name} {self.ip}:{self.port}\n' + '\n'.join([str(peer) for peer in self.peer_list])

    def add_peer(self, peer: pr.Peer):
        self.peer_list.append(peer)

    def listen(self):
        self.sock.listen(16)

    def handle_connection(self, conn, addr):
        while True:
            data = conn.recv(1024)

            if not data: break

            print(data.decode('utf-8'))
        conn.close()

    def run(self):
        while True:
            conn, addr = self.sock.accept()
            threading.Thread(target=self.handle_connection, args=(conn, addr)).start()
