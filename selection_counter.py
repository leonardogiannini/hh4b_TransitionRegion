from ROOT import *
import array, os, sys, numpy, copy

def tree_selection_and(file_string, isData=0, dataset="", cross_section=1.,bbtag_cut=0.9,jet_btag_cut=0.185):
    cut3=0
    cut4=0
    cut5=0
    cut6=0
    print dataset
    print file_string
    try:
        myFile=TFile(file_string, "R")
        tree=myFile.Get("MyTree")
        count_histo=copy.copy(myFile.Get("cutflow"))
        tree.Print("*AA*")
    except:
        print "no file"
    postfix="NoSyst"
    if "JEC_Up" in file_string:
        postfix="JEC_Up"
    if "FJEC_Up" in file_string:
        postfix="FJEC_Up"
    if "JER_Up" in file_string:
        postfix="JER_Up"
    if "FJER_Up" in file_string:
        postfix="FJER_Up"
    if "MJEC_Up" in file_string:
        postfix="MJEC_Up"
    if "JEC_Down" in file_string:
        postfix="JEC_Down"
    if "FJEC_Down" in file_string:
        postfix="FJEC_Down"
    if "JER_Down" in file_string:
        postfix="JER_Down"
    if "FJER_Down" in file_string:
        postfix="FJER_Down"
    if "MJEC_Down" in file_string:
        postfix="MJEC_Down"

    elif "JetHT" in file_string:
        postfix="JetHT"
    elif "BTagCSV" in file_string:
        postfix="BTagCSV"
    print file_string.split("_")[-1], "_"+postfix+"_"
    print "../selection/selected"+"_"+postfix+"_"+file_string.split("_")[-1]
    name="_"+postfix+"_"+file_string.split("_")[-1]
    print "../selection/selected"+name
    print float(bbtag_cut)*10,float(jet_btag_cut)*1000
    Tag="_bb_"+str(int(float(bbtag_cut)*10))+"_cmva_"+str(int(float(jet_btag_cut)*1000))
    print Tag
    print "../selection/selected"+Tag+name,

    AnaysisFile=TFile("../selection/selected"+Tag+name, "recreate")
    
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
    v1=array.array('f', [0.])
    trigger1=array.array('f', [0.])
    trigger2=array.array('f', [0.])
    trigger3=array.array('f', [0.])
    trigger_pre=array.array('f', [0.])
    
    SF=array.array('f', [0.])
    SFup=array.array('f', [0.])
    SFdown=array.array('f', [0.])
    
    cmvaSF=array.array('f', [0.])
    cmvaSFup=array.array('f', [0.])
    cmvaSFdown=array.array('f', [0.])
    cmvaSF2=array.array('f', [0.])
    cmvaSFup2=array.array('f', [0.])
    cmvaSFdown2=array.array('f', [0.])
    
    
    puW_up=array.array('f', [0.])
    puW_down=array.array('f', [0.])
    
    MyTree.Branch("Inv_mass", f1, "Invariant mass")
    MyTree.Branch("dijet_mass", g1, "dijet_mass")
    MyTree.Branch("fatjet_mass", h1, "fatjet_mass")
    MyTree.Branch("cross_section", i1, "cross_section")
    MyTree.Branch("fatjet_hbb", l1, "fatjet_hbb")
    MyTree.Branch("isCR", m1, "isCR")
    MyTree.Branch("Vtype", q1, "Vtype")
    MyTree.Branch("puWeight", o1, "puWeight")
    MyTree.Branch("norm", p1, "norm")
    MyTree.Branch("n_OkJets", r1, "n_OkJets")
    MyTree.Branch("n_OkFj", s1, "n_OkFj")
    MyTree.Branch("evt", t1, "evt")
    MyTree.Branch("boosted", u1, "boosted")
    MyTree.Branch("resolved", v1, "resolved")
    MyTree.Branch("HLT_ht800", trigger1, "HLT_ht800")
    MyTree.Branch("HLT_AK08", trigger2, "HLT_AK08")
    MyTree.Branch("HLT_HH4b", trigger3, "HLT_HH4b")
    MyTree.Branch("HLT_ht350", trigger_pre, "HLT_ht350")
    
    MyTree.Branch("SF", SF, "SF")
    MyTree.Branch("SFup", SFup, "SFup")
    MyTree.Branch("SFdown", SFdown, "SFdown")
    MyTree.Branch("cmvaSF", cmvaSF, "cmvaSF")
    MyTree.Branch("cmvaSFup", cmvaSFup, "cmvaSFup")
    MyTree.Branch("cmvaSFdown", cmvaSFdown, "cmvaSFdown")
    MyTree.Branch("cmvaSF2", cmvaSF2, "cmvaSF2")
    MyTree.Branch("cmvaSFup2", cmvaSFup2, "cmvaSFup2")
    MyTree.Branch("cmvaSFdown2", cmvaSFdown2, "cmvaSFdown2")
    
    MyTree.Branch("puWeightUp", puW_up, "puWeightUp")
    MyTree.Branch("puWeightDown", puW_down, "puWeightDown")


