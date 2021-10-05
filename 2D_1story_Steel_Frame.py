# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 20:28:18 2021

@author: erayt
"""
from openseespy.opensees import *

import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

import matplotlib.pyplot as plt
import openseespy.postprocessing.Get_Rendering as opsplt
import openseespy.postprocessing.ops_vis as opsv


AnalysisType='Pushover'	;		#  Pushover  Gravity

## ------------------------------
## Start of model generation
## -----------------------------
# remove existing model
wipe()

# set modelbuilder
model('basic', '-ndm', 2, '-ndf', 3)

import math

############################################
### Units and Constants  ###################
############################################

inch = 1;
kip = 1;
sec = 1;

# Dependent units
sq_in = inch*inch;
ksi = kip/sq_in;
ft = 12*inch;

# Constants
g = 386.2*inch/(sec*sec);
pi = math.acos(-1);

#######################################
##### Dimensions 
#######################################

# Dimensions Input
H_story=10.0*ft;
W_bayX=16.0*ft;
W_bayY_ab=5.0*ft+10.0*inch;
W_bayY_bc=8.0*ft+4.0*inch;
W_bayY_cd=5.0*ft+10.0*inch;

# Calculated dimensions
W_structure=W_bayY_ab+W_bayY_bc+W_bayY_cd;

################
### Material
################

# Steel02 Material 

matTag=1;
matConnAx=2;
matConnRot=3;

Fy=60.0*ksi;		# Yield stress 
Es=29000.0*ksi;		# Modulus of Elasticity of Steel 
v=0.2;				# Poisson's ratio
Gs=Es/(1+v);		# Shear modulus
b=0.10;				# Strain hardening ratio
params=[18.0,0.925,0.15]		# R0,cR1,cR2
R0=18.0
cR1=0.925
cR2=0.15
a1=0.05
a2=1.00
a3=0.05
a4=1.0
sigInit=0.0
alpha=0.05

uniaxialMaterial('Steel02', matTag, Fy, Es, b, R0, cR1, cR2, a1, a2, a3, a4, sigInit)

# ##################
# ## Sections
# ##################

colSecTag1=1;
colSecTag2=2;
beamSecTag1=3;
beamSecTag2=4;
beamSecTag3=5;

# COMMAND: section('WFSection2d', secTag, matTag, d, tw, bf, tf, Nfw, Nff)

section('WFSection2d', colSecTag1, matTag, 10.5*inch, 0.26*inch, 5.77*inch, 0.44*inch, 15, 16)		# outer Column
section('WFSection2d', colSecTag2, matTag, 10.5*inch, 0.26*inch, 5.77*inch, 0.44*inch, 15, 16)		# Inner Column

#section('WFSection2d', beamSecTag1, matTag, 8.3*inch, 0.44*inch, 8.11*inch, 0.685*inch, 15, 15)		# outer Beam
#section('WFSection2d', beamSecTag2, matTag, 8.2*inch, 0.40*inch, 8.01*inch, 0.650*inch, 15, 15)		# Inner Beam
#section('WFSection2d', beamSecTag3, matTag, 8.0*inch, 0.40*inch, 7.89*inch, 0.600*inch, 15, 15)		# Inner Beam

# Beam size - W10x26
Abeam=7.61*inch*inch;
IbeamY=144.*(inch**4);			# Inertia along horizontal axis
IbeamZ=14.1*(inch**4);			# inertia along vertical axis

# BRB input data
Acore=2.25*inch;
Aend=10.0*inch;
LR_BRB=0.55;


# Create All main nodes
node(1, 0.0, 0.0)
node(2, W_bayX, 0.0)

node(11, 0.0, H_story)
node(12, W_bayX, H_story)


node(1101, 0.0, H_story)
node(1201, W_bayX, H_story)

ColIntTag1=1;
ColIntTag2=2;
BeamIntTag1=3;

#beamIntegration('Lobatto', ColIntTag1, colSecTag1, 6)
beamIntegration('HingeRadau', ColIntTag1, colSecTag1,1,colSecTag1, 10,colSecTag1)
beamIntegration('HingeRadau', ColIntTag2, colSecTag2,1,colSecTag2, 10,colSecTag2)
#beamIntegration('Lobatto', BeamIntTag1, beamSecTag1, 4)
#beamIntegration('HingeRadau', tag, secI, lpI, secJ, lpJ, secE)

fix(1, 1, 1, 1)
fix(2, 1, 1, 1)
# Assign geometric transformation

ColTransfTag=1
BeamTranfTag=2

geomTransf('Linear', ColTransfTag)
geomTransf('Linear', BeamTranfTag)

element('forceBeamColumn', 1, 1, 11, ColTransfTag, ColIntTag1, '-mass', 0.0)
element('forceBeamColumn', 2, 2, 12, ColTransfTag, ColIntTag2, '-mass', 0.0)
#element('elasticBeamColumn', eleTag, *eleNodes, Area, E_mod, G_mod, Jxx, Iy, Iz, transfTag, <'-mass', mass>, <'-cMass'>)

#element('elasticBeamColumn', eleTag, *eleNodes, Area, E_mod, G_mod, Jxx, Iy, Iz, transfTag, <'-mass', mass>, <'-cMass'>)

#element('forceBeamColumn', eleTag, *eleNodes, transfTag, integrationTag, '-iter', maxIter=10, tol=1e-12, '-mass', mass=0.0)


#element('forceBeamColumn', 101, 1101, 1201, BeamTranfTag, BeamIntTag1, '-mass', 0.0)

#element('elasticBeamColumn', 1, 1, 11,Abeam, Es, Gs, 1, IbeamY, IbeamZ, BeamTranfTag, '-mass', 0.0)
#element('elasticBeamColumn', 2, 2, 12,Abeam, Es, Gs, 1, IbeamY, IbeamZ, BeamTranfTag, '-mass', 0.0)

element('elasticBeamColumn', 101, 1101, 1201,Abeam, Es, Gs, 1, IbeamY, IbeamZ, BeamTranfTag, '-mass', 0.0)


# Create the zero length element
#      uniaxialMaterial Bilin  $eleID  $K  $asPos $asNeg $MyPos $MyNeg $LS $LK $LA $LD $cS $cK $cA $cD $th_pP $th_pN $th_pcP $th_pcN $ResP $ResN $th_uP $th_uN $DP $DN;

#      element zeroLength $eleID $nodeR $nodeC -mat $eleID -dir 6

# Constrain the translational DOF with a multi-point constraint
#                   retained constrained DOF_1 DOF_2 ... DOF_n
#equalDOF    $nodeR     $nodeC     1     2

#uniaxialMaterial('ElasticBilin', matTag, EP1, EP2, epsP2, EN1=EP1, EN2=EP2, epsN2=-epsP2)

#uniaxialMaterial('ElasticPP', matTag, Es, epsyP, epsyN=epsyP, eps0=0.0)



'''    
McMy =1.05
LS =1000.0    
LK =1000.0  
LA =1000.0   
LD =1000.0   
cS =1.0   
cK =1.0   
cA =1.0   
cD =1.0   
th_pP =0.025   
th_pN =0.025   
th_pcP =0.3   
th_pcN =0.3   
ResP =0.4   
ResN =0.4   
th_uP =0.4 
th_uN =0.4 
DP =1.0 
DN =1.0
a_mem = ($n+1.0)*(Mycol_12*(McMy-1.0)) / (Ks_col_1*th_pP) 
b =  (a_mem)/(1.0+$n*(1.0-$a_mem)) 

uniaxialMaterial('Bilin',3,K, asPos, asNeg, MyPos, MyNeg, LS, LK, LA, LD, cS, cK, cA, cD, th_pP, th_pN, th_pcP, th_pcN, ResP, ResN, th_uP, th_uN, DP, DN)

element('zeroLength', eleID, nodeR, nodeC, '-mat', eleID '-dir', 6)

'''



equalDOF(11, 1101, 1,2,3)
equalDOF(12, 1201, 1,2,3)

timeSeries("Linear", 1)

# create a plain load pattern
pattern("Plain", 1, 1)

# Create the nodal load
load(11, 0.0, -5.0*kip, 0.0)
load(12, 0.0, -6.0*kip, 0.0)


NstepsGrav = 10

system("BandGEN")
numberer("Plain")
constraints("Plain")
integrator("LoadControl", 1.0/NstepsGrav)
algorithm("Newton")
test('NormUnbalance',1e-8, 10)
analysis("Static")

# perform the analysis
data = np.zeros((NstepsGrav+1,2))
for j in range(NstepsGrav):
    analyze(1)
    data[j+1,0] = nodeDisp(12,2)
    data[j+1,1] = getLoadFactor(1)*5

loadConst('-time', 0.0)
	 
print("Gravity analysis complete")

wipeAnalysis()

###############################
### PUSHOVER ANALYSIS
###############################

if(AnalysisType=="Pushover"):
	
    print("<<<< Running Pushover Analysis >>>>")

    # Create load pattern for pushover analysis
    # create a plain load pattern
    pattern("Plain", 2, 1)

    load(11, 1.61, 0.0, 0.0)
    load(12, 3.22, 0.0, 0.0)
    #load(31, 4.83, 0.0, 0.0)
	
    ControlNode=12
    ControlDOF=1
    MaxDisp=0.15*H_story
    DispIncr=0.01
    NstepsPush=int(MaxDisp/DispIncr)
	
    system("ProfileSPD")
    numberer("Plain")
    constraints("Plain")
    integrator("DisplacementControl", ControlNode, ControlDOF, DispIncr)
    algorithm("Newton")
    test('NormUnbalance',1e-8, 10)
    analysis("Static")
	
    PushDataDir = r'PushoverOut02'
    if not os.path.exists(PushDataDir):
        os.makedirs(PushDataDir)
    recorder('Node', '-file', "PushoverOut02/Node2React.out", '-closeOnWrite', '-node', 2, '-dof',1, 'reaction')
    
    #recorder('Element', '-file', "PushoverOut/BeamStress.out", '-closeOnWrite', '-ele', 102, 'section', '4', 'fiber','1', 'stressStrain')
    recorder('Node', '-file', "PushoverOut02/Node2React.out", '-closeOnWrite', '-node', 2, '-dof',1, 'reaction')
    recorder('Node', '-file', "PushoverOut02/Node1101_d.out", '-closeOnWrite', '-node', 1101, '-dof',3, 'disp')
    recorder('Node', '-file', "PushoverOut02/Node1101_r.out", '-closeOnWrite', '-node', 1101, '-dof',3, 'reaction')
    recorder('Node', '-file', "PushoverOut02/Node1101_TWO.out", '-closeOnWrite', '-node', 1101, '-dof',3, 'disp')



    # analyze(NstepsPush)

    # Perform pushover analysis
    dataPush = np.zeros((NstepsPush+1,5))
    for j in range(NstepsPush):
        analyze(1)
        dataPush[j+1,0] = nodeDisp(12,1)
        reactions()
        dataPush[j+1,1] = nodeReaction(1, 1) + nodeReaction(2, 1)

    plt.plot(dataPush[:,0], -dataPush[:,1])
    plt.xlim(0, MaxDisp)
    plt.xticks(np.linspace(0,MaxDisp,5,endpoint=True))  
    plt.yticks(np.linspace(0, -int(dataPush[NstepsPush,1]),10,endpoint=True)) 
    plt.grid(linestyle='dotted') 
    plt.xlabel('Top Displacement (inch)')
    plt.ylabel('Base Shear (kip)')
    plt.show()
	
	
    print("Pushover analysis complete")    
    

    
disp_2_1101_= pd.DataFrame(pd.read_csv('PushoverOut02/Node1101_TWO.out',delimiter=" ", header = None)).to_numpy() 
#disp_2_re_1101_= pd.DataFrame(pd.read_csv('PushoverOut02/Node1101_TWO_re.out',delimiter=" ", header = None)).to_numpy() 

disp1101 = pd.DataFrame(pd.read_csv('PushoverOut02/Node1101_d.out',delimiter=" ", header = None)).to_numpy() 
reac1101 = pd.DataFrame(pd.read_csv('PushoverOut02/Node1101_r.out',delimiter=" ", header = None)).to_numpy() 


plt.figure(figsize=(12, 9))

plt.plot(disp1101,reac1101) 


#plt.figure(figsize=(12, 9))

#plt.plot(disp_2_1101_) 


Wy = 0
Wx = 0.


'''
Ew = {1: ['-beamUniform', Wy, Wx]}

plt.figure()
minVal, maxVal = opsv.section_force_diagram_2d('M', Ew, sfacM)
plt.title(f'Bending moments, max = {maxVal:.2f}, min = {minVal:.2f}')

plt.show()
'''