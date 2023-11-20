import time
import random

from BoardDatabase import board_database
from Circle import circle as c
if __name__ == '__main__':
    db: board_database.BoardDatabase = board_database.BoardDatabase()

    crcl: c.Circle = c.Circle(0, 0, 0, 0, 0, (1, 2, 3))
    crcl2: c.Circle = c.Circle(0, 0, 0, 0, 0, (0, 0, 0))

    db.addCircle(crcl)
    db.addCircle(crcl2)

    print(db.lockCircle(1))

    db.deleteCircle(1)
    print(db.unlockCircle(1))
    print(db.circles)
