# TEST AREA
import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy,numpy, copy

# Our functions:
import Alphabet_Header
from Alphabet_Header import *
import Plotting_Header
from Plotting_Header import *
import Converters
from Converters import *
import Distribution_Header
from Distribution_Header import *
import Alphabet
from Alphabet import *
import CMS_lumi, tdrstyle

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_13TeV = "2.2 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12

iPeriod =4

# FORMAT IS:
# dist = ("name", "location of file", "name of tree", "weight (can be more complicated than just a number, see MC example below)")
QCD = DIST("Data", "files_76x/data_76x_boosted.root", "MyTree2", "1.")

# Now we arrange them correctly:

DistsWeWantToEstiamte = [QCD]

#tag = "(dijetmass_corr>800&jet1tau21<0.6&jet2tau21<0.6&(jet2pmass<130&jet2pmass>90)&(jet1pmass<130&jet1pmass>100)&(jet1bbtag>0.6&jet2bbtag>0.6)&triggerpass>0.)"
#antitag = "(dijetmass_corr>800&jet1tau21<0.6&jet2tau21<0.6&(jet2pmass<130&jet2pmass>90)&(jet1pmass<130&jet1pmass>100)&(jet1bbtag<0.6&jet2bbtag>0.6)&triggerpass>0.)"


binBoundaries = [ 800, 838, 890, 944, 1000, 1058, 1118, 1181, 1246, 1313, 1383, 1455, 1530, 1607, 1687,1770, 1856, 1945, 2037, 2132, 2231, 2332, 2438, 2546, 2659, 2775, 2895, 3019 ]
FILE = TFile("Hbb_output.root", "RECREATE")

V = TH1F("data_obs", "", len(binBoundaries)-1, array('d',binBoundaries))
N = TH1F("QCD", "", len(binBoundaries)-1, array('d',binBoundaries))
NU = TH1F("QCD_CMS_scale_13TeVUp", "", len(binBoundaries)-1, array('d',binBoundaries))
ND = TH1F("QCD_CMS_scale_13TeVDown", "", len(binBoundaries)-1, array('d',binBoundaries)) 

A =  TH1F("QCD_Antitag", "", len(binBoundaries)-1, array('d',binBoundaries)) 


#Iniatialize the Alphabet class
HbbTest = Alphabetizer("QCDalphaTest", DistsWeWantToEstiamte, [])

# apply a preselection to the trees:
#presel = "(dijetmass>1000&(jet2pmass<135&jet2pmass>105)&jet2tau21<0.4&jet1tau21<0.4&jet2bbtag>-0.84)"
# pick the two variables to do the estiamte it (in this case, Soft Drop Mass (from 70 to 350 in 48 bins) and tau32 (from 0 to 1))
# NOW DO THE ACTUAL ALPHABETIATION: (Creating the regions)
# The command is: .GetRates(cut, bins, truthbins, center, fit)
cut = [0.6, ">"]
# so we need to give it bins:
bins = [[50,80],[80,105],[135,155],[155,200]]
#bins = [[50,70],[70,90],[130,150],[150,200]]
# truth bins (we don't want any because we are looking at real data::)
truthbins = [[105,135]]
# a central value for the fit (could be 0 if you wanted to stay in the mass variable, we are looking at tops, so we'll give it 170 GeV)
center = 120.



F = QuadraticFit([0.1,0.1,0.1], -75, 75, "quadfit", "EMRFNEX0")
#F = LinearFit([0.2,-0.2], -75, 75, "linFit1", "EMRNS")
# All the error stuff is handled by the LinearFit class. We shouldn't have to do anything else!

var_array = ["(fatjet1_mprunedcorr)", "(fatjet1_hbb)", 30,50,200, 200, -1.1, 1.1]

