clear all
macro drop _all

import delimited "/Users/jdimas/GitHub/ACEModel/data/ACEModel.LATEST[1][CROSSSECTIONAL][50].csv"
label define status 1 "POTENTIAL_ENTRANT" 3 "ACTIVE_INCUMBENT" 4 "DEAD"
label values status status
