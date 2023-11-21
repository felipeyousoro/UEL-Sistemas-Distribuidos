import sys
import threading
import time
import random

from BoardDatabase import board_database
from Board import board
from Connection import connection
from Circle import circle as c

if __name__ == '__main__':
    db: board_database.BoardDatabase = board_database.BoardDatabase()
    db.addCircle(c.Circle(0, 100, 200, 10, 3, (0, 0, 255)))
    db.addCircle(c.Circle(0, 200, 100, 10, 3, (255, 0, 0)))
    db.addCircle(c.Circle(0, 200, 200, 10, 3, (0, 255, 0)))

    conn: connection.Connection = connection.Connection(db, 6901, host=True)

    wb: board.Board = board.Board(conn)
    wb.setCircles(db.circles)
    wb.begin()
