from Circle import circle as c


class BoardDatabase:
    DATABASE_UPDATE: int = 1
    DATABASE_DELETE: int = 2
    DATABASE_ADD: int = 3
    DATABASE_ACCEPT: int = 4
    DATABASE_REJECT: int = 5
    DATABASE_LOCK: int = 6
    DATABASE_UNLOCK: int = 7


    def __init__(self):
        self.serial_id: int = 0
        self.circles: list[c.Circle] = []

    def addCircle(self, circle: c.Circle):
        circle.id = self.serial_id
        self.serial_id += 1

        self.circles.append(circle)

        return self.DATABASE_ADD, circle

    def lockCircle(self, id_circle: int):
        local_circle: c.Circle = None
        for c in self.circles:
            if c.id == id_circle:
                local_circle = c
                break

        if local_circle is None or local_circle.locked:
            return self.DATABASE_REJECT, None

        local_circle.locked = True

        return self.DATABASE_LOCK, local_circle

    def unlockCircle(self, id_circle: int):
        local_circle: c.Circle = None
        for c in self.circles:
            if c.id == id_circle:
                local_circle = c
                break

        if local_circle is None or not local_circle.locked:
            return self.DATABASE_REJECT, None

        local_circle.unlock = False

        return self.DATABASE_UNLOCK, local_circle

    def updateCircle(self, id_circle: int, circle: c.Circle):
        local_circle = None
        for c in self.circles:
            if c.id == id_circle:
                local_circle = c
                break

        if local_circle is None or local_circle.locked:
            return self.DATABASE_REJECT, None

        local_circle.x = circle.x
        local_circle.y = circle.y
        local_circle.r = circle.r
        local_circle.width = circle.width
        local_circle.color = circle.color

        return self.DATABASE_UPDATE, local_circle

    def deleteCircle(self, id_circle: int):
        local_circle: c.Circle = None
        position: int = 0
        for c in self.circles:
            if c.id == id_circle:
                local_circle = c
                break
            position += 1

        if local_circle is None or local_circle.locked:
            return self.DATABASE_REJECT, None

        self.circles.pop(position)

        return self.DATABASE_DELETE, local_circle
