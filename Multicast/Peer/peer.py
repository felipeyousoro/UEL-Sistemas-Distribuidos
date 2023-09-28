class Peer:
    def __init__(self, name: str, ip: str):
        self.name: str = name
        self.ip: str = ip
        self.online: bool = False

    def __str__(self):
        return f'Peer: {self.name} - IP: {self.ip} - Online: {self.online}'
