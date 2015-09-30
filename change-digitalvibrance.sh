#!/bin/sh
#


change_settings(){

    DPY=`nvidia-settings -q dpys | grep connected | awk -F " " '{print $3}' | sed 's/[(|)]//g'`
    nvidia-settings -a :0.0/DigitalVibrance[${DPY}]=$1

}

case "$1" in
        help)
        echo "Usage: $0 [ < value between -1024 (nice greyscale) and 1023 (nice for counter strike > ]"
        ;;
        *)
        change_settings $1
RETVAL=$?
esac
exit 0
