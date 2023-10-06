import time


class Peer:
    def __init__(self, name: str, ip: str):
        self.name: str = name
        self.ip: str = ip
        self.online: bool = False

        self.await_time: float = 0
        self.previous_beat_sent: float = 0
        self.last_beat_sent: float = 0
        self.checked:bool = False

    def __str__(self):
        if(self.last_beat_sent != 0):
            return f'Peer: {self.name} - IP: {self.ip} - Online: {self.online} - Await Time: {self.await_time:.5f} - Seconds since last beat: {time.time() - self.last_beat_sent:.5f}'
        else:
            return f'Peer: {self.name} - IP: {self.ip} - Online: {self.online} - Await Time: {self.await_time:.5f} - Seconds since last beat: Yet to receive first beat'