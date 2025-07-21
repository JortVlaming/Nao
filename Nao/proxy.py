from typing import Callable

from .robot import Robot


class Proxy:
    def __init__(self, robot: Robot, name: str):
        self.proxy = robot.get_service(name)

        self._signal_connections = {}  # event_name -> signal_id
        self._callbacks = {}           # event_name -> [callbacks]

    def _on(self, event_name: str, callback: Callable):
        if event_name not in self._callbacks:
            self._callbacks[event_name] = []

        # Connect to the actual Qi signal only once
        if event_name not in self._signal_connections:
            signal = self.proxy.signal(event_name)
            signal_id = signal.connect(lambda *args, en=event_name: self._dispatch(en, *args))
            self._signal_connections[event_name] = signal_id

        self._callbacks[event_name].append(callback)

    def _dispatch(self, event_name, *args):
        for cb in self._callbacks.get(event_name, []):
            cb(*args)

    def disconnect_all(self):
        """
        disconnect all callbacks from the ALBehaviorManager
        :return:
        """
        for event_name, signal_id in self._signal_connections.items():
            self.proxy.signal(event_name).disconnect(signal_id)
        self._signal_connections.clear()
        self._callbacks.clear()