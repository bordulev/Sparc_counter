#!/bin/bash

unset PYTHONPATH
unset PYTHONHOME

DATE=`date +%d%m%y`

#Should not be commented date '+%m' > cfg_month
#Should not be commented date '+%d' > cfg_day_start

#for chamber in AL01 AL03 AL05 AL07 AL09 AL11 AL13 AL15 AS02 AS04 AS06 AS08 AS10 AS12 AS14 AS16 CL01 CL03 CL05 CL07 CL09 CL11 CL13 CL15 CS02 CS04 CS06 CS08 CS10 CS12 CS14 CS16
for chamber in AL01 #Should be commented
do
  echo $chamber > cfg_chamber
  for layer in L1 L2 L3 L4
  do
    echo $chamber
    echo $layer
    echo $layer > cfg_layer
    /usr/bin/python3 launch_cmd.py
    /bin/rm -f cfg_layer
  done
  /bin/rm -f rm cfg_chamber
done
#/bin/rm -f cfg_day_start
#Should not be commented /bin/rm -f cfg_day_stop
#Should not be commented /bin/rm -f cfg_month

date > when_last_launch_was_done

exit 0

