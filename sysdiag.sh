#!/bin/sh
#
#Skeleton script for initial system diagnostics
echo "general system: vmstat 1 4"
vmstat 1 4
echo "==================="
echo "all cpu utilization: mpstat -P ALL 1 4"
mpstat -P ALL 1 4
echo "==================="
echo "disk utilization: iostat -dmx 1 4"
iostat -dmx 1 4
echo "==================="
echo "network devices and errors: sar -n DEV,EDEV 1 4"
sar -n DEV,EDEV 1 4
echo "==================="
echo "TCP and its errors: sar -n TCP,ETCP 1 4"
sar -n TCP,ETCP 1 4
echo "==================="

