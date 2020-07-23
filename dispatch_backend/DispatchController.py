from dispatch_backend.TransitVehicleLAN import TransitVehicleLAN
import json
import typing
from config_api.DispatchDeviceConfigIO import DispatchDeviceConfigIO
from config_api.DeviceConfig import DeviceConfig
from data_layer.APC_Record import APC_Record

class DispatchController:
    dispatch_vehicles = {}
    def __init__(self):
        self.dispatch_vehicles = {}

    def set_lan_configs(self, data):
        config_json_list = json.loads(data["config_json_list"])
        master_device_address = data["master_device_address"]
        for config_json in config_json_list:
            device_address = config["address"]
            config_io = DispatchDeviceConfigIO(_device_address=device_address, _master_device_address=master_device_address)
            config_io.save_config_json(config_json)
            if (config_io.error_state):
                return {"status": "ERROR", "device": device_address}
        return {"status": "SUCCESS"}

    def get_lan_configs(self, data):
        master_device_address = data["master_device_address"]
        config_json_list = []
        response_dict = {"status": "ERROR"}
        try:
            master_config = DeviceConfig(DispatchDeviceConfigIO(_master_device_address=master_device_address))
            device_addresses = master_config.other_LAN_devices()
            for device_address in device_addresses:
                config_io = DispatchDeviceConfigIO(_device_address=device_address, _master_device_address=master_device_address)
                config_json = config_io.load_config_json()
                config_json_list.append(config_json)
            response_dict["status"] = "SUCCESS"
        except:
            print(e)
        response_dict["config_json_list"] = config_json_list
        return response_dict

    def push_apc_record(self, data):
        response_dict = {"status": "ERROR"}
        master_device_address = data["master_device_address"]
        try:
            apc_record = APC_Record.from_json(data["apc_record"])
            try:
                self.dispatch_vehicles[apc_record.id].records.append(apc_record)
                response_dict["status"] = "SUCCESS"
            except KeyError as e:
                # id record doesn't match any dispatch vehicle currently registered, so register it by creating a new list of APC records for that id (with the current APC record in it)
                records = [apc_record]
                master_config = DeviceConfig(DispatchDeviceConfigIO(_master_device_address=master_device_address))
                vehicle = TransitVehicleLAN(
                    id = apc_record.id,
                    master_device_address = master_device_address,
                    master_config = master_config,
                    records = records
                )
                self.dispatch_vehicles[apc_record.id] = vehicle
                response_dict["status"] = "SUCCESS"
            #print([[str(r) for r in self.dispatch_vehicles[key].records] for key in self.dispatch_vehicles.keys()])
        except Exception as e:
            print(e)
        return response_dict

    def get_latest_apc_records(self):
        response_dict = {"status": "ERROR"}
        data = {}
        try:
            dispatch_vehicles = self.dispatch_vehicles
            for id in dispatch_vehicles:
                data[id] = dispatch_vehicles[id].to_dict()
                response_dict["status"] = "SUCCESS"
        except KeyError as e:
            response_dict = {"status": "ERROR"}
        response_dict["data"] = data
        return response_dict