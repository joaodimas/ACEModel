clear all
macro drop _all

import delimited "/Users/jdimas/GitHub/ACEModel/data/ConstantGrowthRate/ACEModel.2017-05-04T15h12m50s[1][PANEL].csv"
xtset firm_id period
label define status 2 "INACTIVE" 3 "ACTIVE" 4 "DEAD"
label values status status

/// Probabilities of R&D
gen prob_res = attraction_res / (attraction_res + attraction_no_res)
gen prob_inn = attraction_inn / (attraction_inn + attraction_imi)

/// Proximity to optimal technology
gen optimal_tasks = prox_opt_tech * 96
by period, sort: egen mean_optimal_tasks = mean(optimal_tasks)

/// Growth
gen log_revenues = ln(revenues)
gen log_previous_revenues = ln(previous_revenues)
by period, sort: egen mean_log_revenues = mean(log_revenues)
by period, sort: egen mean_log_previous_revenues = mean(log_previous_revenues)
gen normalized_log_revenues = log_revenues - mean_log_revenues
gen normalized_log_previous_revenues = log_previous_revenues - mean_log_previous_revenues
gen normalized_revenues_growth = normalized_log_revenues - normalized_log_previous_revenues
