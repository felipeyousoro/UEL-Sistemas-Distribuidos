import random
import threading
import time

from BoardDatabase import board_database
from Circle import circle as c
import socket


class Connection:
    def init_client(self):
        print(f'Connecting to {self.host_port}')
        self.socket.connect(('localhost', self.host_port))

        self.socket.send(b'CODE;JOIN')
        msg = self.socket.recv(128).lstrip(b'0')
        print(msg.decode())
        self.socket.send(b'CODE;ACK')
        self.socket.close()

        self.host_port = int(msg.decode())

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('localhost', self.port))
        self.socket.connect(('localhost', self.host_port))

        self.listen_thread = threading.Thread(target=self.listen_to_host)
        self.listen_thread.start()

    def __init__(self, database: board_database.BoardDatabase, port: int, host=False, host_port=-1):
        self.database = database

        self.host = host
        self.port: int = port
        self.host_port: int = host_port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('localhost', self.port))

        if host:
            self.connections: list[[socket.socket, bool]] = []
            self.open_port: int = 4201

            self.listen_thread = threading.Thread(target=self.listen_to_new_conns)
            self.listen_thread.start()

        else:
            self.init_client()

    def listen_to_host(self):
        while True:
            data = self.socket.recv(128).lstrip(b'0')
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

    def listen_to_connection(self, conn: socket.socket):
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
                    self.send_data_to_connections((b'LOCK;' + str(circle_id).encode() + b';' + str(port).encode()).zfill(128))
            elif header == 'UNLOCK':
                circle_id = int(body.split(b';')[0].decode())
                port = int(body.split(b';')[1].decode())

                self.database.unlockCircle(circle_id, port)
                self.send_data_to_connections((b'UNLOCK;' + str(circle_id).encode() + b';' + str(port).encode()).zfill(128))

    def listen_to_new_conns(self):
        """
        Will listen to new connections and send the current database to them
        Whenever a new connection is made, it will be added to the connections list, a new port will be assigned to communicate with it and a new thread will be started to handle the communication
        """
        print(f'-----    Listening to new connections in port: {self.port}    -----')
        self.socket.listen(24)

        while True:
            conn, addr = self.socket.accept()

            request = conn.recv(128).decode()
            print(f'Request: {request} from {addr}')

            new_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            new_conn.bind(('localhost', self.open_port))
            print(f'New connection: {self.open_port}')
            conn.send(str(self.open_port).encode())

            ack = conn.recv(128).decode()
            print(f'ACK: {ack} from {addr}')

            conn.close()

            new_conn.connect(('localhost', addr[1]))

            self.send_current_db(new_conn)

            self.connections.append([new_conn, True])

            new_conn_thread = threading.Thread(target=self.listen_to_connection, args=(new_conn,))
            new_conn_thread.start()

            self.open_port += 1

    def send_data_to_connections(self, data: bytes):
        data.zfill(128)
        for conn in self.connections:
            if not conn[1]:
                continue
            try:
                conn[0].send(data)
            except:
                print(f'Connection {conn[0]} closed')
                conn[1] = False

    def send_current_db(self, conn: socket.socket):
        try:
            conn.send(b'CODE;INIT-STREAM'.zfill(128))
            for circle in self.database.circles:
                conn.send((b'ADD;' + circle.encode()).zfill(128))
            conn.send(b'CODE;END-INIT-STREAM'.zfill(128))
        except:
            print(f'Failed to send current db to {conn}')

    def request_add_circle(self, circle: c.Circle):
        if self.host:
            self.database.addCircle(circle)
            self.send_data_to_connections((b'ADD;' + circle.encode()).zfill(128))
        else:
            self.socket.send((b'ADD;' + circle.encode()).zfill(128))

    def request_lock_circle(self, circle: c.Circle):
        if self.host:
            code, circle = self.database.lockCircle(circle.id, self.port)
            if code == board_database.BoardDatabase.DATABASE_REJECT:
                pass
            else:
                self.send_data_to_connections((b'LOCK;' + str(circle.id).encode() + b';' + str(self.port).encode()).zfill(128))
        else:
            self.socket.send((b'LOCK;' + str(circle.id).encode() + b';' + str(self.port).encode()).zfill(128))

    def request_unlock_circle(self, circle: c.Circle):
        if self.host:
            self.database.unlockCircle(circle.id, self.port)
            self.send_data_to_connections((b'UNLOCK;' + str(circle.id).encode() + b';' + str(self.port).encode()).zfill(128))
        else:
            self.socket.send((b'UNLOCK;' + str(circle.id).encode() + b';' + str(self.port).encode()).zfill(128))