#*****************************************************************************************###
#Fit_bins=[0,400,500,600,700,5000]
Fit_bins=[800,966,1080, 1400, 3019]
#*****************************************************************************************###
#Fit_bins=[450,692,816,944,1114, 1492,2250]
C1 = TCanvas("C1", "", 800, 600)
C2 = TCanvas("C2", "", 800, 800)
CMS_lumi.CMS_lumi(C2, iPeriod, 22)
for b in range(len(Fit_bins)-1):

	presel = "(trigPass==1&&inv_mass_corr>"+str(Fit_bins[b])+"&&inv_mass_corr<"+str(Fit_bins[b+1])+"&(fatjet2_mprunedcorr<135&fatjet2_mpruned>105)&&fatjet2_hbb>0.6&&fatjet1_tau21<0.6&fatjet2_tau21<0.6)"
#	print presel

#	presel = "(inv_mass_corr>800&(fatjet2_mpruned<130&fatjet2_mpruned>90)&&fatjet2_hbb>0.6&&fatjet1_tau21<0.6&fatjet2_tau21<0.6)"
	HbbTest.SetRegions(var_array, presel) # make the 2D plot
	
#	C1.cd()
	HbbTest.TwoDPlot.Draw() # Show that plot:
	HbbTest.GetRates(cut, bins, truthbins, center, F)

	## Let's plot the results:
	
	C2.cd()
	HbbTest.G.SetTitle("")
	HbbTest.G.Draw("AP")
	HbbTest.G.GetXaxis().SetTitle("#Delta(jet - Higgs)_{mass} (GeV)")
	HbbTest.G.GetYaxis().SetTitle("N_{passed}/N_{failed}")

	HbbTest.Fit.fit.Draw("same")
	HbbTest.Fit.ErrUp.SetLineStyle(2)
	HbbTest.Fit.ErrUp.Draw("same")
	HbbTest.Fit.ErrDn.SetLineStyle(2)
	HbbTest.Fit.ErrDn.Draw("same")
	HbbTest.truthG.SetLineColor(kPink)
	HbbTest.truthG.Draw("opt")
	leg = TLegend(0.6,0.6,0.89,0.89)
	leg.SetLineColor(0)
	leg.SetFillColor(0)
	leg.SetHeader("Invariant mass in range "+str(Fit_bins[b])+"-"+str(Fit_bins[b+1])+"GeV")
	leg.AddEntry(HbbTest.G, "events used in fit", "PL")
	leg.AddEntry(HbbTest.Fit.fit, "fit", "L")
	leg.AddEntry(HbbTest.Fit.ErrUp, "fit errors", "L")
	leg.SetTextSize(0.025)
	leg.Draw()
	
	C2.Print("fit"+str(b)+"_bbtag%s.pdf"%cut[0])
	# Now we actually run the estiamte!
	# cuts:
	tag = "(trigPass==1&&inv_mass_corr>"+str(Fit_bins[b])+"&&inv_mass_corr<"+str(Fit_bins[b+1])+"&fatjet2_mprunedcorr<135&fatjet2_mprunedcorr>105&fatjet1_mpruned<135&fatjet1_mpruned>105&fatjet1_hbb>0.6&fatjet2_hbb>0.6&&fatjet1_tau21<0.6&fatjet2_tau21<0.6)"
	antitag = "(trigPass==1&&inv_mass_corr>"+str(Fit_bins[b])+"&&inv_mass_corr<"+str(Fit_bins[b+1])+"&fatjet2_mprunedcorr<135&fatjet2_mprunedcorr>105&fatjet1_mpruned<135&fatjet1_mpruned>105&fatjet1_hbb<0.6&fatjet2_hbb>0.6&&fatjet1_tau21<0.6&fatjet2_tau21<0.6)"
	
	variable = "inv_mass_corr"

	HbbTest.MakeEstVariable(variable, binBoundaries, antitag, tag)

	for i in HbbTest.hists_MSR:
		V.Add(i,1.)
		print V
	# the estimate is the sum of the histograms in self.hists_EST and self.hist_MSR_SUB
	for i in HbbTest.hists_EST:
		N.Add(i,1.)
	# We can do the same thing for the Up and Down shapes:	
	for i in HbbTest.hists_EST_UP:
		NU.Add(i,1.)
		print NU
	for i in HbbTest.hists_EST_DN:
		ND.Add(i,1.)
		print ND	
	for i in HbbTest.hists_ATAG:
		A.Add(i,1.)


