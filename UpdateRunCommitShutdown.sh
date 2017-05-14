#!/bin/bash
# declare STRING variable
cd /home/jdimas/GitHub/ACEModel
git pull
./simulation.py
mkdir ./data/New_results
rm ./data/*.log
mv ./data/ACEModel.2017*MEAN* ./data/New_results/
mv ./data/ACEModel.2017*params* ./data/New_results/
rm ./data/ACEModel*
git add .
git commit -m "Results"
git push
sudo poweroff
