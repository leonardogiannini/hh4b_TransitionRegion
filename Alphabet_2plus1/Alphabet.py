# Class def for full Alphabetization.
# Does everything except the pretty plots, but makes all components available.

import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy

# Our functions:
import Alphabet_Header
from Alphabet_Header import *
import Plotting_Header
from Plotting_Header import *
import Converters
from Converters import *
import Distribution_Header
from Distribution_Header import *

class Alphabetizer:
	def __init__(self, name, Dist_Plus, Dist_Minus):
		self.name = name
		self.DP = Dist_Plus
		self.DM = Dist_Minus
	def SetRegions(self, var_array, presel):
		# var_array = [x var, y var, x n bins, x min, x max, y n bins, y min, y max]
		self.X = var_array[0]
		self.Pplots = TH2F("added"+self.name, "", var_array[2],var_array[3],var_array[4],var_array[5],var_array[6],var_array[7])
		self.Mplots = TH2F("subbed"+self.name, "", var_array[2],var_array[3],var_array[4],var_array[5],var_array[6],var_array[7])
		for i in self.DP:
			 quick2dplot(i.File, i.Tree, self.Pplots, var_array[0], var_array[1], presel, i.weight)
		for j in self.DM:
			 quick2dplot(j.File, j.Tree, self.Mplots, var_array[0], var_array[1], presel, j.weight)
		self.TwoDPlot = self.Pplots.Clone("TwoDPlot_"+self.name)
		self.TwoDPlot.Add(self.Mplots, -1.)
	def GetRates(self, cut, bins, truthbins, center, FIT):
		self.center = center
		self.G = AlphabetSlicer(self.TwoDPlot, bins, cut[0], cut[1], center) # makes the A/B slices
		if len(truthbins)>0:
			self.truthG = AlphabetSlicer(self.TwoDPlot, truthbins, cut[0], cut[1], center) # makes the A/B slices
		else:
			self.truthG = None
		self.Fit = FIT # reads the right class in, should be initialized and set up already
		AlphabetFitter(self.G, self.Fit) # creates all three distributions (nominal, up, down)
	def MakeEst(self, var_array, antitag, tag):
		# makes an estimate in a region, based on an anti-tag region, of that variable in all dists
		self.Fit.MakeConvFactor(self.X, self.center)
		self.hists_EST = []
		self.hists_EST_SUB = []
		self.hists_EST_UP = []
		self.hists_EST_SUB_UP = []
		self.hists_EST_DN = []
		self.hists_EST_SUB_DN = []
		self.hists_MSR = []
		self.hists_MSR_SUB = []
		self.hists_ATAG = []
		for i in self.DP:
			index=str((self.DP).index(i))
			temphist = TH1F("Hist_VAL"+self.name+"_"+i.name+index, "", var_array[1], var_array[2], var_array[3])
			temphistN = TH1F("Hist_NOMINAL"+self.name+"_"+i.name+index, "", var_array[1], var_array[2], var_array[3])
			temphistU = TH1F("Hist_UP"+self.name+"_"+i.name+index, "", var_array[1], var_array[2], var_array[3])
			temphistD = TH1F("Hist_DOWN"+self.name+"_"+i.name+index, "", var_array[1], var_array[2], var_array[3])
			temphistA = TH1F("Hist_ATAG"+self.name+"_"+i.name+index, "", var_array[1], var_array[2], var_array[3])
			quickplot(i.File, i.Tree, temphist, var_array[0], tag, i.weight)
			quickplot(i.File, i.Tree, temphistN, var_array[0], antitag, "("+i.weight+"*"+self.Fit.ConvFact+")")
			quickplot(i.File, i.Tree, temphistU, var_array[0], antitag, "("+i.weight+"*"+self.Fit.ConvFactUp+")")
			quickplot(i.File, i.Tree, temphistD, var_array[0], antitag, "("+i.weight+"*"+self.Fit.ConvFactDn+")")
			quickplot(i.File, i.Tree, temphistA, var_array[0], antitag, i.weight)
			self.hists_MSR.append(temphist)
			self.hists_EST.append(temphistN)
			self.hists_EST_UP.append(temphistU)
			self.hists_EST_DN.append(temphistD)
			self.hists_ATAG.append(temphistA) 
		for i in self.DM:
			temphist = TH1F("Hist_SUB_VAL"+self.name+"_"+i.name, "", var_array[1], var_array[2], var_array[3])
			temphistN = TH1F("Hist_SUB_NOMINAL"+self.name+"_"+i.name, "", var_array[1], var_array[2], var_array[3])
			temphistU = TH1F("Hist_SUB_UP"+self.name+"_"+i.name, "", var_array[1], var_array[2], var_array[3])
			temphistD = TH1F("Hist_SUB_DOWN"+self.name+"_"+i.name, "", var_array[1], var_array[2], var_array[3])
			quickplot(i.File, i.Tree, temphist, var_array[0], tag, i.weight)
			quickplot(i.File, i.Tree, temphistN, var_array[0], antitag, "("+i.weight+"*"+self.Fit.ConvFact+")")
			quickplot(i.File, i.Tree, temphistU, var_array[0], antitag, "("+i.weight+"*"+self.Fit.ConvFactUp+")")
			quickplot(i.File, i.Tree, temphistD, var_array[0], antitag, "("+i.weight+"*"+self.Fit.ConvFactDn+")")
			self.hists_MSR_SUB.append(temphist)
			self.hists_EST_SUB.append(temphistN)
			self.hists_EST_SUB_UP.append(temphistU)
			self.hists_EST_SUB_DN.append(temphistD)
	def MakeEstVariable(self, variable, binBoundaries, antitag, tag):
		# makes an estimate in a region, based on an anti-tag region, of that variable in all dists
		
		self.Fit.MakeConvFactor(self.X, self.center)
		self.hists_EST = []
		self.hists_EST_SUB = []
		self.hists_EST_UP = []
		self.hists_EST_SUB_UP = []
		self.hists_EST_DN = []
		self.hists_EST_SUB_DN = []
		self.hists_MSR = []
		self.hists_MSR_SUB = []
		self.hists_MCR_SUB = []
		self.hists_ATAG = []
		self.hists_down30 = []
		self.hists_up30 = []
		for i in self.DP:
			index=str((self.DP).index(i))
			temphist = TH1F("Hist_VAL"+self.name+"_"+i.name+index, "", len(binBoundaries)-1, array('d',binBoundaries))
			temphistN = TH1F("Hist_NOMINAL"+self.name+"_"+i.name+index, "", len(binBoundaries)-1, array('d',binBoundaries))
			temphistU = TH1F("Hist_UP"+self.name+"_"+i.name+index, "", len(binBoundaries)-1, array('d',binBoundaries))
			temphistD = TH1F("Hist_DOWN"+self.name+"_"+i.name+index, "", len(binBoundaries)-1, array('d',binBoundaries))
			temphistA = TH1F("Hist_ATAG"+self.name+"_"+i.name+index, "", len(binBoundaries)-1, array('d',binBoundaries))
			print i.weight, "weight"
			quickplot(i.File, i.Tree, temphist, variable, tag, i.weight)
			quickplot(i.File, i.Tree, temphistN, variable, antitag, "("+i.weight+"*"+self.Fit.ConvFact+")")
			quickplot(i.File, i.Tree, temphistU, variable, antitag, "("+i.weight+"*"+self.Fit.ConvFactUp+")")
			quickplot(i.File, i.Tree, temphistD, variable, antitag, "("+i.weight+"*"+self.Fit.ConvFactDn+")")
			quickplot(i.File, i.Tree, temphistA, variable, antitag, i.weight)
			self.hists_MSR.append(temphist)
			self.hists_EST.append(temphistN)
			self.hists_EST_UP.append(temphistU)
			self.hists_EST_DN.append(temphistD)
			self.hists_ATAG.append(temphistA)
		for i in self.DM:
			temphist = TH1F("Hist_SUB_VAL"+self.name+"_"+i.name, "", len(binBoundaries)-1, array('d',binBoundaries))
			temphistA = TH1F("Hist_SUB_ATAG"+self.name+"_"+i.name, "", len(binBoundaries)-1, array('d',binBoundaries))
