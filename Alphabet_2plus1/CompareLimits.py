import ROOT as rt
from ROOT import *
import CMS_lumi, tdrstyle, copy
from math import log
#set the tdr style
#tdrstyle.setTDRStyle()

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_13TeV = "2.69 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12

iPeriod =4


withAcceptance=False
unblind=False

gROOT.Reset()
gROOT.SetStyle("Plain")
gStyle.SetOptStat(0)
gStyle.SetOptFit(0)
gStyle.SetTitleOffset(1.2,"Y")
gStyle.SetPadLeftMargin(0.18)
gStyle.SetPadBottomMargin(0.15)
gStyle.SetPadTopMargin(0.08)
gStyle.SetPadRightMargin(0.05)
gStyle.SetMarkerSize(0.5)
gStyle.SetHistLineWidth(1)
gStyle.SetStatFontSize(0.020)
gStyle.SetTitleSize(0.06, "XYZ")
gStyle.SetLabelSize(0.05, "XYZ")
gStyle.SetNdivisions(510, "XYZ")
gStyle.SetLegendBorderSize(0)

rt.gROOT.ProcessLine("struct limit_t {Double_t limit;};")

def Plot(mg, masses, limits, label, legend, leg=False, obs=False, col=rt.kRed):
    c1 = rt.TCanvas("c22","A Simple Graph Example",200,10,600,600)
    eff=10.
    # we do a plot r*MR
    
    mg.SetTitle("X -> ZZ")
    
    x = []
    yobs = []
    y2up = []
    y1up = []
    y1down = []
    y2down = []
    ymean = []

    for i in range(0,len(masses)):
#        print rad[i][2]*efficiencies[radmasses[j]]

        ymean.append(limits[0][i]*eff)

        yobs.append(limits[1][i]*eff)

    grobs = rt.TGraphErrors(1)
    grobs.SetMarkerStyle(rt.kFullDotLarge)
    grobs.SetLineColor(col)
    grobs.SetLineWidth(3)
#    gr2up = rt.TGraphErrors(1)
#    gr2up.SetMarkerColor(0)
#    gr1up = rt.TGraphErrors(1)
#    gr1up.SetMarkerColor(0)
    grmean = rt.TGraphErrors(1)
    grmean.SetLineColor(1)
    grmean.SetLineWidth(2)
    grmean.SetLineStyle(3)
#    gr1down = rt.TGraphErrors(1)
#    gr1down.SetMarkerColor(0)
#    gr2down = rt.TGraphErrors(1)
#    gr2down.SetMarkerColor(0)
  
    for j in range(0,len(masses)):
        grobs.SetPoint(j, masses[j], yobs[j])
        grmean.SetPoint(j, masses[j], ymean[j])

#    mg.Add(gr2up)#.Draw("same")
#    mg.Add(gr1up)#.Draw("same")
    mg.Add(grmean,"L")#.Draw("same,AC*")
#    mg.Add(gr1down)#.Draw("same,AC*")
#    mg.Add(gr2down)#.Draw("same,AC*")
    if obs: mg.Add(grobs,"L")#.Draw("AC*")
 
    c1.SetLogy(1)
    mg.SetTitle("")
    mg.Draw("AP")
    mg.GetXaxis().SetTitle("Resonance mass (TeV)")
    resonance="G_{RS}"
        #resonance="G_{Bulk}"
    if withAcceptance:
        mg.GetYaxis().SetTitle("#sigma #times B("+resonance+" #rightarrow "+label.split("_")[0].replace("RS1","").replace("Bulk","")+") #times A (fb)")
    else:
        mg.GetYaxis().SetTitle("#sigma #times B("+resonance+" #rightarrow HH to b#bar{b}b#bar{b}) (fb)")
    mg.GetYaxis().SetLabelFont(42)
    mg.GetXaxis().SetLabelFont(42)
    mg.GetYaxis().SetTitleFont(42)
    mg.GetXaxis().SetTitleFont(42)
    mg.GetYaxis().SetTitleSize(0.035)
    mg.GetXaxis().SetTitleSize(0.035)
    mg.GetXaxis().SetLabelSize(0.045)
    mg.GetYaxis().SetLabelSize(0.045)
    mg.GetYaxis().SetRangeUser(10.,10000)
    mg.GetYaxis().SetTitleOffset(1.4)
    mg.GetYaxis().CenterTitle(True)
    mg.GetXaxis().SetTitleOffset(1.1)
    mg.GetXaxis().CenterTitle(True)
    mg.GetXaxis().SetNdivisions(508)
    CMS_lumi.CMS_lumi(c1, iPeriod, iPos)
    c1.cd()
    c1.Update()
    if "qW" in label.split("_")[0] or "qZ" in label.split("_")[0]:
        mg.GetXaxis().SetLimits(0.4,3.5)
    else:
        mg.GetXaxis().SetLimits(0.4,3.5)
    mg.Draw()
    if leg: legend.AddEntry(grobs, label, "l")
    legend.Draw()
    c1.SaveAs("compare2_limits.pdf")
    return copy.copy(mg)

