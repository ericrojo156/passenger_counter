import json
import argparse
from flask import Flask, request
app = Flask(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int)

@app.route("/", methods=["POST"])
def index():
    request_json = request.json
    try:
        print("Dispatch received APC Record:")
        print(request_json)
        return json.dumps({"status": "SUCCESS"})
    except:
        return json.dumps({"status": "ERROR"})

if __name__ == "__main__":
    args = parser.parse_args()
    app.run(host="localhost", port=args.port)