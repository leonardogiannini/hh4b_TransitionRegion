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
#	print ret
#	return ret

def tree_search(path):
	import os
	file_list=os.listdir(path)
	#print file_list
	true_list=[]
	for el in file_list:
		if (el.startswith("tree")):
			true_list.append(el)
	if (true_list!=[]):		
		return true_list, path
	else:
		try:		
			true_list=tree_search(path+"/"+file_list[0])
		except:
			return true_list
		return true_list


area="/gpfs/ddn/srm/cms/store/user/arizzi/VHBBHeppyV20a/"
samples=[

#"GluGluToBulkGravitonToHHTo4B_M-260_narrow_13TeV-madgraph",
#"GluGluToBulkGravitonToHHTo4B_M-270_narrow_13TeV-madgraph",
#"GluGluToBulkGravitonToHHTo4B_M-300_narrow_13TeV-madgraph",
#"GluGluToBulkGravitonToHHTo4B_M-350_narrow_13TeV-madgraph",
##"GluGluToBulkGravitonToHHTo4B_M-400_narrow_13TeV-madgraph",
#"GluGluToBulkGravitonToHHTo4B_M-450_narrow_13TeV-madgraph",
"GluGluToBulkGravitonToHHTo4B_M-500_narrow_13TeV-madgraph",
"GluGluToBulkGravitonToHHTo4B_M-550_narrow_13TeV-madgraph",
#"GluGluToBulkGravitonToHHTo4B_M-600_narrow_13TeV-madgraph",
"GluGluToBulkGravitonToHHTo4B_M-650_narrow_13TeV-madgraph",
"GluGluToBulkGravitonToHHTo4B_M-700_narrow_13TeV-madgraph",
#"GluGluToBulkGravitonToHHTo4B_M-800_narrow_13TeV-madgraph",
"GluGluToBulkGravitonToHHTo4B_M-900_narrow_13TeV-madgraph",

"RSGravTohhTohbbhbb_narrow_M-1000_13TeV-madgraph",
"RSGravTohhTohbbhbb_narrow_M-1200_13TeV-madgraph",
#"RSGravTohhTohbbhbb_narrow_M-1400_13TeV-madgraph",
#"RSGravTohhTohbbhbb_narrow_M-1600_13TeV-madgraph",
"RSGravTohhTohbbhbb_narrow_M-1800_13TeV-madgraph",
"RSGravTohhTohbbhbb_narrow_M-2000_13TeV-madgraph",
#"RSGravTohhTohbbhbb_narrow_M-2500_13TeV-madgraph",
#"RSGravTohhTohbbhbb_narrow_M-3000_13TeV-madgraph",
#"RSGravTohhTohbbhbb_narrow_M-3500_13TeV-madgraph",
]

table1=[]
table2=[]

from ROOT import *
import array, os, sys, numpy, array
from copy import copy
from purity_test import *
jet_pT_cut=40
jet_eta_cut=2.5
jet_btag_cut=0.605

c1=TCanvas("c","c")
c1.SetLogy()
#sel_string=sys.argv[1]+".root"
from ROOT import *
import array, os, sys
table1=[]
plot_list=[]

for sample in samples:

	AnalysisFile=TFile(sample+"_analyzer.root", "recreate")	
	print AnalysisFile	
	MyTree = TTree("MyTree", "MyTree")
	print MyTree
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



	plot=TH1F(sample+"_dijet_mass", "myplot2", 100, 0, 300)
	plot2=TH1F(sample+"_fatjet_mass", "myplot2", 100, 0, 300)

	plotSR=TH1F(sample+"_dijet_massSR", "myplot2", 100, 0, 300)
	plot2SR=TH1F(sample+"_fatjet_massSR", "myplot2", 100, 0, 300)

	hmass32=TH1F(sample+"purity3", "myplot2", 1000, 0, 3000)

	hmass22=TH1F(sample+"purity2", "myplot2", 1000, 0, 3000)		

	hmass12=TH1F(sample+"purity1", "myplot2", 1000, 0, 3000)

	hmass02=TH1F(sample+"purity0", "myplot2", 1000, 0, 3000)

	mypath=area+sample
	file_list=tree_search(mypath)
	true_list=[]
	if file_list!=[]:
		for f in file_list[0]:
			#print f, file_list[1]
			true_list.append(file_list[1]+"/"+f)

	cutflow=[0. for i in range(5)]
	total=[0. for i in range(5)]
	print true_list
	for el in true_list:
		hline_provv=[]
		name=el.split("/")
		myFile=TFile.Open(el, "R")
		tree=myFile.Get("tree")
		friendfilename=sample+"/f"+name[-1]	
