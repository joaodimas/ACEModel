clear all
macro drop _all

global baseName = "ACEModel.2017-04-14T10h53m31s[MEAN]"
global folder = "Chapter 4/500 replications"
global firstPeriod = 1
global lastPeriod = 5000
global xAxisDelta = 1000

global xAxisBegin = $firstPeriod - 1
global xAxisEnd = $lastPeriod
global period = "in $firstPeriod/$lastPeriod"
import delimited "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.csv"

///set graphics off
tsset period




global grEdit1 = ".yaxis1.title.style.editstyle|size(vlarge)|editcopy"
global grEdit2 = ".yaxis1.reset_rule|7,|tickset(major)|ruletype(suggest)"
global grEdit3 = ".yaxis1.title.style.editstyle|margin(right)|editcopy|"
global grEdit4 = ".yaxis1.style.editstyle|majorstyle(tickstyle(textstyle(size(vlarge))))|editcopy|"
global grEdit5 = ".yaxis1.style.editstyle|majorstyle(tickangle(horizontal))|editcopy|"
global grEdit6 = ".xaxis1.reset_rule|$xAxisBegin|$xAxisEnd|$xAxisDelta|,|tickset(major)|ruletype(range)|"
global grEdit7 = ".xaxis1.title.style.editstyle|size(vlarge)|editcopy|"
global grEdit8 = ".xaxis1.title.style.editstyle|margin(top)|editcopy|"
global grEdit9 = ".xaxis1.style.editstyle|majorstyle(tickstyle(textstyle(size(vlarge))))|editcopy|"
global grEdit10 = ".xaxis1.title.text|=|[]"
global grEdit11 = ".xaxis1.title.text.Arrpush|Time"
global grEdit12 = ".style.editstyle|boxstyle(shadestyle(color(white)))|editcopy|"
global grEdit13 = ".style.editstyle|boxstyle(linestyle(color(white)))|editcopy|"
global grEdit14 = ".plotregion1.style.editstyle|margin(medium)|editcopy|"
global grEdit15 = ".SetAspectRatio|0.6|"

global listGrEdit = ""
forval i = 1/15 {
	global listGrEdit = "$listGrEdit ${grEdit`i'}"
}

display "$listGrEdit"




// Generating graph for Aggregate Profits

tsline totprofits $period
gr_edit .yaxis1.title.text = {"Aggregate profits"}

