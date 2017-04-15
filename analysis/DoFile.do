clear

global baseName = "ACEModel.2017-04-15T09h48m42s[MEAN]"
import delimited "/Users/jdimas/GitHub/ACEModel/data/Chapter 4/$baseName.csv"

set graphics off
tsset period

// Generating graph for Aggregate Profits

tsline totprofits

gr_edit .yaxis1.reset_rule 7, tickset(major) ruletype(suggest) 
gr_edit .yaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .yaxis1.title.text = {}
gr_edit .yaxis1.title.text.Arrpush Aggregate profits

gr_edit .xaxis1.reset_rule 0 5000 1000 , tickset(major) ruletype(range) 
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .xaxis1.title.text = {}
gr_edit .xaxis1.title.text.Arrpush Time

gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy

gr_edit .plotregion1.style.editstyle margin(vlarge) editcopy

gr_edit .SetAspectRatio 0.6

graph save Graph "/Users/jdimas/GitHub/ACEModel/data/Chapter 4/$baseName.Aggregate_profits.gph", replace

// End


// Generating graph for Market Price

tsline price

gr_edit .yaxis1.reset_rule 7, tickset(major) ruletype(suggest) 
gr_edit .yaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .yaxis1.title.text = {}
gr_edit .yaxis1.title.text.Arrpush Market price

gr_edit .xaxis1.reset_rule 0 5000 1000 , tickset(major) ruletype(range) 
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .xaxis1.title.text = {}
gr_edit .xaxis1.title.text.Arrpush Time

gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy

gr_edit .plotregion1.style.editstyle margin(vlarge) editcopy

gr_edit .SetAspectRatio 0.6

graph save Graph "/Users/jdimas/GitHub/ACEModel/data/Chapter 4/$baseName.Market_price.gph", replace

// End

// Generating graph for Technological diversity

tsline div

gr_edit .yaxis1.reset_rule 7, tickset(major) ruletype(suggest) 
gr_edit .yaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .yaxis1.title.text = {}
gr_edit .yaxis1.title.text.Arrpush Technological diversity

gr_edit .xaxis1.reset_rule 0 5000 1000 , tickset(major) ruletype(range) 
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .xaxis1.title.text = {}
gr_edit .xaxis1.title.text.Arrpush Time

gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy

gr_edit .plotregion1.style.editstyle margin(vlarge) editcopy

gr_edit .SetAspectRatio 0.6

graph save Graph "/Users/jdimas/GitHub/ACEModel/data/Chapter 4/$baseName.Technological_diversity.gph", replace

// End


// Generating graph for No. firms

tsline firms

gr_edit .yaxis1.reset_rule 5, tickset(major) ruletype(suggest) 
gr_edit .yaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .yaxis1.title.text = {}
gr_edit .yaxis1.title.text.Arrpush No. firms

gr_edit .xaxis1.reset_rule 0 5000 1000 , tickset(major) ruletype(range) 
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .xaxis1.title.text = {}
gr_edit .xaxis1.title.text.Arrpush Time

gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy

gr_edit .plotregion1.style.editstyle margin(vlarge) editcopy

gr_edit .SetAspectRatio 0.6

graph save Graph "/Users/jdimas/GitHub/ACEModel/data/Chapter 4/$baseName.Firms.gph", replace

// End


// Generating graph for Industry marginal cost

tsline wmc

gr_edit .yaxis1.reset_rule 5, tickset(major) ruletype(suggest) 
gr_edit .yaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .yaxis1.title.text = {}
gr_edit .yaxis1.title.text.Arrpush Industry marginal cost

gr_edit .xaxis1.reset_rule 0 5000 1000 , tickset(major) ruletype(range) 
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .xaxis1.title.text = {}
gr_edit .xaxis1.title.text.Arrpush Time

gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy

gr_edit .plotregion1.style.editstyle margin(vlarge) editcopy

gr_edit .SetAspectRatio 0.6

graph save Graph "/Users/jdimas/GitHub/ACEModel/data/Chapter 4/$baseName.Industry_marginal_cost.gph", replace

// End