#		print friendfilename		
#		ff=TFile.Open(friendfilename, "R")
#		ftree=ff.Get("ftree")
#		ftree.Print()
#		tree.AddFriend("ftree", ff)		
#		print tree.GetEntriesFast(), ftree.GetEntriesFast()
		groups=["ungroomed", "pruned" ]

		maxi=tree.GetEntries()
		for entry in range(maxi):
#			print entry
			tree.GetEntry(entry)
			total[0]=total[0]+1
			if (tree.HLT_BIT_HLT_PFHT800_v>0 or tree.HLT_HH4bHighLumi>0 or tree.HLT_BIT_HLT_AK8DiPFJet250_200_TrimMass30_BTagCSV0p45_v>0):
#				print "trigger"
				cutflow[0]=cutflow[0]+1
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
	#			print Fatjets_array
				Fatjets_array.view('f8,f8').sort(order=['f0'], axis=0)
				Fatjets_array=Fatjets_array[::-1]
				index_array=Fatjets_array[:,1]
	#			print Fatjets_array[:,0]
	#			print index_array
		#		index_array=index_array[(index_array >= 0)]
				save_index=[]
				for n1 in index_array:
					if (n1>0):
						n=int(n1)				
						leading_index=n
		#				print leading_index
						if (leading_index>=0):
							if (abs(tree.FatjetAK08ungroomed_eta[leading_index])<jet_eta_cut and tree.FatjetAK08ungroomed_bbtag[leading_index]>0.4 and tree.FatjetAK08ungroomed_mpruned[leading_index]>40 and (tree.FatjetAK08ungroomed_tau2[leading_index]/tree.FatjetAK08ungroomed_tau1[leading_index])<0.6):
								if count_fatjets==0:
									total[1]=total[1]+1
									cutflow[1]=cutflow[1]+1
								count_fatjets=count_fatjets+1
								fj_p4=TLorentzVector()					
								fj_p4.SetPtEtaPhiM(tree.FatjetAK08ungroomed_pt[leading_index], tree.FatjetAK08ungroomed_eta[leading_index], tree.FatjetAK08ungroomed_phi[leading_index], tree.FatjetAK08ungroomed_mpruned[leading_index])								
								for j in range(tree.nJet):
									j_p4=TLorentzVector()								
									j_p4.SetPtEtaPhiM(tree.Jet_pt[j], tree.Jet_eta[j], tree.Jet_phi[j], tree.Jet_mass[j])						
									deltaR=j_p4.DeltaR(fj_p4)
									if (tree.Jet_pt[j]>jet_pT_cut and abs(tree.Jet_eta[j])<jet_eta_cut and tree.Jet_btagCSV[j]>jet_btag_cut and deltaR>1.5):
										count_jetsoutsidef+=1
										if count_jetsoutsidef>1:
											save_index.append(leading_index)
#				print count_jetsoutsidef, count_fatjets
				if (count_jetsoutsidef>=2 and count_fatjets>=1):
#					print "counted"
				
					total[2]=total[2]+1					
					cutflow[2]=cutflow[2]+1
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
						cutflow[3]=cutflow[3]+1
						total[3]=total[3]+1
						fatjet_p4.SetPtEtaPhiM(tree.FatjetAK08ungroomed_pt[H1fatjet_i], tree.FatjetAK08ungroomed_eta[H1fatjet_i], tree.FatjetAK08ungroomed_phi[H1fatjet_i], tree.FatjetAK08ungroomed_mass[H1fatjet_i])
						
