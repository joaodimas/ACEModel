clear all
macro drop _all

import delimited "/Users/jdimas/GitHub/ACEModel/data/Chapter_8/1_replication/ACEModel.2017-04-22T18h28m34s[1][CROSSSECTIONAL][5000].csv"

label define status 2 "INACTIVE" 3 "ACTIVE" 4 "DEAD"
label values status status
gen revenues_growth = log(revenues) - log(previous_revenues)
by period, sort: egen avg_prox_opt_tech = mean(prox_opt_tech)
//histogram revenues_growth, bin(1000) frequency
count if status == 2
