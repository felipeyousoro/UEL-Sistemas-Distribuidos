import socket
import threading
import time
from Peer import peer as pr


class Client:
    LISTENING_PORT = 3000
    BEAT_PORT = 3001
    MESSAGING_PORT = 3002

    TIMEOUT_SECONDS = 5
    MESSAGE_DELAY_SECONDS = 0
    MAX_RESEND_TRIES = 3

    def __init__(self, ip: str, name: str = 'client'):
        self.name: str = name
        self.ip: str = ip

        self.peer_dictionary: dict = {}

        # Listening socket
        self.listening_socket: socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listening_socket.bind((self.ip, Client.LISTENING_PORT))

        # Messaging socket
        self.messaging_socket: socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.messaging_socket.bind((self.ip, Client.MESSAGING_PORT))

        # Heartbeat socket
        self.beat_socket: socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.beat_socket.bind((self.ip, Client.BEAT_PORT))

    def add_peer(self, peer: pr.Peer):
        self.peer_dictionary[peer.name] = peer


    def print_peers(self):
        for peer in self.peer_dictionary.values():
            print(peer)

    def send_heartbeat(self):
        while True:
            for peer in self.peer_dictionary.values():
                # HBT-01 code means check if peer is online
                print(
                    f'[{time.strftime("%H:%M:%S", time.localtime(time.time()))}] Sending heartbeat to {peer.ip}:{Client.BEAT_PORT}')
                try:
                    self.beat_socket.sendto('HBT-01'.encode('utf-8'), (peer.ip, Client.BEAT_PORT))
                except:
                    print(f'[{time.strftime("%H:%M:%S", time.localtime(time.time()))}] ERROR: sending heartbeat to {peer.ip}:{Client.BEAT_PORT}')
                    pass
            time.sleep(5)

    def listen_heartbeat(self):
        while True:
            try:
                msg, addr = self.beat_socket.recvfrom(1024)
                if msg.decode('utf-8') == 'HBT-01':
                    # HBT-02 code means peer is online
                    try:
                        time.sleep(Client.MESSAGE_DELAY_SECONDS)
                        self.beat_socket.sendto('HBT-02'.encode('utf-8'), addr)
                    except:
                        pass
                elif msg.decode('utf-8') == 'HBT-02':
                    print(
                        f'[{time.strftime("%H:%M:%S", time.localtime(time.time()))}] Received heartbeat from {addr[0]}:{Client.BEAT_PORT}')
                    if addr[0] in self.peer_dictionary.keys():
                        self.peer_dictionary[addr[0]].last_beat_answered = time.time()
            except:
                pass

    def check_peers(self):
        while True:
            current_time = time.time()
            for peer in self.peer_dictionary.values():
                if current_time - peer.last_beat_answered > Client.TIMEOUT_SECONDS:
                    peer.online = False
                else:
                    peer.online = True

    def send_message(self):
        #use messaging socket and set timeout for acks
        self.messaging_socket.settimeout(Client.TIMEOUT_SECONDS)
        while True:
            msg = input()
            msg = f'{self.name}: {msg}'
            for peer in self.peer_dictionary.values():
                for i in range(Client.MAX_RESEND_TRIES):
                    try:
                        self.messaging_socket.sendto(msg.encode('utf-8'), (peer.ip, Client.LISTENING_PORT))
                        ack, addr = self.messaging_socket.recvfrom(1024)
                        if ack.decode('utf-8') == 'ACK':
                            print(f'[{time.strftime("%H:%M:%S", time.localtime(time.time()))}] Message sent to {peer.name}')
                            break
                    except:
                        print(f'[{time.strftime("%H:%M:%S", time.localtime(time.time()))}] ERROR: Message not sent to {peer.name}')
                        pass

    def receive_message(self):
        while True:
            msg, addr = self.listening_socket.recvfrom(1024)
            print(f'[{time.strftime("%H:%M:%S", time.localtime(time.time()))}] {msg.decode("utf-8")}')
            time.sleep(Client.MESSAGE_DELAY_SECONDS)
            try:
                self.listening_socket.sendto('ACK'.encode('utf-8'), addr)
            except:
                pass

    def run(self):
        print(f'Client running on {self.ip}:{Client.LISTENING_PORT}')
        print(f'Client heartbeat running on {self.ip}:{Client.BEAT_PORT}')
        threading.Thread(target=self.listen_heartbeat).start()
        threading.Thread(target=self.send_heartbeat).start()
        threading.Thread(target=self.receive_message).start()
        threading.Thread(target=self.check_peers).start()

        self.send_message()