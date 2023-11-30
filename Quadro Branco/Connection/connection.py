import random
import threading
import time

from BoardDatabase import board_database
from Circle import circle as c
import socket


class Connection:
    def __init__(self, database: board_database.BoardDatabase, host=False, host_port=-1):
        #   This socket is used to listen to connection requests
        #   It may be used either for the host to listen for nodes
        # wanting to join the board
        #   Or for the node to communicate with other nodes
        # during an election process
        self.main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.main_socket.bind(('localhost', 0))
        self.main_socket.listen(24)

        self.host = host
        self.host_port: int = host_port
        self.database = database
        self.port: int = self.main_socket.getsockname()[1]

        self.nodes: list[socket.socket, int, int, bool] = []

        self.host_error = False
        self.connections = None
        self.listen_thread = None
        self.host_error_thread = None
        self.comm_socket = None
        self.received_nodes = None

        if host:
            self.init_host()
        else:
            self.init_node()

    def init_node(self):
        print(f'-----    Using this port: {self.port}    -----')
        print(f'Connecting to {self.host_port}')

        # chekc if comm_socket is in use
        # time.sleep(1 + random.random() * 5)
        # Informs the host the socket wants to communicate with it

        self.comm_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.comm_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.comm_socket.bind(('localhost', 0))
        comm_port = self.comm_socket.getsockname()[1]
        self.comm_socket.connect(('localhost', self.host_port))
        self.comm_socket.send((b'CODE;JOIN;' + str(self.port).encode()).zfill(128))
        msg = self.comm_socket.recv(128).lstrip(b'0')
        self.comm_socket.send(b'CODE;ACK'.zfill(128))
        self.comm_socket.close()
        print(f'Received available port: {msg.decode()}')

        self.host_port = int(msg.decode())

        # Connects to the port the host opened to
        #   communicate with the node
        self.comm_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.comm_socket.bind(('localhost', comm_port))
        self.comm_socket.connect(('localhost', self.host_port))

        self.host = False

        self.listen_thread = threading.Thread(target=self.listen_to_host)
        self.listen_thread.daemon = True
        self.listen_thread.start()

        self.host_error = False

        self.host_error_thread = threading.Thread(target=self.host_is_alive)
        self.host_error_thread.daemon = True
        self.host_error_thread.start()

    def init_host(self):
        self.listen_thread = threading.Thread(target=self.listen_to_new_conns)
        self.listen_thread.daemon = True
        self.listen_thread.start()

        self.host = True
        self.host_error = False

    def host_is_alive(self):
        while not self.host_error:
            pass
        self.begin_election()

    # TODO: e se não tiver nenhuma porta que não a minha?
    def get_next_node(self):
        key = self.port

        for node in self.nodes:
            if node[2] > key and node[3]:
                return node

        if not self.nodes[0][3]:
            return None

        return self.nodes[0]

    def election_listen_to_node(self):

        self.received_nodes = []

        print(f'Listening to new nodes in port: {self.port}')

        while True:
            print(f'Current ring status: {self.received_nodes}')
            conn, addr = self.main_socket.accept()

            data = conn.recv(128).lstrip(b'0')

            header = data.split(b';')[0].decode()

            body = data[len(header) + 1:]

            if header == 'COORDINATOR':
                host_port = int(body.decode())
                self.host_port = host_port
                print(f'Coordinator detected, new host: {host_port}')
            elif header == 'ELECTION':
                nodes = body.decode().split(';')
                for node in nodes:
                    if node not in self.received_nodes:
                        self.received_nodes.append(node)
                if str(self.port) in self.received_nodes:
                    self.host_port = int(max(self.received_nodes))
            if self.host_port != -1:
                print(f'FINAL RING: {self.received_nodes}')
                break

    def election_send_to_node(self):
        while True:
            try:
                time.sleep(3)

                next_node = self.get_next_node()
                if next_node is None:
                    print('No clients available, self electing')
                    self.host_port = self.port
                    break

                print(f'Next node in the ring: {next_node[2]}')
                self.comm_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.comm_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.comm_socket.bind(('localhost', 0))
                self.comm_socket.connect(('localhost', next_node[2]))

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
                self.nodes[self.nodes.index(self.get_next_node())][3] = False

    def begin_election(self):
        print('Beginning election')

        self.host = False
        self.host_port = -1
        self.connections = []
        self.comm_socket = None
        self.received_nodes = []

        self.nodes.sort(key=lambda x: x[2])

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
                    self.database.lockCircle(circle_id, port)
                elif header == 'UNLOCK':
                    circle_id = int(body.split(b';')[0].decode())
                    port = int(body.split(b';')[1].decode())
                    self.database.unlockCircle(circle_id, port)
                elif header == 'UPDATE':
                    circle_id = int(body.split(b';')[0].decode())
                    port = int(body.split(b';')[1].decode())
                    circle = c.Circle.decode(body[len(str(circle_id).encode()) + len(str(port).encode()) + 2:])
                    self.database.updateCircle(circle_id, circle, port)
                elif header == 'NEW-CONN':
                    port = int(body.decode())
                    self.nodes.append([None, None, port, True])
                    print(f'New connection: {port}')
                    print(f'Current connections: {self.nodes}')
                else:
                    print('Unknown pack', data)
        except ConnectionResetError:
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
                    code, circle = self.database.unlockCircle(circle_id, port)

                    if code == board_database.BoardDatabase.DATABASE_REJECT:
                        pass
                    else:
                        self.send_data_to_connections(
                            (b'UNLOCK;' + str(circle_id).encode() + b';' + str(port).encode()).zfill(128))
                elif header == 'UPDATE':
                    circle_id = int(body.split(b';')[0].decode())
                    port = int(body.split(b';')[1].decode())
                    circle = c.Circle.decode(body[len(str(circle_id).encode()) + len(str(port).encode()) + 2:])

                    self.database.updateCircle(circle_id, circle, port)
                    self.send_data_to_connections(
                        (b'UPDATE;' + str(circle_id).encode() + b';' + str(port).encode() + b';' + circle.encode()).zfill(128))
        except:
            print(f'Connection {conn} closed')
            conn.close()

    def listen_to_new_conns(self):
        print(f'-----    Listening to new connections in port: {self.port}    -----')

        while True:
            conn, addr = self.main_socket.accept()

            request = conn.recv(128).lstrip(b'0')
            request = request.decode()

            if request.split(';')[0] + ';' + request.split(';')[1] != 'CODE;JOIN':
                print(f'Invalid request: {request}')
                continue

            request_port = int(request.split(';')[2])

            print(f'Request to join from {request_port}')

            new_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            new_conn.bind(('localhost', 0))

            print(f'New port opened for the connection: {new_conn.getsockname()[1]}')
            conn.send(str(new_conn.getsockname()[1]).encode())
            ack = conn.recv(128)
            conn.close()

            new_conn.connect(('localhost', addr[1]))

            self.send_current_db(new_conn)
            self.send_connections(new_conn)

            self.send_data_to_connections((b'NEW-CONN;' + str(request_port).encode()).zfill(128))

            self.nodes.append([new_conn, addr[1], request_port, True])

            new_conn_thread = threading.Thread(target=self.listen_to_connection, args=(new_conn,))
            new_conn_thread.daemon = True
            new_conn_thread.start()

    def send_data_to_connections(self, data: bytes):
        data.zfill(128)
        for c in self.nodes:
            if not c[3]:
                continue
            try:
                c[0].send(data)
            except:
                print(f'Connection {c[0]} closed')
                c[3] = False

    def send_current_db(self, conn: socket.socket):
        try:
            for circle in self.database.circles:
                conn.send((b'ADD;' + circle.encode()).zfill(128))
        except:
            print(f'Failed to send current db to {conn}')

    def send_connections(self, conn: socket.socket):
        try:
            for c in self.nodes:
                if not c[3]:
                    continue
                conn.send((b'NEW-CONN;' + str(c[2]).encode()).zfill(128))
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

    def request_move_circle(self, circle: c.Circle, x: int, y: int):
        if self.host_error:
            print('Host is dead, wait for a new one')
            return
        if self.host:
            self.database.updateCircle(circle.id, c.Circle(circle.id, x, y, circle.r, circle.width, circle.color),
                                       self.port)
            self.send_data_to_connections(
                (b'UPDATE;' + str(circle.id).encode() + b';' + str(self.port).encode() + b';' + c.Circle(
                    circle.id,
                    x, y,
                    circle.r,
                    circle.width,
                    circle.color).encode()).zfill(128))
        else:
            self.comm_socket.send(
                (b'UPDATE;' + str(circle.id).encode() + b';' + str(self.port).encode() + b';' + c.Circle(
                    circle.id,
                    x, y,
                    circle.r,
                    circle.width,
                    circle.color).encode()).zfill(128))

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
