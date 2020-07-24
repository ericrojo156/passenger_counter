import json
import uuid
from device.DeviceState import DeviceState

class APC_Record:
    def __init__(self, id: str, master_device_state: DeviceState, doors=[]):
        self.id = id
        self.doors = doors
        if (master_device_state == None):
            self.master_device = DeviceState()
        else:
            self.master_device = master_device_state
            for device_state in master_device_state.devices_state_list:
                print(device_state)
                self.doors.append(device_state)

    def to_dict(self):
        return {
            "id": self.id,
            "master_device": self.master_device.to_dict(),
            "doors": self.doors
        }

    def __str__(self):
        doors = self.doors
        return json.dumps({
            "id": self.id,
            "master_device": self.master_device.to_dict(),
            "doors": self.doors
        })

    @staticmethod
    def from_json(apc_record_json: str):
        return APC_Record.from_dict(json.loads(apc_record_json))
    
    @staticmethod
    def from_dict(apc_record_dict: dict):
        id = apc_record_dict["id"]
        master_device_state = DeviceState.from_dict(apc_record_dict["master_device"])
        doors = [json.loads(door["device_state"]) for door in apc_record_dict["doors"]]
        apc_record = APC_Record(id=id, master_device_state=master_device_state, doors=doors)
        return apc_record