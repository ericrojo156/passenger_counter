import json
import os
from device.DividerLine import DividerLine
from config_api.ConfigIO import ConfigIO

# Responsible for mapping the internal structure of the configuration json to configuration API to be queried/modifying by the device at runtime
class DeviceConfig:
    def __init__(self, _config_io: ConfigIO):
        self.config_io = _config_io
        self.load_config()

    def load_config(self):
        config_json = self.config_io.load_config_json()
        self.config_dict = json.loads(config_json)

    def save_config(self):
        self.config_io.save_config_json(config_json=json.dumps(self.config_dict))

    def gps_is_enabled(self):
        return self.config_dict.get("trackGPS", True)

    def divider_line(self):
        serialized_line = json.dumps(self.config_dict.get("dividerLine"))
        return DividerLine(serialized_line)

    def is_master(self):
        return self.config_dict.get("isMaster", True)

    def set_as_master(self, is_master):
        self.config_dict["isMaster"] = is_master
        self.save_config()

    def other_LAN_devices(self):
        return self.config_dict.get("otherDevicesOnLAN", [])

    def revert_to_default(self):
        self.config_io.select_default_source()
        self.load_config()

    def set_divider_line(self, divider_line):
        self.config_dict["dividerLine"] = divider_line.to_dict()
        self.save_config()

    def set_custom_configs(self, custom_configs):
        keys = custom_configs.keys()
        for key in keys:
            try:
                self.config_dict[key] = custom_configs[key]
            except KeyError:
                return False
        self.save_config()
        return True

    def get_address(self):
        return self.config_dict["deviceAddress"]

    def set_address(self, address):
        self.config_dict["deviceAddress"] = address
        self.save_config()

    def get_device_label(self):
        return self.config_dict["deviceLabel"]