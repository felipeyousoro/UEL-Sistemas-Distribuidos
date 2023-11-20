class Circle:
    def __init__(self, id: int, x: float, y: float, r: float, width: int, color: (int, int, int)):
        self.id = id
        self.x = x
        self.y = y
        self.r = r
        self.width = width
        self.color = color
        self.locked = False

    def isPointInside(self, x: float, y: float) -> bool:
        return (x - self.x) ** 2 + (y - self.y) ** 2 <= self.r ** 2

    def __repr__(self):
        return f'circle;{self.id};{self.x};{self.y};{self.r};{self.width};{self.color[0]},{self.color[1]},{self.color[2]};{self.locked}'

