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
            if (len(self.doors) == 0):
                for device_state in master_device_state.devices_state_list:
                    self.doors.append(device_state)

    def __str__(self):
        return json.dumps({
            "id": self.id,
            "master_device": str(self.master_device),
            "doors": self.doors
        })

    @staticmethod
    def from_json(apc_record_json: str):
        apc_record_dict = json.loads(apc_record_json)
        master_device_state = DeviceState.from_json(apc_record_dict["master_device"])
        return APC_Record(
            id=apc_record_dict["id"],
            master_device_state=master_device_state,
            doors=apc_record_dict["doors"]
        )