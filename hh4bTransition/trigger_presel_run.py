from ROOT import *
from Analyzer import *
import os
import sys
#	boosted_analyzer(d)

#tree_preselection(file_string, isData=0, dataset="", cross_section=1.,systematic="", bbtag_cut=0.3,jet_btag_cut=-2):


dire=["ZZ_TuneCUETP8M1_13TeV-pythia8","WZ_TuneCUETP8M1_13TeV-pythia8","WW_TuneCUETP8M1_13TeV-pythia8","WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8","TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8","QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8","QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8","QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8","QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8","QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8","QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",]
#a=int(sys.argv[1])

cross_section=[ 347700., 32100., 6831., 1207., 119.9 , 25.24 ,831.76 ,118.7, 47.13, 16.523 ,95.14 ]

cross_section=cross_section[::-1]
print cross_section
for i in dire:
	if i.startswith(sys.argv[1].split("/")[-1].split(".")[0]):
		index=dire.index(i)

print "inizio"

print cross_section[index]
tree_preselection(str(sys.argv[1]), 0, "", cross_section[index])
#tree_preselection(str(sys.argv[1]), 0, "", cross_section[index], "JEC_Up")
#tree_preselection(str(sys.argv[1]), 0, "", cross_section[index], "JEC_Down")
#tree_preselection(str(sys.argv[1]), 0, "", cross_section[index], "JER_Up")
#tree_preselection(str(sys.argv[1]), 0, "", cross_section[index], "JER_Down")
#tree_preselection(str(sys.argv[1]), 0, "", cross_section[index], "FJEC_Up")
#tree_preselection(str(sys.argv[1]), 0, "", cross_section[index], "FJEC_Down")

#tree_preselection(str(sys.argv[1]), 1, "JetHT", 1, "s0")
#tree_preselection(str(sys.argv[1]), 1, "BTagCSV", 1, "s0")

#from  triggerOR_efficiency import *

#tree_selection(sys.argv[1])
#tree_control_region(sys.argv[1])
#file_string, isData=0, dataset="", cross_section=1.,bbtag_cut=0.8,jet_btag_cut=0.185