#			temphistU = TH1F("Hist_SUB_UP"+self.name+"_"+i.name, "",len(binBoundaries)-1, array('d',binBoundaries))
#			temphistD = TH1F("Hist_SUB_DOWN"+self.name+"_"+i.name, "", len(binBoundaries)-1, array('d',binBoundaries))
			temphistU30 = TH1F("Hist_SUB_30percent_up"+self.name+"_"+i.name, "",len(binBoundaries)-1, array('d',binBoundaries))
			temphistD30 = TH1F("Hist_SUB_30percent_down"+self.name+"_"+i.name, "", len(binBoundaries)-1, array('d',binBoundaries))
			quickplot(i.File, i.Tree, temphist, variable, tag, "("+i.weight+")*(isCR)")
			quickplot(i.File, i.Tree, temphistU30, variable, tag, "("+i.weight+")*(1.3)*(isCR)")
			quickplot(i.File, i.Tree, temphistD30, variable, tag, "("+i.weight+")*(0.7)*(isCR)")
			quickplot(i.File, i.Tree, temphistA, variable, antitag, "("+i.weight+")*(isCR==0)")
#			quickplot(i.File, i.Tree, temphistU, variable, antitag, "("+i.weight+"*"+self.Fit.ConvFactUp+")")
#			quickplot(i.File, i.Tree, temphistD, variable, antitag, "("+i.weight+"*"+self.Fit.ConvFactDn+")")
			self.hists_MSR_SUB.append(temphist)
			self.hists_MCR_SUB.append(temphistA)
