import socket
import threading
import time
from Peer import peer as pr


class Client:
    LISTENING_PORT = 3000
    BEAT_PORT = 3001

    def __init__(self, ip: str, name: str = 'client'):
        self.name: str = name
        self.ip: str = ip

        self.peer_list: list[pr.Peer] = []

        # Listening socket
        self.listening_socket: socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listening_socket.bind((self.ip, Client.LISTENING_PORT))

        # Heartbeat socket
        self.beat_socket: socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.beat_socket.bind((self.ip, Client.BEAT_PORT))

    def add_peer(self, peer: pr.Peer):
        self.peer_list.append(peer)

    def print_peers(self):
        for peer in self.peer_list:
            print(peer)

    def send_heartbeat(self):
        while True:
            for peer in self.peer_list:
                # HBT-01 code means check if peer is online
                print(
                    f'[{time.strftime("%H:%M:%S", time.localtime(time.time()))}] Sending heartbeat to {peer.ip}:{Client.BEAT_PORT}')
                peer.online = False
                try:
                    self.beat_socket.sendto('HBT-01'.encode('utf-8'), (peer.ip, Client.BEAT_PORT))
                except:
                    print(f'[{time.strftime("%H:%M:%S", time.localtime(time.time()))}] ERROR: sending heartbeat to {peer.ip}:{Client.BEAT_PORT}')
                    pass
            time.sleep(5)

    def check_heartbeat(self):
        while True:
            try:
                msg, addr = self.beat_socket.recvfrom(1024)
                if msg.decode('utf-8') == 'HBT-01':
                    # HBT-02 code means peer is online
                    try:
                        self.beat_socket.sendto('HBT-02'.encode('utf-8'), addr)
                    except:
                        pass
                elif msg.decode('utf-8') == 'HBT-02':
                    print(
                        f'[{time.strftime("%H:%M:%S", time.localtime(time.time()))}] Received heartbeat from {addr[0]}:{Client.BEAT_PORT}')
                    for peer in self.peer_list:
                        if peer.ip == addr[0]:
                            peer.online = True
            except:
                pass

    def send_message(self):
        while True:
            msg = input()
            for peer in self.peer_list:
                if peer.online:
                    try:
                        self.listening_socket.sendto(f'{self.name}: {msg}'.encode('utf-8'), (peer.ip, Client.LISTENING_PORT))
                    except:
                        pass

    def receive_message(self):
        while True:
            msg, addr = self.listening_socket.recvfrom(1024)
            print(f'[{time.strftime("%H:%M:%S", time.localtime(time.time()))}] {msg.decode("utf-8")}')

    def run(self):
        print(f'Client running on {self.ip}:{Client.LISTENING_PORT}')
        print(f'Client heartbeat running on {self.ip}:{Client.BEAT_PORT}')
        threading.Thread(target=self.check_heartbeat).start()
        threading.Thread(target=self.send_heartbeat).start()
        threading.Thread(target=self.receive_message).start()
        threading.Thread(target=self.send_message).start()
