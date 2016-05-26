import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy, numpy


import Alphabet_Header
from Alphabet_Header import *
import Plotting_Header
from Plotting_Header import *




mass=[500, 550, 600, 650, 700, 750, 800, 900, 1000, 1200, 1400, 1600,1800, 2000, 2500]
sim_masses=[500, 550, 600, 650, 700, 750, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000, 2500]
VAR = "Inv_mass"

#variable bin from dijet analysis 788 838 
#binBoundaries = [800, 838, 890, 944, 1000, 1058, 1118, 1181, 1246, 1313, 1383, 1455, 1530, 1607, 1687,
#        1770, 1856, 1945, 2037, 2132, 2231, 2332, 2438, 2546, 2659, 2775, 2895, 3019 ]#, 3147, 3279, 3416, 3558, 3704, 3854, 4010, 4171, 4337, 4509,
#binBoundaries =numpy.arange(437.5,2000,40.)
binBoundaries =[440, 480, 520, 560, 600, 640, 680, 720, 760, 800, 840, 880, 920, 960, 1000, 1040, 1080, 1120, 1160, 1200,
1240, 1280, 1320, 1360, 1400, 1440, 1480, 1520, 1560, 1600, 1640, 1680, 1720, 1760, 1800, 1880, 1960, 2040, 2120]

binBoundaries=range(440, 2200, 70)
vartitle = "m_{X} (GeV)"
sigregcut = "resolved<0.5&&(HLT_ht800||HLT_AK08||HLT_HH4b)&&(fatjet_hbb>0.9&&fatjet_mass<135&fatjet_mass>105)&(dijet_mass<135&dijet_mass>105)&isCR<0.4"
lumi =2691.
background = TFile("Hbb_output.root")
UD = ['Up','Down']
#SF_tau21=0.979
SF_tau21=1
SF_bbtag=0.9

for m in mass:
    output_file = TFile("datacard/hh2plus1_mX_%s_13TeV.root"%(m),"RECREATE")
    hh=output_file.mkdir("hh")
    hh.cd()

    Signal_mX = TH1F("Signal2plus1_mX_%s"%(m), "", len(binBoundaries)-1, array('d',binBoundaries))
