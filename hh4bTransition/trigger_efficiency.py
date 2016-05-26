from ROOT import *
import copy


c=TCanvas("c", "c")
f2="SR_BTagCSV.root"
f1="SR_JetHT.root"
f3="CR_JetHT.root"
f4="CR_BTagCSV.root"



SR1=TFile(f1, "R")
h3=TH1F("SR_JetHT","SR efficiency; mjj; eff", 300, 0, 3000)
print minitree
print minitree.Draw("Inv_mass>>SR_JetHT", "")
h4=TH1F("SR_JetHT1","SR efficiency; mjj; eff", 300, 0, 3000)
print minitree.Draw("Inv_mass>>SR_JetHT1", "(HLT_ht800||HLT_AK08||HLT_HH4b)&&(fatjet_mass<135&&fatjet_mass<105&&dijet_mass<135&&dijet_mass<105)")
denom=copy.copy(h3)
num=copy.copy(h4)
SR1=TFile(f2, "R")
h1=TH1F("SR_BTagCSV","SR_BTagCSV", 300, 0, 3000)
minitree=SR1.Get("minitree")
print minitree.Draw("Inv_mass>>SR_BTagCSV", "(HLT_AK08==0)&&(HLT_ht800==0)")
h2=TH1F("SR_BTagCSV1","SR_BTagCSV", 300, 0, 3000)
print minitree.Draw("Inv_mass>>SR_BTagCSV1", "HLT_HH4b&&(HLT_AK08==0)&&(HLT_ht800==0)&&(fatjet_mass<135&&fatjet_mass<105&&dijet_mass<135&&dijet_mass<105)")

denom.Add(h1)
num.Add(h2)

num.Sumw2()
denom.Sumw2()
denom.Draw("hist")
num.SetFillColor(kRed)
num.Draw("same hist")
c.Print("SR.pdf")

num.Divide(denom)
num.Draw()
c.Print("ratioSR.pdf")





#SR1=TFile(f3, "R")
#h3=TH1F("SR_JetHT","SR efficiency; mjj; eff", 30, 0, 3000)
#print minitree
#print minitree.Draw("Inv_mass>>SR_JetHT", "HLT_ht350")
#h4=TH1F("SR_JetHT1","SR efficiency; mjj; eff", 30, 0, 3000)
#print minitree.Draw("Inv_mass>>SR_JetHT1", "HLT_ht350&&(HLT_ht800)")
#denom=copy.copy(h3)
#num=copy.copy(h4)
#SR1=TFile(f4, "R")
#h1=TH1F("SR_BTagCSV","SR_BTagCSV", 30, 0, 3000)
#minitree=SR1.Get("minitree")
##print minitree.Draw("Inv_mass>>SR_BTagCSV", "HLT_ht350&&(HLT_AK08==0)&&(HLT_ht800==0)")
#h2=TH1F("SR_BTagCSV1","SR_BTagCSV", 30, 0, 3000)
##print minitree.Draw("Inv_mass>>SR_BTagCSV1", "HLT_ht350&&HLT_HH4b&&(HLT_AK08==0)&&(HLT_ht800==0)")

#denom.Add(h1)
#num.Add(h2)

#num.Sumw2()
#denom.Sumw2()
#denom.Draw("hist")
#num.SetFillColor(kRed)
#num.Draw("same hist")
#c.Print("800only.pdf")

#num.Divide(denom)
#num.Draw()
#c.Print("ratio800.pdf")


