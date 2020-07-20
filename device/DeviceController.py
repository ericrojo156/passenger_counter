from network_layer.lan_stub import lan_send
from network_layer.external_network_stub import post_APC_Record
from device_cli import CUSTOM_CONFIG, PULL_DATA
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit
import json
from data_layer.APC_Record import APC_Record

class DeviceController:
    device_state = None
    config = None
    master_jobs = []
    scheduled_jobs = []
    scheduler = None
    def __init__(self, _device_state, _config):
        self.device_state = _device_state
        self.config = _config
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.manage_background_tasks()

    def handle_request(self, request_dict):
        succeeded = False
        response_dict = {}
        data = {}
        status = "ERROR"
        try:
            command = request_dict["command"]

            if (command == CUSTOM_CONFIG):
                data_dict = json.loads(request_dict["data"])
                succeeded = self.config.set_custom_configs(data_dict)
                self.manage_background_tasks()

            elif (command == PULL_DATA):
                data = {"device_label": self.config.get_device_label(), "device_state": str(self.device_state)}
                succeeded = len(data) > 0

            if (succeeded):
                status = "SUCCESS"
        except Exception as e:
            print(e)
            status = "ERROR"
        response_dict = {"status": status, "data": data}
        return response_dict

    def publish_data(self):
        if (self.config.is_master()):
            post_APC_Record(APC_Record(self.device_state))

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

    def manage_background_tasks(self):
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