#        Signal_mX_trig_up = TH1F("Signal2plus1_mX_%s_CMS_eff_trigUp"%(m), "", len(binBoundaries)-1, array('d',binBoundaries))
#        Signal_mX_trig_down = TH1F("Signal2plus1_mX_%s_CMS_eff_trigDown"%(m), "", len(binBoundaries)-1, array('d',binBoundaries))
    Signal_mX_btag_up = TH1F("Signal2plus1_mX_%s_CMS_eff_btagUp"%(m), "", len(binBoundaries)-1, array('d',binBoundaries))
    Signal_mX_btag_down = TH1F("Signal2plus1_mX_%s_CMS_eff_btagDown"%(m), "", len(binBoundaries)-1, array('d',binBoundaries))
    Signal_mX_cmva_up = TH1F("Signal2plus1_mX_%s_CMS_eff_btagUp"%(m), "", len(binBoundaries)-1, array('d',binBoundaries))
    Signal_mX_cmva_down = TH1F("Signal2plus1_mX_%s_CMS_eff_btagDown"%(m), "", len(binBoundaries)-1, array('d',binBoundaries))
    Signal_mX_pu_up = TH1F("Signal2plus1_mX_%s_CMS_eff_puUp"%(m), "", len(binBoundaries)-1, array('d',binBoundaries))
    Signal_mX_pu_down = TH1F("Signal2plus1_mX_%s_CMS_eff_puDown"%(m), "", len(binBoundaries)-1, array('d',binBoundaries))
    Signal_mX_FJEC_Up = TH1F("Signal2plus1_mX_%s_CMS_eff_JECUp"%(m), "", len(binBoundaries)-1, array('d',binBoundaries))
    Signal_mX_FJEC_Down = TH1F("Signal2plus1_mX_%s_CMS_eff_JECDown"%(m), "", len(binBoundaries)-1, array('d',binBoundaries))
    Signal_mX_FJER_Up = TH1F("Signal2plus1_mX_%s_CMS_eff_JERUp"%(m), "", len(binBoundaries)-1, array('d',binBoundaries))
    Signal_mX_FJER_Down = TH1F("Signal2plus1_mX_%s_CMS_eff_JERDown"%(m), "", len(binBoundaries)-1, array('d',binBoundaries))
    Signal_mX_MJEC_Up = TH1F("Signal2plus1_mX_%s_CMS_eff_massJECUp"%(m), "", len(binBoundaries)-1, array('d',binBoundaries))
    Signal_mX_MJEC_Down = TH1F("Signal2plus1_mX_%s_CMS_eff_massJECDown"%(m), "", len(binBoundaries)-1, array('d',binBoundaries))
    Signal_mX_JEC_Up = TH1F("Signal2plus1_mX_%s_CMS_eff_JEC4Up"%(m), "", len(binBoundaries)-1, array('d',binBoundaries))
    Signal_mX_JEC_Down = TH1F("Signal2plus1_mX_%s_CMS_eff_JEC4Down"%(m), "", len(binBoundaries)-1, array('d',binBoundaries))
    Signal_mX_JER_Up = TH1F("Signal2plus1_mX_%s_CMS_eff_JER4Up"%(m), "", len(binBoundaries)-1, array('d',binBoundaries))
    Signal_mX_JER_Down = TH1F("Signal2plus1_mX_%s_CMS_eff_JER4Down"%(m), "", len(binBoundaries)-1, array('d',binBoundaries))
    
    if m in sim_masses:
        print(m)

        signal_file= TFile("input/selected_bb_9_cmva_185_NoSyst_grav%s.root"%(m))
        tree = signal_file.Get("minitree") 
        tree.GetEntry(1)
        generatedEvents=tree.norm
        print signal_file, tree
        writeplot(tree, Signal_mX_pu_up, VAR, sigregcut, "puWeightUp*SF*cmvaSF*cmvaSF2")
        writeplot(tree, Signal_mX_pu_down, VAR, sigregcut, "puWeightDown*SF*cmvaSF*cmvaSF2")
        writeplot(tree, Signal_mX, VAR, sigregcut, "puWeight*SF*cmvaSF*cmvaSF2")
        writeplot(tree, Signal_mX_btag_up, VAR, sigregcut, "puWeight*SFup*cmvaSF*cmvaSF2")
        writeplot(tree, Signal_mX_btag_down, VAR, sigregcut, "puWeight*SFdown*cmvaSF*cmvaSF2")
        writeplot(tree, Signal_mX_cmva_up, VAR, sigregcut, "puWeight*SFup*cmvaSFup*cmvaSFup2")
        writeplot(tree, Signal_mX_cmva_down, VAR, sigregcut, "puWeight*SFdown*cmvaSFdown*cmvaSFdown2")

        print "ok, Scale factor"

        print(Signal_mX.Integral())

	cmvalnN= 1.+ abs(Signal_mX_cmva_up.GetSumOfWeights()-Signal_mX_cmva_down.GetSumOfWeights())/(2.*Signal_mX_cmva_up.GetSumOfWeights())
        btaglnN= 1.+ abs(Signal_mX_btag_up.GetSumOfWeights()-Signal_mX_btag_down.GetSumOfWeights())/(2.*Signal_mX_btag_up.GetSumOfWeights())
        pulnN= 1.+ abs(Signal_mX_pu_up.GetSumOfWeights()-Signal_mX_pu_down.GetSumOfWeights())/(2.*Signal_mX.GetSumOfWeights())
        Signal_mX.Scale(lumi*1./generatedEvents)
        Signal_mX_btag_up.Scale(lumi*1./generatedEvents)
        Signal_mX_btag_down.Scale(lumi*1./generatedEvents)
        Signal_mX_pu_up.Scale(lumi*1./generatedEvents)
        Signal_mX_pu_down.Scale(lumi*1./generatedEvents)
        Signal_mX_cmva_up.Scale(0.01*lumi*SF_tau21*SF_tau21/generatedEvents)
        Signal_mX_cmva_down.Scale(0.01*lumi*SF_tau21*SF_tau21/generatedEvents)
        
        if not (m==1200 or m==1800):        
         signal_file_FJEC_Up= TFile("input/selected_bb_9_cmva_185_FJEC_Up_grav%s.root"%(m))                 
         tree_FJEC_Up = signal_file_FJEC_Up.Get("minitree")         
         writeplot(tree_FJEC_Up, Signal_mX_FJEC_Up, VAR, sigregcut, "puWeight*SFup*cmvaSF*cmvaSF2")
         Signal_mX_FJEC_Up.Scale(lumi*1./generatedEvents)
        
         signal_file_FJEC_Down= TFile("input/selected_bb_9_cmva_185_FJEC_Down_grav%s.root"%(m))
         tree_FJEC_Down = signal_file_FJEC_Down.Get("minitree")
         writeplot(tree_FJEC_Down, Signal_mX_FJEC_Down, VAR, sigregcut,"puWeight*SFup*cmvaSF*cmvaSF2")
         Signal_mX_FJEC_Down.Scale(lumi*1./generatedEvents)
        
         signal_file_FJER_Up= TFile("input/selected_bb_9_cmva_185_FJER_Up_grav%s.root"%(m))
         tree_FJER_Up = signal_file_FJER_Up.Get("minitree")
         writeplot(tree_FJER_Up, Signal_mX_FJER_Up, VAR, sigregcut, "puWeight*SFup*cmvaSF*cmvaSF2")
         Signal_mX_FJER_Up.Scale(lumi*1./generatedEvents)

         signal_file_FJER_Down= TFile("input/selected_bb_9_cmva_185_FJER_Down_grav%s.root"%(m))
         tree_FJER_Down = signal_file_FJER_Down.Get("minitree")
         writeplot(tree_FJER_Down, Signal_mX_FJER_Down, VAR, sigregcut, "puWeight*SFup*cmvaSF*cmvaSF2")
         Signal_mX_FJER_Down.Scale(lumi*1./generatedEvents)
         
         signal_file_JEC_Up= TFile("input/selected_bb_9_cmva_185_JEC_Up_grav%s.root"%(m))                 
         tree_JEC_Up = signal_file_JEC_Up.Get("minitree")         
         writeplot(tree_JEC_Up, Signal_mX_JEC_Up, VAR, sigregcut, "puWeight*SFup*cmvaSF*cmvaSF2")
         Signal_mX_JEC_Up.Scale(lumi*1./generatedEvents)
        
         signal_file_JEC_Down= TFile("input/selected_bb_9_cmva_185_JEC_Down_grav%s.root"%(m))
         tree_JEC_Down = signal_file_JEC_Down.Get("minitree")
         writeplot(tree_JEC_Down, Signal_mX_JEC_Down, VAR, sigregcut, "puWeight*SFup*cmvaSF*cmvaSF2")
         Signal_mX_JEC_Down.Scale(lumi*1./generatedEvents)
        
         signal_file_JER_Up= TFile("input/selected_bb_9_cmva_185_JER_Up_grav%s.root"%(m))
         tree_JER_Up = signal_file_JER_Up.Get("minitree")
         writeplot(tree_JER_Up, Signal_mX_JER_Up, VAR, sigregcut, "puWeight*SFup*cmvaSF*cmvaSF2")
         Signal_mX_JER_Up.Scale(lumi*1./generatedEvents)

         signal_file_JER_Down= TFile("input/selected_bb_9_cmva_185_JER_Down_grav%s.root"%(m))
         tree_JER_Down = signal_file_JER_Down.Get("minitree")
         writeplot(tree_JER_Down, Signal_mX_JER_Down, VAR, sigregcut, "puWeight*SFup*cmvaSF*cmvaSF2")
         Signal_mX_JER_Down.Scale(lumi*1./generatedEvents)


         signal_file_MJEC_Up= TFile("input/selected_bb_9_cmva_185_MJEC_Up_grav%s.root"%(m))
         tree_MJEC_Up = signal_file_MJEC_Up.Get("minitree")
         writeplot(tree_MJEC_Up, Signal_mX_MJEC_Up, VAR, sigregcut, "puWeight*SFup*cmvaSF*cmvaSF2")
         Signal_mX_MJEC_Up.Scale(lumi*1./generatedEvents)

         signal_file_MJEC_Down= TFile("input/selected_bb_9_cmva_185_MJEC_Down_grav%s.root"%(m))
         tree_MJEC_Down = signal_file_MJEC_Down.Get("minitree")
         writeplot(tree_MJEC_Down, Signal_mX_MJEC_Down, VAR, sigregcut, "puWeight*SFup*cmvaSF*cmvaSF2")
         Signal_mX_MJEC_Down.Scale(lumi*1./generatedEvents)
        
         MJEClnN= 1.+ abs(Signal_mX_MJEC_Up.GetSumOfWeights()-Signal_mX_MJEC_Down.GetSumOfWeights())/(2.*Signal_mX.GetSumOfWeights())
         FJEClnN= 1.+ abs(Signal_mX_FJEC_Up.GetSumOfWeights()-Signal_mX_FJEC_Down.GetSumOfWeights())/(2.*Signal_mX.GetSumOfWeights())
         FJERlnN= 1.+ abs(Signal_mX_FJER_Up.GetSumOfWeights()-Signal_mX_FJER_Down.GetSumOfWeights())/(2.*Signal_mX.GetSumOfWeights())
         JEClnN= 1.+ abs(Signal_mX_JEC_Up.GetSumOfWeights()-Signal_mX_JEC_Down.GetSumOfWeights())/(2.*Signal_mX.GetSumOfWeights())
         JERlnN= 1.+ abs(Signal_mX_JER_Up.GetSumOfWeights()-Signal_mX_JER_Down.GetSumOfWeights())/(2.*Signal_mX.GetSumOfWeights())
        else :
                MJEClnN= 1.02
                FJEClnN= 1.02
                FJERlnN= 1.02
                JEClnN= 1.02
                JERlnN= 1.02
        print("%s %s %s")%(MJEClnN,FJEClnN,FJERlnN)

    signal_integral = Signal_mX.Integral()
    print(signal_integral) 
    background.cd()         
    qcd_integral = QCD.Integral()

    qcd =QCD
    qcd_antitag = QCD_Antitag
    qcd_up = QCD_CMS_scale_13TeVUp
    qcd_down = QCD_CMS_scale_13TeVDown
