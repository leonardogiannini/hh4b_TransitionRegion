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
	
#	r=((mH1-mH1_c)**2+(mH2-mH2_c)**2)**0.5

#	angle=math.atan2(mH2-mH2_c, mH1-mH1_c)
#	print "(mH1, mH2) = (", mH1, ", ", mH2, ") lies in region "

#	ret=-1
#	if (r<r1):
#		ret=0
#		print "qualcosa0"
#	elif (r>r1 and r<r2):
#	
#		if (angle>=0 and angle<pi/2.): ret=1
#		elif (angle>=pi/2. and angle<pi): ret=4
#		elif (angle<0 and angle>=-pi/2.): ret=2
#		elif (angle<pi/2.and angle>=-pi): ret=3
#		else: print "This is within annulus but not within any CR!"
#	
	else: ret=5	
	print ret
	return ret
	
from ROOT import *
import array, os, sys, numpy, copy
#from purity_test import *
jet_pT_cut=40
jet_eta_cut=2.5
jet_btag_cut=0.605
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


def plot_maker(file_string, variable, plot, plot2d, isData=0):
	listofplots=[]
	selection_list=selections()
	
	
	try:
		myFile=TFile("../V20samples/"+file_string, "R")
		tree=myFile.Get("tree")
		tree.Print("*AA*")
	except:
		myFile=TFile("/scratch/arizzi/merge/"+file_string, "R")
		tree=myFile.Get("tree")
	friendfilename="../V20samples/ftree_"+file_string
	ff=TFile.Open(friendfilename, "R")
	ftree=ff.Get("ftree")
	tree.AddFriend("ftree", ff)		
	histo_weight=myFile.Get("CountWeighted")
	norm=histo_weight.GetBinContent(1)
	
	for s in selection_list:
		plot.SetName(s.name)
		plot.SetTitle(s.name)	
		listofplots.append(copy.copy(plot))
	for s in selection_list:
		plot2d.SetName(s.name+"_2d")
		plot2d.SetTitle(s.name)	
		listofplots.append(copy.copy(plot2d))
	
	print listofplots
	tree.GetEntry(1)
	xsec=ftree.cross_section
	print xsec
		
	AnaysisFile=TFile("analyzerCR_"+file_string, "recreate")		
	MyTree = TTree("MyTree", "MyTree")
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
	
	b_1=MyTree.Branch("Inv_mass", f1, "Invariant mass")
	b_2=MyTree.Branch("dijet_mass", g1, "dijet_mass")
	b_3=MyTree.Branch("fatjet_mass", h1, "fatjet_mass")
	b_4=MyTree.Branch("cross_section", i1, "cross_section")
	b_5=MyTree.Branch("fatjet_hbb", l1, "fatjet_hbb")
#	b_6=ftree.Branch("fatjet_tau21", m1, "fatjet_tau21")
	b_7=MyTree.Branch("Vtype", q1, "Vtype")
	b_8=MyTree.Branch("puWeight", o1, "puWeight")
	b_9=MyTree.Branch("norm", p1, "norm")
	b_10=MyTree.Branch("n_OkJets", r1, "n_OkJets")
	b_11=MyTree.Branch("n_OkFj", s1, "n_OkFj")
#	print tree
	mini=tree.GetEntries()
	for entry in range(tree.GetEntries()):
