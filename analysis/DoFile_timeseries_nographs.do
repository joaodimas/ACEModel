clear all
macro drop _all

import delimited "/Users/jdimas/GitHub/ACEModel/data/ACEModel.[LATEST][1][TIMESERIES].csv"

tsset period

gen log_period = ln(period)
gen ratio_res = firmsres / firms
gen ratio_profitable_firms = profitablefirms / firms
gen share_cs = cs / ts
replace share_cs = 1 if share_cs > 1
