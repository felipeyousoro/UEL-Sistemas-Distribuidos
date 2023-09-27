import socket
import threading
import time
from Peer import peer as pr


class Client:
    def __init__(self, ip: str, name: str = 'client'):
        self.name: str = name
        self.ip: str = ip
        self.listening_port: int = 3000

        self.peer_list: list = []

        # Listening port
        self.listening_socket: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listening_socket.bind((self.ip, self.listening_port))

    def add_peer(self, peer: pr.Peer, msg: str = ''):
        self.peer_list.append(peer)
        self.send_msg(peer, msg)

    def handle_connection(self, conn, addr):
        while True:
            data = conn.recv(1024)

            if not data: continue

            print('msg lida por {}:'.format(self.name))
            print(data.decode('utf-8'))

    def send_msg(self, peer: pr.Peer, msg: str):
        n: int = 0
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((peer.ip, 3000))
                while True:
                    n += 1
                    s.send((msg + ': ' + str(n)).encode('utf-8'))
                    time.sleep(5)
            except Exception as e:
                print(f'falha ao enviar mensagem para {peer.name}: {str(e)}')
                time.sleep(10)

    def run(self):
        print('ESCUTANDO EM {}'.format(self.ip))
        self.listening_socket.listen()
        while True:
            conn, addr = self.listening_socket.accept()
            threading.Thread(target=self.handle_connection, args=(conn, addr)).start()

