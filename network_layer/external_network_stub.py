import requests
import json
from data_layer.APC_Record import APC_Record
from device_cli import CUSTOM_CONFIG
from config_api.DeviceConfig import DeviceConfig
dispatch_service = "http://localhost:4000"

def post_APC_Record(apc_record=APC_Record()):
    response_dict = requests.post(f"{dispatch_service}/", json={"apc_record": str(apc_record)}).json()
    return response_dict

def configure_device(config: DeviceConfig = None, master_node_address=""):
    response_dict = {"status": "ERROR"}
    if (len(master_node_ip > 0) and config != None):
        response_dict = requests.post(f"{master_node_address}/", json={"config": json.dumps(config.config_dict), "command": CUSTOM_CONFIG}).json()
        response_dict["status"] = "SUCCESS"
    return response_dict