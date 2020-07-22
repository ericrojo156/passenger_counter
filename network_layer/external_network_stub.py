import requests
import json
from data_layer.APC_Record import APC_Record
from device_cli import SET_CONFIG, GET_CONFIG

from config_api.DeviceConfig import DeviceConfig
dispatch_service = "http://localhost:4000"

def post_APC_Record(master_device_address: str, apc_record: APC_Record = APC_Record()):
    response_dict = requests.post(f"{dispatch_service}/apc_record", json={"apc_record": str(apc_record), "master_device_address": master_device_address}).json()
    return response_dict

def is_valid_config_json(config_json: str):
    return len(config_json) > 0

def is_valid_device_address(master_device_address: str):
    return len(master_device_address) > 0

def configure_device(config_json: str, master_device_address: str):
    response_dict = {"status": "ERROR"}
    if (is_valid_config_json(config_json) and is_valid_master_node_addr(master_device_address)):
        response_dict = requests.post(f"{master_device_address}/", json={"config_json": config_json, "command": SET_CONFIG}).json()
        response_dict["status"] = "SUCCESS"
    return response_dict

def request_device_config_json(master_device_address, device_address, from_default_source):
    response_dict = {"status": "ERROR"}
    if (is_valid_device_address(master_device_address)):
        response_dict = requests.post(f"{master_device_address}/", json={"command": GET_CONFIG, "master_device_address": master_device_address, "device_address": device_address, "from_default_source": from_default_source}).json()
    return response_dict