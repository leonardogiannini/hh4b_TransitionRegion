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

def region_scanner(mH2, minmass, maxmass):
	ret=0
	if (mH2>minmass and mH2<maxmass):
		ret=1
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



def tree_selection(file_string, isData=0, dataset="", cross_section=1.,bbtag_cut=0.4,jet_btag_cut=0.185):
	print dataset
	print file_string
	try:
		myFile=TFile(file_string, "R")
		tree=myFile.Get("MyTree")
		tree.Print("*AA*")
	except:
		print "no file"
	if dataset=="signal":
		name="Grav_"+file_string.split("-")[1].split("_")[0]
	else:
		name=file_string.split("_")[0]+"_"

	AnaysisFile_boosted=TFile(name+"_"+str(int(bbtag_cut*10))+"_"+str(int(jet_btag_cut*1000))+"_v2.root", "recreate")
	
	MyTree = TTree("minitree", "minitree")
	#transition region variables
	f1=array.array('f', [0.])
	g1=array.array('f', [0.])
	h1=array.array('f', [0.])
	i1=array.array('f', [0.])
	l1=array.array('f', [0.])
	m1=array.array('f', [0.])
	q1=array.array('f', [0.])
	o1=array.array('f', [0.])	
	p1=array.array('f', [0.])
	r1=array.array('f', [0.])	
	s1=array.array('f', [0.])
	t1=array.array('f', [0.])
	u1=array.array('f', [0.])

	b_1=MyTree.Branch("Inv_mass", f1, "Invariant mass")
	b_2=MyTree.Branch("dijet_mass", g1, "dijet_mass")
	b_3=MyTree.Branch("fatjet_mass", h1, "fatjet_mass")
	b_4=MyTree.Branch("cross_section", i1, "cross_section")
	b_5=MyTree.Branch("fatjet_hbb", l1, "fatjet_hbb")
	b_6=MyTree.Branch("isCR", m1, "isCR")
	b_7=MyTree.Branch("Vtype", q1, "Vtype")
	b_8=MyTree.Branch("puWeight", o1, "puWeight")
	b_9=MyTree.Branch("norm", p1, "norm")
	b_10=MyTree.Branch("n_OkJets", r1, "n_OkJets")
	b_11=MyTree.Branch("n_OkFj", s1, "n_OkFj")
	b_12=MyTree.Branch("evt", t1, "evt")
	b_13=MyTree.Branch("boosted", u1, "boosted")

#	print tree
	maxi=tree.GetEntries()
	for entry in range(maxi):
