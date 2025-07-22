from typing import List, Callable, Tuple, Dict

from ..proxy import Proxy
from ..robot import Robot


class ALConnectionManager(Proxy):
    def __init__(self, robot: Robot):
        super().__init__(robot, "ALConnectionManager")

    """
    Methods
    """

    def state(self) -> str:
        """
        Returns the global state of the network connectivity. Possible values are:
            - ``online`` if an Internet connection is available.
            - ``ready`` this state means that at least one service is successfully connected.
            - ``offline`` this state means there is no network connection.
        :return: "online", "ready" or "offline"
        """
        return self.proxy.state()

    def scan(self, technology: str|None = None) -> None:
        """
        Scan for neighbor services on all available technologies. This is useful to refresh the list of services, which disappears after a while(specially for WiFi services).
        :param technology: (optional): The type of technology to scan for
        :return:
        """
        if technology:
            self.proxy.scan(technology)
        else:
            self.proxy.scan()

    def services(self) -> List:
        """
        Returns the list of all services with their properties. It might be useful to call the ALConnectionManagerProxy::scan method before.
        :return: An array of NetworkInfo contained in a List
        """
        return self._alvalues_to_list(self.proxy.services())

    def technologies(self) -> List:
        """
        Returns an array of string representing the available technologies, possible values are:
            - “ethernet”
            - “wifi”
            - “bluetooth”
        :return: A list of available technologies.
        """
        return self._alvalues_to_list(self.proxy.technologies())

    def service(self, serviceId: str) -> List:
        """
        Returns the properties of a given service identifier, the NetworkInfo is represented as List
        :param serviceId: The identifier of the service to get the properties.
        :return: the properties of the given service identifier.
        :raise ALError: when the service is not available.
        """
        return self._alvalues_to_list(self.proxy.service(serviceId))

    def connect(self, serviceId: str) -> None:
        """
        Connects to a network service.

        If some information are required to connect to this service, like a passphrase or the service name (for hidden services) an event will be raised.
        :param serviceId: The identifier for the service to connect.
        :return:
        :raise ALError: when the service not available.
        """
        self.proxy.connect(serviceId)

    def disconnect(self, serviceId: str) -> None:
        """
        Disconnects from the service.
        :param serviceId: The identifier of the service to disconnect.
        :return:
        :raise ALError: when the service is not available.
        """
        self.proxy.disconnect(serviceId)

    def forget(self, serviceId: str) -> None:
        """
        Removes a favorite service. Requests the given serviceId to forget association information. This will set the favorite and auto-connect boolean to false.
        :param serviceId: The identifier of the network to forget.
        :return:
        :raise ALError: When the service is not available.
        """
        self.proxy.forget(serviceId)

    def setServiceIPv4(self, serviceId: str, ipv4: Dict[str, str]) -> None:
        """
        Request to apply an IPv4 configuration.
        Possible keys and values are:

-    “Method” [Mandatory]
    Possible values are “dhcp”, “manual”.

    To set the ipv4 to dhcp just reply a map with Method = “dhcp”.
-    “Address”
    The ipv4 address to set for example “192.168.0.100”
-    “Netmask”
    The IPv4 netmask for example “255.255.255.0”
-    “Gateway”
    The IPv4 gateway for example “192.168.0.1”.

        :param serviceId: The identifier of the service.
        :param ipv4: A map representing the IPv4 configuration.
        :return:
        """
        self.proxy.setServiceIPv4(serviceId, ipv4)