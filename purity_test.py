from ROOT import TLorentzVector


def purityTest(j, b, jMatchedbindex):
	nMatches=0
	for i_j in range(4):
		mindR=0.4
		for i_b in range(4):
			dR=j[i_j].DeltaR(b[i_j])
			if (dR<mindR):
				mindR=dR
        		jMatchedbindex[i_j]=i_b
		if (jMatchedbindex[i_j]!=-1):
			for i_i_j in range(i_j):      
				if (jMatchedbindex[i_j]==jMatchedbindex[i_i_j]):
					return -1
     			nMatches=nMatches+1
	return nMatches
			
				
def purityTest21(j, bb_plus_H, jMatchedbindex):
	nMatches=0
	for i_j in range(2):
		mindR=0.4
		for i_b in range(4):
			dR=j[i_j].DeltaR(bb_plus_H[i_b])
#			print i_j,i_b,dR
			if (dR<mindR):
				mindR=dR				
				jMatchedbindex[i_j]=i_b
				
	
	mindRfat=0.8
	for i_h in range(4,6):
		dR=j[2].DeltaR(bb_plus_H[i_h])
		if (dR<mindRfat):
			mindRfat=dR
			jMatchedbindex[2]=i_h
	for i_j in range(3):
		if (jMatchedbindex[i_j]!=-1):
			for i_i_j in range(i_j):      
				if (jMatchedbindex[i_j]==jMatchedbindex[i_i_j]):
					return -1
			nMatches=nMatches+1
	
	return nMatches
		

def purityTest11(j, H_H, jMatchedbindex):
	for i_j in range(2):
		mindR=0.8
		for i_h in range(2):
			dR=j[i_j].DeltaR(H_H[i_j])
			if (dR<mindR):
				mindR=dR
        		jMatchedbindex[i_j]=i_h
	if (jMatchedbindex[i_j]!=-1):
			for i_i_j in range(i_j):      
				if (jMatchedbindex[i_j]==jMatchedbindex[i_i_j]):
					return -1
     			nMatches=nMatches+1
	return nMatches
