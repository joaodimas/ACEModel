clear all
macro drop _all

import delimited "/Users/jdimas/GitHub/ACEModel/data/Chapter_8/1_replication/Panel/ACEModel.2017-04-19T13h30m51s[1][PANEL].csv"
xtset firm_id period
label define status 2 "INACTIVE" 3 "ACTIVE" 4 "DEAD"
label values status status
gen prob_res = attraction_res / (attraction_res + attraction_no_res)
gen prob_inn = attraction_inn / (attraction_inn + attraction_imi)