// Generating graph for Industry price-cost margin

tsline pcm

gr_edit .yaxis1.reset_rule 7, tickset(major) ruletype(suggest) 
gr_edit .yaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .yaxis1.title.text = {}
gr_edit .yaxis1.title.text.Arrpush Industry price-cost margin

gr_edit .xaxis1.reset_rule 0 5000 1000 , tickset(major) ruletype(range) 
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .xaxis1.title.text = {}
gr_edit .xaxis1.title.text.Arrpush Time

gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy

gr_edit .plotregion1.style.editstyle margin(vlarge) editcopy

gr_edit .SetAspectRatio 0.6

graph save Graph "/Users/jdimas/GitHub/ACEModel/data/Chapter 4/$baseName.Industry_price_cost_margin.gph", replace

// End


// Generating graph for Gini coefficient

tsline gini

gr_edit .yaxis1.reset_rule 5, tickset(major) ruletype(suggest) 
gr_edit .yaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .yaxis1.title.style.editstyle margin(right) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .yaxis1.style.editstyle majorstyle(tickangle(horizontal)) editcopy
gr_edit .yaxis1.title.text = {}
gr_edit .yaxis1.title.text.Arrpush Gini coefficient

gr_edit .xaxis1.reset_rule 0 5000 1000 , tickset(major) ruletype(range) 
gr_edit .xaxis1.title.style.editstyle size(vlarge) editcopy
gr_edit .xaxis1.title.style.editstyle margin(top) editcopy
gr_edit .xaxis1.style.editstyle majorstyle(tickstyle(textstyle(size(vlarge)))) editcopy
gr_edit .xaxis1.title.text = {}
gr_edit .xaxis1.title.text.Arrpush Time

gr_edit .style.editstyle boxstyle(shadestyle(color(white))) editcopy
gr_edit .style.editstyle boxstyle(linestyle(color(white))) editcopy

gr_edit .plotregion1.style.editstyle margin(vlarge) editcopy

gr_edit .SetAspectRatio 0.6

graph save Graph "/Users/jdimas/GitHub/ACEModel/data/Chapter 4/$baseName.Gini_coefficient.gph", replace

// End


// Exporting graphs do PNG
set graphics on
graph use "/Users/jdimas/GitHub/ACEModel/data/Chapter 4/$baseName.Aggregate_profits.gph"
graph export "/Users/jdimas/GitHub/ACEModel/data/Chapter 4/$baseName.Aggregate_profits.png", as(png) replace

graph use "/Users/jdimas/GitHub/ACEModel/data/Chapter 4/$baseName.Market_price.gph"
graph export "/Users/jdimas/GitHub/ACEModel/data/Chapter 4/$baseName.Market_price.png", as(png) replace

graph use "/Users/jdimas/GitHub/ACEModel/data/Chapter 4/$baseName.Technological_diversity.gph"
graph export "/Users/jdimas/GitHub/ACEModel/data/Chapter 4/$baseName.Technological_diversity.png", as(png) replace

graph use "/Users/jdimas/GitHub/ACEModel/data/Chapter 4/$baseName.Firms.gph"
graph export "/Users/jdimas/GitHub/ACEModel/data/Chapter 4/$baseName.Firms.png", as(png) replace

graph use "/Users/jdimas/GitHub/ACEModel/data/Chapter 4/$baseName.Industry_marginal_cost.gph"
graph export "/Users/jdimas/GitHub/ACEModel/data/Chapter 4/$baseName.Industry_marginal_cost.png", as(png) replace

graph use "/Users/jdimas/GitHub/ACEModel/data/Chapter 4/$baseName.Industry_price_cost_margin.gph"
graph export "/Users/jdimas/GitHub/ACEModel/data/Chapter 4/$baseName.Industry_price_cost_margin.png", as(png) replace

graph use "/Users/jdimas/GitHub/ACEModel/data/Chapter 4/$baseName.Gini_coefficient.gph"
graph export "/Users/jdimas/GitHub/ACEModel/data/Chapter 4/$baseName.Gini_coefficient.png", as(png) replace
