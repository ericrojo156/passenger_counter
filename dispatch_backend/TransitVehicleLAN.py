from typing import List
from dispatch_backend.DeviceNode import DeviceNode
from config_api.DispatchDeviceConfigIO import DispatchDeviceConfigIO
import json
import uuid

# class that represents a LAN consisting of one or more passenger counter devices aboard a transit vehible
class TransitVehicleLAN:
    def __init__(self, id, master_device_address="", config_io=DispatchDeviceConfigIO(), records=[]):
        self.master_device_address = master_device_address
        self.master_config_io = config_io
        self.records = records
        device_nodes_dict = {}
        nodes = self.get_all_configs_from_lan(master_device_address=master_device_address)
        for node in nodes:
            if (len(node.address) > 0):
                device_nodes_dict[node.address] = node
        self.device_nodes_dict = device_nodes_dict

    def get_all_configs_from_lan(self, master_device_address=master_device_address):
        master_config = self.master_config_io.load_config_json()
        lan_device_addresses = master_config.other_lan_devices()
        return [
            DeviceNode(
                address = device_address,
                config = DeviceConfig(
                    DispatchDeviceConfigIO(
                        _device_address=device_address,
                        _master_device_address=master_device_address
                    )
                )
            )
            for device_address in lan_device_addresses
        ]

    def to_json(self):
        return json.dumps({
            "master_device_address": self.master_device_address,
            "devices": self.device_nodes_dict,
            "latest_record": self.records[-1]
        })