#!/bin/bash

DATE=`date +%d%m%y`

cd /data/software/python3/baranov/sparkcounter

time ./launch.sh > output/out.$DATE.log 2>&1 &



