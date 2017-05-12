clear all
macro drop _all

global baseName = "ACEModel.2017-04-28T10h26m33s[1][TIMESERIES]"
global folder = "NoFixedCosts/Time-series"
global firstPeriod = 1
global lastPeriod = 500
global xAxisDelta = 100
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

set graphics off


// Generating graph for Aggregate output

tsline totoutput $period

gr_edit .yaxis1.title.text = {"Aggregate output"}
gr_edit .xaxis1.title.text = {"$xAxisTitle"}
gr_edit .yaxis1.reset_rule 7, tickset(major) ruletype(suggest) 
gr_edit .yaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .xaxis1.reset_rule $xAxisBegin $xAxisEnd $xAxisDelta , tickset(major) ruletype(range) 
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy
gr_edit .plotregion1.style.editstyle margin(medium) editcopy
gr_edit .SetAspectRatio $aspectRatio

global suffixAggOutput = "Aggregate_output"
graph save Graph "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixAggOutput.gph", replace

// End


// Generating graph for Aggregate Profits

tsline totprofits $period

gr_edit .yaxis1.title.text = {"Aggregate profits"}
gr_edit .xaxis1.title.text = {"$xAxisTitle"}
gr_edit .yaxis1.reset_rule 7, tickset(major) ruletype(suggest) 
gr_edit .yaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .xaxis1.reset_rule $xAxisBegin $xAxisEnd $xAxisDelta , tickset(major) ruletype(range) 
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy
gr_edit .plotregion1.style.editstyle margin(medium) editcopy
gr_edit .SetAspectRatio $aspectRatio

global suffixAggProfits = "Aggregate_profits"
graph save Graph "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixAggProfits.gph", replace

// End


// Generating graph for Market Price

tsline price $period

gr_edit .yaxis1.title.text = {"Market price"}
gr_edit .xaxis1.title.text = {"$xAxisTitle"}
gr_edit .yaxis1.reset_rule 7, tickset(major) ruletype(suggest) 
gr_edit .yaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .xaxis1.reset_rule $xAxisBegin $xAxisEnd $xAxisDelta , tickset(major) ruletype(range) 
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy
gr_edit .plotregion1.style.editstyle margin(medium) editcopy
gr_edit .SetAspectRatio $aspectRatio

global suffixMarketPrice = "Market_price"
graph save Graph "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixMarketPrice.gph", replace

// End

// Generating graph for Technological diversity

tsline div $period

gr_edit .yaxis1.title.text = {"Technological diversity"}
gr_edit .xaxis1.title.text = {"$xAxisTitle"}
gr_edit .yaxis1.reset_rule 7, tickset(major) ruletype(suggest) 
gr_edit .yaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .xaxis1.reset_rule $xAxisBegin $xAxisEnd $xAxisDelta , tickset(major) ruletype(range) 
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy
gr_edit .plotregion1.style.editstyle margin(medium) editcopy
gr_edit .SetAspectRatio $aspectRatio

global suffixTechDiversity = "Technological_diversity"
graph save Graph "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixTechDiversity.gph", replace

// End


// Generating graph for No. firms

tsline firms $period

gr_edit .yaxis1.title.text = {"No. firms"}
gr_edit .xaxis1.title.text = {"$xAxisTitle"}
gr_edit .yaxis1.reset_rule 5, tickset(major) ruletype(suggest) 
gr_edit .yaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .xaxis1.reset_rule $xAxisBegin $xAxisEnd $xAxisDelta , tickset(major) ruletype(range) 
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy
gr_edit .plotregion1.style.editstyle margin(medium) editcopy
gr_edit .SetAspectRatio $aspectRatio

global suffixFirms = "Firms"
graph save Graph "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixFirms.gph", replace

// End


// Generating graph for Industry marginal cost

tsline wmc $period

gr_edit .yaxis1.title.text = {"Industry marginal cost"}
gr_edit .xaxis1.title.text = {"$xAxisTitle"}
gr_edit .yaxis1.reset_rule 5, tickset(major) ruletype(suggest) 
gr_edit .yaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .xaxis1.reset_rule $xAxisBegin $xAxisEnd $xAxisDelta , tickset(major) ruletype(range) 
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy
gr_edit .plotregion1.style.editstyle margin(medium) editcopy
gr_edit .SetAspectRatio $aspectRatio

global suffixIndustryMarginalCost = "Industry_marginal_cost"
graph save Graph "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixIndustryMarginalCost.gph", replace

// End


// Generating graph for Industry price-cost margin

tsline pcm $period

gr_edit .yaxis1.title.text = {"Industry price-cost margin"}
gr_edit .xaxis1.title.text = {"$xAxisTitle"}
gr_edit .yaxis1.reset_rule 7, tickset(major) ruletype(suggest) 
gr_edit .yaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .xaxis1.reset_rule $xAxisBegin $xAxisEnd $xAxisDelta , tickset(major) ruletype(range) 
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy
gr_edit .plotregion1.style.editstyle margin(medium) editcopy
gr_edit .SetAspectRatio $aspectRatio

global suffixIndustryPCM = "Industry_price_cost_margin"
graph save Graph "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixIndustryPCM.gph", replace

