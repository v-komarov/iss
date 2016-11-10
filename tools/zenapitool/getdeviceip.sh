#!/bin/sh

#python zenapitool.py device-list -c ic -f table | awk '$2 ~/'Switch'/ {print $1}' >> device_list.txt

python zenapitool.py device-list -p "/Devices/Network" -c icCV -f table  -w device_list.txt
