import threading
import time

from BoardDatabase import board_database
from Board import board
from Circle import circle as c
import socket


class Connection:
    def __init__(self, database: board_database.BoardDatabase, port: int, host=False):
        self.database = database

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('localhost', port))

        self.connections: list[[socket.socket, bool]] = []
        self.open_port: int = 4201

        self.rcv_thread = threading.Thread(target=self.run)
        self.rcv_thread.start()

        self.macaco_thread = threading.Thread(target=self.macaco)
        self.macaco_thread.start()


    def run(self):
        print('Listening')
        self.socket.listen(5)

        while True:
            conn, addr = self.socket.accept()

            request = conn.recv(1024).decode()
            print(f'Request: {request} from {addr}')

            new_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            new_connection.bind(('localhost', self.open_port))
            print(f'New connection: {self.open_port}')
            conn.send(str(self.open_port).encode())

            ack = conn.recv(1024).decode()
            print(f'Ack: {ack} from {addr}')

            conn.close()

            new_connection.connect(('localhost', addr[1]))
            self.connections.append([new_connection, True])

            self.open_port += 1

    def send(self, data: bytes):
        print(f'Sending {data}')
        for conn in self.connections:
            try:
                conn[0].send(data)
            except:
                print(f'Connection {conn[0]} closed')
                conn[1] = False

    def macaco(self):
        while True:
            time.sleep(5)
            self.connections = [conn for conn in self.connections if conn[1]]
            print(f'Connections: {self.connections}')
            for circle in self.database.circles:
                self.send(circle.encode())