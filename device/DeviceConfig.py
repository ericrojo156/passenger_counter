import json
import os
from device.DividerLine import DividerLine

# Responsible for mapping the internal structure of the configuration json to configuration API to be queried/modifying by the device at runtime
class DeviceConfig:
    default_config_filepath = os.getcwd() + "/device/default_device_config.json"
    custom_config_filepath = os.getcwd() + "/device/device_config.json"
    def __init__(self):
        if (os.path.isfile(self.custom_config_filepath)):
            self.config_file_path = self.custom_config_filepath
        else:
            self.config_file_path = self.default_config_filepath
        self.load_config()

    def load_config(self):
        filepath = self.config_file_path
        with open(self.config_file_path) as f:
            config_json_str = f.read()
        self.config_dict = json.loads(config_json_str)

    def save_config(self):
        filepath = self.custom_config_filepath
        if (os.path.isfile(filepath)):
            os.remove(filepath)
        with open(filepath, 'x') as f:
            config_json_str = json.dumps(self.config_dict)
            f.write(config_json_str)

    def gps_is_enabled(self):
        return self.config_dict.get("trackGPS", True)

    def divider_line(self):
        serialized_line = json.dumps(self.config_dict.get("dividerLine"))
        return DividerLine(serialized_line)

    def is_master(self):
        return self.config_dict.get("isMaster", True)

    def set_is_master(self, is_master):
        self.config_dict["isMaster"] = is_master
        self.save_config()

    def other_LAN_devices(self):
        return self.config_dict.get("otherDevicesOnLAN", [])

    def revert_to_default(self):
        self.config_file_path = self.default_config_filepath
        if (os.path.isfile(self.custom_config_filepath)):
            os.remove(self.custom_config_filepath)
        self.load_config()

    def set_divider_line(self, divider_line):
        self.config_dict["dividerLine"] = divider_line.to_dict()
        self.save_config()