// End


// Generating graph for Gini coefficient

tsline gini $period

gr_edit .yaxis1.title.text = {"Gini coefficient"}
gr_edit .xaxis1.title.text = {"$xAxisTitle"}
gr_edit .yaxis1.reset_rule 5, tickset(major) ruletype(suggest) 
gr_edit .yaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .xaxis1.reset_rule $xAxisBegin $xAxisEnd $xAxisDelta , tickset(major) ruletype(range) 
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy
gr_edit .plotregion1.style.editstyle margin(medium) editcopy
gr_edit .SetAspectRatio $aspectRatio

global suffixGini = "Gini"
graph save Graph "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixGini.gph", replace

// End


// Generating graph for Avg. prox. to optimal technology

tsline avgproxopt $period

gr_edit .yaxis1.title.text = {"Avg. proximity to optimal tech."}
gr_edit .xaxis1.title.text = {"$xAxisTitle"}
gr_edit .yaxis1.reset_rule 5, tickset(major) ruletype(suggest) 
gr_edit .yaxis1.title.style.editstyle size(large) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .xaxis1.reset_rule $xAxisBegin $xAxisEnd $xAxisDelta , tickset(major) ruletype(range) 
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy
gr_edit .plotregion1.style.editstyle margin(medium) editcopy
gr_edit .SetAspectRatio $aspectRatio

global suffixAvgProxOptTech = "Avg_prox_opt_tech"
graph save Graph "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixAvgProxOptTech.gph", replace

// End


// Generating graph for Consumer surplus

tsline cs $period

gr_edit .yaxis1.title.text = {"Consumer surplus"}
gr_edit .xaxis1.title.text = {"$xAxisTitle"}
gr_edit .yaxis1.reset_rule 6, tickset(major) ruletype(suggest) 
gr_edit .yaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .xaxis1.reset_rule $xAxisBegin $xAxisEnd $xAxisDelta , tickset(major) ruletype(range) 
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy
gr_edit .plotregion1.style.editstyle margin(medium) editcopy
gr_edit .SetAspectRatio $aspectRatio

global suffixConsumerSurplus = "Consumer_surplus"
graph save Graph "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixConsumerSurplus.gph", replace

// End


// Generating graph for Share of consumer surplus

tsline share_cs $period

gr_edit .yaxis1.title.text = {"Consumers' share of total surplus"}
gr_edit .xaxis1.title.text = {"$xAxisTitle"}
gr_edit .yaxis1.reset_rule 6, tickset(major) ruletype(suggest) 
gr_edit .yaxis1.title.style.editstyle size(large) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .xaxis1.reset_rule $xAxisBegin $xAxisEnd $xAxisDelta , tickset(major) ruletype(range) 
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy
gr_edit .plotregion1.style.editstyle margin(medium) editcopy
gr_edit .SetAspectRatio $aspectRatio

global suffixShareCS = "Share_consumer_surplus"
graph save Graph "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixShareCS.gph", replace

// End

// Generating graph for Ratio of firms doing research

tsline ratio_res $period

gr_edit .yaxis1.title.text = {"% of firms investing in R&D"}
gr_edit .xaxis1.title.text = {"$xAxisTitle"}
gr_edit .yaxis1.reset_rule 6, tickset(major) ruletype(suggest) 
gr_edit .yaxis1.title.style.editstyle size(large) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .xaxis1.reset_rule $xAxisBegin $xAxisEnd $xAxisDelta , tickset(major) ruletype(range) 
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy
gr_edit .plotregion1.style.editstyle margin(medium) editcopy
gr_edit .SetAspectRatio $aspectRatio

global suffixRatioRes = "Ratio_of_firms_inv_RnD"
graph save Graph "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixRatioRes.gph", replace

// End


// Generating graph for Cost share of innovation

tsline costshareinn $period

gr_edit .yaxis1.title.text = {"% invested in innovation"}
gr_edit .xaxis1.title.text = {"$xAxisTitle"}
gr_edit .yaxis1.reset_rule 6, tickset(major) ruletype(suggest) 
gr_edit .yaxis1.title.style.editstyle size(large) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .xaxis1.reset_rule $xAxisBegin $xAxisEnd $xAxisDelta , tickset(major) ruletype(range) 
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy
gr_edit .plotregion1.style.editstyle margin(medium) editcopy
gr_edit .SetAspectRatio $aspectRatio

global suffixCostShareInnovation = "Cost_share_innovation"
graph save Graph "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixCostShareInnovation.gph", replace

// End


// Generating graph for Ratio of firms that realized profits

tsline ratio_profitable_firms $period

gr_edit .yaxis1.title.text = {"% of firms realizing profits"}
gr_edit .xaxis1.title.text = {"$xAxisTitle"}
gr_edit .yaxis1.reset_rule 6, tickset(major) ruletype(suggest) 
gr_edit .yaxis1.title.style.editstyle size(large) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .xaxis1.reset_rule $xAxisBegin $xAxisEnd $xAxisDelta , tickset(major) ruletype(range) 
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy
gr_edit .plotregion1.style.editstyle margin(medium) editcopy
gr_edit .SetAspectRatio $aspectRatio

