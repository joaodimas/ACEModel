#!/bin/bash
# declare STRING variable
cd /home/jdimas/GitHub/ACEModel
git pull
./simulation.py
rm ./data/*.log
mv ./data/ACEModel.2017*MEAN* ./data/Chapter\ 4/
rm ./data/ACEModel*
git add .
git commit -m "Results"
git pull

