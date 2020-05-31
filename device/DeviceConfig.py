import json
import os
from DividerLine import DividerLine

# Responsible for mapping the internal structure of the configuration json to configuration API to be queried/modifying by the device at runtime
class DeviceConfig:
    def __init__(self):
        if (os.path.isfile("device_config.json")):
            self.config_file_path = "device_config.json"
        else:
            self.config_file_path = "default_device_config.json"

    def load_config(self):
        filepath = self.config_file_path
        with open(self.config_file_path) as f:
            config_json_str = f.read()
        self.config_dict = json.loads(config_json_str)

    def save_config(self):
        self.filepath = "device_config.json"
        with open(self.config_file_path, 'x') as f:
            config_json_str = json.dumps(self.config_dict)
            f.write(config_json_str)

    def gps_is_enabled(self):
        return self.config_dict.get("gps", True)

    def divider_line(self):
        serialized_line = self.config_dict.get("dividerLine", "")
        return DividerLine(serialized_line)

    def is_master(self):
        return self.config_dict.get("isMaster", True)

    def other_LAN_devices(self):
        return self.config_dict.get("otherDevicesOnLAN", [])