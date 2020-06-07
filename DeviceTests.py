from device.DeviceState import DeviceState
from device.DeviceConfig import DeviceConfig
from device.DividerLine import DividerLine
import json
import os

default_config_filepath = os.getcwd() + "/device/default_device_config.json"
custom_config_filepath = os.getcwd() + "/device/device_config.json"

def deviceStateTests():
    device = DeviceState()
    assert(device.gps_coords["lat"] == 0 and device.gps_coords["lng"] == 0)

    assert(device.count == 0)
    device.incCount()
    assert(device.count == 1)

    device.decCount()
    assert(device.count == 0)
    device.decCount()
    assert(device.count == 0)

    device.update_gps_coords("60.123456", "70.123456")
    assert(device.gps_coords["lat"] == "60.123456")
    assert(device.gps_coords["lng"] == "70.123456")

def deviceConfigTests_defaultConfig():
    if (os.path.isfile(custom_config_filepath)):
        os.remove(custom_config_filepath)
    config = DeviceConfig()
    assert(config.config_file_path == default_config_filepath)
    default_line = {
        "equation": {
            "a": 1,
            "b": 0,
            "order": 1
        },
        "onBoardingDirection": [1, 1]
    }
    assert(config.gps_is_enabled() == True)
    assert(config.divider_line().slope == default_line["equation"]["a"])
    assert(config.divider_line().intercept == default_line["equation"]["b"])
    assert(config.divider_line().order == default_line["equation"]["order"])
    assert(config.divider_line().onboarding_direction_vector == default_line["onBoardingDirection"])
    assert(config.is_master() == True)
    assert(len(config.other_LAN_devices()) == 0)
    assert(config.is_master())

def deviceConfigTests_customConfig():
    config = DeviceConfig()
    line = {
        "equation": {
            "a": 3,
            "b": 5,
            "order": 1
        },
        "onBoardingDirection": [2, 4]
    }
    serialized_line = json.dumps(line)
    divider_line = DividerLine(serialized_line)
    config.set_divider_line(divider_line)
    config.set_is_master(False)
    assert(config.divider_line().slope == line["equation"]["a"])
    assert(config.divider_line().intercept == line["equation"]["b"])
    assert(config.divider_line().order == line["equation"]["order"])
    assert(config.divider_line().onboarding_direction_vector == line["onBoardingDirection"])
    assert(not config.is_master())

    nextSession = DeviceConfig()
    assert(nextSession.config_file_path == custom_config_filepath)
    assert(nextSession.divider_line().slope == line["equation"]["a"])
    assert(nextSession.divider_line().intercept == line["equation"]["b"])
    assert(nextSession.divider_line().order == line["equation"]["order"])
    assert(nextSession.divider_line().onboarding_direction_vector == line["onBoardingDirection"])
    assert(not config.is_master())

    nextSession.revert_to_default()
    default_line = {
        "equation": {
            "a": 1,
            "b": 0,
            "order": 1
        },
        "onBoardingDirection": [1, 1]
    }
    assert(nextSession.divider_line().slope == default_line["equation"]["a"])
    assert(nextSession.divider_line().intercept == default_line["equation"]["b"])
    assert(nextSession.divider_line().order == default_line["equation"]["order"])
    assert(nextSession.divider_line().onboarding_direction_vector == default_line["onBoardingDirection"])
    assert(nextSession.is_master())

    freshConfig = DeviceConfig()
    assert(freshConfig.config_file_path == default_config_filepath)
    assert(not os.path.isfile(custom_config_filepath))
    assert(freshConfig.gps_is_enabled() == True)
    assert(freshConfig.divider_line().slope == default_line["equation"]["a"])
    assert(freshConfig.divider_line().intercept == default_line["equation"]["b"])
    assert(freshConfig.divider_line().order == default_line["equation"]["order"])
    assert(freshConfig.divider_line().onboarding_direction_vector == default_line["onBoardingDirection"])
    assert(freshConfig.is_master() == True)
    assert(len(config.other_LAN_devices()) == 0)
    assert(freshConfig.is_master())

if __name__ == "__main__":
    deviceStateTests()
    deviceConfigTests_defaultConfig()
    deviceConfigTests_customConfig()
