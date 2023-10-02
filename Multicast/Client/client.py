import socket
import threading
import time
from Peer import peer as pr


class Client:
    LISTENING_PORT = 3000
    BEAT_PORT = 3001
    MESSAGING_PORT = 3002

    TIMEOUT_LIMIT_SECONDS = 5

    HEARTBEAT_SEND_DELAY_SECONDS = 3

    ACK_SEND_DELAY_SECONDS = 3

    MAX_RESEND_TRIES = 3

    PRINT_HEARTBEAT = False
    PRINT_ACK = False

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
        self.peer_dictionary[peer.ip] = peer

    def print_peers(self):
        for peer in self.peer_dictionary.values():
            print(peer)

    def send_heartbeat(self):
        while True:
            time.sleep(Client.HEARTBEAT_SEND_DELAY_SECONDS)
            for peer in self.peer_dictionary.values():
                try:
                    if (Client.PRINT_HEARTBEAT):
                        print(
                            f'[{time.strftime("%H:%M:%S", time.localtime(time.time()))}] Sending heartbeat to {peer.ip}:{Client.BEAT_PORT}')
                    self.beat_socket.sendto('HBT'.encode('utf-8'), (peer.ip, Client.BEAT_PORT))
                except:
                    if (Client.PRINT_HEARTBEAT):
                        print(
                            f'[{time.strftime("%H:%M:%S", time.localtime(time.time()))}] ERROR: sending heartbeat to {peer.ip}:{Client.BEAT_PORT}')
                    pass

    def listen_heartbeat(self):
        while True:
            msg, addr = self.beat_socket.recvfrom(1024)
            if msg.decode('utf-8') == 'HBT':
                if addr[0] in self.peer_dictionary.keys():
                    self.peer_dictionary[addr[0]].last_beat_answered = time.time()
                if (Client.PRINT_HEARTBEAT):
                    print(
                        f'[{time.strftime("%H:%M:%S", time.localtime(time.time()))}] Received heartbeat from {addr[0]}:{Client.BEAT_PORT}')


    def check_peers(self):
        while True:
            current_time = time.time()
            for peer in self.peer_dictionary.values():
                if current_time - peer.last_beat_answered > Client.TIMEOUT_SECONDS:
                    peer.online = False
                else:
                    peer.online = True

    def menu(self):
        print('Choose an option:')
        print('1 - Print connected peers, whether they\'re online or not')
        print('2 - Send message to all connected peers')
        print('3 - Enable/Disable heartbeat messages')
        print('4 - Set sending message delay')
        print('5 - Set timeout for ACKs')
        print('6 - Set max number of resend tries')
        print('7 - Enable/Disable ACK messages')
        print('Else - Exit')
        while True:
            option = input()
            if option == '1':
                self.print_peers()
            elif option == '2':
                self.send_message()
            elif option == '3':
                Client.PRINT_HEARTBEAT = not Client.PRINT_HEARTBEAT
            elif option == '4':
                print('oi')
            elif option == '5':
                print('Current timeout: ', Client.TIMEOUT_LIMIT_SECONDS)
                Client.TIMEOUT_SECONDS = int(input('Timeout in seconds: '))
            elif option == '6':
                print('Current max resend tries: ', Client.MAX_RESEND_TRIES)
                Client.MAX_RESEND_TRIES = int(input('Max resend tries: '))
            elif option == '7':
                Client.PRINT_ACK = not Client.PRINT_ACK
            else:
                break

    def send_message(self):
        self.messaging_socket.settimeout(Client.TIMEOUT_LIMIT_SECONDS)

        msg = input('Message: ')
        msg = f'{self.name}: {msg}'
        for peer in self.peer_dictionary.values():
            for i in range(Client.MAX_RESEND_TRIES):
                try:
                    self.messaging_socket.sendto(msg.encode('utf-8'), (peer.ip, Client.LISTENING_PORT))
                    ack, addr = self.messaging_socket.recvfrom(1024)
                    if ack.decode('utf-8') == 'ACK':
                        if (Client.PRINT_ACK):
                            print(
                                f'[{time.strftime("%H:%M:%S", time.localtime(time.time()))}] Message sent to {peer.name}')
                        break
                except:
                    if (Client.PRINT_ACK):
                        print(
                            f'[{time.strftime("%H:%M:%S", time.localtime(time.time()))}] ERROR: Message not sent to {peer.name}')
                    pass

    def receive_message(self):
        while True:
            msg, addr = self.listening_socket.recvfrom(1024)
            print(f'[{time.strftime("%H:%M:%S", time.localtime(time.time()))}] {msg.decode("utf-8")}')
            try:
                time.sleep(Client.ACK_SEND_DELAY_SECONDS)
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

        self.menu()
