#!/bin/bash
for i in 500 550 600 650 700 750 800 900 1000 1200 1400 1600 1800 2000 2500
do
	echo "mass point $i"
	mkdir Limits/sig$i
	echo Limits/sig$i
#	combine datacard/hh2plus1_mX_$i\_13TeV.txt -M Asymptotic -v2 -t -1 -m $i -n CMSHH4b --rMax 1000 --rMin 0.0001 &> CMS_HH4b_$i\_13TeV_asymptoticCLs.out
	combine datacard/hh2plus1_mX_$i\_13TeV.txt -M Asymptotic -v2  -m $i -n CMSHH4b --rMax 1000 --rMin 0.0001 &> CMS_HH4b_$i\_13TeV_asymptoticCLs.out
	
	mv higgsCombineCMSHH4b.Asymptotic.mH$i\.root Limits/CMS_$i\_HH4b_13TeV_asymptoticCLs.root
	echo Limits/sig$i
	combine -M MaxLikelihoodFit --robustFit=1 --rMin=-5 --rMax=5 -t -1 --plots --out Limits/sig$i datacard/hh2plus1_mX_$i\_13TeV.txt &> CMS_HH4b_$i\_13TeV_MaxLikelihood.out
done