#		print entry
		tree.GetEntry(entry)
		if len(tree.fatjets_pt)>1:
			print len(tree.fatjets_pt)
		count_fatjets=0
		count_jetsoutsidef=0
		count_jetsoutsidef_atag=0
		leading_mass_old=40.
		leading_index=-1

		save_index=[]
		save_jet_index=[]
		save_atag_jet_index=[]
		for n in range(len(tree.fatjets_pt)):
			leading_index=n			
			if (tree.fatjets_bbtag[leading_index]>bbtag_cut):
				count_fatjets=count_fatjets+1
				fj_p4=TLorentzVector()
				fj_p4.SetPtEtaPhiM(tree.fatjets_pt[leading_index], tree.fatjets_eta[leading_index], tree.fatjets_phi[leading_index], tree.fatjets_mass[leading_index])
				for j in range(len(tree.jets_pt)):
					if (tree.jets_fatjet[j]==leading_index):
						j_p4=TLorentzVector()
						j_p4.SetPtEtaPhiM(tree.jets_pt[j], tree.jets_eta[j], tree.jets_phi[j], tree.jets_mass[j])						
						deltaR=j_p4.DeltaR(fj_p4)
						if (tree.jets_btag[j]>jet_btag_cut and deltaR>1.5):
							count_jetsoutsidef+=1
							save_jet_index.append(j)
						if (tree.jets_btag[j]<jet_btag_cut and deltaR>1.5):
							count_jetsoutsidef_atag+=1
							save_atag_jet_index.append(j)
				if count_jetsoutsidef>1:
					save_index.append(leading_index)
							
			
			if (count_jetsoutsidef>=2 and count_fatjets>=1):
				print "counted", entry
				print save_jet_index, save_index, save_atag_jet_index
				foundHH=0
				m_diff_old=50.								
				H1fatjet_i=-1
				H2jet1_i=-1
				H2jet2_i=-1
				fatjet_p4=TLorentzVector()
				jet3_p4=TLorentzVector()
				jet4_p4=TLorentzVector()
	
				for j in save_index:

					fatjet_p4.SetPtEtaPhiM(tree.fatjets_pt[j], tree.fatjets_eta[j], tree.fatjets_phi[j], tree.fatjets_mass[j])
		
					for k in save_jet_index:									
						jet3_p4.SetPtEtaPhiM(tree.jets_pt[k], tree.jets_eta[k], tree.jets_phi[k], tree.jets_mass[k])
						for l in save_jet_index:
							if (l!=k):
								jet4_p4.SetPtEtaPhiM(tree.jets_pt[l], tree.jets_eta[l], tree.jets_phi[l], tree.jets_mass[l])
								deltaRfat3=jet3_p4.DeltaR(fatjet_p4)
								deltaRfat4=jet4_p4.DeltaR(fatjet_p4)										
								deltaR2=jet3_p4.DeltaR(jet4_p4)							
								m_diff=abs(tree.fatjets_mpruned[j]+10-(jet3_p4+jet4_p4).M())
#								if (tree.Jet_pt[l]>jet_pT_cut and abs(tree.Jet_eta[l])<jet_eta_cut and tree.Jet_btagCMVAV2[l]>jet_btag_cut and deltaRfat4>1.5):
#									if (tree.Jet_pt[k]>jet_pT_cut and abs(tree.Jet_eta[k])<jet_eta_cut and tree.Jet_btagCMVAV2[k]>jet_btag_cut and deltaRfat3>1.5):
#								
						
								if (m_diff<m_diff_old and deltaRfat3>1.5 and deltaRfat4>1.5 and deltaR2<1.5):

									H1fatjet_i=j
									H2jet1_i=k
									H2jet2_i=l															
									m_diff_old=m_diff									
									foundHH=1
	
					if (foundHH==1):
					
						fatjet_p4.SetPtEtaPhiM(tree.fatjets_pt[H1fatjet_i], tree.fatjets_eta[H1fatjet_i], tree.fatjets_phi[H1fatjet_i], tree.fatjets_mass[H1fatjet_i])
									
						print "hcandidates"
						jet3_p4.SetPtEtaPhiM(tree.jets_pt[H2jet1_i], tree.jets_eta[H2jet1_i], tree.jets_phi[H2jet1_i], tree.jets_mass[H2jet1_i])
						jet4_p4.SetPtEtaPhiM(tree.jets_pt[H2jet2_i], tree.jets_eta[H2jet2_i], tree.jets_phi[H2jet2_i], tree.jets_mass[H2jet2_i])
						pTH1=(fatjet_p4).Pt()
						pTH2=(jet3_p4+jet4_p4).Pt()
						mH1=tree.fatjets_mpruned[H1fatjet_i]
						mH2=(jet3_p4+jet4_p4).M()
		
						region=withinRegion(mH1, mH2, 20., 10., 110., 120.)
						f1[0]=(jet3_p4+jet4_p4+fatjet_p4).M()
						g1[0]=mH2
						h1[0]=mH1
						i1[0]=tree.cross_section
						l1[0]=tree.fatjets_bbtag[H1fatjet_i]
						q1[0]=tree.Vtype
						o1[0]=tree.puWeight
						p1[0]=tree.norm
						r1[0]=count_jetsoutsidef
						s1[0]=count_fatjets
						m1[0]=0.
						t1[0]=tree.evt
						u1[0]=0.
						MyTree.Fill()

	MyTree.Write()
	AnaysisFile_boosted.Close()

	myFile.Close()

