import qi

class Robot:
    def __init__(self, ip: str, port: int = 9559):
        self.ip = ip
        self.port = port
        self.session = self._connect()

    def _connect(self):
        session = qi.Session()
        session.connect(f"tcp://{self.ip}:{self.port}")
        return session

    def get_service(self, name: str):
        return self.session.service(name)
