#!/bin/sh
#

#little script for changing digital vibrance for nvidia GPU on linux
# 

# To create awesome greyscale like
#./change-digitalvibrance.sh -1024


# To play csgo 
#./change-digitalvibrance.sh 1023
DPY=`nvidia-settings -q dpys | grep enabled | awk -F " " '{print $3}' | sed 's/[(|)]//g'`
nvidia-settings -a :0.0/DigitalVibrance[${DPY}]=$1

