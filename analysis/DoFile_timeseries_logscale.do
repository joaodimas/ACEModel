clear all
macro drop _all

global baseName = "ACEModel.2017-04-16T20h10m08s[MEAN][TIMESERIES]"
global folder = "Chapter_5/500_replications/Time series"
global firstPeriod = 1
global lastPeriod = 5000
global xAxisDelta = 1000
global xAxisBegin = $firstPeriod - 1
global xAxisEnd = $lastPeriod
global period = "in $firstPeriod/$lastPeriod"
global xAxisTitle = "Time"
global aspectRatio = 0.6


import delimited "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.csv"

tsset period

gen log_period = ln(period)
gen ratio_res = firmsres / firms
gen ratio_profitable_firms = profitablefirms / firms
gen share_cs = cs / ts
replace share_cs = 1 if share_cs > 1


// Generating graph for Aggregate output

tsline totoutput, xscale(log)

gr_edit .yaxis1.title.text = {"Aggregate output"}
gr_edit .xaxis1.title.text = {"$xAxisTitle"}
gr_edit .yaxis1.reset_rule 5, tickset(major) ruletype(suggest) 
gr_edit .xaxis1.reset_rule 4, tickset(major) ruletype(suggest)
gr_edit .xaxis1.edit_tick 2 5000 `""', custom tickset(major) editstyle(tickstyle(show_labels(no)) tickstyle(show_ticks(no)) )
gr_edit .xaxis1.add_ticks 1 `""', tickset(major)
gr_edit .xaxis1.add_ticks 10 `""', tickset(major)
gr_edit .xaxis1.add_ticks 100 `""', tickset(major)
gr_edit .xaxis1.add_ticks 1000 `""', tickset(major)
gr_edit .yaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy
gr_edit .plotregion1.style.editstyle margin(medium) editcopy
gr_edit .SetAspectRatio $aspectRatio

global suffixAggOutput = "Aggregate_output"
graph export "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixAggOutput.logscale.png", as(png) replace

// End



// Generating graph for Market Price

tsline price, xscale(log)

gr_edit .yaxis1.title.text = {"Market price"}
gr_edit .xaxis1.title.text = {"$xAxisTitle"}
gr_edit .yaxis1.reset_rule 7, tickset(major) ruletype(suggest) 
gr_edit .xaxis1.reset_rule 4, tickset(major) ruletype(suggest)
gr_edit .xaxis1.edit_tick 2 5000 `""', custom tickset(major) editstyle(tickstyle(show_labels(no)) tickstyle(show_ticks(no)) )
gr_edit .xaxis1.add_ticks 1 `""', tickset(major)
gr_edit .xaxis1.add_ticks 10 `""', tickset(major)
gr_edit .xaxis1.add_ticks 100 `""', tickset(major)
gr_edit .xaxis1.add_ticks 1000 `""', tickset(major)
gr_edit .yaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy
gr_edit .plotregion1.style.editstyle margin(medium) editcopy
gr_edit .SetAspectRatio $aspectRatio

global suffixMarketPrice = "Market_price"
graph export "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixMarketPrice.logscale.png", as(png) replace

// End

// Generating graph for Technological diversity

tsline div, xscale(log)

gr_edit .yaxis1.title.text = {"Technological diversity"}
gr_edit .xaxis1.title.text = {"$xAxisTitle"}
gr_edit .yaxis1.reset_rule 7, tickset(major) ruletype(suggest) 
gr_edit .xaxis1.reset_rule 4, tickset(major) ruletype(suggest)
gr_edit .xaxis1.edit_tick 2 5000 `""', custom tickset(major) editstyle(tickstyle(show_labels(no)) tickstyle(show_ticks(no)) )
gr_edit .xaxis1.add_ticks 1 `""', tickset(major)
gr_edit .xaxis1.add_ticks 10 `""', tickset(major)
gr_edit .xaxis1.add_ticks 100 `""', tickset(major)
gr_edit .xaxis1.add_ticks 1000 `""', tickset(major)
gr_edit .yaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy
gr_edit .plotregion1.style.editstyle margin(medium) editcopy
gr_edit .SetAspectRatio $aspectRatio

global suffixTechDiversity = "Technological_diversity"
graph export "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixTechDiversity.logscale.png", as(png) replace

// End


// Generating graph for No. firms

tsline firms, xscale(log)

gr_edit .yaxis1.title.text = {"No. firms"}
gr_edit .xaxis1.title.text = {"$xAxisTitle"}
gr_edit .xaxis1.reset_rule 4, tickset(major) ruletype(suggest)
gr_edit .yaxis1.reset_rule 4, tickset(major) ruletype(suggest) 
gr_edit .xaxis1.edit_tick 2 5000 `""', custom tickset(major) editstyle(tickstyle(show_labels(no)) tickstyle(show_ticks(no)) )
gr_edit .xaxis1.add_ticks 1 `""', tickset(major)
gr_edit .xaxis1.add_ticks 10 `""', tickset(major)
gr_edit .xaxis1.add_ticks 100 `""', tickset(major)
gr_edit .xaxis1.add_ticks 1000 `""', tickset(major)
gr_edit .yaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy
gr_edit .plotregion1.style.editstyle margin(medium) editcopy
gr_edit .SetAspectRatio $aspectRatio

