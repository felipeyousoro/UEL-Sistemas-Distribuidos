import socket
import threading
import time
from Peer import peer as pr


class Client:
    LISTENING_PORT = 3000
    BEAT_PORT = 3001
    MESSAGING_PORT = 3002

    # Tempo padrão de espera para um peer
    DEFAULT_AWAIT_TIME: float = 2

    HEARTBEAT_INTERVAL_SECONDS: float = 2

    APPLICATION_DELAY_SECONDS: float = 0

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
        peer.await_time = Client.DEFAULT_AWAIT_TIME
        self.peer_dictionary[peer.ip] = peer

    def print_peers(self):
        for peer in self.peer_dictionary.values():
            print(peer)

    def send_heartbeat(self):
        while True:
            # Intervalo entre cada beat.
            time.sleep(Client.HEARTBEAT_INTERVAL_SECONDS)

            # Delay ARTIFICIAL (inserção de atraso no envio)
            time.sleep(Client.APPLICATION_DELAY_SECONDS)

            for peer in self.peer_dictionary.values():
                try:
                    self.beat_socket.sendto('HBT'.encode('utf-8'), (peer.ip, Client.BEAT_PORT))
                except:
                    pass

    def listen_heartbeat(self):
        while True:
            try:
                msg, addr = self.beat_socket.recvfrom(1024)

                # Delay ARTIFICIAL (inserção de atraso na resposta)
                time.sleep(Client.APPLICATION_DELAY_SECONDS)

                if msg.decode('utf-8') == 'HBT':
                    if addr[0] in self.peer_dictionary.keys():
                        self.peer_dictionary[addr[0]].previous_beat_sent = self.peer_dictionary[addr[0]].last_beat_sent
                        self.peer_dictionary[addr[0]].last_beat_sent = time.time()
                        self.peer_dictionary[addr[0]].checked = False
            except:
                pass

    def check_peers(self):
        while True:
            for peer in self.peer_dictionary.values():
                # Como definido em aula, o tempo total de espera é o dobro
                # do delta T, sendo delta T o tempo resultante da soma do tempo
                # "base" (heartbeat) com tempo de espera do peer (timeout).
                #
                # Para afirmar que um peer está offline, é necessário
                # que o tempo entre o ultimo beat enviado e o tempo
                # atual seja maior que o tempo total de espera.
                current_time = time.time()
                delta_t = Client.HEARTBEAT_INTERVAL_SECONDS + peer.await_time

                if current_time - peer.last_beat_sent > 2 * delta_t:
                    if peer.online:
                        print(
                            f'[{time.strftime("%H:%M:%S", time.localtime(time.time()))}] {peer.name} disconnected. Time elapsed since last beat: {current_time - peer.last_beat_sent:.5f}')

                    # Se o peer for determinado que está offline,
                    # devemos resetá-lo para as configurações iniciais.
                    peer.await_time = Client.DEFAULT_AWAIT_TIME
                    peer.previous_beat_sent = 0.0
                    peer.last_beat_sent = 0.0
                    peer.online = False
                    peer.checked = False
                else:
                    if not peer.online:
                        print(f'[{time.strftime("%H:%M:%S", time.localtime(time.time()))}] {peer.name} connected')
                    elif peer.previous_beat_sent == 0.0:
                        pass
                    else:
                        # Se esta online, atualizar o tempo de espera do peer.
                        #
                        # Caso o tempo entre os dois ultimos beats seja maior que o delta T,
                        # então o novo tempo de espera será a diferença entre os dois beats,
                        # desconsiderando o tempo base (heartbeat).
                        #
                        # Caso contrário, o novo tempo de espera será a metade do tempo de espera atual.
                        if peer.checked:
                            continue

                        if peer.last_beat_sent - peer.previous_beat_sent >= delta_t:
                            peer.await_time = (peer.last_beat_sent
                                               - peer.previous_beat_sent
                                               - Client.HEARTBEAT_INTERVAL_SECONDS)
                        else:
                            peer.await_time = peer.await_time / 2

                        peer.checked = True

                    peer.online = True

    def send_message(self):
        self.messaging_socket.settimeout(0.01)

        # Isto aqui é para limpar o buffer do socket,
        # pois pode ser que existam alguns ACKs pendentes
        # de outros peers que demoraram a responder.
        while True:
            try:
                msg, addr = self.messaging_socket.recvfrom(1024)
            except:
                break

        msg = input('Message: ')
        print(
            f'[{time.strftime("%H:%M:%S", time.localtime(time.time()))}] {self.name}: {msg}')

        for peer in self.peer_dictionary.values():
            delta_t = Client.HEARTBEAT_INTERVAL_SECONDS + peer.await_time
            self.messaging_socket.settimeout(delta_t)

            msg_sent_time = time.time()

            # A mensagem será enviada para um peer N vezes
            # até que ele responda com um ACK. Caso nenhum
            # ACK seja recebido, a aplicação irá desistir
            # de enviar a mensagem para este peer.
            for i in range(Client.MAX_RESEND_TRIES):
                # Se o peer não estiver online, não enviar a mensagem.
                if not peer.online:
                    continue

                try:
                    # Delay ARTIFICIAL (inserção de atraso no envio)
                    time.sleep(Client.APPLICATION_DELAY_SECONDS)

                    self.messaging_socket.sendto(msg.encode('utf-8'), (peer.ip, Client.LISTENING_PORT))

                    ack, addr = self.messaging_socket.recvfrom(1024)

                    time.sleep(Client.APPLICATION_DELAY_SECONDS)

                    # Confirmação de que o peer correto recebeu a mensagem.
                    if ack.decode('utf-8') == 'ACK' and addr[0] == peer.ip:
                        current_time = time.time()
                        print(
                            f'[{time.strftime("%H:%M:%S", time.localtime(time.time()))}] ACK received from {peer.name} in {current_time - msg_sent_time:.5f} seconds')
                        break
                except:
                    pass

    def receive_message(self):
        while True:
            msg, addr = self.listening_socket.recvfrom(1024)

            # Verificando se o peer que enviou a mensagem
            # está na lista de peers conectados.
            if addr[0] not in self.peer_dictionary.keys() or not self.peer_dictionary[addr[0]].online:
                continue

            # Delay ARTIFICIAL (inserção de atraso na resposta)
            time.sleep(Client.APPLICATION_DELAY_SECONDS)

            peer = self.peer_dictionary[addr[0]]
            print(
                f'[{time.strftime("%H:%M:%S", time.localtime(time.time()))}] {peer.name}: {msg.decode("utf-8")}')

            try:
                # Tentativa de envio do ACK.
                #
                # Caso o envio falhe, é possível que a mensagem
                # seja recebida novamente.
                time.sleep(Client.APPLICATION_DELAY_SECONDS)
                self.listening_socket.sendto('ACK'.encode('utf-8'), addr)
            except:
                pass

    def menu(self):
        while True:
            print('Choose an option:')
            print('1 - Print connected peers, whether they\'re online or not')
            print('2 - Send message to all connected peers')
            print('3 - Set heartbeat interval. Current: ' + str(Client.HEARTBEAT_INTERVAL_SECONDS))
            print('4 - Set application delay. Current: ' + str(Client.APPLICATION_DELAY_SECONDS))
            print('5 - Set default timeout limit. Current: ' + str(Client.DEFAULT_AWAIT_TIME))
            print('6 - Exit')
            option = input()
            if option == '1':
                self.print_peers()
            elif option == '2':
                self.send_message()
            elif option == '3':
                Client.HEARTBEAT_INTERVAL_SECONDS = float(input('Interval: '))
            elif option == '4':
                Client.APPLICATION_DELAY_SECONDS = float(input('Delay: '))
            elif option == '5':
                Client.DEFAULT_AWAIT_TIME = float(input('Timeout: '))
            elif option == '6':
                break
            else:
                print('Invalid option: ' + option)

    def run(self):
        print(f'Client running on {self.ip}:{Client.LISTENING_PORT}')
        print(f'Client heartbeat running on {self.ip}:{Client.BEAT_PORT}')

        listen_heartbeat_thread = threading.Thread(target=self.listen_heartbeat)
        listen_heartbeat_thread.daemon = True
        listen_heartbeat_thread.start()

        send_heartbeat_thread = threading.Thread(target=self.send_heartbeat)
        send_heartbeat_thread.daemon = True
        send_heartbeat_thread.start()

        receive_message_thread = threading.Thread(target=self.receive_message)
        receive_message_thread.daemon = True
        receive_message_thread.start()

        check_peers_thread = threading.Thread(target=self.check_peers)
        check_peers_thread.daemon = True
        check_peers_thread.start()

        self.menu()

        print('Aplicação encerrada')
