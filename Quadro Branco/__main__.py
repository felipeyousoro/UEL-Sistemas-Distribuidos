import time
import random

from BoardDatabase import board_database
from Board import board
from Connection import connection
from Circle import circle as c

if __name__ == '__main__':
    db: board_database.BoardDatabase = board_database.BoardDatabase()
    db.addCircle(c.Circle(0, 0, 0, 0, 0, (0, 0, 0)))
    conn: connection.Connection = connection.Connection(db, 6901, host=True)
    while True:
        db.addCircle(c.Circle(0, random.randint(0, 100), random.randint(0, 100), random.randint(0, 100), random.randint(0, 100), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
        time.sleep(30)

    #wb: board.Board = board.Board(conn)
    #wb.begin()