global suffixFirms = "Firms"
graph export "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixFirms.logscale.png", as(png) replace

// End

// Generating graph for No. entrants

tsline entries, xscale(log)


gr_edit .yaxis1.title.text = {"No. entrants"}
gr_edit .xaxis1.title.text = {"$xAxisTitle"}
gr_edit .xaxis1.reset_rule 4, tickset(major) ruletype(suggest)
gr_edit .yaxis1.reset_rule 5, tickset(major) ruletype(suggest) 
gr_edit .xaxis1.edit_tick 2 5000 `""', custom tickset(major) editstyle(tickstyle(show_labels(no)) tickstyle(show_ticks(no)) )
gr_edit .xaxis1.add_ticks 1 `""', tickset(major)
gr_edit .xaxis1.add_ticks 10 `""', tickset(major)
gr_edit .xaxis1.add_ticks 100 `""', tickset(major)
gr_edit .xaxis1.add_ticks 1000 `""', tickset(major)
gr_edit .yaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy
gr_edit .plotregion1.style.editstyle margin(medium) editcopy
gr_edit .SetAspectRatio $aspectRatio

global suffixEntrants = "Entrants"
graph export "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixEntrants.logscale.png", as(png) replace

// End


// Generating graph for No. exits

tsline exits, xscale(log)


gr_edit .yaxis1.title.text = {"No. exits"}
gr_edit .xaxis1.title.text = {"$xAxisTitle"}
gr_edit .xaxis1.reset_rule 4, tickset(major) ruletype(suggest)
gr_edit .yaxis1.reset_rule 6, tickset(major) ruletype(suggest) 
gr_edit .xaxis1.edit_tick 2 5000 `""', custom tickset(major) editstyle(tickstyle(show_labels(no)) tickstyle(show_ticks(no)) )
gr_edit .xaxis1.add_ticks 1 `""', tickset(major)
gr_edit .xaxis1.add_ticks 10 `""', tickset(major)
gr_edit .xaxis1.add_ticks 100 `""', tickset(major)
gr_edit .xaxis1.add_ticks 1000 `""', tickset(major)
gr_edit .yaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy
gr_edit .plotregion1.style.editstyle margin(medium) editcopy
gr_edit .SetAspectRatio $aspectRatio

global suffixExits = "Exits"
graph export "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixExits.logscale.png", as(png) replace

// End


// Generating graph for Industry marginal cost

tsline wmc, xscale(log)

