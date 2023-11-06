## Local production of S, SBI, I, Bkg of ggH in order to probe the competitive statistics available in central production
## Perform histogram overlays, finding particular variables inside TTrees (_file0->ls() == tree, with variables, such as mth.mth, etc.)
## Call this program via:
## `python3 histoverlayplotter.py`

#!/usr/bin/env python3                                                                                                                          
import ROOT
import argparse
import os
import CMS_lumi
import math
import numpy as np

#This script should be in the directory, or have the total path to the root file
f1 = ROOT.TFile.Open('ggH_123_H.root', 'READ')
f2 = ROOT.TFile.Open('ggH_127_C.root', 'READ')
f3 = ROOT.TFile.Open('ggH_126_H+C.root', 'READ')
f4 = ROOT.TFile.Open('ggH_124_I.root', 'READ')

##Need to normalize by xsec
##- proc 127 | xsec = 36.8071 -----------
##- proc 126 | xsec = 62.4109 -----------
##- proc 123 | xsec = 29.3133 ----------- 
##- proc 124 | xsec = -3.71846 |HC| Interference

x123 = 29.3133
x127 = 36.8071
x126 = 62.4109
x124 = -3.71846

    ## Inside each, we have tree->mth.mth variable, which has ~167068 entries

tree1 = f1.Get("tree")
hH = ROOT.TH1F("H", "ggH hypothesis shapes per m_{T}", 25, 125, 500) #1st the signal hist
#hH = f1.Get('tree')
    ## Need 3 for loops, one per tree - loop over events to fill histogram - define the TH1F object first then TH1F.Fill(tree.mth)
for i in range(0,tree1.GetEntries()): # want to go from 0th entry in mth.mth to last entry in mth.mth
    
    tree1.GetEntry(i)
    if tree1.mth < 160:
        continue
    hH.Fill(tree1.mth, x123/tree1.GetEntries())# * x123) # normalize by xsec (evtWeight stored in xsec value == usu +1 or -1 for I
    
tree2 = f2.Get("tree")
hC = ROOT.TH1F("C", "Continuum", 25, 125, 500) #2nd the continuum background
for i in range(0,tree2.GetEntries()):
    tree2.GetEntry(i)
    if tree2.mth < 160:
        continue
    hC.Fill(tree2.mth, x127/tree2.GetEntries())# * x127)

tree3 = f3.Get("tree")
hHC = ROOT.TH1F("HC", "SBI", 25, 125, 500) #3rd the $|H+C|^2$
for i in range(0,tree3.GetEntries()):
    tree3.GetEntry(i)
    if tree3.mth < 160:
        continue
    hHC.Fill(tree3.mth, x126/tree3.GetEntries())# * x126)

tree4 = f4.Get("tree")
hI = ROOT.TH1F("I", "Interference", 25, 125, 500) #4th the Interference term (-evtWeight)
for i in range(0,tree4.GetEntries()):
    tree4.GetEntry(i)
    if tree4.mth < 160:
        continue
    hI.Fill(tree4.mth, x124/tree4.GetEntries())# * x124)

    # Define output directory:                                                                                                                     
if not os.path.exists('combinedplots/'): os.makedirs('combinedplots/')
outputDir = "combinedplots/"

###Initialize histogram
# hist = ROOT.TH1F("", "", 800, 800)
# hist.setMarkerStyle(ROOT,kFullCircle)

# h1 = ROOT.TGraph(hH)
# h2 = ROOT.TGraph(hC)
# h3 = ROOT.TGraph(hHC)

# mg = ROOT.TMultiGraph() # multigraph initialization - https://root.cern/doc/master/classTMultiGraph.html#afc6700fbae200601558e164468e9890e
    
# hH.SetLineColor(2)
# hH.SetMarkerColor(2) # sets a different color per input
# #hH.RemovePoint(0)
# mg.Add(h1) # add by iterating through      
# #hist1.Draw("HIST")
# #hist.Draw("HIST SAME")                                                                              

# hC.SetLineColor(3)
# hC.SetMarkerColor(3)
# #hC.RemovePoint(0)
# mg.Add(h2)                                                                                           

# hHC.SetLineColor(4)
# hHC.SetMarkerColor(4)
# #hHC.RemovePoint(0)
# mg.Add(h3)

# mg.SetTitle("ggH HWW event histograms by #m_{T}")
# mg.Draw("PLC")

    #mg.GetHistogram().GetXaxis().SetRangeUser(20.5,120.);

canvas = ROOT.TCanvas('ggH events per m_{T}', 'ggH events per m_{T}', 800, 800)
canvas.cd()

canvas.SetGrid() #want a grid
#canvas.SetTitle("ggH hypotheses per m_{T}")
#canvas.SetTitleFont(12)
    #mg.SetMinimum(args.ymin);
    #mg.SetMaximum(args.ymax);
#mg.GetXaxis().SetRangeUser(100,3000) # axis is lower-case >_<
#mg.GetYaxis().SetRangeUser(0,100)
#mg.Draw('AP0') # connected line with error bar dots                                                                                 


###
hH.SetStats(0) #don't want statistics box
hH.GetYaxis().SetRangeUser(-1,10)
hH.SetTitle("ggH hypotheses per m_{T}")
hH.SetTitleFont(12)

hH.SetLineColor(858)
hH.SetLineWidth(2)
hH.SetMarkerStyle(20)
hH.SetMarkerColor(858)
#hH.SetFillColor(858)

hC.SetLineColor(877)
hC.SetLineWidth(2)
hC.SetMarkerStyle(21)
hC.SetMarkerColor(877)
#hC.SetFillColor(877)

hHC.SetLineColor(898)
hHC.SetLineWidth(2)
hHC.SetMarkerStyle(22)
hHC.SetMarkerColor(898)
#hHC.SetFillColor(898)

hI.SetLineColor(1)
hI.SetLineWidth(2)
hI.SetMarkerStyle(33)
hI.SetMarkerColor(1)

hH.GetXaxis().SetTitle("m_{T}")
hH.GetYaxis().SetTitle("\sigma_{wgt}/genEvents")

hH.Draw("HIST")
hH.Draw("SAME P")
hC.Draw("HIST SAME")
hC.Draw("SAME P")
hHC.Draw("HIST SAME")
hHC.Draw("SAME P")
hI.Draw("HIST SAME")
hI.Draw("SAME P")

legend = ROOT.TLegend(0.65, 0.5, 0.9, 0.7)#(0.65, 0.1, 0.9, 0.4) # x1, y1, x2, y2
legend.SetTextFont(72)
legend.SetBorderSize(0) #1
legend.SetFillStyle(0) #transparent
legend.SetTextSize(0.02)
legend.AddEntry(hH, 'H Signal', 'lp')
legend.AddEntry(hC, 'C Continuum', 'lp')
legend.AddEntry(hHC, '\ |H+C|^2', 'lp') #'f' for fill box
legend.AddEntry(hI, 'I Interference', 'lp')
legend.Draw()

CMS_lumi.cmsText = 'CMS'
CMS_lumi.writeExtraText = True
CMS_lumi.extraText = 'Preliminary Simulation'
CMS_lumi.lumi_13TeV = ""
CMS_lumi.CMS_lumi(canvas, 4, 11)
                                                                                              
canvas.Modified()
canvas.Update()
canvas.SaveAs(outputDir + "ggH_HWW_histos" + ".png")