#			self.hists_EST_SUB_UP.append(temphistU)
#			self.hists_EST_SUB_DN.append(temphistD)
			self.hists_down30.append(temphistD30 )
			self.hists_up30.append(temphistU30 )

	def SetRegionsDouble(self, var_array, presel):
	# var_array = [x var, y var, x n bins, x min, x max, y n bins, y min, y max, z var, z n bins, z min, z max]
		self.X = var_array[0]
		self.Y = var_array[1]
		print var_array[9],var_array[10],var_array[11]
		self.Pplots = TH3F("added"+self.name, "", var_array[2],var_array[3],var_array[4],var_array[5],var_array[6],var_array[7], var_array[9],var_array[10],var_array[11])
		self.Mplots = TH3F("subbed"+self.name, "", var_array[2],var_array[3],var_array[4],var_array[5],var_array[6],var_array[7], var_array[9],var_array[10],var_array[11])
		for i in self.DP:
			 quick3dplot(i.File, i.Tree, self.Pplots, var_array[0], var_array[1], var_array[8], presel, i.weight)
		for j in self.DM:
			 quick3dplot(j.File, j.Tree, self.Mplots, var_array[0], var_array[1], var_array[8], presel, j.weight)
		self.ThreeDPlot = self.Pplots.Clone("ThreeDPlot_"+self.name)
		self.ThreeDPlot.Add(self.Mplots, -1.)
	def GetRatesDouble(self, cut, bins, bins2, truthbins, truthbins2, center, center2, FIT):
		self.center = center
		self.G = AlphabetSlicer3d(self.ThreeDPlot, bins, bins2, cut[0], cut[1], center, center2) # makes the A/B slices
		if len(truthbins)>0:
			self.truthG = AlphabetSlicer3d(self.ThreeDPlot, truthbins, truthbins2, cut[0], cut[1], center, center2) # makes the A/B slices
		else:
			self.truthG = None
		self.Fit = FIT # reads the right class in, should be initialized and set up already
		AlphabetFitter(self.G, self.Fit) # creates all three distributions (nominal, up, down)
    
