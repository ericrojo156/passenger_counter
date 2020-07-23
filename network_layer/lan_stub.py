import requests
import json

def lan_send(fromAddress, toAddress, command, data={}):
    response_dict = requests.post(f"{toAddress}/", json={"command": command, "data": json.dumps(data)}).json()
    return response_dict