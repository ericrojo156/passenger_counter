from DeviceConfig import DeviceConfig

class DeviceState:
    def __init__(self):
        self.count = 0
        self.config = DeviceConfig()
        self.gps_coords = {
            "lat": 0,
            "lng": 0
        }

    def incrementCount(self):
        self.count = self.count + 1

    def decrementCount(self):
        self.count = self.count - 1

    def update_gps_coords(self, lat, lng):
        self.gps_coords["lat"] = lat
        self.gps_coords["lng"] = lng