for b in range(1,len(binBoundaries)-0):
	if NU.GetBinContent(b)==0:
		 NU.SetBinContent(b,0.0001)
	if ND.GetBinContent(b)==0:
		 ND.SetBinContent(b,0.0001)
	if N.GetBinContent(b)==0:
		 N.SetBinContent(b,0.0001)
	if V.GetBinContent(b)==0:
		 V.SetBinContent(b,0.0001)


FILE.cd()

FILE.Write()
FILE.Save()

print A, N,ND,NU,V
C3 = TCanvas("C3", "", 800, 600)

vartitle = "m_{X} (GeV)"

NU.SetLineColor(kBlack)
ND.SetLineColor(kBlack)
NU.SetLineStyle(2)
ND.SetLineStyle(2)
#NUTT.SetLineStyle(1)
#NDTT.SetLineStyle(1)
N.SetLineColor(kBlack)
N.SetFillColor(kPink+3)



V.SetStats(0)
V.Sumw2()
V.SetLineColor(1)
V.SetFillColor(0)
V.SetMarkerColor(1)
V.SetMarkerStyle(20)
#N.GetYaxis().SetTitle("events / "+str((hbins[2]-hbins[1])/hbins[0])+" GeV")
N.GetXaxis().SetTitle(vartitle)

leg2 = TLegend(0.6,0.6,0.89,0.89)
#leg2.SetHeader("cut @ #tau_{2}/#tau_{1} < 0.4")
leg2.SetLineColor(0)
leg2.SetFillColor(0)
leg2.AddEntry(V, "Data", "PL")
leg2.AddEntry(N, "backgorund prediction", "F")
leg2.AddEntry(NU, "uncertainty", "F")




FindAndSetMax([V,N, NU, ND])

C3.cd()
N.Draw("Hist")
V.Draw("same E0")
NU.Draw("hist same")
ND.Draw("hist same")

leg2.Draw()
C3.Print("bkg_bbtag%s.pdf"%cut[0])


C4 = TCanvas("C4", "", 800, 800)
C4.cd()
Pull = copy.copy(V)
#.("Pull")
Pull.Add(N, -1.)

for i in range(Pull.GetNbinsX()+1):
	a = Pull.GetBinContent(i)
	ae = V.GetBinError(i)
	u = NU.GetBinContent(i) - N.GetBinContent(i)
	d = ND.GetBinContent(i) - N.GetBinContent(i)
	ue = math.sqrt(ae**2 + u**2)
	de = math.sqrt(ae**2 + d**2)
	if a > 0.:
		e = ue
	else:
		e = de
	if e > 1:
		f = a/e
	else:
		f = a
	Pull.SetBinContent(i, f)

Pull.GetXaxis().SetTitle("")
Pull.SetStats(0)
Pull.SetFillStyle(1001)
Pull.SetLineColor(kPink+2)
Pull.SetFillColor(kPink+2)
Pull.GetXaxis().SetNdivisions(0)
Pull.GetYaxis().SetNdivisions(4)
Pull.GetYaxis().SetTitle("(Data - Bkg)/#sigma")
Pull.GetYaxis().SetLabelSize(85/15*Pull.GetYaxis().GetLabelSize())
Pull.GetYaxis().SetTitleSize(4.2*Pull.GetYaxis().GetTitleSize())
Pull.GetYaxis().SetTitleOffset(0.175)
Pull.GetYaxis().SetRangeUser(-3.,3.)

#draw the lumi text on the canvas

plot = TPad("pad1", "The pad 80% of the height",0,0.15,1,1)
pull = TPad("pad2", "The pad 20% of the height",0,0,1.0,0.15)
plot.Draw()
leg2.Draw()
pull.Draw()
plot.cd()
N.Draw("Hist")
V.Draw("same E0")
NU.Draw("hist same")
ND.Draw("hist same")

pull.cd()
Pull.Draw("hist")


CMS_lumi.CMS_lumi(C4, iPeriod, iPos)
C4.cd()
C4.Update()
C4.Print("pull.pdf")
print V.Integral()
print A.Integral()




