import requests
import argparse
cli_parser = argparse.ArgumentParser()
cli_parser.add_argument('--address', type=str)
cli_parser.add_argument("--command", type=str)
cli_parser.add_argument('--data', default=None, type=str)

CUSTOM_CONFIG = "custom_config"
PULL_DATA = "pull_data"

if __name__ == "__main__":
    cli_args = cli_parser.parse_args()
    address = cli_args.address
    command = cli_args.command
    data = cli_args.data

    status = requests.post(f"{address}/", json={"command": command, "data": data}).json()["status"]

    if (status == "ERROR"):
        print(f"command failure: address={address}, command={command}")