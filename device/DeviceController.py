from network_layer.lan_stub import lan_send
from network_layer.external_network_stub import post_APC_Record
from device_cli import *
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from config_api.DeviceConfig import DeviceConfig
from config_api.EndpointDeviceConfigIO import EndpointDeviceConfigIO
import atexit
import json
from device.DeviceState import DeviceState
from data_layer.APC_Record import APC_Record

class DeviceController:
    device_state = None
    config: DeviceConfig = None
    master_jobs = []
    scheduled_jobs = []
    scheduler = None
    def __init__(self, _device_state: DeviceState, _config=DeviceConfig(EndpointDeviceConfigIO())):
        self.device_state = _device_state
        self.config = _config
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.manage_master_daemons()

    def handle_request(self, request_dict):
        succeeded = False
        response_dict = {}
        data = {}
        status = "ERROR"
        try:
            command = request_dict["command"]

            if (command == SET_CONFIG):
                config_dict = json.loads(request_dict["config_json"])
                succeeded = self.config.set_custom_configs(config_dict)
                # must refresh the background task management for this device, for the scenario that it has changed status as master or not (only master devices should be performing the background task)
                self.manage_master_daemons()

            elif (command == PULL_DATA):
                data = {"device_label": self.config.get_device_label(), "device_state": str(self.device_state)}
                succeeded = len(data) > 0

            elif (command == GET_CONFIG):
                this_address = self.config.get_address()
                device_address = request_dict["device_address"]
                if (this_address == device_address):
                    config_json = self.config.load_config_json(request_dict["from_default_source"])
                    succeeded = len(config_json) > 0
                    data = config_json
                else: # get config froconfig_dictce (not master) on the same LAN
                    master_device_address = request_dict["master_device_address"]
                    response_dict = lan_send(fromAddress=master_device_address, toAddress=device_address, command=GET_CONFIG, data={})
            if (succeeded):
                status = "SUCCESS"

        except Exception as e:
            print(e)
            status = "ERROR"
        response_dict = {"status": status, "data": data}
        return response_dict

    def publish_data(self):
        if (self.config.is_master()):
            id = self.config.get_id()
            post_APC_Record(master_device_address=self.config.get_address(), apc_record=APC_Record(id, self.device_state))

    def pull_and_publish_data(self):
        others_on_lan = self.config.other_LAN_devices()
        devices_state_list = []
        for toAddress in others_on_lan:
            thisAddress = self.config.get_address()
            response_dict = lan_send(fromAddress=thisAddress, toAddress=toAddress, command=PULL_DATA)
            if (response_dict["status"] == "SUCCESS"):
                devices_state_list.append(response_dict["data"])
        self.device_state.collect_devices_states(devices_state_list)
        self.publish_data()

    def manage_master_daemons(self):
        if ((len(self.master_jobs) == 0) and self.config.is_master()):
            # set scheduled jobs for master device
            slave_data_collection = self.scheduler.add_job(
                func = self.pull_and_publish_data,
                trigger = IntervalTrigger(seconds=2),
                id = 'Slave_Data_Pull',
                name = 'Slave_Data_Pull',
                replace_existing = True)
            self.master_jobs.append(slave_data_collection)

            # register cron job cleanup to atexit
            atexit.register(self.cleanup_master_jobs)
        elif((len(self.master_jobs) > 0) and not self.config.is_master()):
            self.cleanup_master_jobs

    def cleanup_master_jobs(self):
        for job in self.master_jobs:
                self.scheduled_jobs.remove(job)

    def set_address(self, address):
        self.config.set_address(address)