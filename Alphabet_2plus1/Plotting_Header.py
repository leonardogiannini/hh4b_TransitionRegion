#
import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import scipy

def writeplot(myTree, plot, var, Cut, Weight): # Fills a plot from a file (needs to have a TTree called "tree"... might change this later)
#        print var3+":"+var2+":"+var+">>"+"temp", "("+ Weight+")*("+Cut+")", "writeplot"
        temp = plot.Clone("temp") # Allows to add multiple distributions to the plot
        myTree.Draw(var+">>"+"temp", "("+ Weight+")*("+Cut+")", "goff")
        print temp.Integral()
         # Actual plotting (and making of the cut + Weighing if necsr)
        plot.Add(temp)



def quickplot(File, tree, plot, var, Cut, Weight): # Fills  a plot from a file (needs to have a TTree called "tree"...)
        print var+">>"+"temp", "("+Weight+")*("+Cut+")"
        print "quikplot"
        temp = plot.Clone("temp") # Allows to add multiple distributions to the plot
        chain = ROOT.TChain(tree)
        chain.Add(File)
        n=chain.Draw(var+">>"+"temp", "("+Weight+")*("+Cut+")", "goff")
        print temp.Integral()
         # Actual plotting (and making of the cut + Weighing if necsr)
        plot.Add(temp)
        

def quick2dplot(File, tree, plot, var, var2, Cut, Weight): # Same as above, but 2D plotter
        temp = plot.Clone("temp")
        chain = ROOT.TChain(tree)
        chain.Add(File)
        chain.Draw(var2+":"+var+">>"+"temp", "("+ Weight+")*("+Cut+")", "goff")
        
        plot.Add(temp)


def quick3dplot(File, tree, plot, var, var2, var3, Cut, Weight): # Same as above, but 2D plotter
        print var3+":"+var2+":"+var+">>"+"temp", "("+ Weight+")*("+Cut+")"
        print "quik3d"
        temp = plot.Clone("temp")
        chain = ROOT.TChain(tree)
        chain.Add(File)
        chain.Draw(var3+":"+var2+":"+var+">>"+"temp", "("+ Weight+")*("+Cut+")", "goff")
        
        plot.Add(temp)

def FindAndSetMax(someset):
        maximum = 0.0
        for i in someset:
                i.SetStats(0)
                t = i.GetMaximum()
                if t > maximum:
                        maximum = t
        for j in someset:
                j.GetYaxis().SetRangeUser(0,maximum*1.25)
