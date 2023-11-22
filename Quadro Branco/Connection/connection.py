import random
import threading
import time

from BoardDatabase import board_database
from Board import board
from Circle import circle as c
import socket


class Connection:
    def __init__(self, database: board_database.BoardDatabase, port: int, host=False, host_port=0):
        self.database = database

        self.host = host

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('localhost', port))

        if host:
            self.connections: list[[socket.socket, bool]] = []
            self.open_port: int = 4201

            self.listen_thread = threading.Thread(target=self.listen_to_connections)
            self.listen_thread.start()

        else:
            self.socket.connect(('localhost', host_port))

    def listen_to_connections(self):
        """
        Will listen to new connections and send the current database to them
        Whenever a new connection is made, it will be added to the connections list, a new port will be assigned to communicate with it and a new thread will be started to handle the communication
        """
        print('Listening BILU TETEIA')
        self.socket.listen(24)

        while True:
            conn, addr = self.socket.accept()

            request = conn.recv(128).decode()
            print(f'Request: {request} from {addr}')

            new_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            new_connection.bind(('localhost', self.open_port))
            print(f'New connection: {self.open_port}')
            conn.send(str(self.open_port).encode())

            ack = conn.recv(128).decode()
            print(f'ACK: {ack} from {addr}')

            conn.close()

            new_connection.connect(('localhost', addr[1]))

            self.send_current_db(new_connection)

            self.connections.append([new_connection, True])

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
            for circle in self.database.circles:
                conn.send(circle.encode().zfill(128))
            conn.send(b'CODE;END-INIT-STREAM'.zfill(128))
        except:
            print(f'Failed to send current db to {conn}')

    def request_add_circle(self, circle: c.Circle):
        # print(f'Adicionando circulo {circle}')
        # print(self.database.circles)
        if self.host:
            self.database.addCircle(circle)
            self.send(circle.encode().zfill(128))
        else:
            print('a gente ve dps')
