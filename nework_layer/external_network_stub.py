import requests
import json
from data_layer.APC_Record import APC_Record

dispatch_service = "http://localhost:4000"

def external_post(apc_record=APC_Record()):
    response_dict = requests.post(f"{dispatch_service}/", json={"apc_record": str(apc_record)}).json()
    return response_dict