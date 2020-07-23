import typing
from config_api.ConfigIO import ConfigIO
import os
import json

class EndpointDeviceConfigIO(ConfigIO):
    config_dir_path = os.getcwd() + "/config_api"
    default_config_filepath = "/default_device_config.json"
    custom_config_filepath = "/device_config.json"

    def __init__(self, _config_dir_path=None):
        self.cache = None
        if (_config_dir_path != None):
            self.config_dir_path = _config_dir_path
        self.default_config_filepath = self.config_dir_path + self.default_config_filepath
        self.custom_config_filepath = self.config_dir_path + self.custom_config_filepath
        if (os.path.isfile(self.custom_config_filepath)):
            self.config_file_path = self.custom_config_filepath
            self.select_default_source(False)
        else:
            self.config_file_path = self.default_config_filepath
            self.select_default_source(True)

    def save_config_json(self, config_json: str):
        try:
            filepath = self.custom_config_filepath
            if (os.path.isfile(filepath)):
                os.remove(filepath)
            with open(filepath, 'x') as f:
                f.write(config_json)
                self.cache = config_json
            self.select_default_source(False)
        except Exception as e:
            print(e)
        
    def load_config_json(self) -> str:
        if (self.cache == None):
            filepath = self.config_file_path
            with open(self.config_file_path) as f:
                config_json = f.read()
            return config_json
        else:
            return self.cache

    def select_default_source(self, should_select=True):
        # changing the default source invalides the cache, since the previously cached config may not be the default or custom config to be acquired from the specified source
        self.cache = None
        if (should_select):
            self.config_file_path = self.default_config_filepath
            if (os.path.isfile(self.custom_config_filepath)):
                os.remove(self.custom_config_filepath)
        else:
            self.config_file_path = self.custom_config_filepath