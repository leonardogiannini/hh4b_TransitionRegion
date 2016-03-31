from ROOT import *
from tree_analyzer_selection import *
import sys
b=0.8
c=0.185
print b, c


samples=["BulkGravTohhTohbbhbb_narrow_M-1400_13TeV-madgraph.root",
"BulkGravTohhTohbbhbb_narrow_M-1600_13TeV-madgraph.root",
"GluGluToBulkGravitonToHHTo4B_M-500_narrow_13TeV-madgraph.root",
"GluGluToBulkGravitonToHHTo4B_M-550_narrow_13TeV-madgraph.root",
"GluGluToBulkGravitonToHHTo4B_M-600_narrow_13TeV-madgraph.root",
"GluGluToBulkGravitonToHHTo4B_M-650_narrow_13TeV-madgraph.root",
"GluGluToBulkGravitonToHHTo4B_M-700_narrow_13TeV-madgraph.root",
"GluGluToBulkGravitonToHHTo4B_M-800_narrow_13TeV-madgraph.root",
"GluGluToBulkGravitonToHHTo4B_M-900_narrow_13TeV-madgraph.root",
"RSGravTohhTohbbhbb_narrow_M-1000_13TeV-madgraph.root",
"RSGravTohhTohbbhbb_narrow_M-1200_13TeV-madgraph.root",
"RSGravTohhTohbbhbb_narrow_M-1800_13TeV-madgraph.root",
"RSGravTohhTohbbhbb_narrow_M-2000_13TeV-madgraph.root",
#"RSGravTohhTohbbhbb_narrow_M-2500_13TeV-madgraph.root"
]
for d in samples:
	tree_selection("../vetoB_"+d, 0, "signal", 1, b, c)
	tree_control_region("../vetoB_"+d, 0, "signal", 1, b, c)
tree_selection("mc_vetoB.root", 0, "dd", 1, b, c)
tree_selection("data_vetoB.root", 0, "ddl", 1, b, c)
tree_control_region("mc_vetoB.root", 0, "dd", 1, b, c)
tree_control_region("data_vetoB.root", 0, "ddl", 1, b, c)
#tree_selection("data_preselcted.root", 0, "ddl", 1, b, c)






