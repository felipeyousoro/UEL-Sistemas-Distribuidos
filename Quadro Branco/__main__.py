import sys
import threading
import socket

from BoardDatabase import board_database
from Board import board
from Connection import connection
from Circle import circle as c

if __name__ == '__main__':
    db: board_database.BoardDatabase = board_database.BoardDatabase()

    is_host = sys.argv[1] == 'host'
    if is_host:
        conn: connection.Connection = connection.Connection(db, host=True)
    else:
        host_port = int(sys.argv[2])
        conn: connection.Connection = connection.Connection(db, host_port=host_port)

    wb: board.Board = board.Board(conn)
    wb.begin()

