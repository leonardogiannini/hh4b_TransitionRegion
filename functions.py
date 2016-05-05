from ROOT import *

import array, os, sys, numpy, copy

def div_except(a, b):
    if b>0:
        return float(a)/b
    else:
        return 1

jet_pT_cut=30
jet_eta_cut=2.4
jet_btag_cut=0.185
bbtag_cut=0.3
tau21_cut=1.


def veto_boosted_event(f_vars):
    boosted=-1
#F_vars=[tree.nFatjetAK08ungroomed, tree.FatjetAK08ungroomed_pt, tree.FatjetAK08ungroomed_eta, tree.FatjetAK08ungroomed_phi,
#tree.FatjetAK08ungroomed_mass, tree.FatjetAK08ungroomed_mprunedcorr, tree.FatjetAK08ungroomed_tau1, tree.FatjetAK08ungroomed_tau2,
#tree.FatjetAK08ungroomed_bbtag, tree.FatjetAK08ungroomed_mpruned]
    if f_vars[0]>1:
        indexes=[]
        for i in range(0, f_vars[0]):
            if (abs( f_vars[2][i])<2.4 and  f_vars[1][i]>300):
                indexes.append(i)
        print "primi jet buoni", indexes
        try: ij1=indexes[0]
        except: ij1=-1
        try: ij2=indexes[1]
        except: ij2=-1
        if (ij1>-1 and ij2>-1):
            if abs( f_vars[2][ij1]- f_vars[2][ij2])<1.3:
                if  (f_vars[8][ij1]>0.6 and f_vars[8][ij2]>0.6):
                     if  (f_vars[5][ij1]>105 and f_vars[5][ij2]>105):
                        if  (f_vars[5][ij1]<135 and f_vars[5][ij2]<135):
                            if f_vars[6][ij1]>0: fatjet_tau21=f_vars[7][ij1]/f_vars[6][ij1]
                            else: fatjet_tau21=1
                            if f_vars[6][ij2]>0: fatjet2_tau21=f_vars[7][ij2]/f_vars[6][ij2]
                            else: fatjet2_tau21=1
                            boosted=1
                            if fatjet2_tau21<0.6 and fatjet_tau21<0.6:
                                boosted=0.6
    return boosted

#devo prendere i primi 2 jet centrali con pt>300
#chiedere deltaeta, tau21, hbb, mprunedcorr

def veto_resolved_event(jet_variables):
    print 1
    return

#qui devo rivedere il codice della resolved

def sort_by_mass_save_candidates(f_vars, j_vars, systematic):
    count_fatjets=0
    count_jetsoutsidef=0
    leading_mass_old=40.
    leading_index=-1
    Fatjets_array=numpy.zeros((f_vars[0], 2))
    jets_btag_array=numpy.zeros((j_vars[0], 4))
    Fatjets_array=Fatjets_array-1
    jets_btag_array=jets_btag_array-1
    for n in range(f_vars[0]):
        Fatjets_array[n][0]=f_vars[5][n]
        Fatjets_array[n][1]=n
    #get indexes sorted by mass
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
            fj_p4=TLorentzVector()                    
            fj_p4.SetPtEtaPhiM(f_vars[1][leading_index], f_vars[2][leading_index], f_vars[3][leading_index], f_vars[4][leading_index])
#            print f_vars[9][leading_index], f_vars[5][leading_index]
#            F_vars=[tree.nFatjetAK08ungroomed, tree.FatjetAK08ungroomed_pt, tree.FatjetAK08ungroomed_eta, tree.FatjetAK08ungroomed_phi, tree.FatjetAK08ungroomed_mass, 
#            5)tree.FatjetAK08ungroomed_mprunedcorr, 
#            6)tree.FatjetAK08ungroomed_tau1, 7)tree.FatjetAK08ungroomed_tau2,
#            8)tree.FatjetAK08ungroomed_bbtag, 
#               9)tree.FatjetAK08ungroomed_mprunedcorr_UP, 10)tree.FatjetAK08ungroomed_JEC_L1L2L3, 
#                11) tree.FatjetAK08ungroomed_JEC_UP, 12)tree.FatjetAK08ungroomed_JER_UP_PT ]

            if (systematic=="FJEC_Up"):
                correction_factor=1+(f_vars[11][leading_index]-f_vars[10][leading_index])
                fj_p4*=correction_factor
            
            if (systematic=="FJEC_Down"):
                correction_factor=1-(f_vars[11][leading_index]-f_vars[10][leading_index])
                fj_p4*=correction_factor
                
            if (systematic=="FJER_Up"):
                correction_factor=div_except(f_vars[12][leading_index],f_vars[1][leading_index])
                fj_p4*=correction_factor
            
            if (systematic=="FJER_Down"):
                pJERDown=2*f_vars[1][leading_index]-f_vars[12][leading_index]
                correction_factor=div_except((pJERDown),f_vars[1][leading_index])
                fj_p4*=correction_factor
                
          
   
            if (abs(fj_p4.Eta())<jet_eta_cut and f_vars[8][leading_index]>bbtag_cut and f_vars[5][leading_index]>40 and (f_vars[7][leading_index]/f_vars[6][leading_index])<tau21_cut):
                count_fatjets=count_fatjets+1
                for j in range( j_vars[0]):
#                    print "pt", j_vars[1][j], "JEC", j_vars[6][j], j_vars[7][j], j_vars[8][j], "JER", j_vars[9][j], j_vars[10][j], j_vars[11][j]
                    if (systematic=="JEC_Up"): 
                        try: jet_pT = j_vars[1][j]*j_vars[6][j]/j_vars[7][j] 
                        except: jet_pT = j_vars[1][j]
                    elif (systematic=="JEC_Down"): 
                        try: jet_pT = j_vars[1][j]*j_vars[8][j]/j_vars[7][j] 
                        except: jet_pT = j_vars[1][j]
                    elif (systematic=="JER_Up"): 
                        try: jet_pT = j_vars[1][j]*j_vars[9][j]/j_vars[10][j]
                        except: jet_pT = j_vars[1][j]
                    elif (systematic=="JER_Down"): 
                        try: jet_pT = j_vars[1][j]*j_vars[11][j]/j_vars[10][j] 
                        except: jet_pT = j_vars[1][j]
                    else: jet_pT = j_vars[1][j]

                    j_p4=TLorentzVector()
                    j_p4.SetPtEtaPhiM(jet_pT,j_vars[2][j], j_vars[3][j], j_vars[4][j])
                    deltaR=j_p4.DeltaR(fj_p4)
                    if (j_p4.Pt()>jet_pT_cut and abs(j_p4.Eta())<jet_eta_cut and deltaR>1.5):
                        count_jetsoutsidef+=1
                        save_jet_index.append(j)
                        print "empty", jets_btag_array[j]
                        print j
                        jets_btag_array[j][0]=j_vars[5][j]
                        jets_btag_array[j][1]=j
                        jets_btag_array[j][2]=leading_index
                        jets_btag_array[j][3]=j_p4.Pt() 
                        print "filled", jets_btag_array[j]
                if count_jetsoutsidef>1:
                    save_index.append(leading_index)
                    print jets_btag_array
                    print "array ritornato ?"                 
    return save_index, jets_btag_array, count_jetsoutsidef, count_fatjets