#    print tree
    maxi=tree.GetEntries()
    for entry in range(maxi):
#        print entry, bbtag_cut, jet_btag_cut
        tree.GetEntry(entry)
#        if len(tree.fatjets_pt)>1:
#            print len(tree.fatjets_pt)
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
                        j_p4=TLorentzVector()
                        j_p4.SetPtEtaPhiM(tree.jets_pt[j], tree.jets_eta[j], tree.jets_phi[j], tree.jets_mass[j])
                        deltaR=j_p4.DeltaR(fj_p4)
#                        print deltaR, tree.jets_btag[j]
#                        print jet_btag_cut
                        if (tree.jets_btag[j]>jet_btag_cut and deltaR>1.5):
                            count_jetsoutsidef+=1
                            save_jet_index.append(j)
                        if (tree.jets_btag[j]<jet_btag_cut and deltaR>1.5):
                            count_jetsoutsidef_atag+=1
                            save_atag_jet_index.append(j)
#                        print save_jet_index, save_atag_jet_index
                        
                if count_jetsoutsidef>1:
                    save_index.append(leading_index)
                    print "jet-fatjet", tree.fatjets_bbtag[leading_index]
                            
        if ( count_fatjets>=1): cut3=cut3+1
        if (count_jetsoutsidef>=2 and count_fatjets>=1):
            cut4=cut4+1
            
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
                            m_diff=abs(tree.fatjets_mprunedcorr[j]-(jet3_p4+jet4_p4).M())
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
                mH1=tree.fatjets_mprunedcorr[H1fatjet_i]
                mH2=(jet3_p4+jet4_p4).M()

        #                        region=withinRegion(mH1, mH2, 20., 10., 110., 120.)
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
                u1[0]=tree.boosted_evt
                v1[0]=tree.resolved_evt
                trigger1[0]=tree.HLT_ht800
                trigger2[0]=tree.HLT_AK08
                trigger3[0]=tree.HLT_HH4b
                trigger_pre[0]=tree.HLT_ht350
                if pTH1<300:
                    sf=0.913
                    sfup=sf+0.15
                    sfd=sf-0.15
                elif pTH1<400:
                    sf=0.913
                    sfup=sf+0.088
                    sfd=sf-0.088
                elif pTH1<500:
                    sf=0.914
                    sfup=sf+0.141
                    sfd=sf-0.141
                else:
                    sf=0.914
                    sfup=sf+0.15
                    sfd=sf-0.15
                SF[0]=sf
                SFup[0]=sfup
                SFdown[0]=sfd
                
                cmvaSF[0]=tree.CMVAweight[H2jet1_i]
                cmvaSFup[0]=tree.CMVAweightUp[H2jet1_i]
                cmvaSFdown[0]=tree.CMVAweightDown[H2jet1_i]
                cmvaSF2[0]=tree.CMVAweight[H2jet2_i]
                cmvaSFup2[0]=tree.CMVAweightUp[H2jet2_i]
                cmvaSFdown2[0]=tree.CMVAweightDown[H2jet2_i]
                
                
                puW_up[0]=tree.puWeightUp
                puW_down[0]=tree.puWeightDown
                MyTree.Fill()
                cut5=cut5+1
                if (mH2<135 and mH2>105 and mH1<135 and mH1>105):
                    cut6=cut6+1
    count_histo.SetBinContent(5, cut4)
    count_histo.SetBinContent(6, cut5)
    count_histo.SetBinContent(7, cut6)
    print cut3
    for i in range(1,8):
        print count_histo.GetBinContent(i)
    count_histo.Write()
    MyTree.Write()
    AnaysisFile.Close()

    myFile.Close()


