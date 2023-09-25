import socket
import threading
import time
from Multicast.Peer import peer as pr


class Client:
    def __init__(self, name: str):
        self.name: str = name
        self.ip: str = socket.gethostbyname(socket.gethostname())
        self.listening_port: int = 3000
        self.connecting_port: int = 3001

        self.peer_list: list = []

        # Listening port
        self.listening_socket: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listening_socket.bind((self.ip, self.listening_port))

        # Connecting port
        self.connecting_socket: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print(f'Client {self.name} created at {self.ip}:{self.listening_port}')

    def __str__(self):
        return f'Client: {self.name} {self.ip}:{self.port}\n' + '\n'.join([str(peer) for peer in self.peer_list])

    def add_peer(self, peer: pr.Peer):
        self.peer_list.append(peer)

    def handle_connection(self, conn, addr):
        while True:
            data = conn.recv(1024)

            if not data: continue

            print(data.decode('utf-8'))
            break
        print('leu')

    def send_shit(self, conn, addr):
        print('dA SEND FDP')
        self.connecting_socket.connect((socket.gethostbyname_ex(socket.gethostname())[2][1], 3000))
        print('ok agora vai dar send')
        while True:
            self.connecting_socket.send('vsfff'.encode('utf-8'))
            time.sleep(1)

    def run(self):
        self.listening_socket.listen()
        while True:
            conn, addr = self.listening_socket.accept()
            threading.Thread(target=self.handle_connection, args=(conn, addr)).start()

            threading.Thread(target=self.send_shit, args=(conn, addr)).start()
            break
        print('conectou')