#    tt_up = QCD_CMS_TTbarUp
#    tt_down = QCD_CMS_TTbarDown
    data = data_obs

    qcd.SetName("QCD2plus1")
    qcd_up.SetName("QCD2plus1_CMS_scale_13TeVUp")
    qcd_down.SetName("QCD2plus1_CMS_scale_13TeVDown")
    output_file.cd()
    hh.cd()
    qcd_stat_up =TH1F("qcd_stat_up","",len(binBoundaries)-1, array('d',binBoundaries))
    qcd_stat_down =TH1F("qcd_stat_down","",len(binBoundaries)-1, array('d',binBoundaries))
    
    for bin in range(0,len(binBoundaries)-1):
        for Q in UD:
            qcd_syst =TH1F("%s_bin%s%s"%("QCD2plus1_CMS_stat_13TeV",bin,Q),"",len(binBoundaries)-1, array('d',binBoundaries))
            bin_stat = qcd.GetBinContent(bin+1)
            bin_at = qcd_antitag.GetBinContent(bin+1)
            if bin_at < 1 and bin_at >0:  
                    bin_at=1.
            
            if Q == 'Up':
                    if bin_at >0 :
                           qcd_stat_up.SetBinContent(bin+1,bin_stat+qcd_antitag.GetBinError(bin+1)/bin_at*bin_stat)        
                           qcd_syst.SetBinContent(bin+1,bin_stat+qcd_antitag.GetBinError(bin+1)/bin_at*bin_stat)
                    else : 
                            qcd_syst.SetBinContent(bin+1,0.001)
                            qcd_stat_up.SetBinContent(bin+1,0.001)
                            
            if Q == 'Down':
                    if bin_at >0 :
                            if ( bin_stat-qcd_antitag.GetBinError(bin+1)/bin_at*bin_stat >0 ):
                                    qcd_syst.SetBinContent(bin+1,bin_stat-qcd_antitag.GetBinError(bin+1)/bin_at*bin_stat)
                                    qcd_stat_down.SetBinContent(bin+1,bin_stat-qcd_antitag.GetBinError(bin+1)/bin_at*bin_stat)
                            else :
                                    qcd_syst.SetBinContent(bin+1, 0.001)
                                    qcd_stat_down.SetBinContent(bin+1, 0.001)
                    else :         
                            qcd_syst.SetBinContent(bin+1,0.001)
                            qcd_stat_down.SetBinContent(bin+1,0.001)
            qcd_syst.Write()
            

    qcd.Write()
    qcd_up.Write()
    qcd_down.Write()
    qcd_stat_up.Write()
    qcd_stat_down.Write()
