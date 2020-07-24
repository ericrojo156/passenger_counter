echo "#!/bin/bash" > kill_script.sh

(python dispatch_service.py --port 4000)& echo "dispatch service running on localhost:4000, pid=${!}"
echo "kill -9 ${!}" >> kill_script.sh

(python device_service.py --port 3000 --configDir "simulated_network/device1")& echo "device running on localhost:3000, pid=${!}"
echo "kill -9 ${!}" >> kill_script.sh

(python device_service.py --port 3001 --configDir "simulated_network/device2")& echo "device running on localhost:3001, pid=${!}"
echo "kill -9 ${!}" >> kill_script.sh

(python device_service.py --port 3002 --configDir "simulated_network/device3")& echo "device running on localhost:3002, pid=${!}"
echo "kill -9 ${!}" >> kill_script.sh

(python device_service.py --port 3003 --configDir "simulated_network/device4")& echo "device running on localhost:3003, pid=${!}"
echo "kill -9 ${!}" >> kill_script.sh

(python device_service.py --port 3004 --configDir "simulated_network/device5")& echo "device running on localhost:3004, pid=${!}"
echo "kill -9 ${!}" >> kill_script.sh

(python device_service.py --port 3005 --configDir "simulated_network/device6")& echo "device running on localhost:3005, pid=${!}"
echo "kill -9 ${!}" >> kill_script.sh

(python device_service.py --port 3006 --configDir "simulated_network/device7")& echo "device running on localhost:3006, pid=${!}"
echo "kill -9 ${!}" >> kill_script.sh

(python device_service.py --port 3007 --configDir "simulated_network/device8")& echo "device running on localhost:3007, pid=${!}"
echo "kill -9 ${!}" >> kill_script.sh

echo "rm simulated_network/device1/device_config.json" >> kill_script.sh
echo "rm simulated_network/device2/device_config.json" >> kill_script.sh
echo "rm simulated_network/device3/device_config.json" >> kill_script.sh
echo "rm simulated_network/device4/device_config.json" >> kill_script.sh
echo "rm simulated_network/device5/device_config.json" >> kill_script.sh

echo "rm simulated_network/device6/device_config.json" >> kill_script.sh
echo "rm simulated_network/device7/device_config.json" >> kill_script.sh
echo "rm simulated_network/device8/device_config.json" >> kill_script.sh
