import json
import argparse
from dispatch_backend.DispatchController import DispatchController
from flask import Flask, request
app = Flask(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int)

dispatch_controller = None

@app.route("/", methods=["POST"])
def index():
    request_json = request.json
    try:
        print("Dispatch received APC Record:")
        print(request_json)
        response_dict = dispatch_controller.handle_request(request_json)
        response_dict = {}
        return json.dumps(response_dict)
    except:
        return json.dumps({"status": "ERROR"})

if __name__ == "__main__":
    dispatch_controller = DispatchController()
    args = parser.parse_args()
    app.run(host="localhost", port=args.port)