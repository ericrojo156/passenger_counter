import json
import uuid
from device.DeviceState import DeviceState

class APC_Record:
    def __init__(self, id: str, master_device_state: DeviceState, device_label=""):
        self.id = id
        self.device_label = device_label
        self.doors = []
        if (master_device_state == None):
            self.master_device = DeviceState()
        else:
            self.master_device = master_device_state
            for device_state in master_device_state.devices_state_list:
                self.doors.append(device_state)

    def to_dict(self):
        return {
            "id": self.id,
            "device_label": self.device_label,
            "master_device": self.master_device.to_dict(),
            "doors": self.doors
        }

    def __str__(self):
        doors = self.doors
        return json.dumps({
            "id": self.id,
            "device_label": self.device_label,
            "master_device": self.master_device.to_dict(),
            "doors": self.doors
        })

    @staticmethod
    def from_json(apc_record_json: str):
        return APC_Record.from_dict(json.loads(apc_record_json))
    
    @staticmethod
    def from_dict(apc_record_dict: dict):
        id = apc_record_dict["id"]
        device_label = apc_record_dict["device_label"]
        master_device_state = DeviceState.from_dict(apc_record_dict["master_device"])
        apc_record = APC_Record(id=id, master_device_state=master_device_state, device_label=device_label)
        return apc_record