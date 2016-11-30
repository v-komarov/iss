#!/bin/sh

#python zenapitool.py device-list -c ic -f table | awk '$2 ~/'Switch'/ {print $1}' >> device_list.txt

#python zenapitool.py device-list -p "/Devices/Network" -c icCV -f table  -w device_list.txt

#python zenapitool.py device-list -p "/Groups/Node 10" -c icCV -f table  -w device_list_node10.txt

#python zenapitool.py device-list -p "/Groups/Node 08/Segment 030" -c icCV -f table  -w device_list_node8_segment_30.txt

python zenapitool.py device-list -p "/Groups/Node 08/Segment 033" -c icCV -f table  -w device_list_node8_segment_33.txt

