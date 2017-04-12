rm ./data/*.log
mv ./data/ACEModel.2017*MEAN* ./data/Chapter\ 4/
rm ./data/ACEModel*
git add .
git commit -m “Results”
git pull

