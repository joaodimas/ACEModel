clear all
macro drop _all

import delimited "/Users/jdimas/GitHub/ACEModel/data/MeanMktSize32/ACEModel.2017-04-19T15h18m28s[1][CROSSSECTIONAL][5000].csv"
label define status 2 "INACTIVE" 3 "ACTIVE" 4 "DEAD"
label values status status
gen prob_res = attraction_res / (attraction_res + attraction_no_res)
gen prob_inn = attraction_inn / (attraction_inn + attraction_imi)

