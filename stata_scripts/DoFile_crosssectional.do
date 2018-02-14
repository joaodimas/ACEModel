clear all
macro drop _all

import delimited "/Users/jdimas/GitHub/ACEModel/data/NoFixedCosts/Cross-sectional/ACEModel.2017-04-28T10h26m33s[1][CROSSSECTIONAL][500].csv"

label define status 2 "INACTIVE" 3 "ACTIVE" 4 "DEAD"
label values status status
gen revenues_growth = log(revenues) - log(previous_revenues)
by period, sort: egen avg_prox_opt_tech = mean(prox_opt_tech)
tab status
gen prox_opt_tech2 = prox_opt_tech * 2
reg mkt_share attraction_res prox_opt_tech prox_opt_tech2

gen log_revenues = ln(revenues)
gen log_previous_revenues = ln(previous_revenues)
egen mean_log_revenues = mean(log_revenues)
egen mean_log_previous_revenues = mean(log_previous_revenues)
gen normalized_log_revenues = log_revenues - mean_log_revenues
gen normalized_log_previous_revenues = log_previous_revenues - mean_log_previous_revenues
gen normalized_revenues_growth = normalized_log_revenues - normalized_log_previous_revenues

histogram normalized_revenues_growth, density bin(10)
