#!/bin/bash

DATE=`date +%d%m%y`

cd /afs/cern.ch/user/i/ibordule/prod/Sparkcounter

time ./launch.sh > output/out.$DATE.log 2>&1 &



