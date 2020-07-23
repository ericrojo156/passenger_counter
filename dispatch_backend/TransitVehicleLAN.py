from typing import List
from dispatch_backend.DeviceNode import DeviceNode
from config_api.DispatchDeviceConfigIO import DispatchDeviceConfigIO
from config_api.DeviceConfig import DeviceConfig
import json
import uuid

# class that represents a LAN consisting of one or more passenger counter devices aboard a transit vehible
class TransitVehicleLAN:
    def __init__(self, id, master_device_address="", master_config=DeviceConfig(DispatchDeviceConfigIO()), records=[]):
        self.id = id
        self.master_device_address = master_device_address
        self.master_config = master_config
        self.records = records

    def get_lan_devices_configs(self, master_device_address):
        lan_device_addresses = self.master_config.other_LAN_devices()
        lan_devices_configs = []
        for device_address in lan_device_addresses:
            device_config = DeviceConfig(
                DispatchDeviceConfigIO(
                    _device_address=device_address,
                    _master_device_address=master_device_address
                )
            )
            lan_devices_configs.append(device_config)
        return lan_devices_configs

    def __str__(self):
        return json.dumps({
            "id": self.id,
            "master_device_address": self.master_device_address,
            "latest_record": self.records[-1].to_json()
        })

    def to_dict(self):
        return {
            "id": self.id,
            "master_device_address": self.master_device_address,
            "latest_record": self.records[-1].to_dict()
        }