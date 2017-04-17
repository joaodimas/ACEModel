clear all
macro drop _all

import delimited "/Users/jdimas/GitHub/ACEModel/data/ACEModel.LATEST[1][CROSSSECTIONAL][5000]"
label define status 2 "INACTIVE" 3 "ACTIVE" 4 "DEAD"
label values status status
