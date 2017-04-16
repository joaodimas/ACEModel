rm ./data/*.log
mv ./data/ACEModel.2017*MEAN* ./data/New_results
rm ./data/ACEModel*
git add .
git commit -m “Results”
git pull

