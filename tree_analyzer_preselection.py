H_mass=125.1

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

class selection:
    def __init__(self, selstring, index, name):
	self.selstring = selstring
	self.index = index
	self.name = name

def selections():
	levels=[

	selection("",0, "HHcandidates"),
	
	selection("",1, "Signal_region"),	
	selection("",2, "Sideband_A"),	
	selection("",3, "Sideband_B"),	
	selection("",4, "Sideband_C"),	
	selection("",5, "Sideband_D"),
	
	
	]
	return levels



def tree_preselection(file_string, isData=0, dataset="", cross_section=1.,bbtag_cut=0.3,jet_btag_cut=-2):
	listofplots=[]
	selection_list=selections()
	
	print dataset
	try:
		myFile=TFile("../../V20samples/"+file_string, "R")
		tree=myFile.Get("tree")
		tree.Print("*bbtag*")
	except:
		myFile=TFile("/scratch/arizzi/merge/"+file_string, "R")
		tree=myFile.Get("tree")

	histo_weight=myFile.Get("CountWeighted")
	print histo_weight, myFile
	norm=histo_weight.GetBinContent(1)
	print norm , "la normalizzazione"
		
	print listofplots
	tree.GetEntry(1)
	xsec=cross_section
	print xsec, "cross_section"	
	
	
	AnaysisFile_boosted=TFile("vetoB_"+file_string, "recreate")
	MyTree = TTree("MyTree", "MyTree")
	MyTree2 = TTree("MyTree2", "MyTree2")
	#transition region variables
	
	fatjets_pt= vector('double')()
	fatjets_eta= vector('double')()
	fatjets_phi= vector('double')()
	fatjets_mass= vector('double')()
	fatjets_mpruned= vector('double')()
	fatjets_bbtag= vector('double')()

	jets_pt= vector('double')()
	jets_eta= vector('double')()
	jets_phi= vector('double')()
	jets_mass= vector('double')()
	jets_btag= vector('double')()
	jets_fatjet= vector('double')()

	b_evt=array.array('f', [0.])

	i1=array.array('f', [0.])
	q1=array.array('f', [0.])
	o1=array.array('f', [0.])
	p1=array.array('f', [0.])
	r1=array.array('f', [0.])
	s1=array.array('f', [0.])
	t1=array.array('f', [0.])

	b_1=MyTree.Branch("fatjets_pt", fatjets_pt)
	b_2=MyTree.Branch("fatjets_eta", fatjets_eta)
	b_3=MyTree.Branch("fatjets_phi", fatjets_phi)
	b_4=MyTree.Branch("fatjets_mass", fatjets_mass)
	b_5=MyTree.Branch("fatjets_mpruned", fatjets_mpruned)
	b_6=MyTree.Branch("fatjets_bbtag", fatjets_bbtag)

	jb_1=MyTree.Branch("jets_pt", jets_pt)
	jb_2=MyTree.Branch("jets_eta", jets_eta)
	jb_3=MyTree.Branch("jets_phi", jets_phi)
	jb_4=MyTree.Branch("jets_mass", jets_mass)
	jb_5=MyTree.Branch("jets_btag", jets_btag)
	jb_5=MyTree.Branch("jets_fatjet", jets_fatjet)

	b_7=MyTree.Branch("Vtype", q1, "Vtype")
	b_8=MyTree.Branch("puWeight", o1, "puWeight")
	b_9=MyTree.Branch("norm", p1, "norm")
	b_10=MyTree.Branch("n_OkJets_byCSV", r1, "n_OkJets_byCSV")
	b_11=MyTree.Branch("n_OkFj", s1, "n_OkFj")
	b_12=MyTree.Branch("evt", t1, "evt")
	b_13=MyTree.Branch("cross_section", i1, "cross_section")
	b_14=MyTree.Branch("boosted_evt", b_evt, "boosted_evt")
	
	#fatjet only variables
	fatjet_pt=array.array('f', [0.])	
	fatjet_mpruned=array.array('f', [0.])
	fatjet_hbb=array.array('f', [0.,0.])
	fatjet_tau21=array.array('f', [0.])
	fatjet2_pt=array.array('f', [0.])	
	fatjet2_mpruned=array.array('f', [0.])
	fatjet2_hbb=array.array('f', [0.])
	fatjet2_tau21=array.array('f', [0.])
	f_xsec=array.array('f', [0.])
	f_vtype=array.array('f', [0.])
	f_puw=array.array('f', [0.])
	f_norm=array.array('f', [0.])
	f_evt=array.array('f', [0.])
	f_mass=array.array('f', [0.])

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
	fb_13=MyTree2.Branch("inv_mass", f_mass, "inv_mass")

#	print tree
	maxi=tree.GetEntries()
	for entry in range(maxi):
