import socket
import threading
import time
from Peer import peer as pr


class Client:
    LISTENING_PORT = 3000
    BEAT_PORT = 3001
    MESSAGING_PORT = 3002

    TIMEOUT_LIMIT_SECONDS: float = 5

    HEARTBEAT_INTERVAL_SECONDS: float = 3

    APPLICATION_DELAY_SECONDS: float = 0

    MAX_RESEND_TRIES = 3

    PRINT_DEBUG = False

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
        peer.delta_time = Client.TIMEOUT_LIMIT_SECONDS
        self.peer_dictionary[peer.ip] = peer

    def print_peers(self):
        for peer in self.peer_dictionary.values():
            print(peer)

    def send_heartbeat(self):
        while True:
            time.sleep(Client.HEARTBEAT_INTERVAL_SECONDS)

            for peer in self.peer_dictionary.values():
                try:
                    if (Client.PRINT_DEBUG):
                        print(
                            f'[{time.strftime("%H:%M:%S", time.localtime(time.time()))}] Sending heartbeat to {peer.ip}:{Client.BEAT_PORT}')

                    self.beat_socket.sendto('HBT'.encode('utf-8'), (peer.ip, Client.BEAT_PORT))

                except:
                    if (Client.PRINT_DEBUG):
                        print(
                            f'[{time.strftime("%H:%M:%S", time.localtime(time.time()))}] ERROR: sending heartbeat to {peer.ip}:{Client.BEAT_PORT}')
                    pass

    def listen_heartbeat(self):
        while True:
            try:
                msg, addr = self.beat_socket.recvfrom(1024)
                if msg.decode('utf-8') == 'HBT':
                    if addr[0] in self.peer_dictionary.keys():
                        self.peer_dictionary[addr[0]].last_beat_answered = time.time()
                    if (Client.PRINT_DEBUG):
                        print(
                            f'[{time.strftime("%H:%M:%S", time.localtime(time.time()))}] Received heartbeat from {addr[0]}:{Client.BEAT_PORT}')
            except:
                pass

    def check_peers(self):
        while True:
            current_time = time.time()
            for peer in self.peer_dictionary.values():
                if current_time - peer.last_beat_answered > 2 * peer.delta_time:
                    peer.delta_time = Client.TIMEOUT_LIMIT_SECONDS
                    peer.online = False
                else:
                    peer.online = True

    def send_message(self):
        self.messaging_socket.settimeout(Client.TIMEOUT_LIMIT_SECONDS)

        msg = input('Message: ')

        for peer in self.peer_dictionary.values():
            for i in range(Client.MAX_RESEND_TRIES):
                try:
                    self.messaging_socket.sendto(msg.encode('utf-8'), (peer.ip, Client.LISTENING_PORT))

                    start_time = time.time()

                    ack, addr = self.messaging_socket.recvfrom(1024)

                    if ack.decode('utf-8') == 'ACK':
                        elapsed_time = time.time() - start_time

                        if (elapsed_time > 2 * peer.delta_time):
                            peer.delta_time = elapsed_time
                        elif (elapsed_time < peer.delta_time):
                            peer.delta_time = peer.delta_time / 2

                        if (Client.PRINT_DEBUG):
                            print(
                                f'[{time.strftime("%H:%M:%S", time.localtime(time.time()))}] Message sent to {peer.name}')
                    break

                except:
                    if (Client.PRINT_DEBUG):
                        print(
                            f'[{time.strftime("%H:%M:%S", time.localtime(time.time()))}] ERROR: Message not sent to {peer.name}')
                    pass

    def receive_message(self):
        while True:
            msg, addr = self.listening_socket.recvfrom(1024)

            time.sleep(Client.APPLICATION_DELAY_SECONDS)

            if addr[0] not in self.peer_dictionary.keys() or not self.peer_dictionary[addr[0]].online:
                continue

            peer = self.peer_dictionary[addr[0]]

            print(f'[{time.strftime("%H:%M:%S", time.localtime(time.time()))}] Message from {peer.name}: {msg.decode("utf-8")}')

            try:
                self.listening_socket.sendto('ACK'.encode('utf-8'), addr)

            except:
                pass

    def menu(self):
        while True:
            print('Choose an option:')
            print('1 - Print connected peers, whether they\'re online or not')
            print('2 - Send message to all connected peers')
            print('3 - Set heartbeat interval. Current: ' + str(Client.HEARTBEAT_INTERVAL_SECONDS))
            print('4 - Set application delay (for ACKs). Current: ' + str(Client.APPLICATION_DELAY_SECONDS))
            print('5 - Set default timeout limit. Current: ' + str(Client.TIMEOUT_LIMIT_SECONDS))
            print('Else - Exit')
            option = input()
            if option == '1':
                self.print_peers()
            elif option == '2':
                self.send_message()
            elif option == '3':
                Client.PRINT_DEBUG = not Client.PRINT_DEBUG
            elif option == '4':
                Client.HEARTBEAT_INTERVAL_SECONDS = float(input('Interval: '))
            elif option == '5':
                Client.APPLICATION_DELAY_SECONDS = float(input('Delay: '))
            elif option == '6':
                Client.TIMEOUT_LIMIT_SECONDS = float(input('Timeout: '))
            else:
                break

    def run(self):
        print(f'Client running on {self.ip}:{Client.LISTENING_PORT}')
        print(f'Client heartbeat running on {self.ip}:{Client.BEAT_PORT}')
        threading.Thread(target=self.listen_heartbeat).start()
        threading.Thread(target=self.send_heartbeat).start()
        threading.Thread(target=self.receive_message).start()
        threading.Thread(target=self.check_peers).start()

        self.menu()

        # Fecha os sockets
        self.listening_socket.close()
        self.messaging_socket.close()
        self.beat_socket.close()
