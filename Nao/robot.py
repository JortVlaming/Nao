import qi

class Robot:
    def __init__(self, ip: str, port: int = 9559):
        self.ip = ip
        self.port = port
        self.session = self._connect()

    def _connect(self):
        session = qi.Session()
        try:
            session.connect(f"tcp://{self.ip}:{self.port}")
        except RuntimeError as rte:
            if "The call request could not be handled" in str(rte):
                return None
            raise rte
        return session

    def get_service(self, name: str):
        if self.session is None:
            return None
        return self.session.service(name)
