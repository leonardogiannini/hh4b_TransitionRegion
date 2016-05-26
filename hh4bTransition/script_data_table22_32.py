from ROOT import *
import CMS_lumi, tdrstyle
#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_13TeV = "2.69 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Simulation"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12

iPeriod =4


gStyle.SetOptStat(0)

bbtag=[0.3,0.4,0.5,0.6,0.7,0.8,0.9]
jetbatg=[0.185,0.285,0.385,0.485,0.585,0.685,0.785,0.885]
masslow=[100,105,110,115,120]
masshigh=[130,135,140,145,150]
masses=[600, 700, 750, 800, 900, 1000]
#masses=[1000]
left=[5, 7, 12, 16, 21, 31]
right=[10, 13, 18, 23, 28, 39]
c1=TCanvas("c","C", 800, 600)
sign_table=[TH2F("table1","Graviton 600", 8,0,8,  25,0,25),
TH2F("table2", "Graviton 700", 8,0,8,  25,0,25),
TH2F("table3", "Graviton 750", 8,0,8,  25,0,25),
TH2F("table4", "Graviton 800", 8,0,8,  25,0,25),
TH2F("table5", "Graviton 900", 8,0,8,  25,0,25),
TH2F("table6", "Graviton 1000", 8,0,8,  25,0,25),]
root_output=TFile("output2.root", "RECREATE")
for mass in masses:
    sign_ll=[]
    i=masses.index(mass)
    for b in jetbatg[:]:
        for ml in masslow[:]:
            for mh in masshigh[:]:
                        
#                rfile=TFile("../optimization/mc_"+str(int(b*10))+"_"+str(int(0.185*1000))+".root")
#                tree=rfile.Get("minitree")
#                bg=TH1F("bg"+str(mass), "", 100, 500, 2500)
#                tree.Draw("Inv_mass>>bg"+str(mass), "(fatjet_mass<135&&fatjet_mass>105&&dijet_mass>"+str(ml)+"&&dijet_mass<"+str(mh)+")*cross_section*2200*puWeight/norm")
#                bg1=bg.Integral(left[i],right[i])
#                root_output.cd()
#                bg.Write()
#                rfile.Close()
#                selected_bb_6_cmva_485_NoSyst_grav1000.root
                rfile=TFile("../optimization/selected_bb_6_cmva_"+str(int(b*1000))+"_NoSyst_grav"+str(mass)+".root")
                print rfile
                rfile.Print()
                tree=rfile.Get("minitree")
                sig=TH1F("sig"+str(mass)+"_bb_"+str(int(b*1000))+"_"+str(ml)+"<dijet_mass<"+str(mh), "", 100, 500, 2500)                
                tree.Draw("Inv_mass>>"+sig.GetName(), "(fatjet_mass<135&&fatjet_mass>105&&dijet_mass>"+str(ml)+"&&dijet_mass<"+str(mh)+")*cross_section*2690*puWeight/norm")
                root_output.cd()
                sig.Write()
                print sig.Integral()
                print "maxe", sig.GetMaximumBin()
                maxi=sig.GetBinContent(sig.GetMaximumBin())
                print maxi, maxi/10
                a1=sig.FindFirstBinAbove(maxi/10)
                a2=sig.FindLastBinAbove(maxi/10)
                print "OK", left[i], right[i], a1, a2 
                sig1=sig.Integral(a1, a2)
                rfile.Close()
                bg1=0
                rfile=TFile("../optimization/selected_bb_6_cmva_"+str(int(b*1000))+"_NoSyst_mc.root")
                tree=rfile.Get("minitree")
                bg=TH1F("bg"+str(mass)+"_bb_"+str(int(b*1000))+"_"+str(ml)+"<dijet_mass<"+str(mh), "", 100, 500, 2500)
                tree.Draw("Inv_mass>>"+bg.GetName(), "(fatjet_mass<135&&fatjet_mass>105&&dijet_mass>"+str(ml)+"&&dijet_mass<"+str(mh)+")*cross_section*2690*puWeight/norm")
                bg1=bg.Integral(a1, a2 )
                print bg.Integral(), a1, a2
                root_output.cd()
                bg.Write()
                rfile.Close()
                significance=sig1/(1.5+bg1**0.5+0.05*bg1)
