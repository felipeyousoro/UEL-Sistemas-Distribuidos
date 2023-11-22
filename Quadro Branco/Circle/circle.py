class Circle:
    def __init__(self, id: int, x: int, y: int, r: int, width: int, color: (int, int, int)):
        self.id = id
        self.x = x
        self.y = y
        self.r = r
        self.width = width
        self.color = color
        self.lock_holder = -1

    def isPointInside(self, x: int, y: int) -> bool:
        return (x - self.x) ** 2 + (y - self.y) ** 2 <= self.r ** 2

    def __repr__(self):
        return f'circle;{self.id};{self.x};{self.y};{self.r};{self.width};{self.color[0]},{self.color[1]},{self.color[2]};{self.lock_holder}'

    def encode(self) -> bytes:
        return repr(self).encode()

    @staticmethod
    def decode(data: bytes):
        data = data.decode()
        data = data.split(';')
        return Circle(int(data[1]), int(data[2]), int(data[3]), int(data[4]), int(data[5]), (int(data[6].split(',')[0]), int(data[6].split(',')[1]), int(data[6].split(',')[2])))