foreach grEdit in $listGrEdit {
	local command = subinstr("`grEdit'","|"," ",20)
	local command = subinstr("`command'","[]","{}",20)
	gr_edit `command'
}





graph save Graph "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.Aggregate_profits.gph", replace

// End


// Generating graph for Market Price

tsline price $period

gr_edit .yaxis1.reset_rule 7, tickset(major) ruletype(suggest) 
gr_edit .yaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .yaxis1.title.text = {}
gr_edit .yaxis1.title.text.Arrpush Market price

gr_edit .xaxis1.reset_rule $xAxisBegin $xAxisEnd $xAxisDelta , tickset(major) ruletype(range) 
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .xaxis1.title.text = {}
gr_edit .xaxis1.title.text.Arrpush Time

gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy

gr_edit .plotregion1.style.editstyle margin(medium) editcopy

gr_edit .SetAspectRatio 0.6

graph save Graph "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.Market_price.gph", replace

// End

// Generating graph for Technological diversity

tsline div $period

gr_edit .yaxis1.reset_rule 7, tickset(major) ruletype(suggest) 
gr_edit .yaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .yaxis1.title.text = {}
gr_edit .yaxis1.title.text.Arrpush Technological diversity

gr_edit .xaxis1.reset_rule $xAxisBegin $xAxisEnd $xAxisDelta , tickset(major) ruletype(range) 
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .xaxis1.title.text = {}
gr_edit .xaxis1.title.text.Arrpush Time

gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy

gr_edit .plotregion1.style.editstyle margin(medium) editcopy

gr_edit .SetAspectRatio 0.6

graph save Graph "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.Technological_diversity.gph", replace

// End


// Generating graph for No. firms

tsline firms $period

gr_edit .yaxis1.reset_rule 5, tickset(major) ruletype(suggest) 
gr_edit .yaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .yaxis1.title.text = {}
gr_edit .yaxis1.title.text.Arrpush No. firms

gr_edit .xaxis1.reset_rule $xAxisBegin $xAxisEnd $xAxisDelta , tickset(major) ruletype(range) 
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .xaxis1.title.text = {}
gr_edit .xaxis1.title.text.Arrpush Time

gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy

gr_edit .plotregion1.style.editstyle margin(medium) editcopy

gr_edit .SetAspectRatio 0.6

graph save Graph "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.Firms.gph", replace

// End


// Generating graph for Industry marginal cost

tsline wmc $period

gr_edit .yaxis1.reset_rule 5, tickset(major) ruletype(suggest) 
gr_edit .yaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .yaxis1.title.text = {}
gr_edit .yaxis1.title.text.Arrpush Industry marginal cost

gr_edit .xaxis1.reset_rule $xAxisBegin $xAxisEnd $xAxisDelta , tickset(major) ruletype(range) 
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .xaxis1.title.text = {}
gr_edit .xaxis1.title.text.Arrpush Time

gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy

gr_edit .plotregion1.style.editstyle margin(medium) editcopy

gr_edit .SetAspectRatio 0.6

graph save Graph "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.Industry_marginal_cost.gph", replace

// End


// Generating graph for Industry price-cost margin

tsline pcm $period

gr_edit .yaxis1.reset_rule 7, tickset(major) ruletype(suggest) 
gr_edit .yaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .yaxis1.title.text = {}
gr_edit .yaxis1.title.text.Arrpush Industry price-cost margin

gr_edit .xaxis1.reset_rule $xAxisBegin $xAxisEnd $xAxisDelta , tickset(major) ruletype(range) 
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .xaxis1.title.text = {}
gr_edit .xaxis1.title.text.Arrpush Time

gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy

gr_edit .plotregion1.style.editstyle margin(medium) editcopy

gr_edit .SetAspectRatio 0.6

graph save Graph "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.Industry_price_cost_margin.gph", replace

// End


// Generating graph for Gini coefficient

tsline gini $period

gr_edit .yaxis1.reset_rule 5, tickset(major) ruletype(suggest) 
gr_edit .yaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .yaxis1.title.text = {}
gr_edit .yaxis1.title.text.Arrpush Gini coefficient

gr_edit .xaxis1.reset_rule $xAxisBegin $xAxisEnd $xAxisDelta , tickset(major) ruletype(range) 
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .xaxis1.title.text = {}
gr_edit .xaxis1.title.text.Arrpush Time

gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy

gr_edit .plotregion1.style.editstyle margin(medium) editcopy

gr_edit .SetAspectRatio 0.6

graph save Graph "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.Gini_coefficient.gph", replace

// End


// Exporting graphs do PNG
set graphics on
graph use "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.Aggregate_profits.gph"
graph export "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.Aggregate_profits.png", as(png) replace

graph use "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.Market_price.gph"
graph export "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.Market_price.png", as(png) replace

graph use "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.Technological_diversity.gph"
graph export "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.Technological_diversity.png", as(png) replace

graph use "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.Firms.gph"
graph export "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.Firms.png", as(png) replace

graph use "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.Industry_marginal_cost.gph"
graph export "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.Industry_marginal_cost.png", as(png) replace

graph use "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.Industry_price_cost_margin.gph"
graph export "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.Industry_price_cost_margin.png", as(png) replace

graph use "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.Gini_coefficient.gph"
graph export "/Users/jdimas/GitHub/ACEModel/data/$folder/$baseName.Gini_coefficient.png", as(png) replace
