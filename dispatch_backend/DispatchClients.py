from typing import List
from dispatch_backend.DeviceNode import DeviceNode

# class that represents a LAN consisting of one or more passenger counter devices aboard a transit vehible
class DispatchClients:
    def __init__(self, device_nodes: List[DeviceNode]):
        self.device_nodes = device_nodes