#                significance=sig1
                print significance, sig1, bg1
                sign_ll.append(significance)

    print sign_ll
    for s in range(len(sign_ll)):
        print len(sign_ll)
        print s/25+1, s%25+1
        sign_table[i].SetBinContent(s/25+1, s%25+1, sign_ll[s])

    axis=sign_table[i].GetXaxis()
    print axis
    axis.SetBinLabel(1,"0.185")
    axis.SetBinLabel(2,"0.285")
    axis.SetBinLabel(3,"0.385")
    axis.SetBinLabel(4,"0.485")
    axis.SetBinLabel(5,"0.585")
    axis.SetBinLabel(6,"0.685")
    axis.SetBinLabel(7,"0.785")
    axis.SetBinLabel(8,"0.885")
    axis2=sign_table[i].GetYaxis()
    print axis2
    axis2.SetBinLabel(1,"100-130")
    axis2.SetBinLabel(2,"100-135")
    axis2.SetBinLabel(3,"100-140")
    axis2.SetBinLabel(4,"100-145")
    axis2.SetBinLabel(5,"100-150")
    axis2.SetBinLabel(6,"105-130")
    axis2.SetBinLabel(7,"105-135")
    axis2.SetBinLabel(8,"105-140")
    axis2.SetBinLabel(9,"105-145")
    axis2.SetBinLabel(10,"105-150")
    axis2.SetBinLabel(11,"110-130")
    axis2.SetBinLabel(12,"110-135")
    axis2.SetBinLabel(13,"110-140")
    axis2.SetBinLabel(14,"110-145")
    axis2.SetBinLabel(15,"110-150")
    axis2.SetBinLabel(16,"115-130")
    axis2.SetBinLabel(17,"115-135")
    axis2.SetBinLabel(18,"115-140")
    axis2.SetBinLabel(19,"115-145")
    axis2.SetBinLabel(20,"115-150")
    axis2.SetBinLabel(21,"120-130")
    axis2.SetBinLabel(22,"120-135")
    axis2.SetBinLabel(23,"120-140")
    axis2.SetBinLabel(24,"120-145")
    axis2.SetBinLabel(25,"120-150")
    print sign_table[i].Integral()
c1.cd()
plot1 = TPad("p1", "The pad 80% of the height",0,0.5,0.33,1)
plot2 = TPad("p2", "The pad 20% of the height",0.33,0.5,0.66,1)
plot3 = TPad("p3", "The pad 80% of the height",0.66,0.5,1,1)
plot4 = TPad("p4", "The pad 20% of the height",0,0.5,0.33,0)
plot5 = TPad("p5", "The pad 80% of the height",0.33,0.5,0.66,0)
plot6= TPad("p6", "The pad 20% of the height",0.66,0.5,1.0,0)
#plot1.cd()
#CMS_lumi.CMS_lumi(plot1, iPeriod, iPos)
plot1.Draw()
#plot2.cd()
#CMS_lumi.CMS_lumi(plot2, iPeriod, iPos)
plot2.Draw()
#plot3.cd()
#CMS_lumi.CMS_lumi(plot3, iPeriod, iPos)
plot3.Draw()
#plot4.cd()
#CMS_lumi.CMS_lumi(plot4, iPeriod, iPos)
plot4.Draw()
#plot5.cd()
#CMS_lumi.CMS_lumi(plot5, iPeriod, iPos)
plot5.Draw()
#plot6.cd()
#CMS_lumi.CMS_lumi(plot6, iPeriod, iPos)
plot6.Draw()
plot1.cd()

print 3
sign_table[0].Draw("colz")
plot2.cd()

print 3
sign_table[1].Draw("colz")
plot3.cd()

print 3
sign_table[2].Draw("colz")
plot4.cd()

print 3
sign_table[3].Draw("colz")
plot5.cd()

print 3
sign_table[4].Draw("colz")
plot6.cd()

print 3
sign_table[5].Draw("colz")
c1.Print("table_tag_FOM.pdf")
root_output.Close()