if __name__ == '__main__':
    newfile=TFile("limit_graphs.root", "recreate")
    masses=[1, 1.2, 1.4,1.6, 1.8, 2., 2.5, 3]
    limits=[[66.162109375,33.0810546875,22.216796875,15.6860351562,11.0778808594,9.18579101562,11.1999511719,17.1508789062],
     [48.9857654553,21.6155402025,15.3255791646,16.904052552,18.1415219009,8.66636225975,9.27253636179,16.5731329456]]
    mg = rt.TMultiGraph()
    legend=rt.TLegend(0.6,0.6,0.85,0.85)
    
    g1=Plot(mg, masses, limits, "boosted postfit", legend, leg=True, obs=True )
    newfile.cd()

    g1.Write()
    
    masses=[0.5, 0.55, 0.6,0.65, 0.7, 0.75, 0.8, 0.9, 1., 1.4, 1.6, 2.]
    limits=[[6093.75, 1710.9375,832.03125, 385.7421875 ,243.1640625, 181.15234375,133.7890625, 90.087890625 ,66.650390625,55.908203125,
69.091796875, 160.64453125, 4109.375],[6093.75, 1710.9375,832.03125, 385.7421875 ,243.1640625, 181.15234375,133.7890625, 90.087890625 ,66.650390625,55.908203125,
69.091796875, 160.64453125, 4109.375]]
    

    g1=Plot(mg, masses, limits, "WP hbb 0.6", legend, leg=True, obs=True , col=rt.kCyan)
    newfile.cd()

    g1.Write()
    
    
    masses=[0.5, 0.55, 0.6,0.65, 0.7, 0.75, 0.8, 0.9, 1., 1.4, 1.6, 2.]
    limits=[[5734.375,1679.6875,832.03125,400.390625,249.0234375,186.5234375,141.11328125,93.505859375,70.556640625,58.349609375,
    69.580078125,160.64453125,3703.125],[5734.375,1679.6875,832.03125,400.390625,249.0234375,186.5234375,141.11328125,93.505859375,70.556640625,58.349609375,
    69.580078125,160.64453125,3703.125]]
    
    g1=Plot(mg, masses, limits, "boosted", legend, leg=False, obs=True , col=rt.kCyan)
    newfile.cd()

    g1.Write()
    
    
    masses=[0.5, 0.55, 0.6,0.65, 0.7, 0.75, 0.8, 0.9, 1., 1.4, 1.6, 2.]
    limits=[[6406.25,1511.71875,847.65625,423.828125,256.8359375,191.89453125,139.16015625,101.07421875,72.509765625,68.603515625,102.05078125,
198.2421875,4953.125],[6406.25,1511.71875,847.65625,423.828125,256.8359375,191.89453125,139.16015625,101.07421875,72.509765625,68.603515625,102.05078125,
198.2421875,4953.125]]
    
    g1=Plot(mg, masses, limits, "boosted", legend, leg=False,obs=True, col=rt.kCyan)
    newfile.cd()

    g1.Write()
    
    
    masses=[0.5, 0.55, 0.6,0.65, 0.7, 0.75, 0.8, 0.9, 1., 1.4, 1.6, 2.]
    limits=[[5671.875,1449.21875,720.703125,338.8671875,209.9609375,158.69140625,113.76953125,83.251953125,56.884765625,46.0205078125,55.419921875,
146.97265625,3296.875],
[5671.875,1449.21875,720.703125,338.8671875,209.9609375,158.69140625,113.76953125,83.251953125,56.884765625,46.0205078125,55.419921875,
146.97265625,3296.875]]
    
    g1=Plot(mg, masses, limits, "boosted", legend, leg=False,obs=True, col=rt.kCyan)
    newfile.cd()

    g1.Write()
    
    masses=[0.5, 0.55, 0.6,0.65, 0.7, 0.75, 0.8, 0.9, 1., 1.4, 1.6, 2.]
    limits=[[5828.125,1339.84375,697.265625,303.7109375,200.1953125,149.90234375,103.02734375,76.416015625,55.419921875,43.0908203125,
    47.4853515625,163.57421875,4390.625],
[5828.125,1339.84375,697.265625,303.7109375,200.1953125,149.90234375,103.02734375,76.416015625,55.419921875,43.0908203125,
    47.4853515625,163.57421875,4390.625]]
    
    g1=Plot(mg, masses, limits, "hbb 0.9 - cmva 0.185", legend, leg=True ,obs=True, col=rt.kBlue)
    newfile.cd()

    g1.Write()

    masses=[0.5, 0.55, 0.6,0.65, 0.7, 0.75, 0.8, 0.9, 1., 1.4, 1.6, 2.]
    limits=[[6593.75,1394.53125,744.140625,293.9453125,196.2890625,139.6484375,93.505859375,74.462890625,57.373046875,48.7060546875,
57.373046875,190.91796875,5890.625],
[6593.75,1394.53125,744.140625,293.9453125,196.2890625,139.6484375,93.505859375,74.462890625,57.373046875,48.7060546875,
57.373046875,190.91796875,5890.625]]
    
    g1=Plot(mg, masses, limits, "hbb 0.9 - cmva 0.485", legend, leg=True, obs=True, col=rt.kOrange)
    newfile.cd()

    g1.Write()

    masses=[0.5, 0.525, 0.55,0.575,0.6,0.625,0.65,0.675 ,0.7,0.725, 0.75,0.775, 0.8,0.825,0.86,0.875, 0.9,0.95 ,1., 1.05, 1.1, 1.15,1.2]
    limits=[[282.2 ,252.9 ,233.4 ,205.1 ,180.2 ,162.6 ,147.0 ,137.2 ,129.4,121.6 ,114.7 ,109.9 ,104.0 ,
    100.1 ,97.2 , 93.8 , 87.4 , 84.5 , 81.5 , 81.5 , 83.5 , 88.4 , 94.2],
    [291.5 ,217.8 ,222.5 ,212.6 ,161.4 ,129.9 ,137.9 ,179.9 ,216.9, 192.7 ,124.2 ,71.5 , 57.2 ,
     61.9 , 68.5 , 84.2 , 96.2 , 122.2 ,132.3 ,100.7 ,60.9 , 57.9 , 83.5]
]
    
    g1=Plot(mg, masses, limits, "resolved postfit", legend, leg=True ,obs=True, col=rt.kGreen)
    newfile.cd()

    g1.Write()
    
    newfile.Close()
    
    
    
    
    


