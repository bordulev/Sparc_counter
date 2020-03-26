#!/bin/bash

DATE=`date +%d%m%y`

cd /afs/cern.ch/user/i/ibordule/prod/Sparkcounter/Spark_analyser

time ./launch.sh #> output/out.$DATE.log 2>&1 &

cd /afs/cern.ch/user/i/ibordule/prod/Sparkcounter/CSC_database_txt_to_root

./CSCConvertorTxtToRoot

