import time


class Peer:
    def __init__(self, name: str, ip: str):
        self.name: str = name
        self.ip: str = ip
        self.online: bool = False

        self.delta_time: float

        self.last_beat_answered: float = 0

    def __str__(self):
        if(self.last_beat_answered != 0):
            return f'Peer: {self.name} - IP: {self.ip} - Online: {self.online} - Delta Time: {self.delta_time:.5f} - Seconds since last beat: {time.time() - self.last_beat_answered:.5f}'
        else:
            return f'Peer: {self.name} - IP: {self.ip} - Online: {self.online} - Delta Time: {self.delta_time:.5f} - Seconds since last beat: Yet to receive first beat'