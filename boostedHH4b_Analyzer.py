H_mass=125.

def withinRegion(mH1, mH2,r1=30,r2=30.,mH1_c=H_mass,mH2_c=H_mass):
	import math
	if (abs(mH1-mH1_c)<r1 and abs(mH2-mH2_c)<r1):
		ret=0
	elif (abs(mH1-(mH1_c-50))<r2 and abs(mH2-(mH2_c-50))<r2):
		ret=1
	elif (abs(mH1-(mH1_c-30))<r2 and abs(mH2-(mH2_c-30))<r2):
		ret=2
	elif (abs(mH1-(mH1_c+30))<r2 and abs(mH2-(mH2_c+30))<r2):
		ret=3
	elif (abs(mH1-(mH1_c+50))<r2 and abs(mH2-(mH2_c+50))<r2):
		ret=4
	
	else: ret=5	
#	print ret
	return ret
	
from ROOT import *
import array, os, sys, numpy, copy
#from purity_test import *
jet_pT_cut=30
jet_eta_cut=2.5
jet_btag_cut=0.185
bbtag_cut=0.4
tau21_cut=0.6



def boosted_analyzer(file_string, isData=0, dataset="", cross_section=1.,systematic="None"):

	
	print dataset
	try:
		print file_string
		myFile=TFile(file_string, "R")
		tree=myFile.Get("tree")
		tree.Print("*bbtag*")
	except:
		print "nofile"
	if isData==1:
		norm=1
	else:
		histo_weight=myFile.Get("CountWeighted")
		print histo_weight, myFile
		norm=histo_weight.GetBinContent(1)
	
	print norm , "la normalizzazione"
	xsec=cross_section
	print xsec, "cross_section"
	AnaysisFile_boosted=TFile("presel_Leo_"+file_string.split("/")[-1], "recreate")
	
	MyTree2 = TTree("MyTree2", "MyTree2")
	#transition region variables	
	
	#fatjet only variables
	fatjet_pt=array.array('f', [0.])	
	fatjet_mpruned=array.array('f', [0.])
	fatjet_mpruned_corr=array.array('f', [0.])
	fatjet_hbb=array.array('f', [0.,0.])
	fatjet_tau21=array.array('f', [0.])
	fatjet2_pt=array.array('f', [0.])	
	fatjet2_mpruned=array.array('f', [0.])
	fatjet2_mpruned_corr=array.array('f', [0.])
	fatjet2_hbb=array.array('f', [0.])
	fatjet2_tau21=array.array('f', [0.])
	f_xsec=array.array('f', [0.])
	f_vtype=array.array('f', [0.])
	f_puw=array.array('f', [0.])
	f_norm=array.array('f', [0.])
	f_evt=array.array('f', [0.])
	f_mass=array.array('f', [0.])
	f_mass_corr=array.array('f', [0.])
	f_mass_corr2=array.array('f', [0.])
	htJet40eta3=array.array('f', [0.])
	trigPass=array.array('f', [0.])
	event_flavour=array.array('f', [0.])
	subjet_btag0=array.array('f', [0.])
	subjet_btag1=array.array('f', [0.])
	subjet_btag2=array.array('f', [0.])
	subjet_btag3=array.array('f', [0.])
	#branches for fatjets
	fb_1=MyTree2.Branch("fatjet1_pt", fatjet_pt,"fatjet1_pt")	
	fb_2=MyTree2.Branch("fatjet1_mpruned", fatjet_mpruned, "fatjet1_mpruned")
	fb_3=MyTree2.Branch("fatjet1_hbb", fatjet_hbb, "fatjet1_hbb")
	fb_4=MyTree2.Branch("fatjet1_tau21", fatjet_tau21, "fatjet1_tau21")
	fb_5=MyTree2.Branch("fatjet2_pt", fatjet2_pt,"fatjet2_pt")
	fb_6=MyTree2.Branch("fatjet2_mpruned", fatjet2_mpruned, "fatjet2_mpruned")
	fb_7=MyTree2.Branch("fatjet2_hbb", fatjet2_hbb, "fatjet2_hbb")
	fb_8=MyTree2.Branch("fatjet2_tau21", fatjet2_tau21, "fatjet2_tau21")
	fb_9=MyTree2.Branch("cross_section", f_xsec, "cross_section")
	fb_10=MyTree2.Branch("Vtype", f_vtype, "Vtype")
	fb_11=MyTree2.Branch("puWeight", f_puw, "puWeight")
	fb_12=MyTree2.Branch("norm", f_norm, "norm")
	fb_13=MyTree2.Branch("evt", f_evt, "evt")
	fb_14=MyTree2.Branch("inv_mass", f_mass, "inv_mass")
	fb_15=MyTree2.Branch("inv_mass_corr", f_mass_corr, "inv_mass_corr")
	
	fb_17=MyTree2.Branch("htJet40eta3", htJet40eta3, "htJet40eta3")
	fb_18=MyTree2.Branch("flavour", event_flavour, "flavour")
	fb_19=MyTree2.Branch("trigPass", trigPass, "trigPass")
	
	fb_20=MyTree2.Branch("fatjet1_mprunedcorr", fatjet_mpruned_corr, "fatjet1_mprunedcorr")
	fb_21=MyTree2.Branch("fatjet2_mprunedcorr", fatjet2_mpruned_corr, "fatjet2_mprunedcorr")
	
	fb_22=MyTree2.Branch("subjet_btag0", subjet_btag0, "subjet_btag0")
	fb_23=MyTree2.Branch("subjet_btag1", subjet_btag1, "subjet_btag1")
	fb_24=MyTree2.Branch("subjet_btag2", subjet_btag2, "subjet_btag2")
	fb_25=MyTree2.Branch("subjet_btag3", subjet_btag3, "subjet_btag3")
	
	fb_26=MyTree2.Branch("inv_mass_sub", f_mass_corr2, "inv_mass_sub")
