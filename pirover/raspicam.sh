#!/bin/sh
if [ $$ != `pgrep -fo $0`  ]; then
    echo `basename $0` is already running.
    exit 1
fi
while true
do
    /usr/bin/raspistill -t 150 -ex auto -awb auto -o raspicam.tmp -vf -hf -w 320 -h 240
    mv raspicam.tmp raspicam.jpg
    sleep 0.5
done
