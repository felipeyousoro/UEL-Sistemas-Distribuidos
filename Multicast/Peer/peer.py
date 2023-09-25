class Peer:
    def __init__(self, name: str, ip: str, port: int):
        self.name = name
        self.ip = ip
        self.port = port

    def __str__(self):
        return f'Peer: {self.name} {self.ip}:{self.port}'