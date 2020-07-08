import requests
import json

def lan_send(fromAddress, toAddress, command, payload={}):
    response_dict = requests.post(f"{toAddress}/", json={"command": command, "data": json.dumps(payload)}).json()
    return response_dict