#		print entry
		tree.GetEntry(entry)
		weight=(ftree.cross_section)*(tree.puWeight)/norm
		if (tree.json==1 and (tree.HLT_BIT_HLT_AK8DiPFJet250_200_TrimMass30_BTagCSV0p45_v>0 or tree.HLT_BIT_HLT_PFHT800_v>0 or tree.HLT_HH4bHighLumi>0)):
			count_fatjets=0
			count_jetsoutsidef=0		
			leading_mass_old=40.
			leading_index=-1
			Fatjets_array=numpy.zeros((10, 2))
			Fatjets_array=Fatjets_array-1
			for n in range(tree.nFatjetAK08ungroomed):
				Fatjets_array[n][0]=tree.FatjetAK08ungroomed_mpruned[n]
				Fatjets_array[n][1]=n
	#					print "il mio vettore", Fatjets_array

			Fatjets_array.view('f8,f8').sort(order=['f0'], axis=0)
			Fatjets_array=Fatjets_array[::-1]
			index_array=Fatjets_array[:,1]

	#		index_array=index_array[(index_array >= 0)]
			save_index=[]
			for n1 in index_array:
				n=int(n1)				
				leading_index=n				
				if (leading_index>=0):
					if (abs(tree.FatjetAK08ungroomed_eta[leading_index])<jet_eta_cut and tree.FatjetAK08ungroomed_bbtag[leading_index]<bbtag_cut and tree.FatjetAK08ungroomed_mpruned[leading_index]>40 and (tree.FatjetAK08ungroomed_tau2[leading_index]/tree.FatjetAK08ungroomed_tau1[leading_index])<tau21_cut):
						print "atcut ", 2
					
						count_fatjets=count_fatjets+1
						fj_p4=TLorentzVector()					
						fj_p4.SetPtEtaPhiM(tree.FatjetAK08ungroomed_pt[leading_index], tree.FatjetAK08ungroomed_eta[leading_index], tree.FatjetAK08ungroomed_phi[leading_index], tree.FatjetAK08ungroomed_mass[leading_index])								
						for j in range(tree.nJet):
							j_p4=TLorentzVector()								
							j_p4.SetPtEtaPhiM(tree.Jet_pt[j], tree.Jet_eta[j], tree.Jet_phi[j], tree.Jet_mass[j])						
							deltaR=j_p4.DeltaR(fj_p4)
							if (tree.Jet_pt[j]>jet_pT_cut and abs(tree.Jet_eta[j])<jet_eta_cut and tree.Jet_btagCSV[j]>jet_btag_cut and deltaR>1.5):
								count_jetsoutsidef+=1
								if count_jetsoutsidef>1:
									save_index.append(leading_index)

			if (count_jetsoutsidef>=2 and count_fatjets>=1):
				print "counted"
				
				foundHH=0
				m_diff_old=50.								
				H1fatjet_i=-1
				H2jet1_i=-1
				H2jet2_i=-1
				fatjet_p4=TLorentzVector()
				jet3_p4=TLorentzVector()
				jet4_p4=TLorentzVector()
		
				for j in save_index:

					fatjet_p4.SetPtEtaPhiM(tree.FatjetAK08ungroomed_pt[j], tree.FatjetAK08ungroomed_eta[j], tree.FatjetAK08ungroomed_phi[j], tree.FatjetAK08ungroomed_mass[j])
			
					for k in range(tree.nJet):									
						jet3_p4.SetPtEtaPhiM(tree.Jet_pt[k], tree.Jet_eta[k], tree.Jet_phi[k], tree.Jet_mass[k])
						for l in range(tree.nJet):
							if (l!=k):
								jet4_p4.SetPtEtaPhiM(tree.Jet_pt[l], tree.Jet_eta[l], tree.Jet_phi[l], tree.Jet_mass[l])
								deltaRfat3=jet3_p4.DeltaR(fatjet_p4)
								deltaRfat4=jet4_p4.DeltaR(fatjet_p4)										
								deltaR2=jet3_p4.DeltaR(jet4_p4)							
								m_diff=abs(tree.FatjetAK08ungroomed_mpruned[j]+10-(jet3_p4+jet4_p4).M())
								if (tree.Jet_pt[l]>jet_pT_cut and abs(tree.Jet_eta[l])<jet_eta_cut and tree.Jet_btagCSV[l]>jet_btag_cut and deltaRfat4>1.5):
									if (tree.Jet_pt[k]>jet_pT_cut and abs(tree.Jet_eta[k])<jet_eta_cut and tree.Jet_btagCSV[k]>jet_btag_cut and deltaRfat3>1.5):
								
							
										if (m_diff<m_diff_old and deltaRfat3>1.5 and deltaRfat4>1.5 and deltaR2<1.5):

											H1fatjet_i=j
											H2jet1_i=k
											H2jet2_i=l															
											m_diff_old=m_diff									
											foundHH=1
			
				if (foundHH==1):
					
					fatjet_p4.SetPtEtaPhiM(tree.FatjetAK08ungroomed_pt[H1fatjet_i], tree.FatjetAK08ungroomed_eta[H1fatjet_i], tree.FatjetAK08ungroomed_phi[H1fatjet_i], tree.FatjetAK08ungroomed_mass[H1fatjet_i])
									
					print "hcandidates"
					jet3_p4.SetPtEtaPhiM(tree.Jet_pt[H2jet1_i], tree.Jet_eta[H2jet1_i], tree.Jet_phi[H2jet1_i], tree.Jet_mass[H2jet1_i])
					jet4_p4.SetPtEtaPhiM(tree.Jet_pt[H2jet2_i], tree.Jet_eta[H2jet2_i], tree.Jet_phi[H2jet2_i], tree.Jet_mass[H2jet2_i])
					pTH1=(fatjet_p4).Pt()
					pTH2=(jet3_p4+jet4_p4).Pt()
					mH1=tree.FatjetAK08ungroomed_mpruned[H1fatjet_i]
					mH2=(jet3_p4+jet4_p4).M()
					listofplots[0].Fill((jet3_p4+jet4_p4+fatjet_p4).M(), weight)
					listofplots[6].Fill(mH1, mH2, weight)
					region=withinRegion(mH1, mH2, 20., 10., 110., 120.)
				
					f1[0]=(jet3_p4+jet4_p4+fatjet_p4).M()
					g1[0]=mH2
					h1[0]=mH1
					i1[0]=ftree.cross_section
					l1[0]=tree.FatjetAK08ungroomed_bbtag[H1fatjet_i]
					q1[0]=tree.Vtype
					o1[0]=tree.puWeight
					p1[0]=norm
					r1[0]=count_jetsoutsidef
					s1[0]=count_fatjets
					MyTree.Fill()
					if (region==0): 
						listofplots[1].Fill((jet3_p4+jet4_p4+fatjet_p4).M(), weight)
						listofplots[7].Fill(mH1, mH2, weight)
					elif (region==1): 
						listofplots[2].Fill((jet3_p4+jet4_p4+fatjet_p4).M(), weight)
						listofplots[8].Fill(mH1, mH2, weight)
					elif (region==2): 
						listofplots[3].Fill((jet3_p4+jet4_p4+fatjet_p4).M(), weight)
						listofplots[9].Fill(mH1, mH2, weight)
					elif (region==3): 
						listofplots[4].Fill((jet3_p4+jet4_p4+fatjet_p4).M(), weight)
						listofplots[10].Fill(mH1, mH2, weight)
					elif (region==4): 
						listofplots[5].Fill((jet3_p4+jet4_p4+fatjet_p4).M(), weight)
						listofplots[11].Fill(mH1, mH2, weight)
						print 5

					
	MyTree.Write()
	AnaysisFile.Close()
	ff.Close()
	myFile.Close()
	return listofplots
					

plot=TH1F("myplot", "myplot2", 1000, 0, 3000)
plot2d=TH2F("myplot", "myplot2", 1000, 0, 200, 1000, 0, 200)
dire=["ZZ_TuneCUETP8M1_13TeV-pythia8","WZ_TuneCUETP8M1_13TeV-pythia8","WW_TuneCUETP8M1_13TeV-pythia8","WJetsToQQ_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8","TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8","QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8","QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8","QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8","QCD_HT700to1000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8","QCD_HT500to700_TuneCUETP8M1_13TeV-madgraphMLM-pythia8","QCD_HT300to500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8",]
a=int(sys.argv[1])

print "inizio"
print a
for d in dire[a:a+1]:
	rfile=TFile(d+"_CR_sidebands1.root", "RECREATE")
	lis=plot_maker(d+".root", "", plot, plot2d, isData=0)	

	print "file"
	rfile.cd()
	for l in lis:
		l.Write()

	rfile.Close()				
				
				
