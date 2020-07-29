python device_cli.py --address "http://localhost:3000" --command "set_config" --data '{"deviceAddress": "http://localhost:3000", "deviceLabel": "vehicle1", "isMaster": true, "otherDevicesOnLAN": ["http://localhost:3001", "http://localhost:3002", "http://localhost:3003", "http://localhost:3004"]}'
python device_cli.py --address "http://localhost:3001" --command "set_config" --data '{"deviceAddress": "http://localhost:3001", "deviceLabel": "slave1"}'
python device_cli.py --address "http://localhost:3002" --command "set_config" --data '{"deviceAddress": "http://localhost:3002", "deviceLabel": "slave2"}'
python device_cli.py --address "http://localhost:3003" --command "set_config" --data '{"deviceAddress": "http://localhost:3003", "deviceLabel": "slave3"}'
python device_cli.py --address "http://localhost:3004" --command "set_config" --data '{"deviceAddress": "http://localhost:3004", "deviceLabel": "slave4"}'

python device_cli.py --address "http://localhost:3005" --command "set_config" --data '{"deviceAddress": "http://localhost:3005", "deviceLabel": "vehicle2", "isMaster": true, "otherDevicesOnLAN": ["http://localhost:3006", "http://localhost:3007"]}'
python device_cli.py --address "http://localhost:3006" --command "set_config" --data '{"deviceAddress": "http://localhost:3006", "deviceLabel": "slave5"}'
python device_cli.py --address "http://localhost:3007" --command "set_config" --data '{"deviceAddress": "http://localhost:3007", "deviceLabel": "slave6"}'