def tree_controlregion_and(file_string, isData=0, dataset="", cross_section=1.,bbtag_cut=0.9,jet_btag_cut=0.185):
    cut3=0
    cut4=0
    cut5=0
    cut6=0
    print dataset
    print file_string
    try:
        myFile=TFile(file_string, "R")
        tree=myFile.Get("MyTree")
        count_histo=copy.copy(myFile.Get("cutflow"))
        tree.Print("*AA*")
    except:
        print "no file"
    postfix="NoSyst"
    if "JEC_Up" in file_string:
        postfix="JEC_Up"
    if "FJEC_Up" in file_string:
        postfix="FJEC_Up"
    if "JER_Up" in file_string:
        postfix="JER_Up"
    if "FJER_Up" in file_string:
        postfix="FJER_Up"
    if "MJEC_Up" in file_string:
        postfix="MJEC_Up"
    if "JEC_Down" in file_string:
        postfix="JEC_Down"
    if "FJEC_Down" in file_string:
        postfix="FJEC_Down"
    if "JER_Down" in file_string:
        postfix="JER_Down"
    if "FJER_Down" in file_string:
        postfix="FJER_Down"
    if "MJEC_Down" in file_string:
        postfix="MJEC_Down"
    elif "JetHT" in file_string:
        postfix="JetHT"
    elif "BTagCSV" in file_string:
        postfix="BTagCSV"
    print file_string.split("_")[-1], "_"+postfix+"_"
    print "../selection/selected"+"_"+postfix+"_"+file_string.split("_")[-1]
    name="_"+postfix+"_"+file_string.split("_")[-1]
    print "../selection/selected"+name
    print float(bbtag_cut)*10,float(jet_btag_cut)*1000
    Tag="_bb_"+str(int(float(bbtag_cut)*10))+"_cmva_"+str(int(float(jet_btag_cut)*1000))
    print Tag
    print "../selection/selected"+Tag+name,

    AnaysisFile=TFile("../selection/selectedAtag"+Tag+name, "recreate")
    
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
    v1=array.array('f', [0.])
    trigger1=array.array('f', [0.])
    trigger2=array.array('f', [0.])
    trigger3=array.array('f', [0.])
    trigger_pre=array.array('f', [0.])
    
    SF=array.array('f', [0.])
    SFup=array.array('f', [0.])
    SFdown=array.array('f', [0.])
    
    cmvaSF=array.array('f', [0.])
    cmvaSFup=array.array('f', [0.])
    cmvaSFdown=array.array('f', [0.])
    cmvaSF2=array.array('f', [0.])
    cmvaSFup2=array.array('f', [0.])
    cmvaSFdown2=array.array('f', [0.])
    
    puW_up=array.array('f', [0.])
    puW_down=array.array('f', [0.])
    
    MyTree.Branch("Inv_mass", f1, "Invariant mass")
    MyTree.Branch("dijet_mass", g1, "dijet_mass")
    MyTree.Branch("fatjet_mass", h1, "fatjet_mass")
    MyTree.Branch("cross_section", i1, "cross_section")
    MyTree.Branch("fatjet_hbb", l1, "fatjet_hbb")
    MyTree.Branch("isCR", m1, "isCR")
    MyTree.Branch("Vtype", q1, "Vtype")
    MyTree.Branch("puWeight", o1, "puWeight")
    MyTree.Branch("norm", p1, "norm")
    MyTree.Branch("n_OkJets", r1, "n_OkJets")
    MyTree.Branch("n_OkFj", s1, "n_OkFj")
    MyTree.Branch("evt", t1, "evt")
    MyTree.Branch("boosted", u1, "boosted")
    MyTree.Branch("resolved", v1, "resolved")
    MyTree.Branch("HLT_ht800", trigger1, "HLT_ht800")
    MyTree.Branch("HLT_AK08", trigger2, "HLT_AK08")
    MyTree.Branch("HLT_HH4b", trigger3, "HLT_HH4b")
    MyTree.Branch("HLT_ht350", trigger_pre, "HLT_ht350")
    
    MyTree.Branch("SF", SF, "SF")
    MyTree.Branch("SFup", SFup, "SFup")
    MyTree.Branch("SFdown", SFdown, "SFdown")
    MyTree.Branch("cmvaSF", cmvaSF, "cmvaSF")
    MyTree.Branch("cmvaSFup", cmvaSFup, "cmvaSFup")
    MyTree.Branch("cmvaSFdown", cmvaSFdown, "cmvaSFdown")
    MyTree.Branch("cmvaSF2", cmvaSF2, "cmvaSF2")
    MyTree.Branch("cmvaSFup2", cmvaSFup2, "cmvaSFup2")
    MyTree.Branch("cmvaSFdown2", cmvaSFdown2, "cmvaSFdown2")
    
    MyTree.Branch("puWeightUp", puW_up, "puWeightUp")
    MyTree.Branch("puWeightDown", puW_down, "puWeightDown")