def tree_control_region(file_string, isData=0, dataset="", cross_section=1.,bbtag_cut=0.4,jet_btag_cut=0.185):
	print dataset
	try:
		myFile=TFile(file_string, "R")
		tree=myFile.Get("MyTree")
		tree.Print("*AA*")
	except:
		print "no file"
	if dataset=="signal":
		name="Grav_Atag_"+file_string.split("-")[1].split("_")[0]
	else:
		name=file_string.split("_")[0]+"_Atag"
	AnaysisFile_boosted=TFile(name+"_"+str(int(bbtag_cut*10))+"_"+str(int(jet_btag_cut*1000))+"_v2.root", "recreate")
	
	MyTree = TTree("minitree", "minitree")
	#transition region variables
	f1=array.array('f', [0.])
	g1=array.array('f', [0.])
	h1=array.array('f', [0.])
	i1=array.array('f', [0.])
	l1=array.array('f', [0.])
	m1=array.array('f', [0.])
	q1=array.array('f', [0.])
	o1=array.array('f', [0.])	
	p1=array.array('f', [0.])
	r1=array.array('f', [0.])	
	s1=array.array('f', [0.])
	t1=array.array('f', [0.])
	u1=array.array('f', [0.])

	b_1=MyTree.Branch("Inv_mass", f1, "Invariant mass")
	b_2=MyTree.Branch("dijet_mass", g1, "dijet_mass")
	b_3=MyTree.Branch("fatjet_mass", h1, "fatjet_mass")
	b_4=MyTree.Branch("cross_section", i1, "cross_section")
	b_5=MyTree.Branch("fatjet_hbb", l1, "fatjet_hbb")
	b_6=MyTree.Branch("isCR", m1, "isCR")
	b_7=MyTree.Branch("Vtype", q1, "Vtype")
	b_8=MyTree.Branch("puWeight", o1, "puWeight")
	b_9=MyTree.Branch("norm", p1, "norm")
	b_10=MyTree.Branch("n_OkJets", r1, "n_OkJets")
	b_11=MyTree.Branch("n_OkFj", s1, "n_OkFj")
	b_12=MyTree.Branch("evt", t1, "evt")
	b_13=MyTree.Branch("boosted", u1, "boosted")

#	print tree
	maxi=tree.GetEntries()
	for entry in range(maxi):
#		print entry
		tree.GetEntry(entry)
		if len(tree.fatjets_pt)>1:
			print len(tree.fatjets_pt)
		count_fatjets=0
		count_jetsoutsidef=0
		count_jetsoutsidef_atag=0
		leading_mass_old=40.
		leading_index=-1

		save_index=[]
		save_jet_index=[]
		save_atag_jet_index=[]
		for n in range(len(tree.fatjets_pt)):
			leading_index=n			
			if (tree.fatjets_bbtag[leading_index]>bbtag_cut):
				count_fatjets=count_fatjets+1
				fj_p4=TLorentzVector()
				fj_p4.SetPtEtaPhiM(tree.fatjets_pt[leading_index], tree.fatjets_eta[leading_index], tree.fatjets_phi[leading_index], tree.fatjets_mass[leading_index])
				for j in range(len(tree.jets_pt)):
					if (tree.jets_fatjet[j]==leading_index):
						j_p4=TLorentzVector()
						j_p4.SetPtEtaPhiM(tree.jets_pt[j], tree.jets_eta[j], tree.jets_phi[j], tree.jets_mass[j])						
						deltaR=j_p4.DeltaR(fj_p4)
						if (tree.jets_btag[j]>jet_btag_cut and deltaR>1.5):
							count_jetsoutsidef+=1
							save_jet_index.append(j)
						if (tree.jets_btag[j]<jet_btag_cut and deltaR>1.5):
							count_jetsoutsidef_atag+=1
							save_atag_jet_index.append(j)
				if (count_jetsoutsidef>0 and count_jetsoutsidef_atag>0 ):
					save_index.append(leading_index)
							
			
			if (count_jetsoutsidef==1 and count_jetsoutsidef_atag>0 and count_fatjets>=1):
				print "counted", entry
				print save_jet_index, save_index, save_atag_jet_index
				foundHH=0
				m_diff_old=50.								
				H1fatjet_i=-1
				H2jet1_i=-1
				H2jet2_i=-1
				fatjet_p4=TLorentzVector()
				jet3_p4=TLorentzVector()
				jet4_p4=TLorentzVector()
	
				for j in save_index:

					fatjet_p4.SetPtEtaPhiM(tree.fatjets_pt[j], tree.fatjets_eta[j], tree.fatjets_phi[j], tree.fatjets_mass[j])
		
					for k in save_jet_index:									
						jet3_p4.SetPtEtaPhiM(tree.jets_pt[k], tree.jets_eta[k], tree.jets_phi[k], tree.jets_mass[k])
						for l in save_atag_jet_index:
							if (l!=k):
								jet4_p4.SetPtEtaPhiM(tree.jets_pt[l], tree.jets_eta[l], tree.jets_phi[l], tree.jets_mass[l])
								deltaRfat3=jet3_p4.DeltaR(fatjet_p4)
								deltaRfat4=jet4_p4.DeltaR(fatjet_p4)										
								deltaR2=jet3_p4.DeltaR(jet4_p4)							
								m_diff=abs(tree.fatjets_mpruned[j]+10-(jet3_p4+jet4_p4).M())
