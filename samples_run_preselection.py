from ROOT import *
from tree_analyzer_preselection import *


dire=["ZZ_TuneCUETP8M1_13TeV-pythia8","WZ_TuneCUETP8M1_13TeV-pythia8","WW_TuneCUETP8M1_13TeV-pythia8","WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8","TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8","QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8","QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8","QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8","QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8","QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8","QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",]
a=int(sys.argv[1])

cross_section=[ 347700., 32100., 6831., 1207., 119.9 , 25.24 ,831.76 ,118.7, 47.13, 16.523 ,95.14 ]

cross_section=cross_section[::-1]
print cross_section
#def tree_analyzer(file_string, plot, plot2d, isData=0, dataset="", cross_section=1.):
print "inizio"
		

#for d in dire[a:a+1]:
#	tree_preselection(d+".root", 0, 2, cross_section[a])




samples=[
"BulkGravTohhTohbbhbb_narrow_M-1400_13TeV-madgraph.root",
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
###"RSGravTohhTohbbhbb_narrow_M-2500_13TeV-madgraph.root",
###"RSGravTohhTohbbhbb_narrow_M-3000_13TeV-madgraph.root",
#"Grav3000.root",
#"Grav2500.root",
#"Grav3500.root"

]


for d in samples[a:a+1]:
	tree_preselection(d, 0, 2, 1)


HT_samples=["VHBB_HEPPY_V20_JetHT__Run2015C_25ns-16Dec2015-v1",
"VHBB_HEPPY_V20a_JetHT__Run2015D-16Dec2015-v1_0",
"VHBB_HEPPY_V20a_JetHT__Run2015D-16Dec2015-v1_1",
"VHBB_HEPPY_V20a_JetHT__Run2015D-16Dec2015-v1_2",
"VHBB_HEPPY_V20a_JetHT__Run2015D-16Dec2015-v1_3",
"VHBB_HEPPY_V20a_JetHT__Run2015D-16Dec2015-v1_4",
"VHBB_HEPPY_V20a_JetHT__Run2015D-16Dec2015-v1_5",
"VHBB_HEPPY_V20a_JetHT__Run2015D-16Dec2015-v1_6",
"VHBB_HEPPY_V20a_JetHT__Run2015D-16Dec2015-v1_7",
"VHBB_HEPPY_V20a_JetHT__Run2015D-16Dec2015-v1_8",
"VHBB_HEPPY_V20a_JetHT__Run2015D-16Dec2015-v1_9"
]
btag_samples=["VHBB_HEPPY_V20_BTagCSV__Run2015C_25ns-16Dec2015-v1",
"VHBB_HEPPY_V20a_BTagCSV__Run2015D-16Dec2015-v1"]






for d in btag_samples[a:a+1]:	
	tree_preselection(d+".root",0,"BtagCSV", 1,)
	

for d in HT_samples[a:a+1]:
	
	tree_preselection(d+".root", 0, "jetHT", 1,)









