clear all
macro drop _all

import delimited "/Users/jdimas/GitHub/ACEModel/data/NoFixedCosts_NoTechShocks_NoCycles/Time-series/ACEModel.2017-04-28T10h26m33s[1][TIMESERIES].csv"

tsset period

gen log_period = ln(period)
gen ratio_res = firmsres / firms
gen ratio_profitable_firms = profitablefirms / firms
gen share_cs = cs / ts
replace share_cs = 1 if share_cs > 1

twoway (line mktsize period) (line meanmktsize period) in 2921/3000, yscale(log)
