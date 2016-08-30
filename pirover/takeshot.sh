#!/bin/sh
if [ -e raspicam.$1 ]; then
    mv raspicam.$1 takeshot.$1
fi
