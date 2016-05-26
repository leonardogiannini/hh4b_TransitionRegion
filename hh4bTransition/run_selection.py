from selection import*
from ROOT import *

import sys

#tree_selection(file_string, isData=0, dataset="", cross_section=1.,bbtag_cut=0.8,jet_btag_cut=0.185):
#tree_controlregion(file_string, isData=0, dataset="", cross_section=1.,bbtag_cut=0.8,jet_btag_cut=0.185):

tree_selection(sys.argv[1],bbtag_cut=0.9, jet_btag_cut=0.185)
#tree_controlregion(sys.argv[1],bbtag_cut=0.9, jet_btag_cut=0.185)