#		print entry
		
		tree.GetEntry(entry)
		if tree.isData:
			puWeight=1.
			norm=1.
		else:
			puWeight=tree.puWeight
		weight=(cross_section)*(puWeight)/norm
		if dataset=="BtagCSV":
			trigger_bit=(not(tree.HLT_BIT_HLT_AK8DiPFJet250_200_TrimMass30_BTagCSV0p45_v>0) and not(tree.HLT_BIT_HLT_PFHT800_v>0) and tree.HLT_HH4bHighLumi>0)
		else:
			trigger_bit=(tree.HLT_BIT_HLT_AK8DiPFJet250_200_TrimMass30_BTagCSV0p45_v>0 or tree.HLT_BIT_HLT_PFHT800_v>0 or tree.HLT_HH4bHighLumi>0)
		0
		if (tree.json==1 and trigger_bit):
#			print trigger_bit, tree.HLT_BIT_HLT_AK8DiPFJet250_200_TrimMass30_BTagCSV0p45_v , tree.HLT_BIT_HLT_PFHT800_v , tree.HLT_HH4bHighLumi
#			print (tree.HLT_BIT_HLT_AK8DiPFJet250_200_TrimMass30_BTagCSV0p45_v>0 or tree.HLT_BIT_HLT_PFHT800_v>0 or tree.HLT_HH4bHighLumi>0)
#			print (not(tree.HLT_BIT_HLT_AK8DiPFJet250_200_TrimMass30_BTagCSV0p45_v>0) and not(tree.HLT_BIT_HLT_PFHT800_v>0) and tree.HLT_HH4bHighLumi>0)
#			
			if tree.nFatjetAK08ungroomed>1:
				if (tree.FatjetAK08ungroomed_tau2[0]/tree.FatjetAK08ungroomed_tau1[0]<0.6 and tree.FatjetAK08ungroomed_tau2[1]/tree.FatjetAK08ungroomed_tau1[1]<0.6):
					if abs(tree.FatjetAK08ungroomed_eta[0]-tree.FatjetAK08ungroomed_eta[1])<1.3:
						fatjet_pt[0]=tree.FatjetAK08ungroomed_pt[0]						
						fatjet_mpruned[0]=tree.FatjetAK08ungroomed_mpruned[0]
						fatjet_hbb[0]=tree.FatjetAK08ungroomed_bbtag[0]
						fatjet_tau21[0]=tree.FatjetAK08ungroomed_tau2[0]/tree.FatjetAK08ungroomed_tau1[0]
						fatjet2_pt[0]=tree.FatjetAK08ungroomed_pt[1]						
						fatjet2_mpruned[0]=tree.FatjetAK08ungroomed_mpruned[1]
						fatjet2_hbb[0]=tree.FatjetAK08ungroomed_bbtag[1]
						fatjet2_tau21[0]=tree.FatjetAK08ungroomed_tau2[1]/tree.FatjetAK08ungroomed_tau1[1]
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
						MyTree2.Fill()

			if (tree.Vtype==-1 or tree.Vtype==4):
				count_fatjets=0
				count_jetsoutsidef=0
				leading_mass_old=40.
				leading_index=-1
				Fatjets_array=numpy.zeros((10, 2))
				jets_btag_array=numpy.zeros((20, 3))
				Fatjets_array=Fatjets_array-1
				jets_btag_array=jets_btag_array-1
				for n in range(tree.nFatjetAK08ungroomed):
					Fatjets_array[n][0]=tree.FatjetAK08ungroomed_mpruned[n]
					Fatjets_array[n][1]=n
		#					print "il mio vettore", Fatjets_array

				Fatjets_array.view('f8,f8').sort(order=['f0'], axis=0)
				Fatjets_array=Fatjets_array[::-1]
				index_array=Fatjets_array[:,1]

				index_array=index_array[(index_array >= 0)]
				save_index=[]
				save_jet_index=[]

				for n1 in index_array:
					n=int(n1)				
					leading_index=n				
					if (leading_index>=0):
						if (abs(tree.FatjetAK08ungroomed_eta[leading_index])<jet_eta_cut and tree.FatjetAK08ungroomed_bbtag[leading_index]>bbtag_cut and tree.FatjetAK08ungroomed_mpruned[leading_index]>40 and (tree.FatjetAK08ungroomed_tau2[leading_index]/tree.FatjetAK08ungroomed_tau1[leading_index])<tau21_cut):
	#						print "atcut ", 2
					
							count_fatjets=count_fatjets+1
							fj_p4=TLorentzVector()					
							fj_p4.SetPtEtaPhiM(tree.FatjetAK08ungroomed_pt[leading_index], tree.FatjetAK08ungroomed_eta[leading_index], tree.FatjetAK08ungroomed_phi[leading_index], tree.FatjetAK08ungroomed_mass[leading_index])								
							for j in range(tree.nJet):
								j_p4=TLorentzVector()								
								j_p4.SetPtEtaPhiM(tree.Jet_pt[j], tree.Jet_eta[j], tree.Jet_phi[j], tree.Jet_mass[j])						
								deltaR=j_p4.DeltaR(fj_p4)
								if (tree.Jet_pt[j]>jet_pT_cut and abs(tree.Jet_eta[j])<jet_eta_cut and tree.Jet_btagCMVAV2[j]>jet_btag_cut and deltaR>1.5):
									count_jetsoutsidef+=1
									save_jet_index.append(j)
									jets_btag_array[j][0]=tree.Jet_btagCMVAV2[j]
									jets_btag_array[j][1]=j
									jets_btag_array[j][2]=leading_index
							if count_jetsoutsidef>1:
								save_index.append(leading_index)
				b_evt[0]=0.
				if  dataset!="BtagCSV":
					if(tree.HLT_BIT_HLT_PFHT800_v>0):
						if tree.nFatjetAK08ungroomed>1:
							if (abs(tree.FatjetAK08ungroomed_eta[0])<2.5 and abs(tree.FatjetAK08ungroomed_eta[1])<2.5):
								if abs(tree.FatjetAK08ungroomed_eta[0]-tree.FatjetAK08ungroomed_eta[1])<1.3:
									if (tree.FatjetAK08ungroomed_bbtag[0]>0.6 and tree.FatjetAK08ungroomed_bbtag[1]>0.6):
										print "hbbbb"
										if ((tree.FatjetAK08ungroomed_tau2[0]/tree.FatjetAK08ungroomed_tau1[0])<0.6 ):
											if ((tree.FatjetAK08ungroomed_tau2[1]/tree.FatjetAK08ungroomed_tau1[1])<0.6 ):
												print "boosted5"
												if (tree.FatjetAK08ungroomed_mpruned[0]>100 and tree.FatjetAK08ungroomed_mpruned[1]>100):
													if (tree.FatjetAK08ungroomed_mpruned[0]<130 and tree.FatjetAK08ungroomed_mpruned[1]<130):
														print "boosted6"
														b_evt[0]=1.
				if (count_jetsoutsidef>=2 and count_fatjets>=1):
