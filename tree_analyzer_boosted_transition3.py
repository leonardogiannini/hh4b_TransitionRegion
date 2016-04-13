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


File_tr=TFile.Open("trigger_objects.root", "R")
histo_efficiency=copy.copy(File_tr.Get("histo_efficiency"))
File_tr.Close()
def trigger_function(histo_efficiency,htJet30=700):
	result = histo_efficiency.GetBinContent(htJet30)
	return result


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



def tree_preselection(file_string, isData=0, dataset="", cross_section=1.,systematic="", bbtag_cut=0.3,jet_btag_cut=-2):
	print dataset
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

	xsec=cross_section
	print xsec, "cross_section"	
	
	
	AnaysisFile_boosted=TFile("presel_Transition_"+systematic+"_"+file_string.split("/")[-1], "recreate")
	MyTree = TTree("MyTree", "MyTree")
		
	fatjets_pt= vector('double')()
	fatjets_eta= vector('double')()
	fatjets_phi= vector('double')()
	fatjets_mass= vector('double')()
	fatjets_mpruned= vector('double')()
	fatjets_bbtag= vector('double')()
	inv_mass= vector('double')()

	jets_pt= vector('double')()
	jets_eta= vector('double')()
	jets_phi= vector('double')()
	jets_mass= vector('double')()
	jets_btag= vector('double')()
	jets_fatjet= vector('double')()

	b_evt=array.array('f', [0.])
	CMVAweight= vector('double')()
	CMVAweightUp= vector('double')()
	CMVAweightDown= vector('double')()


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
	jb_6=MyTree.Branch("jets_fatjet", jets_fatjet)
	b_7=MyTree.Branch("CMVAweight", CMVAweight)
	b_8=MyTree.Branch("CMVAweightUp", CMVAweightUp)
	b_9=MyTree.Branch("CMVAweightDown", CMVAweightDown)

	b_7=MyTree.Branch("Vtype", q1, "Vtype")
	b_8=MyTree.Branch("puWeight", o1, "puWeight")
	b_9=MyTree.Branch("norm", p1, "norm")
	b_10=MyTree.Branch("n_OkJets_byCSV", r1, "n_OkJets_byCSV")
	b_11=MyTree.Branch("n_OkFj", s1, "n_OkFj")
	b_12=MyTree.Branch("evt", t1, "evt")
	b_13=MyTree.Branch("cross_section", i1, "cross_section")
	b_14=MyTree.Branch("boosted_evt", b_evt, "boosted_evt")
	
	
#	print tree
	maxi=tree.GetEntries()
	for entry in range(maxi):
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

			if (tree.Vtype==-1 or tree.Vtype==4):
				count_fatjets=0
				count_jetsoutsidef=0
				leading_mass_old=40.
				leading_index=-1
				Fatjets_array=numpy.zeros((10, 2))
				jets_btag_array=numpy.zeros((20, 4))
				Fatjets_array=Fatjets_array-1
				jets_btag_array=jets_btag_array-1

				if tree.nFatjetAK08ungroomed>1:
					if systematic=="JEC_Up":
						print systematic
					elif systematic=="JEC_Down":
						print systematic
					elif systematic=="JER_Up":
						print systematic
					elif systematic=="JER_Down":
						print systematic

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
						if tree.FatjetAK08ungroomed_mpruned[n]>0:
							correction_factor=tree.FatjetAK08ungroomed_mprunedcorr[n]/tree.FatjetAK08ungroomed_mpruned[n]
						else: correction_factor=1
						print correction_factor, "correction_factor"
						if (abs(tree.FatjetAK08ungroomed_eta[leading_index])<jet_eta_cut and tree.FatjetAK08ungroomed_bbtag[leading_index]>bbtag_cut and tree.FatjetAK08ungroomed_mpruned[leading_index]>40 and (tree.FatjetAK08ungroomed_tau2[leading_index]/tree.FatjetAK08ungroomed_tau1[leading_index])<tau21_cut):
	#						print "atcut ", 2
				
							count_fatjets=count_fatjets+1
							fj_p4=TLorentzVector()					
							fj_p4.SetPtEtaPhiM(tree.FatjetAK08ungroomed_pt[leading_index], tree.FatjetAK08ungroomed_eta[leading_index], tree.FatjetAK08ungroomed_phi[leading_index], tree.FatjetAK08ungroomed_mass[leading_index])								
							fj_p4.Print()
							print fj_p4.M()
							if (systematic=="FJEC_Up"): fj_p4*=correction_factor
							if (systematic=="FJEC_Down"): fj_p4*=(2-correction_factor)
							print systematic
							fj_p4.Print()
							print fj_p4.M()
							for j in range(tree.nJet):

								if (systematic=="JEC_Up"): jet_pT = tree.Jet_pt[j]*tree.Jet_corr_JECUp[j]/tree.Jet_corr[j]
								elif (systematic=="JEC_Down"): jet_pT = tree.Jet_pt[j]*tree.Jet_corr_JECDown[j]/tree.Jet_corr[j]
								elif (systematic=="JER_Up"): jet_pT = tree.Jet_pt[j]*tree.Jet_corr_JERUp[j]*tree.Jet_corr_JER[j]
								elif (systematic=="JER_Down"): jet_pT = tree.Jet_pt[j]*tree.Jet_corr_JERDown[j]*tree.Jet_corr_JER[j]

								else: jet_pT = tree.Jet_pt[j]
