import json
import os
import uuid
from device.DividerLine import DividerLine
from config_api.ConfigIO import ConfigIO

# Responsible for mapping the internal structure of the configuration json to configuration API to be queried/modifying by the device at runtime
class DeviceConfig:
    def __init__(self, config_io: ConfigIO):
        self.config_io = config_io
        self.load_config()
        self.id = self.get_id()

    # NOTE: saves the id to device config if the request for id fails
    def get_id(self):
        id = None
        try:
            id = self.config_dict["id"]
        except KeyError:
            id = str(uuid.uuid4())
            self.config_dict["id"] = id
            self.save_config()
        return id

    def set_config(self, config_dict):
        self.config_dict = config_dict

    def load_config_json(self):
        config_json = self.config_io.load_config_json()
        return config_json

    def load_config(self):
        config_json = self.load_config_json()
        self.config_dict = json.loads(config_json)
        return self.config_dict

    def save_config(self):
        config_json = json.dumps(self.config_dict)
        self.config_io.save_config_json(config_json=config_json)

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

    def set_custom_configs(self, config_json):
        config_dict = json.loads(config_json)
        keys = config_dict.keys()
        try:
            for key in keys:
                self.config_dict[key] = config_dict[key]
            self.save_config()
        except Exception as e:
            print(e)
            return False
        return True

    def get_address(self):
        return self.config_dict["deviceAddress"]

    def set_address(self, address):
        self.config_dict["deviceAddress"] = address
        self.save_config()

    def get_device_label(self):
        return self.config_dict["deviceLabel"]