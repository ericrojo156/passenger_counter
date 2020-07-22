from config_api.DeviceConfig import DeviceConfig
from config_api.DispatchDeviceConfigIO import DispatchDeviceConfigIO

class DeviceNode:
    def __init__(self, address="", config=DeviceConfig(DispatchDeviceConfigIO())):
        self.address = address
        self.config = config
    
    def is_master(self):
        return self.config.is_master()