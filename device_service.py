from flask import Flask, request
from device.DeviceState import DeviceState
from config_api.DeviceConfig import DeviceConfig
from config_api.EndpointDeviceConfigIO import EndpointDeviceConfigIO
from device.DeviceController import DeviceController
import json
import argparse
app = Flask(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int)
parser.add_argument('--configDir', type=str, default=None)

controller = None

# stub endpoint for receiving generic messages from other devices on the LAN (if master device: send commands to slave devices; if slave device: recieve commands from the master device)
@app.route("/", methods=["POST"])
def index():
    request_json = request.json
    try:
        response_dict = controller.handle_request(request_json)
        return json.dumps(response_dict)
    except:
        return json.dumps({"status": "ERROR"})

if __name__ == "__main__":
    args = parser.parse_args()
    state = DeviceState()
    config = DeviceConfig(EndpointDeviceConfigIO(args.configDir))
    controller = DeviceController(state, config)
    controller.set_address(f"http://localhost:{args.port}")
    app.run(host="localhost", port=args.port)