#!/bin/sh
if [ -e raspicam.$1 ]; then
    mv raspicam.$1 takephoto.$1
fi