#	print tree
	maxi=tree.GetEntries()
	for entry in range(maxi):
		if entry%100==0:

			print entry
			
		tree.GetEntry(entry)
		if tree.isData:
			puWeight=1.
			norm=1.
		else:
			puWeight=tree.puWeight
		weight=(cross_section)*(puWeight)/norm


		ht_ =0
		for i in range(0,len(tree.Jet_pt)):
			if abs(tree.Jet_eta[i])<3 and tree.Jet_pt[i] >40 :
				ht_=ht_+tree.Jet_pt[i]

		if (tree.json==1):
#			print trigger_bit, tree.HLT_BIT_HLT_AK8DiPFJet250_200_TrimMass30_BTagCSV0p45_v , tree.HLT_BIT_HLT_PFHT800_v , tree.HLT_HH4bHighLumi
#			print (tree.HLT_BIT_HLT_AK8DiPFJet250_200_TrimMass30_BTagCSV0p45_v>0 or tree.HLT_BIT_HLT_PFHT800_v>0 or tree.HLT_HH4bHighLumi>0)
#			print (not(tree.HLT_BIT_HLT_AK8DiPFJet250_200_TrimMass30_BTagCSV0p45_v>0) and not(tree.HLT_BIT_HLT_PFHT800_v>0) and tree.HLT_HH4bHighLumi>0)
#			
			if tree.nFatjetAK08ungroomed>1:
				
				if (abs(tree.FatjetAK08ungroomed_eta[0])<2.5 and abs(tree.FatjetAK08ungroomed_eta[1])<2.5):
					if abs(tree.FatjetAK08ungroomed_eta[0]-tree.FatjetAK08ungroomed_eta[1])<1.3:
						fatjet_pt[0]=tree.FatjetAK08ungroomed_pt[0]
						fatjet_mpruned[0]=tree.FatjetAK08ungroomed_mpruned[0]
						fatjet_mpruned_corr[0]=tree.FatjetAK08ungroomed_mprunedcorr[0]
						fatjet_hbb[0]=tree.FatjetAK08ungroomed_bbtag[0]
						if tree.FatjetAK08ungroomed_tau1[0]>0:
							fatjet_tau21[0]=tree.FatjetAK08ungroomed_tau2[0]/tree.FatjetAK08ungroomed_tau1[0]
						else:
							fatjet_tau21[0]=1
						fatjet2_pt[0]=tree.FatjetAK08ungroomed_pt[1]						
						fatjet2_mpruned[0]=tree.FatjetAK08ungroomed_mpruned[1]
						fatjet2_mpruned_corr[0]=tree.FatjetAK08ungroomed_mprunedcorr[1]
						fatjet2_hbb[0]=tree.FatjetAK08ungroomed_bbtag[1]
						if tree.FatjetAK08ungroomed_tau1[1]>0:
							fatjet2_tau21[0]=tree.FatjetAK08ungroomed_tau2[1]/tree.FatjetAK08ungroomed_tau1[1]
						else:
							fatjet2_tau21[0]=1
						f_xsec[0]=cross_section
						f_vtype[0]=tree.Vtype
						f_puw[0]=puWeight
						f_norm[0]=norm
						f_evt[0]=tree.evt


						fj_0=TLorentzVector()					
						fj_0.SetPtEtaPhiM(tree.FatjetAK08ungroomed_pt[0], tree.FatjetAK08ungroomed_eta[0], tree.FatjetAK08ungroomed_phi[0], tree.FatjetAK08ungroomed_mass[0])
						fj_1=TLorentzVector()					
						fj_1.SetPtEtaPhiM(tree.FatjetAK08ungroomed_pt[1], tree.FatjetAK08ungroomed_eta[1], tree.FatjetAK08ungroomed_phi[1], tree.FatjetAK08ungroomed_mass[1])
						f_mass[0]=((fj_0+fj_1).M())
						f_mass_corr[0] = ((fj_0+fj_1).M()) - (fatjet_mpruned[0]-125)-(fatjet2_mpruned[0]-125)
						f_mass_corr2[0] = ((fj_0+fj_1).M()) - (fatjet_mpruned_corr[0]-125)-(fatjet2_mpruned_corr[0]-125)
						htJet40eta3[0] = ht_
						trigPass[0]=tree.HLT_BIT_HLT_PFHT800_v
						
						#matching#
						sj_0=TLorentzVector()
						s_index0=-1
						s_index1=-1
						s_index2=-1
						s_index3=-1
						for s in range(tree.nSubjetAK08softdrop):
							sj_0.SetPtEtaPhiM(tree.SubjetAK08softdrop_pt[s], tree.SubjetAK08softdrop_eta[s], tree.SubjetAK08softdrop_phi[s], tree.SubjetAK08softdrop_mass[s])
							deltar=sj_0.DeltaR(fj_0)
							if (s_index0==-1 and deltar<0.5):
								s_index0=s
							elif (s_index1==-1 and deltar<0.5):
								s_index1=s
							deltar=sj_0.DeltaR(fj_1)
							if (s_index2==-1 and deltar<0.5):
								s_index2=s
							elif (s_index3==-1 and deltar<0.5):
								s_index3=s
						subjet_btag0[0]=-1
						subjet_btag1[0]=-1
						subjet_btag2[0]=-1
						subjet_btag3[0]=-1
						if s_index0>-1: subjet_btag0[0]=tree.SubjetAK08softdrop_btag[s_index0]
						if s_index1>-1: subjet_btag1[0]=tree.SubjetAK08softdrop_btag[s_index1]
						if s_index2>-1: subjet_btag2[0]=tree.SubjetAK08softdrop_btag[s_index2]
						if s_index3>-1: subjet_btag3[0]=tree.SubjetAK08softdrop_btag[s_index3]
						event_flavour[0]=-100
						if isData==1:
							event_flavour[0]=-1
						elif tree.FatjetAK08ungroomed_BhadronFlavour[0]>=2:
							if tree.FatjetAK08ungroomed_BhadronFlavour[1]>=2:
								print "2b-2b"
								event_flavour[0]=20
							elif (tree.FatjetAK08ungroomed_BhadronFlavour[1]==1 and tree.FatjetAK08ungroomed_ChadronFlavour[1]>=1):
								print "2b-bc"
								event_flavour[0]=19
							elif (tree.FatjetAK08ungroomed_BhadronFlavour[1]==1 and tree.FatjetAK08ungroomed_ChadronFlavour[1]==0):
								print "2b-b"
								event_flavour[0]=18
							elif (tree.FatjetAK08ungroomed_BhadronFlavour[1]==0 and tree.FatjetAK08ungroomed_ChadronFlavour[1]>=2):
								print "2b-2c"
								event_flavour[0]=17
							elif (tree.FatjetAK08ungroomed_BhadronFlavour[1]==0 and tree.FatjetAK08ungroomed_ChadronFlavour[1]==1):
								print "2b-c"
								event_flavour[0]=16
							elif (tree.FatjetAK08ungroomed_BhadronFlavour[1]==0 and tree.FatjetAK08ungroomed_ChadronFlavour[1]==0):
								print "2b-l"
								event_flavour[0]=15
						elif (tree.FatjetAK08ungroomed_BhadronFlavour[0]==1 and tree.FatjetAK08ungroomed_ChadronFlavour[0]>=1):
							if tree.FatjetAK08ungroomed_BhadronFlavour[1]>=2:
								print "2b-bc"
								event_flavour[0]=19
							elif (tree.FatjetAK08ungroomed_BhadronFlavour[1]==1 and tree.FatjetAK08ungroomed_ChadronFlavour[1]>=1):
								print "bc-bc"
								event_flavour[0]=14
							elif (tree.FatjetAK08ungroomed_BhadronFlavour[1]==1 and tree.FatjetAK08ungroomed_ChadronFlavour[1]==0):
								print "bc-b"
								event_flavour[0]=13
							elif (tree.FatjetAK08ungroomed_BhadronFlavour[1]==0 and tree.FatjetAK08ungroomed_ChadronFlavour[1]>=2):
								print "bc-2c"
								event_flavour[0]=12
							elif (tree.FatjetAK08ungroomed_BhadronFlavour[1]==0 and tree.FatjetAK08ungroomed_ChadronFlavour[1]==1):
								print "bc-c"
								event_flavour[0]=11
							elif (tree.FatjetAK08ungroomed_BhadronFlavour[1]==0 and tree.FatjetAK08ungroomed_ChadronFlavour[1]==0):
								print "bc-l"
								event_flavour[0]=10
						elif (tree.FatjetAK08ungroomed_BhadronFlavour[0]==1 and tree.FatjetAK08ungroomed_ChadronFlavour[0]==0):
							if tree.FatjetAK08ungroomed_BhadronFlavour[1]>=2:
								print "2b-b"
								event_flavour[0]=18
							elif (tree.FatjetAK08ungroomed_BhadronFlavour[1]==1 and tree.FatjetAK08ungroomed_ChadronFlavour[1]>=1):
								print "bc-b"
								event_flavour[0]=13
							elif (tree.FatjetAK08ungroomed_BhadronFlavour[1]==1 and tree.FatjetAK08ungroomed_ChadronFlavour[1]==0):
								print "b-b"
								event_flavour[0]=9
							elif (tree.FatjetAK08ungroomed_BhadronFlavour[1]==0 and tree.FatjetAK08ungroomed_ChadronFlavour[1]>=2):
								print "b-2c"
								event_flavour[0]=8
							elif (tree.FatjetAK08ungroomed_BhadronFlavour[1]==0 and tree.FatjetAK08ungroomed_ChadronFlavour[1]==1):
								print "b-c"
								event_flavour[0]=7
							elif (tree.FatjetAK08ungroomed_BhadronFlavour[1]==0 and tree.FatjetAK08ungroomed_ChadronFlavour[1]==0):
								print "b-l"
								event_flavour[0]=6
						elif (tree.FatjetAK08ungroomed_BhadronFlavour[0]==0 and tree.FatjetAK08ungroomed_ChadronFlavour[0]>=2):
							if tree.FatjetAK08ungroomed_BhadronFlavour[1]>=2:
								print "2b-2c"
								event_flavour[0]=17
							elif (tree.FatjetAK08ungroomed_BhadronFlavour[1]==1 and tree.FatjetAK08ungroomed_ChadronFlavour[1]>=1):
								print "bc-2c"
								event_flavour[0]=12
							elif (tree.FatjetAK08ungroomed_BhadronFlavour[1]==1 and tree.FatjetAK08ungroomed_ChadronFlavour[1]==0):
								print "b-2c"
								event_flavour[0]=8
							elif (tree.FatjetAK08ungroomed_BhadronFlavour[1]==0 and tree.FatjetAK08ungroomed_ChadronFlavour[1]>=2):
								print "2c-2c"
								event_flavour[0]=5
							elif (tree.FatjetAK08ungroomed_BhadronFlavour[1]==0 and tree.FatjetAK08ungroomed_ChadronFlavour[1]==1):
								print "2c-c"
								event_flavour[0]=4
							elif (tree.FatjetAK08ungroomed_BhadronFlavour[1]==0 and tree.FatjetAK08ungroomed_ChadronFlavour[1]==0):
								print "2c-l"
								event_flavour[0]=3
						elif (tree.FatjetAK08ungroomed_BhadronFlavour[0]==0 and tree.FatjetAK08ungroomed_ChadronFlavour[0]==1):
							if tree.FatjetAK08ungroomed_BhadronFlavour[1]>=2:
								print "2b-c"
								event_flavour[0]=16
							elif (tree.FatjetAK08ungroomed_BhadronFlavour[1]==1 and tree.FatjetAK08ungroomed_ChadronFlavour[1]>=1):
								print "bc-c"
								event_flavour[0]=11
							elif (tree.FatjetAK08ungroomed_BhadronFlavour[1]==1 and tree.FatjetAK08ungroomed_ChadronFlavour[1]==0):
								print "b-c"
								event_flavour[0]=7
							elif (tree.FatjetAK08ungroomed_BhadronFlavour[1]==0 and tree.FatjetAK08ungroomed_ChadronFlavour[1]>=2):
								print "2c-c"
								event_flavour[0]=4
							elif (tree.FatjetAK08ungroomed_BhadronFlavour[1]==0 and tree.FatjetAK08ungroomed_ChadronFlavour[1]==1):
								print "c-c"
								event_flavour[0]=2
							elif (tree.FatjetAK08ungroomed_BhadronFlavour[1]==0 and tree.FatjetAK08ungroomed_ChadronFlavour[1]==0):
								print "c-l"
								event_flavour[0]=1
						elif (tree.FatjetAK08ungroomed_BhadronFlavour[0]==0 and tree.FatjetAK08ungroomed_ChadronFlavour[0]==0):
							if tree.FatjetAK08ungroomed_BhadronFlavour[1]>=2:
								print "2b-l"
								event_flavour[0]=15
							elif (tree.FatjetAK08ungroomed_BhadronFlavour[1]==1 and tree.FatjetAK08ungroomed_ChadronFlavour[1]>=1):
								print "bc-l"
								event_flavour[0]=10
							elif (tree.FatjetAK08ungroomed_BhadronFlavour[1]==1 and tree.FatjetAK08ungroomed_ChadronFlavour[1]==0):
								print "b-l"
								event_flavour[0]=6
							elif (tree.FatjetAK08ungroomed_BhadronFlavour[1]==0 and tree.FatjetAK08ungroomed_ChadronFlavour[1]>=2):
								print "2c-l"
								event_flavour[0]=3
							elif (tree.FatjetAK08ungroomed_BhadronFlavour[1]==0 and tree.FatjetAK08ungroomed_ChadronFlavour[1]==1):
								print "c-l"
								event_flavour[0]=1
							elif (tree.FatjetAK08ungroomed_BhadronFlavour[1]==0 and tree.FatjetAK08ungroomed_ChadronFlavour[1]==0):
								print "l-l"
								event_flavour[0]=0
						else: 
							print "ERRORE"
#						print int(round(htJet40eta3[0]))
						
						MyTree2.Fill()


	MyTree2.Write()
	AnaysisFile_boosted.Close()

	myFile.Close()
	
