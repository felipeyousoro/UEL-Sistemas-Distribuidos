class Peer:
    def __init__(self, name: str, ip: str):
        self.name = name
        self.ip = ip

    def __str__(self):
        return f'Peer: {self.name} {self.ip}'