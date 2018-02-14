clear all
macro drop _all

import delimited "/Users/jdimas/GitHub/ACEModel/data/Chapter_4_Shocks_NoCycles/500_replications/Time series/ACEModel.2017-05-14T16h25m52s[MEAN][TIMESERIES].csv"

tsset period

gen log_period = ln(period)
gen ratio_res = firmsres / firms
gen ratio_profitable_firms = profitablefirms / firms
gen share_cs = cs / ts
replace share_cs = 1 if share_cs > 1

tsline entries exits avgmagtechshock firms actfirms in 4951/5000
