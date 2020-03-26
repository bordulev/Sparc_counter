#!/bin/bash

if [ -r CSCConvertorTxtToRoot ]; then
  /bin/rm -rf CSCConvertorTxtToRoot
fi

if [ -r $1 ]; then
  echo $1 "will compile soon"
  g++ $1 `root-config --cflags` `root-config --libs --glibs` -o CSCConvertorTxtToRoot
  ##g++ -g -std=c++0x -I /usr/include/root $1 `root-config --libs --glibs` -o CSCConvertorTxtToRoot
  ls -ltF CSCConvertorTxtToRoot
else
  echo "any file for compilation is missing"
fi

if [ -r CSCConvertorTxtToRoot ]; then
  ./CSCConvertorTxtToRoot
else 
  echo "executable is missing"
fi
