#!/bin/sh
cd /home/pi/pirover
sh raspicam.sh
python pirover.py >> /tmp/pirover.log