#						print "hcandidates"
						jet3_p4.SetPtEtaPhiM(tree.Jet_pt[H2jet1_i], tree.Jet_eta[H2jet1_i], tree.Jet_phi[H2jet1_i], tree.Jet_mass[H2jet1_i])
						jet4_p4.SetPtEtaPhiM(tree.Jet_pt[H2jet2_i], tree.Jet_eta[H2jet2_i], tree.Jet_phi[H2jet2_i], tree.Jet_mass[H2jet2_i])
						plot.Fill((jet3_p4+jet4_p4).M())
						plot2.Fill(tree.FatjetAK08ungroomed_mpruned[H1fatjet_i])
						pTH1=(fatjet_p4).Pt()
						pTH2=(jet3_p4+jet4_p4).Pt()
						mH1=tree.FatjetAK08ungroomed_mpruned[H1fatjet_i]
						mH2=(jet3_p4+jet4_p4).M()
				
						region=withinRegion(mH1, mH2, 20., 10., 110., 120.)
						AnalysisFile.cd()
						f1[0]=(jet3_p4+jet4_p4+fatjet_p4).M()
						g1[0]=mH2
						h1[0]=mH1
						i1[0]=1.
						l1[0]=tree.FatjetAK08ungroomed_bbtag[H1fatjet_i]
						q1[0]=tree.Vtype
						o1[0]=tree.puWeight
						p1[0]=1.
						r1[0]=count_jetsoutsidef
						s1[0]=count_fatjets
						MyTree.Fill()
						MyTree.Print()
						print MyTree
						if (region==0): 
							plotSR.Fill((jet3_p4+jet4_p4).M())	
							plot2SR.Fill(tree.FatjetAK08ungroomed_mpruned[H1fatjet_i])										
							cutflow[4]=cutflow[4]+1
							total[4]=total[4]+1
#							print 0
							b1_p4=TLorentzVector()
							b2_p4=TLorentzVector()
							b3_p4=TLorentzVector()
							b4_p4=TLorentzVector()
							b1_p4.SetPtEtaPhiM(tree.GenBQuarkFromH_pt[0], tree.GenBQuarkFromH_eta[0], tree.GenBQuarkFromH_phi[0], tree.GenBQuarkFromH_mass[0])
							b2_p4.SetPtEtaPhiM(tree.GenBQuarkFromH_pt[1], tree.GenBQuarkFromH_eta[1], tree.GenBQuarkFromH_phi[1], tree.GenBQuarkFromH_mass[1])
							b3_p4.SetPtEtaPhiM(tree.GenBQuarkFromH_pt[2], tree.GenBQuarkFromH_eta[2], tree.GenBQuarkFromH_phi[2], tree.GenBQuarkFromH_mass[2])
							b4_p4.SetPtEtaPhiM(tree.GenBQuarkFromH_pt[3], tree.GenBQuarkFromH_eta[3], tree.GenBQuarkFromH_phi[3], tree.GenBQuarkFromH_mass[3])
							h1_p4=TLorentzVector()
							h2_p4=TLorentzVector()
							h1_p4.SetPtEtaPhiM(tree.GenHiggsBoson_pt[0], tree.GenHiggsBoson_eta[0], tree.GenHiggsBoson_phi[0], tree.GenHiggsBoson_mass[0])
							h2_p4.SetPtEtaPhiM(tree.GenHiggsBoson_pt[1], tree.GenHiggsBoson_eta[1], tree.GenHiggsBoson_phi[1], tree.GenHiggsBoson_mass[1])
							j=[jet3_p4, jet4_p4, fatjet_p4] 
							b=[b1_p4, b2_p4, b3_p4, b4_p4, h1_p4, h2_p4]

							jMatchedbindex=[-1, -1, -1]
							purity=purityTest21(j, b, jMatchedbindex)
#							print "purity", purity
#							print jMatchedbindex
							if (purity==3):
								hmass32.Fill((jet3_p4+jet4_p4+fatjet_p4).M())
							elif (purity==2):
								hmass22.Fill((jet3_p4+jet4_p4+fatjet_p4).M())			
							elif (purity==1):
								hmass12.Fill((jet3_p4+jet4_p4+fatjet_p4).M())
							else:
								hmass02.Fill((jet3_p4+jet4_p4+fatjet_p4).M())
		
		myFile.Close()
#		ff.Close()
		
	plot_list.append(copy(plot))
	plot_list.append(copy(plot2))
	plot_list.append(copy(plotSR))
	plot_list.append(copy(plot2SR))

	plot_list.append(copy(hmass32))
	plot_list.append(copy(hmass22))
	plot_list.append(copy(hmass12))
	plot_list.append(copy(hmass02))
	table1.append(cutflow)	
	table2.append(total)
	MyTree.Write()
	MyTree.Print()
	AnalysisFile.Close()