#    tt_up.Write()
#    tt_down.Write()
    Signal_mX.Write()
    data.Write()
    hh.Write()
    output_file.Write()
    #output_file.Close()

    

    text_file = open("datacard/hh2plus1_mX_%s_13TeV.txt"%(m), "w")


    text_file.write("max    1     number of categories\n")
    text_file.write("jmax   1     number of samples minus one\n")
    text_file.write("kmax    *     number of nuisance parameters\n")
    text_file.write("-------------------------------------------------------------------------------\n")
    text_file.write("shapes * * hh2plus1_mX_%s_13TeV.root hh/$PROCESS hh/$PROCESS_$SYSTEMATIC\n"%(m))
    text_file.write("-------------------------------------------------------------------------------\n")
    text_file.write("bin                                            hh4b2plus1\n")
    text_file.write("observation                                    -1\n")
    text_file.write("-------------------------------------------------------------------------------\n")
    text_file.write("bin                                             hh4b2plus1            hh4b2plus1\n")
    text_file.write("process                                          0      1\n")
    text_file.write("process                                         Signal2plus1_mX_%s  QCD2plus1\n"%(m))
    text_file.write("rate                                            %f  %f\n"%(signal_integral,qcd_integral))
    text_file.write("-------------------------------------------------------------------------------\n")
    text_file.write("lumi_13TeV lnN                          1.027       -\n")        
