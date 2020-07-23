from config_api.ConfigIO import ConfigIO
from network_layer.external_network_stub import configure_device, request_device_config_json
import json

class DispatchDeviceConfigIO(ConfigIO):
    #from_default_source = True
    master_device_address = ""

    def __init__(self, _device_address="", _master_device_address=""):
        self.error_state = False
        self.config_json_cache = None
        self.master_device_address = _master_device_address
        if (len(_device_address) > 0):
            self.device_address = _device_address
        else: # if device address is unspecified, then assign to master address (thereby assuming the config is to be loaded from the master device rather than a slave device)
            self.device_address = _master_device_address
            
    def save_config_json(self, config_json: str):
        try:
            self.config_json_cache = config_json
            response_dict = configure_device(config_json=config_json, master_device_address=self.master_device_address)
            if (response_dict["status"] == "ERROR"):
                self.error_state = True
            else:
                self.error_state = False
        except Exception as e:
            print(e)
            self.error_state = True

    def load_config_json(self) -> str:
        config_json = self.config_json_cache
        if (not config_json):
            response_dict = request_device_config_json(
                master_device_address=self.master_device_address,
                device_address=self.device_address
            )
            if (response_dict["status"] == "SUCCESS"):
                config_json = json.dumps(response_dict["data"])
                self.config_json_cache = config_json
            else:
                self.config_json_cache = json.dumps({"EMPTY_CONFIG": f"unable to load configuration from device at {self.device_address}"})
        return self.config_json_cache

    # this implementation should be agnostic to whether its remote module decides to load the default or custom config source
    def select_default_source(self, should_select=True):
        pass