global suffixRatioProfitable = "Ratio_of_firms_profitable"
graph save Graph "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixRatioProfitable.gph", replace

// End


// Generating graph for Age
tsline avgage maxage minage $period

gr_edit .yaxis1.title.text = {"Age"}
gr_edit .xaxis1.title.text = {"$xAxisTitle"}
gr_edit .legend.plotregion1.label[1].text = {"Avg. age"}
gr_edit .legend.plotregion1.key[1].view.style.editstyle line(color(ebblue)) editcopy
gr_edit .legend.plotregion1.label[2].text = {"Max. age"}
gr_edit .legend.plotregion1.key[2].view.style.editstyle line(color(forest_green)) editcopy
gr_edit .legend.plotregion1.label[3].text = {"Min. age"}
gr_edit .legend.plotregion1.key[3].view.style.editstyle line(color(maroon)) editcopy
gr_edit .yaxis1.reset_rule 10, tickset(major) ruletype(suggest) 
gr_edit .yaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .xaxis1.reset_rule $xAxisBegin $xAxisEnd $xAxisDelta , tickset(major) ruletype(range) 
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy
gr_edit .plotregion1.style.editstyle margin(medium) editcopy
gr_edit .SetAspectRatio $aspectRatio

global suffixAge = "Age"
graph save Graph "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixAge.gph", replace

// End


// Generating graph for HHI
tsline hindex $period

gr_edit .yaxis1.title.text = {"Herfindahl–Hirschman Index"}
gr_edit .xaxis1.title.text = {"$xAxisTitle"}
gr_edit .yaxis1.reset_rule 5, tickset(major) ruletype(suggest) 
gr_edit .yaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .xaxis1.reset_rule $xAxisBegin $xAxisEnd $xAxisDelta , tickset(major) ruletype(range) 
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy
gr_edit .plotregion1.style.editstyle margin(medium) editcopy
gr_edit .SetAspectRatio $aspectRatio

global suffixHHI = "HHI"
graph save Graph "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixHHI.gph", replace

// End

tsline firmsres firmsinn firmsimi firms $period

gr_edit .yaxis1.title.text = {"No. firms"}
gr_edit .xaxis1.title.text = {"$xAxisTitle"}
gr_edit .legend.plotregion1.label[1].text = {"Any R&D"}
gr_edit .legend.plotregion1.key[1].view.style.editstyle line(color(ebblue)) editcopy
gr_edit .legend.plotregion1.label[2].text = {"Innovation"}
gr_edit .legend.plotregion1.key[2].view.style.editstyle line(color(forest_green)) editcopy
gr_edit .legend.plotregion1.label[3].text = {"Imitation"}
gr_edit .legend.plotregion1.key[3].view.style.editstyle line(color(maroon)) editcopy
gr_edit .legend.plotregion1.label[4].text = {"All firms"}
gr_edit .yaxis1.reset_rule 8, tickset(major) ruletype(suggest) 
gr_edit .yaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .xaxis1.reset_rule $xAxisBegin $xAxisEnd $xAxisDelta , tickset(major) ruletype(range) 
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy
gr_edit .plotregion1.style.editstyle margin(medium) editcopy
gr_edit .SetAspectRatio $aspectRatio

global suffixRD_Inn_Imi = "RnD_Inn_Imi"
graph save Graph "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixRD_Inn_Imi.gph", replace



// Exporting graphs do PNG
set graphics on

graph use "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixAggOutput.gph"
graph export "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixAggOutput.png", as(png) replace

graph use "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixAggProfits.gph"
graph export "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixAggProfits.png", as(png) replace

graph use "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixMarketPrice.gph"
graph export "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixMarketPrice.png", as(png) replace

graph use "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixTechDiversity.gph"
graph export "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixTechDiversity.png", as(png) replace

graph use "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixFirms.gph"
graph export "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixFirms.png", as(png) replace

graph use "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixIndustryMarginalCost.gph"
graph export "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixIndustryMarginalCost.png", as(png) replace

graph use "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixIndustryPCM.gph"
graph export "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixIndustryPCM.png", as(png) replace

graph use "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixGini.gph"
graph export "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixGini.png", as(png) replace

graph use "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixAvgProxOptTech.gph"
graph export "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixAvgProxOptTech.png", as(png) replace

graph use "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixConsumerSurplus.gph"
graph export "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixConsumerSurplus.png", as(png) replace

graph use "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixRatioRes.gph"
graph export "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixRatioRes.png", as(png) replace

graph use "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixRatioProfitable.gph"
graph export "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixRatioProfitable.png", as(png) replace

graph use "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixAge.gph"
graph export "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixAge.png", as(png) replace

graph use "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixCostShareInnovation.gph"
graph export "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixCostShareInnovation.png", as(png) replace

graph use "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixShareCS.gph"
graph export "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixShareCS.png", as(png) replace

graph use "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixHHI.gph"
graph export "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixHHI.png", as(png) replace

graph use "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixRD_Inn_Imi.gph"
graph export "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.$suffixRD_Inn_Imi.png", as(png) replace




		 
