import socket
import sys
import time

from Circle import circle as c

if __name__ == '__main__':
    c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c_socket.bind(('localhost', int(sys.argv[1])))

    c_socket.connect(('localhost', 6901))

    while True:
        c_socket.send(b'ping;join')
        msg = c_socket.recv(1024)
        print(f'Received: {msg.decode()}')
        print(f'Returning ACK')
        c_socket.send(b'ack')
        c_socket.close()
        break

    c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c_socket.bind(('localhost', int(sys.argv[1])))
    print(f'Connecting to {msg.decode()}')
    c_socket.connect(('localhost', int(msg.decode())))
    print(f'Connected to {msg.decode()}')

    while True:
        msg = c_socket.recv(1024)
        print(msg.decode())

    c_socket.close()
    print(f'Socket closed')