import json
from device.DeviceState import DeviceState

class APC_Record:
    def __init__(self, id: str, master_device_state=None):
        self.id = id
        self.doors = []
        if (master_device_state == None):
            self.master_device = DeviceState()
        else:
            self.master_device = master_device_state
            print("APC Record devices state list:")
            for device_state in master_device_state.devices_state_list:
                self.doors.append(device_state)

    def __str__(self):
        return json.dumps({
            "id": id,
            "master_device": str(self.master_device),
            "doors": self.doors
        })