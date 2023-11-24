import random
import threading
import time

from BoardDatabase import board_database
from Circle import circle as c
import socket


class Connection:
    def init_node(self):
        print(f'Connecting to {self.host_port}')

        # Informs the host the socket wants to communicate with it
        self.comm_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.comm_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.comm_socket.bind(('localhost', self.port - 100))
        self.comm_socket.connect(('localhost', self.host_port))
        self.comm_socket.send(b'CODE;JOIN')
        msg = self.comm_socket.recv(128).lstrip(b'0')
        print(msg.decode())
        self.comm_socket.send(b'CODE;ACK')
        self.comm_socket.close()

        self.host_port = int(msg.decode())

        # Connects to the port the host opened to
        #   communicate with the node
        self.comm_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.comm_socket.bind(('localhost', self.port - 100))
        self.comm_socket.connect(('localhost', self.host_port))

        self.listen_thread = threading.Thread(target=self.listen_to_host)
        self.listen_thread.daemon = True
        self.listen_thread.start()

        self.host_error_thread = threading.Thread(target=self.host_is_alive)
        self.host_error_thread.daemon = True
        self.host_error_thread.start()

        self.host_error = False

    def init_host(self):
        self.open_port = 4201

        self.listen_thread = threading.Thread(target=self.listen_to_new_conns)
        self.listen_thread.daemon = True
        self.listen_thread.start()

        self.host_error = False

    def host_is_alive(self):
        while not self.host_error:
            pass
        self.begin_election()

    # TODO: e se não tiver nenhuma porta que não a minha?
    def get_next_node(self):
        key = self.port - 100

        for node in self.nodes:
            if node[1] > key and node[2]:
                return node

        return self.nodes[0]

    def election_listen_to_node(self):
        self.received_nodes = []

        print(f'Listening to new nodes in port: {self.port}')
        conn, addr = self.listen_socket.accept()

        while True:
            data = conn.recv(128).lstrip(b'0')

            header = data.split(b';')[0].decode()

            body = data[len(header) + 1:]

            if header == 'COORDINATOR':
                host_port = int(body.decode())
                self.host_port = host_port
                print(f'New host: {host_port}')
                break
            elif header == 'ELECTION':
                nodes = body.decode().split(';')
                for node in nodes:
                    if node not in self.received_nodes:
                        self.received_nodes.append(node)
                print(f'Oi: {self.received_nodes}')
                if str(self.port) in self.received_nodes:
                    print('FILHO DA PUTAAAAAAAAAAAAAAAAAAAAA!!')
                    self.host_port = int(max(self.received_nodes))
                    break

    def election_send_to_node(self):
        self.comm_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.comm_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.comm_socket.bind(('localhost', self.port - 100))
        self.comm_socket.connect(('localhost', self.get_next_node()[1] + 100))

        while True:
            time.sleep(2)
            try:
                if self.host_port == -1:
                    nodes_to_send = self.received_nodes.copy()
                    nodes_to_send.append(str(self.port))
                    self.comm_socket.send(b'ELECTION;' + ';'.join(nodes_to_send).encode())
                else:
                    self.comm_socket.send(b'COORDINATOR;' + str(self.host_port).encode())
                    self.comm_socket.close()
                    break
            except Exception as err:
                print(err)
                #self.nodes[self.nodes.index(self.get_next_node())][2] = False

    def begin_election(self):
        print('Começando eleição')

        self.host = False
        self.host_port = -1
        self.connections = []
        self.comm_socket = None
        self.received_nodes = []

        self.nodes.sort(key=lambda x: x[1])

        if len(self.nodes) == 0:
            self.host_port = self.port
        else:
            listen_thread = threading.Thread(target=self.election_listen_to_node)
            listen_thread.daemon = True
            listen_thread.start()

            self.election_send_to_node()

        if self.host_port == self.port:
            print('Sou o novo host')
            self.init_host()
        else:
            print(f'Novo host: {self.host_port}')
            time.sleep(2)
            self.init_node()

        self.nodes = []

    def __init__(self, database: board_database.BoardDatabase, port: int, host=False, host_port=-1):
        self.database = database

        self.host = host
        self.port: int = port
        self.host_port: int = host_port

        #   This socket is used to listen to connection requests
        #   It may be used either for the host to listen for nodes
        # wanting to join the board
        #   Or for the node to communicate with other node
        # during an election process
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_socket.bind(('localhost', self.port))
        self.listen_socket.listen(24)

        self.nodes: list[socket.socket, int, bool] = []

        self.host_error = False
        self.open_port = None
        self.connections = None
        self.listen_thread = None
        self.host_error_thread = None
        self.comm_socket = None
        self.received_nodes = None

        if host:
            self.init_host()
        else:
            self.init_node()

    def listen_to_host(self):
        try:
            while True:
                data = self.comm_socket.recv(128).lstrip(b'0')
                header = data.split(b';')[0].decode()

                body = data[len(header) + 1:]
                if header == 'ADD':
                    circle = c.Circle.decode(body)
                    self.database.addCircle(circle)
                elif header == 'LOCK':
                    circle_id = int(body.split(b';')[0].decode())
                    port = int(body.split(b';')[1].decode())
                    code, circle = self.database.lockCircle(circle_id, port)
                elif header == 'UNLOCK':
                    circle_id = int(body.split(b';')[0].decode())
                    port = int(body.split(b';')[1].decode())
                    self.database.unlockCircle(circle_id, port)
                elif header == 'NEW-CONN':
                    port = int(body.decode())
                    self.nodes.append([None, port, True])
        except:
            self.host_error = True

    def listen_to_connection(self, conn: socket.socket):
        try:
            while True:
                data = conn.recv(128).lstrip(b'0')
                header = data.split(b';')[0].decode()

                body = data[len(header) + 1:]
                if header == 'ADD':
                    circle = c.Circle.decode(body)
                    self.database.addCircle(circle)
                    self.send_data_to_connections((b'ADD;' + circle.encode()).zfill(128))
                elif header == 'LOCK':
                    circle_id = int(body.split(b';')[0].decode())
                    port = int(body.split(b';')[1].decode())

                    code, circle = self.database.lockCircle(circle_id, port)
                    if code == board_database.BoardDatabase.DATABASE_REJECT:
                        pass
                    else:
                        self.send_data_to_connections(
                            (b'LOCK;' + str(circle_id).encode() + b';' + str(port).encode()).zfill(128))
                elif header == 'UNLOCK':
                    circle_id = int(body.split(b';')[0].decode())
                    port = int(body.split(b';')[1].decode())

                    self.database.unlockCircle(circle_id, port)
                    self.send_data_to_connections(
                        (b'UNLOCK;' + str(circle_id).encode() + b';' + str(port).encode()).zfill(128))
        except:
            print(f'Connection {conn} closed')
            conn.close()

    def listen_to_new_conns(self):
        print(f'-----    Listening to new connections in port: {self.port}    -----')

        while True:
            conn, addr = self.listen_socket.accept()

            request = conn.recv(128).decode()
            print(f'Request to join from {addr}')

            new_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            new_conn.bind(('localhost', self.open_port))
            print(f'New port opened for the connection: {self.open_port}')
            conn.send(str(self.open_port).encode())

            ack = conn.recv(128).decode()

            conn.close()

            new_conn.connect(('localhost', addr[1]))

            self.send_current_db(new_conn)
            self.send_connections(new_conn)

            self.send_data_to_connections((b'NEW-CONN;' + str(addr[1]).encode()).zfill(128))

            self.nodes.append([new_conn, addr[1], True])

            new_conn_thread = threading.Thread(target=self.listen_to_connection, args=(new_conn,))
            new_conn_thread.daemon = True
            new_conn_thread.start()

            self.open_port += 1

    def send_data_to_connections(self, data: bytes):
        data.zfill(128)
        for c in self.nodes:
            if not c[2]:
                continue
            try:
                c[0].send(data)
            except:
                print(f'Connection {c[0]} closed')
                c[2] = False

    def send_current_db(self, conn: socket.socket):
        try:
            for circle in self.database.circles:
                conn.send((b'ADD;' + circle.encode()).zfill(128))
        except:
            print(f'Failed to send current db to {conn}')

    def send_connections(self, conn: socket.socket):
        try:
            for c in self.nodes:
                if not c[2]:
                    continue
                conn.send((b'NEW-CONN;' + str(c[1]).encode()).zfill(128))
        except:
            print(f'Failed to send connections to {conn}')

    def request_add_circle(self, circle: c.Circle):
        if self.host_error:
            print('Host is dead, wait for a new one')
            return
        if self.host:
            self.database.addCircle(circle)
            self.send_data_to_connections((b'ADD;' + circle.encode()).zfill(128))
        else:
            self.comm_socket.send((b'ADD;' + circle.encode()).zfill(128))

    def request_lock_circle(self, circle: c.Circle):
        if self.host_error:
            print('Host is dead, wait for a new one')
            return
        if self.host:
            code, circle = self.database.lockCircle(circle.id, self.port)
            if code == board_database.BoardDatabase.DATABASE_REJECT:
                pass
            else:
                self.send_data_to_connections(
                    (b'LOCK;' + str(circle.id).encode() + b';' + str(self.port).encode()).zfill(128))
        else:
            self.comm_socket.send((b'LOCK;' + str(circle.id).encode() + b';' + str(self.port).encode()).zfill(128))

    def request_unlock_circle(self, circle: c.Circle):
        if self.host_error:
            print('Host is dead, wait for a new one')
            return
        if self.host:
            self.database.unlockCircle(circle.id, self.port)
            self.send_data_to_connections(
                (b'UNLOCK;' + str(circle.id).encode() + b';' + str(self.port).encode()).zfill(128))
        else:
            self.comm_socket.send((b'UNLOCK;' + str(circle.id).encode() + b';' + str(self.port).encode()).zfill(128))