#								if (tree.Jet_pt[l]>jet_pT_cut and abs(tree.Jet_eta[l])<jet_eta_cut and tree.Jet_btagCMVAV2[l]>jet_btag_cut and deltaRfat4>1.5):
#									if (tree.Jet_pt[k]>jet_pT_cut and abs(tree.Jet_eta[k])<jet_eta_cut and tree.Jet_btagCMVAV2[k]>jet_btag_cut and deltaRfat3>1.5):
#								
						
								if (m_diff<m_diff_old and deltaRfat3>1.5 and deltaRfat4>1.5 and deltaR2<1.5):

									H1fatjet_i=j
									H2jet1_i=k
									H2jet2_i=l															
									m_diff_old=m_diff									
									foundHH=1
	
					if (foundHH==1):
					
						fatjet_p4.SetPtEtaPhiM(tree.fatjets_pt[H1fatjet_i], tree.fatjets_eta[H1fatjet_i], tree.fatjets_phi[H1fatjet_i], tree.fatjets_mass[H1fatjet_i])
									
						print "hcandidates"
						jet3_p4.SetPtEtaPhiM(tree.jets_pt[H2jet1_i], tree.jets_eta[H2jet1_i], tree.jets_phi[H2jet1_i], tree.jets_mass[H2jet1_i])
						jet4_p4.SetPtEtaPhiM(tree.jets_pt[H2jet2_i], tree.jets_eta[H2jet2_i], tree.jets_phi[H2jet2_i], tree.jets_mass[H2jet2_i])
						pTH1=(fatjet_p4).Pt()
						pTH2=(jet3_p4+jet4_p4).Pt()
						mH1=tree.fatjets_mpruned[H1fatjet_i]
						mH2=(jet3_p4+jet4_p4).M()
		
						region=withinRegion(mH1, mH2, 20., 10., 110., 120.)
						f1[0]=(jet3_p4+jet4_p4+fatjet_p4).M()
						g1[0]=mH2
						h1[0]=mH1
						i1[0]=tree.cross_section
						l1[0]=tree.fatjets_bbtag[H1fatjet_i]
						q1[0]=tree.Vtype
						o1[0]=tree.puWeight
						p1[0]=tree.norm
						r1[0]=count_jetsoutsidef
						s1[0]=count_fatjets
						m1[0]=1.
						t1[0]=tree.evt
						u1[0]=tree.boosted_evt
						MyTree.Fill()

	MyTree.Write()
	AnaysisFile_boosted.Close()

	myFile.Close()