#    print tree
    maxi=tree.GetEntries()
    for entry in range(maxi):
#        print entry
        tree.GetEntry(entry)
#        if len(tree.fatjets_pt)>1:
#            print len(tree.fatjets_pt)
        count_fatjets=0
        count_jetsoutsidef=0
        count_jetsoutsidef_atag=0
        leading_mass_old=40.
        leading_index=-1

        save_index=[]
        save_jet_index=[]
        save_atag_jet_index=[]
        foundHH=0
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
                if count_jetsoutsidef>0:
                    save_index.append(leading_index)
                            
            
            if (count_jetsoutsidef==1 and count_jetsoutsidef_atag>1 and count_fatjets>=1):
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
                                m_diff=abs(tree.fatjets_mprunedcorr[j]-(jet3_p4+jet4_p4).M())
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
            mH1=tree.fatjets_mprunedcorr[H1fatjet_i]
            mH2=(jet3_p4+jet4_p4).M()

#                        region=withinRegion(mH1, mH2, 20., 10., 110., 120.)
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
            v1[0]=tree.resolved_evt
            trigger1[0]=tree.HLT_ht800
            trigger2[0]=tree.HLT_AK08
            trigger3[0]=tree.HLT_HH4b
            trigger_pre[0]=tree.HLT_ht350
            
            if pTH1<300:
                sf=0.9135
                sfup=sf+0.15
                sfd=sf-0.15
            elif pTH1<400:
                sf=0.913
                sfup=sf+0.088
                sfd=sf-0.088
            elif pTH1<500:
                sf=0.914
                sfup=sf+0.141
                sfd=sf-0.141
            else:
                sf=0.9135
                sfup=sf+0.15
                sfd=sf-0.15
            SF[0]=sf
            SFup[0]=sfup
            SFdown[0]=sfd
            
            cmvaSF[0]=tree.CMVAweight[H2jet1_i]
            cmvaSFup[0]=tree.CMVAweightUp[H2jet1_i]
            cmvaSFdown[0]=tree.CMVAweightDown[H2jet1_i]
            cmvaSF2[0]=tree.CMVAweight[H2jet2_i]
            cmvaSFup2[0]=tree.CMVAweightUp[H2jet2_i]
            cmvaSFdown2[0]=tree.CMVAweightDown[H2jet2_i]
            
            puW_up[0]=tree.puWeightUp
            puW_down[0]=tree.puWeightDown
            MyTree.Fill()
            
        if ( count_fatjets>=1): cut3=cut3+1
        if (count_jetsoutsidef==1 and count_jetsoutsidef_atag>1 and count_fatjets>=1): 
            cut4=cut4+1
            if (foundHH==1): 
                cut5=cut5+1
                if (mH2<135 and mH2>105 and mH1<135 and mH1>105):
                    cut6=cut6+1
    count_histo.SetBinContent(5, cut4)
    count_histo.SetBinContent(6, cut5)
    count_histo.SetBinContent(7, cut6)
    print cut3
    for i in range(1,8):
        print count_histo.GetBinContent(i)
    count_histo.Write()

    MyTree.Write()
    AnaysisFile.Close()

    myFile.Close()
    
