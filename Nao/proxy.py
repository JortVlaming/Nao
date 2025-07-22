from typing import Callable, Literal

from .robot import Robot


class Proxy:
    def __init__(self, robot: Robot, name: str):
        self.robot = robot
        self.proxy = robot.get_service(name)

        self._signal_connections = {}    # event_name -> signal_id
        self._callbacks = {}             # event_name -> [callbacks]

        self._memory_subscriptions = {}  # event_name -> (subscriber_name, callback_name)

        self.debug_mode = False

    def _on(self, name: str, callback: Callable[..., None], source: Literal["event", "signal"] = "signal"):
        """
        Register a callback either to a proxy signal or an ALMemory event.

        :param name: Name of the event or signal.
        :param callback: Callable to invoke when triggered.
        :param source: "signal" to connect via proxy.signal(name),
                       "event" to connect via ALMemory.subscribeToEvent(name).
        """
        if self.debug_mode:
            print("Callback registered for " + name + " sourced from " + source + "s")
        if source == "event":
            if name not in self._callbacks:
                self._callbacks[name] = []

                # Compose a unique method name for the memory callback
                callback_method_name = f"_memory_cb_{name.replace('/', '_')}"

                # Define the memory callback that dispatches to registered callbacks
                def memory_callback(value):
                    self._dispatch(name, value)

                # Attach the callback method to this instance dynamically
                setattr(self, callback_method_name, memory_callback)

                # Create a unique subscriber name
                subscriber_name = f"{self.__class__.__name__}_{name.replace('/', '_')}"

                # Subscribe via ALMemory
                memory = self.robot.get_service("ALMemory")
                memory.subscribeToEvent(name, subscriber_name, callback_method_name)

                # Store subscription info for potential future cleanup
                if not hasattr(self, "_memory_subscriptions"):
                    self._memory_subscriptions = {}
                self._memory_subscriptions[name] = (subscriber_name, callback_method_name)

            # Register the user callback
            self._callbacks[name].append(callback)

        else:
            # For signals: connect directly to proxy.signal(name)
            signal = self.proxy.signal(name)
            signal_id = signal.connect(lambda *args: self._dispatch(name, *args))

            # Store the connection for disconnecting later
            if not hasattr(self, "_signal_connections"):
                self._signal_connections = {}
            if not hasattr(self, "_callbacks"):
                self._callbacks = {}

            self._signal_connections[name] = signal_id
            if name not in self._callbacks:
                self._callbacks[name] = []
            self._callbacks[name].append(callback)

    def _dispatch(self, event_name, *args):
        for cb in self._callbacks.get(event_name, []):
            cb(*args)

    def disconnect_all(self):
        for event_name, signal_id in self._signal_connections.items():
            self.proxy.signal(event_name).disconnect(signal_id)
        self._signal_connections.clear()

        # Unsubscribe from ALMemory events
        memory = self.robot.get_service("ALMemory")
        for event_name, (subscriber, _) in self._memory_subscriptions.items():
            memory.unsubscribeToEvent(event_name, subscriber)
        self._memory_subscriptions.clear()

        self._callbacks.clear()

    def _alvalues_to_list(self, alvalue):
        if hasattr(alvalue, "__iter__") and not isinstance(alvalue, (str, bytes)):
            return list(alvalue)
        else:
            return [alvalue]