fille=TFile("signal_1_calibration.root", "RECREATE")
for p in plot_list:
	
	p.Write()
fille.Close
	
print table1
print table2 
c1=TCanvas("c","c", 800, 400)
#c1.SetLogx()
c1.SetGrid()
graph_list=[]
cuts=["0","1 suitable Fatjet","1 + 2 suitable jets","HH candidates","Signal Region",]
for c in range(len(cuts)):
	graph=TGraph(len(samples)-1)
	graph.SetName("cut_number_"+str(c))
	for s in samples:
#		print table1[samples.index(s)]
#		print table1[samples.index(s)][-1]
		if (float(table1[samples.index(s)][c])!=0 and table2[samples.index(s)][0]!=0):
	
			graph.SetPoint(samples.index(s),int((s.split("-")[1]).split("_")[0]), float(table1[samples.index(s)][c])/table2[samples.index(s)][0])
##			print int((s.split("-")[1]).split("_")[0]), float(table1[samples.index(s)][c][0])/table2[samples.index(s)][c][0]
		else:
			graph.SetPoint(samples.index(s),int((s.split("-")[1]).split("_")[0]), 0.)
	graph.SetMarkerStyle(33)
	if c==0:
		graph.SetLineColor(kViolet)
		graph.SetMarkerColor(kViolet)
	
	elif c<2:
		graph.SetLineColor((c)%4+kGreen)
		graph.SetMarkerColor((c)%4+kGreen)
	elif c<3:
		graph.SetLineColor((c)%4+kPink)
		graph.SetMarkerColor((c)%4+kPink)
	elif c<4:
		graph.SetLineColor((c)%4+kViolet)
		graph.SetMarkerColor((c)%4+kViolet)
	elif c<5:
		graph.SetLineColor((c)%4+kOrange)
		graph.SetMarkerColor((c)%4+kOrange)
	elif c<25:
		graph.SetLineColor((c)%4+kAzure)
		graph.SetMarkerColor((c)%4+kAzure)
	elif c<29:
		graph.SetLineColor((c)%4+kTeal)
		graph.SetMarkerColor((c)%4+kTeal)
	elif c<33:
		graph.SetLineColor(kRed)
		graph.SetMarkerColor(kRed)
	elif c<37:
		graph.SetLineColor(kCyan)
		graph.SetMarkerColor(kCyan)
	elif c<41:
		graph.SetLineColor(kMagenta)
		graph.SetMarkerColor(kMagenta)
	elif c<45:
		graph.SetLineColor(kOrange)
		graph.SetMarkerColor(kOrange)

	graph.SetLineWidth(1)
	graph_list.append(graph)


print graph_list
#print graph_list
vuoto=TGraph(2)
vuoto.SetPoint(0,350,0.)
vuoto.SetPoint(1,3500,1.0)
vuoto.SetMarkerColor(0)
vuoto.SetLineColor(0)

vuoto.GetXaxis().SetTitle("Signal Mass [Gev]")
vuoto.GetYaxis().SetTitle("Signal Efficiency")

vuoto.Draw("ALP")
legend=TLegend(0.70,0.12,0.96,0.89)
legend.SetFillColorAlpha(0,0.)
for c in range(0,len(graph_list)):
	print graph_list[c].GetName()
	graph_list[c].Draw("LP same")
	if c==0:
		legend.AddEntry(graph_list[c], "Trigger", "l")
		print "7"
#	elif c<5:
#		legend.AddEntry(graph_list[c], "PFHT900_v, w preselection", "l")
#	elif c<9:
#		legend.AddEntry(graph_list[c], "AK8DiPFJet280, w preselection", "l")
#	elif c<13:
#		legend.AddEntry(graph_list[c], "AK8PFHT700, w preselection", "l")
#	elif c<17:
#		legend.AddEntry(graph_list[c], "AK8PFJet360, w preselection", "l")
#	elif c<21:
#		legend.AddEntry(graph_list[c], "Resolved", "l")x
	else:
		legend.AddEntry(graph_list[c], cuts[c], "l")

	
legend.SetBorderSize(0) 
legend.SetTextSize(0.03)	
legend.Draw("L")
c1.Print("obj_trigger.pdf")


