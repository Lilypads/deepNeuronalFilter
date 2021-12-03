#!/bin/bash

mkdir -p cppData
n=1;
max=8; //how many recording to run
while [ "$n" -le "$max" ]; do
  mkdir -p "cppData/recording$n"
  n=`expr "$n" + 1`;
done

echo "Successfully created the cpp folders"

cmake .
make
./run_ecg_filter

