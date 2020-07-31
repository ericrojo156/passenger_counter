#! /bin/sh
pppd nodetach noauth defaultroute ipcp-accept-remote ipcp-accept-local debug usepeerdns crtscts lock 115200 /dev/ttyUSB2 connect "chat -v -E -t12 -f /home/ctodd/Devices/HAT/network/chat"
