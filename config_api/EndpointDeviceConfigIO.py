import typing
from config_api.ConfigIO import ConfigIO
import os
import json

class EndpointDeviceConfigIO(ConfigIO):
    config_dir_path = os.getcwd() + "/config_api"
    default_config_filepath = "/default_device_config.json"
    custom_config_filepath = "/device_config.json"

    def __init__(self, _config_dir_path=None):
        if (_config_dir_path != None):
            self.config_dir_path = _config_dir_path
        self.default_config_filepath = self.config_dir_path + self.default_config_filepath
        self.custom_config_filepath = self.config_dir_path + self.custom_config_filepath
        if (os.path.isfile(self.custom_config_filepath)):
            self.config_file_path = self.custom_config_filepath
        else:
            self.config_file_path = self.default_config_filepath

    def save_config_json(self, config_json: str):
        filepath = self.custom_config_filepath
        if (os.path.isfile(filepath)):
            os.remove(filepath)
        with open(filepath, 'x') as f:
            config_json_str = config_json
            f.write(config_json_str)

    def load_config_json(self) -> str:
        filepath = self.config_file_path
        with open(self.config_file_path) as f:
            config_json_str = f.read()
        return config_json_str

    def select_default_source(self):
        self.config_file_path = self.default_config_filepath
        if (os.path.isfile(self.custom_config_filepath)):
            os.remove(self.custom_config_filepath)