#					print "counted", entry
#					print save_jet_index, save_index
					f_i=0
					fatjets_pt.clear()
					fatjets_eta.clear()
					fatjets_phi.clear()
					fatjets_mass.clear()
					fatjets_mpruned.clear()
					fatjets_bbtag.clear()

					for j in save_index:
						fatjets_pt.push_back(tree.FatjetAK08ungroomed_pt[j])
						fatjets_eta.push_back(tree.FatjetAK08ungroomed_eta[j])
						fatjets_phi.push_back(tree.FatjetAK08ungroomed_phi[j])
						fatjets_mass.push_back(tree.FatjetAK08ungroomed_mass[j])
						fatjets_mpruned.push_back(tree.FatjetAK08ungroomed_mpruned[j])
						fatjets_bbtag.push_back(tree.FatjetAK08ungroomed_bbtag[j])
						f_i=f_i+1
#						
					jets_btag_array.view('f8,f8,f8').sort(order=['f0'], axis=0)
					jets_btag_array=jets_btag_array[::-1]
					index_array2=jets_btag_array[:,1]
					index_array2=index_array2[(index_array2 >= 0)]
#					print jets_btag_array
#					print index_array2
					j_i=0
					
					jets_pt.clear()
					jets_eta.clear()
					jets_phi.clear()
					jets_mass.clear()
					jets_btag.clear()
					jets_pt.clear()
					jets_eta.clear()
					jets_phi.clear()
					jets_mass.clear()
					jets_btag.clear()
					jets_fatjet.clear()
					for j2 in index_array2:
#						print j_i
						j2=int(j2)
#						print tree.Jet_pt[j2]
						jets_pt.push_back(tree.Jet_pt[j2])
						jets_eta.push_back(tree.Jet_eta[j2])
						jets_phi.push_back(tree.Jet_phi[j2])
						jets_mass.push_back(tree.Jet_mass[j2])
						jets_btag.push_back(tree.Jet_btagCMVAV2[j2])
						jets_fatjet.push_back(jets_btag_array[j_i][2])

						j_i=j_i+1
					i1[0]=cross_section
					
					q1[0]=tree.Vtype
					o1[0]=puWeight
					p1[0]=norm
					r1[0]=count_jetsoutsidef
					s1[0]=count_fatjets					
					t1[0]=tree.evt
					#print jets_btag[0],  jets_btag[1], jets_btag[-1]

					print len(jets_btag), "lenght"
#					print jets_fatjet[0]
					print fatjets_mpruned[0]
					MyTree.Fill()


					
	MyTree.Write()
	MyTree2.Write()
	AnaysisFile_boosted.Close()

	myFile.Close()
	