#								print tree.Jet_corr_JERDown[j], tree.Jet_corr_JER[j], tree.Jet_corr_JERUp[j]
								j_p4=TLorentzVector()								
								j_p4.SetPtEtaPhiM(jet_pT, tree.Jet_eta[j], tree.Jet_phi[j], tree.Jet_mass[j])						
								deltaR=j_p4.DeltaR(fj_p4)
								if (jet_pT>jet_pT_cut and abs(tree.Jet_eta[j])<jet_eta_cut and tree.Jet_btagCMVAV2[j]>jet_btag_cut and deltaR>1.5):
									count_jetsoutsidef+=1
									save_jet_index.append(j)
									
									jets_btag_array[j][0]=tree.Jet_btagCMVAV2[j]
									jets_btag_array[j][1]=j
									jets_btag_array[j][2]=leading_index
									jets_btag_array[j][3]=jet_pT
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
					print "counted", entry
					print save_jet_index, save_index
					f_i=0
					fatjets_pt.clear()
					fatjets_eta.clear()
					fatjets_phi.clear()
					fatjets_mass.clear()
					fatjets_mpruned.clear()
					fatjets_bbtag.clear()

					for j in save_index:
						correction_factor=tree.FatjetAK08ungroomed_mprunedcorr[j]/tree.FatjetAK08ungroomed_mpruned[j]
						fj_p4=TLorentzVector()					
						fj_p4.SetPtEtaPhiM(tree.FatjetAK08ungroomed_pt[j], tree.FatjetAK08ungroomed_eta[j], tree.FatjetAK08ungroomed_phi[j], tree.FatjetAK08ungroomed_mass[j])
						if (systematic=="FJEC_Up"): fj_p4*=correction_factor
						if (systematic=="FJEC_Down"): fj_p4*=(2-correction_factor)
						fatjets_pt.push_back(fj_p4.Pt())
						fatjets_eta.push_back(fj_p4.Eta())
						fatjets_phi.push_back(fj_p4.Phi())
						fatjets_mass.push_back(fj_p4.M())
						fatjets_mpruned.push_back(tree.FatjetAK08ungroomed_mpruned[j])
						fatjets_bbtag.push_back(tree.FatjetAK08ungroomed_bbtag[j])
						f_i=f_i+1
#						
					jets_btag_array.view('f8,f8,f8, f8').sort(order=['f0'], axis=0)
					jets_btag_array=jets_btag_array[::-1]
					index_array2=jets_btag_array[:,1]
					pT_array2=jets_btag_array[:,3]
					index_array2=index_array2[(index_array2 >= 0)]
					print jets_btag_array
					print index_array2
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
					CMVAweight.clear()
					CMVAweightUp.clear()
					CMVAweightDown.clear()
					for j2 in index_array2:
						
						print j_i
						j2=int(j2)
						print "jet_pt +/- syst", tree.Jet_pt[j2], pT_array2[j_i]
						jets_pt.push_back(pT_array2[j_i])
						jets_eta.push_back(tree.Jet_eta[j2])
						jets_phi.push_back(tree.Jet_phi[j2])
						jets_mass.push_back(tree.Jet_mass[j2])
						jets_btag.push_back(tree.Jet_btagCMVAV2[j2])
						jets_fatjet.push_back(jets_btag_array[j_i][2])

						if isData==1:
							CMVAweight.push_back(1)
							CMVAweightUp.push_back(1)
							CMVAweightDown.push_back(1)
						else:
							CMVAweight.push_back(tree.Jet_btagCMVAV2MSF[j2])
							CMVAweightUp.push_back(tree.Jet_btagCMVAV2MSF_Up[j2])
							CMVAweightDown.push_back(tree.Jet_btagCMVAV2MSF_Down[j2])

						j_i=j_i+1
					i1[0]=cross_section
					
					q1[0]=tree.Vtype
					o1[0]=puWeight
					p1[0]=norm
					r1[0]=count_jetsoutsidef
					s1[0]=count_fatjets					
					t1[0]=tree.evt
					
					print len(jets_btag), "lenght"
					print jets_fatjet[0]
					print fatjets_mpruned[0]
					MyTree.Fill()

	MyTree.Write()
	AnaysisFile_boosted.Close()
	myFile.Close()


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
	f_mass_corr=array.array('f', [0.])
	htJet40eta3=array.array('f', [0.])
	trigPass=array.array('f', [0.])
	event_flavour=array.array('f', [0.])
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
				if systematic=="JEC_Up":
					print systematic
				elif systematic=="JEC_Down":
					print systematic
				elif systematic=="JER_Up":
					print systematic
				elif systematic=="JER_Down":
					print systematic

				if (abs(tree.FatjetAK08ungroomed_eta[0])<2.5 and abs(tree.FatjetAK08ungroomed_eta[1])<2.5):
					if abs(tree.FatjetAK08ungroomed_eta[0]-tree.FatjetAK08ungroomed_eta[1])<1.3:
						fatjet_pt[0]=tree.FatjetAK08ungroomed_pt[0]
						fatjet_mpruned[0]=tree.FatjetAK08ungroomed_mpruned[0]
						fatjet_hbb[0]=tree.FatjetAK08ungroomed_bbtag[0]
						if tree.FatjetAK08ungroomed_tau1[0]>0:
							fatjet_tau21[0]=tree.FatjetAK08ungroomed_tau2[0]/tree.FatjetAK08ungroomed_tau1[0]
						else:
							fatjet_tau21[0]=1
						fatjet2_pt[0]=tree.FatjetAK08ungroomed_pt[1]						
						fatjet2_mpruned[0]=tree.FatjetAK08ungroomed_mpruned[1]
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

						htJet40eta3[0] = ht_
						trigPass[0]=tree.HLT_BIT_HLT_PFHT800_v
						event_flavour[0]=-100
						if tree.FatjetAK08ungroomed_BhadronFlavour[0]>=2:
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
	