gr_edit .yaxis1.title.text = {"Industry marginal cost"}
gr_edit .xaxis1.title.text = {"$xAxisTitle"}
gr_edit .yaxis1.reset_rule 5, tickset(major) ruletype(suggest) 
gr_edit .xaxis1.reset_rule 4, tickset(major) ruletype(suggest)
gr_edit .xaxis1.edit_tick 2 5000 `""', custom tickset(major) editstyle(tickstyle(show_labels(no)) tickstyle(show_ticks(no)) )
gr_edit .xaxis1.add_ticks 1 `""', tickset(major)
gr_edit .xaxis1.add_ticks 10 `""', tickset(major)
gr_edit .xaxis1.add_ticks 100 `""', tickset(major)
gr_edit .xaxis1.add_ticks 1000 `""', tickset(major)
gr_edit .yaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy
gr_edit .plotregion1.style.editstyle margin(medium) editcopy
gr_edit .SetAspectRatio $aspectRatio

global suffixIndustryMarginalCost = "Industry_marginal_cost"
graph export "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixIndustryMarginalCost.logscale.png", as(png) replace

// End


// Generating graph for Industry price-cost margin

tsline pcm, xscale(log)

gr_edit .yaxis1.title.text = {"Industry price-cost margin"}
gr_edit .xaxis1.title.text = {"$xAxisTitle"}
gr_edit .yaxis1.reset_rule 7, tickset(major) ruletype(suggest) 
gr_edit .xaxis1.reset_rule 4, tickset(major) ruletype(suggest)
gr_edit .xaxis1.edit_tick 2 5000 `""', custom tickset(major) editstyle(tickstyle(show_labels(no)) tickstyle(show_ticks(no)) )
gr_edit .xaxis1.add_ticks 1 `""', tickset(major)
gr_edit .xaxis1.add_ticks 10 `""', tickset(major)
gr_edit .xaxis1.add_ticks 100 `""', tickset(major)
gr_edit .xaxis1.add_ticks 1000 `""', tickset(major)
gr_edit .yaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy
gr_edit .plotregion1.style.editstyle margin(medium) editcopy
gr_edit .SetAspectRatio $aspectRatio

global suffixIndustryPCM = "Industry_price_cost_margin"
graph export "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixIndustryPCM.logscale.png", as(png) replace

// End


// Generating graph for Gini coefficient

tsline gini, xscale(log)

gr_edit .yaxis1.title.text = {"Gini coefficient"}
gr_edit .xaxis1.title.text = {"$xAxisTitle"}
gr_edit .yaxis1.reset_rule 5, tickset(major) ruletype(suggest)
gr_edit .xaxis1.reset_rule 4, tickset(major) ruletype(suggest)
gr_edit .xaxis1.edit_tick 2 5000 `""', custom tickset(major) editstyle(tickstyle(show_labels(no)) tickstyle(show_ticks(no)) )
gr_edit .xaxis1.add_ticks 1 `""', tickset(major)
gr_edit .xaxis1.add_ticks 10 `""', tickset(major)
gr_edit .xaxis1.add_ticks 100 `""', tickset(major)
gr_edit .xaxis1.add_ticks 1000 `""', tickset(major) 
gr_edit .yaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy
gr_edit .plotregion1.style.editstyle margin(medium) editcopy
gr_edit .SetAspectRatio $aspectRatio

global suffixGini = "Gini"
graph export "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixGini.logscale.png", as(png) replace

// End


// Generating graph for HHI
tsline hindex, xscale(log)

gr_edit .yaxis1.title.text = {"Herfindahl–Hirschman Index"}
gr_edit .xaxis1.title.text = {"$xAxisTitle"}
gr_edit .xaxis1.edit_tick 2 2000 `""', custom tickset(major) editstyle(tickstyle(show_labels(no)) tickstyle(show_ticks(no)) )
gr_edit .xaxis1.edit_tick 2 3000 `""', custom tickset(major) editstyle(tickstyle(show_labels(no)) tickstyle(show_ticks(no)) )
gr_edit .xaxis1.edit_tick 2 4000 `""', custom tickset(major) editstyle(tickstyle(show_labels(no)) tickstyle(show_ticks(no)) )
gr_edit .xaxis1.edit_tick 2 5000 `""', custom tickset(major) editstyle(tickstyle(show_labels(no)) tickstyle(show_ticks(no)) )
gr_edit .xaxis1.add_ticks 1 `""', tickset(major)
gr_edit .xaxis1.add_ticks 10 `""', tickset(major)
gr_edit .xaxis1.add_ticks 100 `""', tickset(major)
gr_edit .xaxis1.add_ticks 1000 `""', tickset(major)
gr_edit .xaxis1.reset_rule 4, tickset(major) ruletype(suggest)
gr_edit .yaxis1.reset_rule 5, tickset(major) ruletype(suggest) 
gr_edit .yaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy
gr_edit .plotregion1.style.editstyle margin(medium) editcopy
gr_edit .SetAspectRatio $aspectRatio

global suffixHHI = "HHI"
graph export "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixHHI.logscale.png", as(png) replace

/// End


		 