#        text_file.write("CMS_eff_tau21_sf lnN                    1.25       -\n") #(0.129/1.031)*(2) 
    text_file.write("CMS_pileup lnN                    %f       -\n"%(pulnN))  
    text_file.write("CMS_eff_Htag_sf lnN                    1.1       -\n")   
    text_file.write("CMS_FJEC lnN                      %f        -\n"%(FJEClnN))    
    text_file.write("CMS_JEC lnN                      %f        -\n"%(JEClnN))
    text_file.write("CMS_massJEC lnN                 %f        -\n"%(MJEClnN))
    text_file.write("CMS_eff_bbtag_sf lnN                    %f       -\n"%(cmvalnN))
    text_file.write("CMS_eff_cmva_sf lnN                    %f       -\n"%(btaglnN))
    text_file.write("CMS_FJER lnN                    %f        -\n"%(FJERlnN))
    text_file.write("CMS_JER lnN                    %f        -\n"%(JERlnN))
    text_file.write("CMS_eff_trig lnN           1.1       -\n")   
    text_file.write("CMS_scale_13TeV shapeN2                           -       1.000\n")
    text_file.write("CMS_PDF_Scales lnN   1.02 -       \n")

    for bin in range(0,len(binBoundaries)-1):
            text_file.write("CMS_stat_13TeV_bin%s shapeN2                           -       1.000\n"%(bin))


    text_file.close()


    qcd_up.SetLineColor(kBlack)
    qcd_down.SetLineColor(kBlack)
    qcd_up.SetLineStyle(2)
    qcd_down.SetLineStyle(2)
    qcd_stat_up.SetLineColor(kAzure+1)
    qcd_stat_down.SetLineColor(kAzure+1)
    qcd_stat_up.SetLineStyle(2)
    qcd_stat_down.SetLineStyle(2)        
    qcd.SetLineColor(kBlack)
    qcd.SetFillColor(kTeal+2)



    data.SetStats(0)
    data.Sumw2()
    data.SetLineColor(1)
    data.SetFillColor(0)
    data.SetMarkerColor(1)
    data.SetMarkerStyle(20)
    #qcd.GetYaxis().SetTitle("events / "+str((bins[2]-bins[1])/bins[0])+" GeV")
    qcd.GetXaxis().SetTitle(vartitle)

    leg2 = TLegend(0.6,0.6,0.89,0.89)
    leg2.SetLineColor(0)
    leg2.SetFillColor(0)
    leg2.AddEntry(data, "QCD in SR", "PL")
    leg2.AddEntry(qcd, "QCD prediction", "F")
    leg2.AddEntry(qcd_up, "transfer function uncertainty", "F")
    leg2.AddEntry(qcd_stat_up, "statistical uncertainty", "F")

#    leg2.AddEntry(tt_up, "TTbar uncertainty", "F")
    C3 = TCanvas("C3", "", 800, 600)
    C3.cd()
    qcd.Draw("Hist")
    qcd_up.Draw("same hist")
    qcd_down.Draw("same hist")
#    tt_up.Draw("same hist")
#    tt_down.Draw("same hist")
    qcd_stat_up.Draw("same")
    qcd_stat_down.Draw("same")
    leg2.Draw()
    Signal_mX.SetFillColor(kRed)
    Signal_mX.Draw("hist same")
    C3.Print("split_unc"+str(m)+".pdf")

    output_file.Close()

