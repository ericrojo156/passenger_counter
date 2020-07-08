import json
class DeviceState:
    def __init__(self):
        self.count = 0
        self.gps_coords = {
            "lat": 0,
            "lng": 0
        }
        self.devices_state_list = []

    def incCount(self):
        self.count = self.count + 1

    def decCount(self):
        if (self.count > 0):
            self.count = self.count - 1

    def update_gps_coords(self, lat, lng):
        self.gps_coords["lat"] = lat
        self.gps_coords["lng"] = lng

    def collect_devices_states(self, devices_state_list):
        self.devices_state_list = []
        for slave_state in devices_state_list:
            self.devices_state_list.append(slave_state)

    def __str__(self):
        return json.dumps({
            "passenger_count": self.count,
            "gps_coords": self.gps_coords
        })