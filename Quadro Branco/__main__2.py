import socket
import sys
import threading
import time

from Circle import circle as c
from Board import board as board

def macaco(conn: socket.socket, board: board.Board, circles: list[c.Circle]):
    while True:
        msg = conn.recv(128).lstrip(b'0')
        print(msg.decode())
        circles.append(c.Circle.decode(msg))
        board.setCircles(circles)

if __name__ == '__main__':
    c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c_socket.bind(('localhost', int(sys.argv[1])))

    c_socket.connect(('localhost', 6901))

    while True:
        c_socket.send(b'CODE;JOIN')
        msg = c_socket.recv(1024)
        print(f'Received: {msg.decode()}')
        print(f'Returning ACK')
        c_socket.send(b'CODE;ACK')
        c_socket.close()
        break

    c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c_socket.bind(('localhost', int(sys.argv[1])))
    print(f'Connecting to {msg.decode()}')
    c_socket.connect(('localhost', int(msg.decode())))
    print(f'Connected to {msg.decode()}')

    msg = None
    circle_list = []
    while True:
        msg = c_socket.recv(128).lstrip(b'0')
        if msg == b'CODE;END-INIT-STREAM':
            break
        circle_list.append(c.Circle.decode(msg))

    watanaboard = board.Board(None)
    watanaboard.setCircles(circle_list)

    macaco_thread = threading.Thread(target=macaco, args=(c_socket, watanaboard, circle_list))
    macaco_thread.start()

    watanaboard.begin()

    c_socket.close()
    print(f'Socket closed')