# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 22:35:12 2020

@author: erayt
"""

from openseespy.opensees import *
import numpy as np
import matplotlib.pyplot as plt
import openseespy.postprocessing.Get_Rendering as opsplt
import openseespy.postprocessing.Get_Rendering as createODB
import openseespy.postprocessing.ops_vis as opsv
#import openseespy.postprocessing.ops_vis as opsv
import pandas as pd
from datetime import datetime

#This script produces the model of a cable stayed bridge and the result of the modal analysis.
#Eray Temur
wipe()
starttime = datetime.now()


Es = 0.3091327
# model build
model('basic','-ndm',3, '-ndf',6)
a = 4
#create nodes

node(105,-70,0,28.281,'-ndf'  ,6)
node(164,-70,0,26.19919,'-ndf'  ,6)
node(204,-69.3575,0.6425,26.19919,'-ndf'  ,6)
node(205,-70.6425,0.6425,26.19919,'-ndf'  ,6)
node(206,-69.3575,-0.6425,26.19919,'-ndf'  ,6)
node(207,-70.6425,-0.6425,26.19919,'-ndf'  ,6)

node(184,-71.875,-1.875,18,'-ndf'  ,6)
node(185,-68.125,-1.875,18,'-ndf'  ,6)
node(186,-71.875,1.875,18,'-ndf'  ,6)
node(187,-68.125,1.875,18,'-ndf'  ,6)

node(136,-66.25,3.75,18,'-ndf'  ,6)

node(138,-73.75,3.75,18,'-ndf'  ,6)
node(148,-66.25,-3.75,18,'-ndf'  ,6)
node(150,-73.75,-3.75,18,'-ndf'  ,6)

node(29,-70,0,18,'-ndf'  ,6)
node(16,-70,0,-3.718,'-ndf'  ,6)

node(137,-66.25,3.75,-3.718,'-ndf'  ,6)
node(139,-73.75,3.75,-3.718,'-ndf'  ,6)
node(149,-66.25,-3.75,-3.718,'-ndf'  ,6)
node(151,-73.75,-3.75,-3.718,'-ndf'  ,6)
 


#exec(open("./Node_Coord_13.py").read())
exec(open("./Section_13.py").read())
exec(open("./Beam_Int_13_2.py").read())
exec(open("./Materials_13.py").read())
#exec(open("./Boundary_13.py").read())
exec(open("./GeoTran_13.py").read()) 
#exec(open("./Elements_13_2.py").read())

sc = 1
#   Section Comp_gen: secTag E A Iz Iy G J <alphaY> <alphaZ>
#section('Elastic', 104, 200000000, sc*1.08, sc*0.51, sc*0.51, 76923080, 1.933, 0.8074527, 0.8074527)
section('Elastic', 104, 200000000, sc*1.08, sc*0.51, sc*0.51, 76923080, 1.0731, 1, 1)

#   beam Integration
beamIntegration('Lobatto',400,104,10)



exec(open("./P2_2_Geo.py").read())

element('forceBeamColumn',8,105,164,4,8,'-mass',0,'-iter',10,0.00001)
#   Element RIGID:eleTag    NodeI    NodeJ    NIP    secTag    geoTranTag    <-mass massDens>    <-iter maxIters tol> 
element('forceBeamColumn',187,205,164,120,187,'-mass',0,'-iter',10,0.00001)
#   Element RIGID:eleTag    NodeI    NodeJ    NIP    secTag    geoTranTag    <-mass massDens>    <-iter maxIters tol> 
element('forceBeamColumn',188,164,206,121,188,'-mass',0,'-iter',10,0.00001)
#   Element RIGID:eleTag    NodeI    NodeJ    NIP    secTag    geoTranTag    <-mass massDens>    <-iter maxIters tol> 
element('forceBeamColumn',189,204,164,122,189,'-mass',0,'-iter',10,0.00001)
#   Element RIGID:eleTag    NodeI    NodeJ    NIP    secTag    geoTranTag    <-mass massDens>    <-iter maxIters tol> 
element('forceBeamColumn',190,164,207,123,190,'-mass',0,'-iter',10,0.00001)

element('forceBeamColumn',193,204,187,126,193,'-mass',3.661923,'-iter',10,0.00001)
#   Element Pier_P2_2_final:eleTag    NodeI    NodeJ    NIP    secTag    geoTranTag    <-mass massDens>    <-iter maxIters tol> 
element('forceBeamColumn',194,205,186,127,194,'-mass',3.661923,'-iter',10,0.00001)
element('forceBeamColumn',191,207,184,124,191,'-mass',3.661923,'-iter',10,0.00001)
#   Element Pier_P2_2_final:eleTag    NodeI    NodeJ    NIP    secTag    geoTranTag    <-mass massDens>    <-iter maxIters tol> 
element('forceBeamColumn',192,206,185,125,192,'-mass',3.661923,'-iter',10,0.00001)
#


element('forceBeamColumn',247,29,186,176,247,'-mass',4.07552,'-iter',10,0.00001)
#   Element Kutu_bag:eleTag    NodeI    NodeJ    NIP    secTag    geoTranTag    <-mass massDens>    <-iter maxIters tol> 
element('forceBeamColumn',248,186,138,177,248,'-mass',4.07552,'-iter',10,0.00001)
element('forceBeamColumn',245,148,185,174,245,'-mass',4.07552,'-iter',10,0.00001)
#   Element Kutu_bag:eleTag    NodeI    NodeJ    NIP    secTag    geoTranTag    <-mass massDens>    <-iter maxIters tol> 
element('forceBeamColumn',246,185,29,175,246,'-mass',4.07552,'-iter',10,0.00001)
element('forceBeamColumn',251,29,184,180,251,'-mass',4.07552,'-iter',10,0.00001)
#   Element Kutu_bag:eleTag    NodeI    NodeJ    NIP    secTag    geoTranTag    <-mass massDens>    <-iter maxIters tol> 
element('forceBeamColumn',252,184,150,181,252,'-mass',4.07552,'-iter',10,0.00001)
element('forceBeamColumn',249,136,187,178,249,'-mass',4.07552,'-iter',10,0.00001)
#   Element Kutu_bag:eleTag    NodeI    NodeJ    NIP    secTag    geoTranTag    <-mass massDens>    <-iter maxIters tol> 
element('forceBeamColumn',250,187,29,179,250,'-mass',4.07552,'-iter',10,0.00001)

element('forceBeamColumn',155,136,138,2,155,'-mass',1.550988,'-iter',10,0.00001)
element('forceBeamColumn',154,148,136,1,154,'-mass',1.550988,'-iter',10,0.00001)
element('forceBeamColumn',153,150,148,89,153,'-mass',1.550988,'-iter',10,0.00001)
element('forceBeamColumn',152,138,150,88,152,'-mass',1.550988,'-iter',10,0.00001)
element('forceBeamColumn',10,29,16,6,10,'-mass',2.458776,'-iter',10,0.00001)


element('forceBeamColumn',86,138,139,55,86,'-mass',2.458776,'-iter',10,0.00001)
element('forceBeamColumn',85,136,137,54,85,'-mass',2.458776,'-iter',10,0.00001)
element('forceBeamColumn',94,148,149,61,94,'-mass',2.458776,'-iter',10,0.00001)
element('forceBeamColumn',95,150,151,62,95,'-mass',2.458776,'-iter',10,0.00001)





opsplt.plot_model()


#%%
#exec(open("./Soil_Springs_03_trial.py").read())
#exec(open("./Element_under_soil_bc_03_Trial_Disp.py").read())

def rot2DSpringModel(eleID, nodeR, nodeC, K):
    #uniaxialMaterial('Bilin',eleID,K, asPos, asNeg, MyPos, MyNeg, LS, LK, LA, LD, cS, cK, cA, cD, th_pP, th_pN, th_pcP, th_pcN, ResP, ResN, th_uP, th_uN, DP, DN)
    #uniaxialMaterial('ElasticBilin',eleID,K*100, 0.001*K,0.01)
    uniaxialMaterial('ElasticPP',eleID,K*100, 0.01)
    #uniaxialMaterial('Elastic',eleID,K*100)
    element('zeroLength', eleID, nodeR, nodeC, '-mat', eleID, '-dir', 4)
    element('zeroLength', eleID+20000, nodeR, nodeC, '-mat', eleID, '-dir', 5)
    equalDOF(nodeR, nodeC, 1, 2, 3, 6)
    return

Sec_mod = 0.1871
Fy = 345
#Top nodes of Piles

Nonl_nodes = [138,136,29,150,148,154,152,69,158,156,99,97,98,93,73,89,108,103,104,120,118,119,114,109,112,126,124,125]
NN_P22 = Nonl_nodes[0:5]
Nonl_nodes = NN_P22
for i in range(len(Nonl_nodes[5:10])):
    node(int(Nonl_nodes[i]+20000),nodeCoord(Nonl_nodes[i])[0],nodeCoord(Nonl_nodes[i])[1],nodeCoord(Nonl_nodes[i])[2],'-ndf',6)
    rot2DSpringModel(int(20000+i), int(Nonl_nodes[i]+20000), Nonl_nodes[i], 80000)
    
#element('forceBeamColumn',99001, 151, 11192,95,400,'-mass', +1.391642E+01,  '-iter',   10,  +1.000000E-12)
#exec(open("./Elements_13_3.py").read()) #For alteration of nodes for the rotational springs
opsplt.createODB("Pier22", "Lateral")

#recorder Node -file DFree123.out -time -node 2 -dof 1 2 3 disp;      
'''
recorder('Node', '-file', 'Disp_trial_111192.out', '-time','-node', 111192, '-dof', 1,2,3,4,5,6 , 'disp')
recorder('Node', '-file', 'Disp_trial_11192.out', '-time','-node', 11192, '-dof', 1,2,3,4,5,6 , 'disp')
recorder('Node', '-file', 'Disp_trial_100.out', '-time','-node', 100, '-dof', 1,2,3,4,5,6 , 'disp')
recorder('Node', '-file', 'Disp_trial_4761.out', '-time','-node', 4761, '-dof', 1,2,3,4,5,6 , 'disp')
recorder('Node', '-file', 'Disp_trial_151.out', '-time','-node', 151, '-dof', 1,2,3,4,5,6 , 'disp')
'''
recorder('Node', '-file', 'Disp_1_d2.out', '-time','-node', 1, '-dof', 1,2,3,4,5,6 , 'disp')
recorder('Node', '-file', 'Disp_20152_d2.out', '-time','-node', 20152, '-dof', 1,2,3,4,5,6 , 'disp')
recorder('Node', '-file', 'Reac_1_d2.out', '-time','-node', 1, '-dof', 1,2,3,4,5,6 , 'reaction')
recorder('Node', '-file', 'Reac_20152_d2.out', '-time','-node', 20152, '-dof', 1,2,3,4,5,6 , 'reaction')
#i = 0
#recorder('Element', '-file', 'Element_d2_'+str(int(20000+10))+'.out',  '-time', '-closeOnWrite', '-ele', 618, 'force' )

#for i in range(len(Nonl_nodes)):
    #rot2DSpringModel(int(20000+i), int(Nonl_nodes[i]+20000), Nonl_nodes[i], Fy*Sec_mod)
'''
i = 5
recorder('Node', '-file', 'Disp_trial_'+str(Nonl_nodes[i])+'.out', '-time','-node', Nonl_nodes[i], '-dof', 1,2,3,4,5,6 , 'disp')
recorder('Node', '-file', 'Reac_trial_'+str(Nonl_nodes[i])+'.out', '-time','-node', Nonl_nodes[i], '-dof', 1,2,3,4,5,6 , 'reaction')
recorder('Node', '-file', 'Disp_trial1_'+str(int(Nonl_nodes[i]+20000))+'.out', '-time','-node', int(Nonl_nodes[i]+20000), '-dof', 1,2,3,4,5,6 , 'disp')
recorder('Node', '-file', 'Reac_trial1_'+str(int(Nonl_nodes[i]+20000))+'.out', '-time','-node', int(Nonl_nodes[i]+20000), '-dof', 1,2,3,4,5,6 , 'reaction')
'''
record()

mass(105, 100,100,100,0,0,0)

fix(105,0,0,0,1,1,1)

timeSeries('Linear', 1)
pattern('Plain', 1, 1)

load(105,0,100000,0,0,0,0)

system('BandSPD')

# Create the constraint handler, the transformation method
constraints('Plain')

# Create the DOF numberer, the reverse Cuthill-McKee algorithm
numberer('RCM')

# Create the convergence test, the norm of the residual with a tolerance of
# 1e-12 and a max number of iterations of 10
#test('NormDispIncr', 1.0e-8, 10, 3)

# Create the solution algorithm, a Newton-Raphson algorithm
algorithm('Linear')

# Create the integration scheme, the LoadControl scheme using steps of 0.1
# Create the analysis object
analysis('Static')

# ------------------------------
# End of analysis generation
# ------------------------------

integrator('LoadControl', 0.1)
# Run Analysis
analyze(11)


opsplt.plot_deformedshape(Model="Pier22", LoadCase="Lateral")


#%%
disp_1 = pd.DataFrame(pd.read_csv('Disp_1_d2.out',delimiter=" ", header = None)).to_numpy() 
disp_20152 = pd.DataFrame(pd.read_csv('Disp_20152_d2.out',delimiter=" ", header = None)).to_numpy() 
reac_1 = pd.DataFrame(pd.read_csv('Reac_1_d2.out',delimiter=" ", header = None)).to_numpy() 
reac_20152 = pd.DataFrame(pd.read_csv('Reac_20152_d2.out',delimiter=" ", header = None)).to_numpy() 

plt.figure()
plt.plot(disp_1[:,3])




#%%



############################# Construction of Support nodes and EQ disp records##########################
#22
a = np.arange(111192,111232,1).reshape(40,1)
a = np.repeat(a, 5, axis=1)
b = np.arange(0,50000,10000).reshape(1,5)
P22 = a+b
P1 = P22.flatten()
eq_id = np.tile(np. concatenate( (np.arange(1,39+1,1), [114] ) ),5)
#31
a1 = np.arange(11786,11824,1).reshape(38,1)
a1 = np.repeat(a1, 5, axis=1)
b1 = np.arange(0,5000,1000).reshape(1,5)
P31 = a1+b1
eq_id1 = np.tile(np.arange(39,39+38,1),5)
#33
a2 = np.arange(11761,11785,1).reshape(24,1)
a2 = np.repeat(a2, 9, axis=1)
b2 = np.arange(0,9000,1000).reshape(1,9)
P33 = a2+b2
eq_id2 = np.tile(np.concatenate((np.arange(78,78+23,1), [114] )),9)
#34
a3 = np.arange(11489,11503,1).reshape(14,1)
a3 = np.repeat(a3, 9, axis=1)
b3 = np.arange(0,9000,1000).reshape(1,9)
P34 = a3+b3
eq_id3 = np.tile(np.concatenate((np.arange(101,101+13,1), [114])),9)

EQ_rec = (eq_id)
    
P_1 = P22.flatten(order='f')
P_2 = P31.flatten(order='f')
P_3 = P33.flatten(order='f')
P_4 = P34.flatten(order='f')
    
Sup_nodes = (P_1)#np.concatenate((P_1,P_2,P_3,P_4),axis=0)





g = 9.81

#%% Creating the Dead Load pattern from the masses of the elements

#Read the element definition file directly and delimit the data using comma.
Ele_scripts = (pd.read_csv('Elements_13_3.py',delimiter=",", error_bad_lines=False,header = None))

#Drop the first column cause it contains primarily "element('forceBeamColumn'," part/
Elements_Attr = Ele_scripts.loc[:,1:]

#Drop the Nan containing cells it gives you just normally defined elements containing element ID, nodes and mass. Then locate the corresponding column number.
Elements_Attr = Elements_Attr.dropna()


opsplt.createODB("Pier31","Lateral")
# Create a Plain load pattern with a Linear TimeSeries

#eleLoad('-ele', *eleTags, '-range', eleTag1, eleTag2, '-type', '-beamUniform', Wy, <Wz>, Wx=0.0, '-beamPoint', Py, <Pz>, xL, Px=0.0, '-beamThermal', *tempPts)
a = 0
UnitM = np.zeros([1,Elements_Attr.shape[0]])
timeSeries('Linear', 1)
pattern('Plain', 1, 1)
for i in range(Elements_Attr.shape[0]):
    
    EleLength1 = np.sum(((np.array(nodeCoord(int(Elements_Attr.iloc[i, 2]))) - np.array(nodeCoord(int(Elements_Attr.iloc[i, 1]))))**2), axis=0)
    EleLength = np.sqrt(EleLength1)
    UnitM[0,a] = g*(Elements_Attr.iloc[i, 6]*EleLength)/2
    load(int(Elements_Attr.iloc[i, 1]),0.0,0, -UnitM[0,a], 0,0,0)
    load(int(Elements_Attr.iloc[i, 2]),0.0,0, -UnitM[0,a], 0,0,0) 
    #eleLoad('-ele',int(Elements_Attr.iloc[i, 0]), '-type', '-beamUniform',0,0,-UnitM[0,a]*100)
    a = a+1

'''
eleLoad('-ele',206, '-type', '-beamUniform',70.077279,-70.077279,70.077279 )
eleLoad('-ele',207, '-type', '-beamUniform',0,-70.077279,70.077279 )
eleLoad('-ele',208, '-type', '-beamUniform',0,-70.077279,70.077279 )
eleLoad('-ele',209, '-type', '-beamUniform',0,-70.077279,70.077279 )
eleLoad('-ele',210, '-type', '-beamUniform',0,-70.077279,70.077279 )
eleLoad('-ele',211, '-type', '-beamUniform',0,-70.077279,70.077279 )
'''

#load(3, 0.0, -100000, 0.0,0,0,0)
#load(4, 0.0, -1000, 0.0)

# Create the system of equation, a sparse solver with partial pivoting
system('BandSPD')

# Create the constraint handler, the transformation method
constraints('Plain')

# Create the DOF numberer, the reverse Cuthill-McKee algorithm
numberer('RCM')

# Create the convergence test, the norm of the residual with a tolerance of
# 1e-12 and a max number of iterations of 10
#test('NormDispIncr', 1.0e-8, 10, 3)

# Create the solution algorithm, a Newton-Raphson algorithm
algorithm('Linear')

# Create the integration scheme, the LoadControl scheme using steps of 0.1
# Create the analysis object
analysis('Static')

# ------------------------------
# End of analysis generation
# ------------------------------

integrator('LoadControl', 0.1)
# Run Analysis
analyze(10)

# ------------------------------
# Finally perform the analysis
# ------------------------------

# perform the gravity load analysis, requires 10 steps to reach the load level





 #%%

g = 9.81
opsplt.createODB("Pier22", "EQ1")


for i in range(114):#len(Sup_nodes)-1):
    i = i+1
    #print(i)
    timeSeries('Path', int(i+1), '-dt', 0.005, '-filePath','EQQ1_disp_1_'+str(i)+'.txt','-factor',  g*2)



cc =1





pattern('MultipleSupport', 2)
for i in range(len(EQ_rec)):#len(Sup_nodes)-1):
    cc = cc +1
    #i = 12
    #print(EQ_rec[i])
    
    #timeSeries('Path', int(EQ_rec[i]), '-dt', 0.005, '-filePath','EQ_disp_1_'+str(EQ_rec[i])+'.txt','-factor', 200.0)
    #timeSeries('Path', 102, '-dt', 0.005, '-filePath','EQ_disp_1_102.txt','-factor', 200.0)
    groundMotion(cc,'Plain','-disp',int(EQ_rec[i]+1))
    imposedMotion(int(Sup_nodes[i]),1,cc) # node, dof, gmTag    
    imposedMotion(int(Sup_nodes[i]),2,cc) # node, dof, gmTag 
        


loadConst('-time', 0.0)
maxNumIter = 10
wipeAnalysis()
constraints('Transformation')
numberer('RCM')
system('BandGeneral')
#op.test('EnergyIncr', Tol, maxNumIter)
#op.algorithm('ModifiedNewton')
#NewmarkGamma = 0.5
#NewmarkBeta = 0.25
#op.integrator('Newmark', NewmarkGamma, NewmarkBeta)
#op.analysis('Transient')
#
#
#Nsteps =  int(TmaxAnalysis/ DtAnalysis)
#
#ok = op.analyze(Nsteps, DtAnalysis)
record()

nPts = 5176
dt = 0.005
tCurrent = getTime()

# for gravity analysis, load control is fine, 0.1 is the load factor increment (http://opensees.berkeley.edu/wiki/index.php/Load_Control)

testT = {1:'NormDispIncr', 2: 'RelativeEnergyIncr', 3:'EnergyIncr', 4: 'RelativeNormUnbalance',5: 'RelativeNormDispIncr', 6: 'NormUnbalance'}
algo= {1:'KrylovNewton', 2: 'SecantNewton' , 3:'ModifiedNewton' , 4: 'RaphsonNewton',5: 'PeriodicNewton', 6: 'BFGS', 7: 'Broyden', 8: 'NewtonLineSearch'}

#tFinal = TmaxAnalysis
tFinal = nPts*dt
time = [tCurrent]
u1 = [0.0]
u1_R = [0.0]
u_spr_D = [0.0]
u_spr_R = [0.0]         
ok = 0
Tol = 1e-8
el_tags = getEleTags()




alphaM =0.0811
betaKcurr = 0.0006161
betaKcomm = 0.0006161
betaKinit = 0.0006161
rayleigh(alphaM, betaKcurr, betaKinit, betaKcomm)

node_tags = getNodeTags()

constraints('Transformation')
numberer('Plain')
system('UmfPack')
test('NormDispIncr',+1.000000E-8,40)
algorithm('KrylovNewton')
integrator('Newmark',+5.000000E-01,+2.500000E-01)
analysis('Transient')
numb = 12
# calculate eigenvalues & print results     
numEigen = 12
eigenValues = eigen(numEigen)
#PI = -np.cos(1.0)
analyze(5176,0.005)
endtime = datetime.now()
print("runtime: "+ str(endtime-starttime))


opsplt.plot_deformedshape(Model="Pier22", LoadCase="EQ1")

#disp = pd.DataFrame(pd.read_csv('Disp_trial_11192.out',delimiter=" ", header = None)).to_numpy() 
#plt.figure() 
#plt.plot(disp[1:5000,1])

#%%


ani = opsplt.animate_deformedshape(Model="Pier31",LoadCase="EQ1", dt=10,tStart=0.0, tEnd=20, scale=100)
from matplotlib.animation import PillowWriter
writer = PillowWriter(fps=10)
ani.save("Pier31_01.gif", writer=writer) 


    #%% Modal Analysis


# calculate eigenvalues & print results     
numEigen = 12
eigenValues = eigen(numEigen)
#PI = -np.cos(1.0)

ome=[]
per = []
freq = []
for eig in range(len(eigenValues)):
    ome.append(np.sqrt(eigenValues[eig]))
    per.append(2*np.pi/ome[-1])
    freq.append(1/per[-1])
#eigen(solver='-fullGenLapack', numb)

recorder('Node', '-file', 'MODAL_Node_NodeEigen_EigenVec_1_PY.out', '-time','-nodeRange', 1, 1001, '-dof', 1, 2, 3, 4, 5, 6, 'eigen1')
record()
#create nodes
#exec(open("Elements.py").read())
#opsplt.plot_model()  # command from Get_Rendering module
#opsv.plot_model()  # command from ops_vis module

#%% Modal Analysis Drawing
opsplt.plot_modeshape(2, 1000)




 #%% Loading the disp and reac results

disp_150 = pd.DataFrame(pd.read_csv('Disp_150_d2.out',delimiter=" ", header = None)).to_numpy() 
disp_20150 = pd.DataFrame(pd.read_csv('Disp_20150_d2.out',delimiter=" ", header = None)).to_numpy() 
reac_150 = pd.DataFrame(pd.read_csv('Reac_150_d2.out',delimiter=" ", header = None)).to_numpy() 
reac_20150 = pd.DataFrame(pd.read_csv('Reac_20150_d2.out',delimiter=" ", header = None)).to_numpy() 
ele_618 = pd.DataFrame(pd.read_csv('Element_d2_'+str(int(20000+10))+'.out',delimiter=" ", header = None)).to_numpy() 

#%%
#disp4761 = pd.DataFrame(pd.read_csv('Disp_trial_4761.out',delimiter=" ", header = None)).to_numpy() 
plt.figure()
plt.plot(disp_20150[:2400,5],ele_618[:2400,5])
plt.title("Hysteresis of a hinge for Disp input 2 165_1 scaled by 2",fontname="Times New Roman",fontweight="bold")
plt.xlabel("Rotation")
plt.ylabel("Moment x")
plt.savefig('Moment_Rotation2_20150_618_Disp_Correction_trial07.pdf')  

#plt.figure()
#plt.plot(disp[1:5000,1])

#%%

plt.figure()
plt.plot(disp_20150[:,5])
#plt.plot((disp_20150[:,4]))
 #%%
plt.figure()
plt.plot(ele_618[:,5])


#%%


ani = opsplt.animate_deformedshape(Model="GHB_bridge_model",LoadCase="EQ1", dt=10,tStart=0.0, tEnd=20, scale=100)
from matplotlib.animation import PillowWriter
writer = PillowWriter(fps=10)
ani.save("GHB_exampletrOlder_01.gif", writer=writer) 



 #%%
i = 5
disp5 = pd.DataFrame(pd.read_csv('Disp_trial1_'+str(int(Nonl_nodes[i]+20000))+'.out',delimiter=" ", header = None)).to_numpy() 
reac5 = pd.DataFrame(pd.read_csv('Reac_trial1_'+str(int(Nonl_nodes[i]+20000))+'.out',delimiter=" ", header = None)).to_numpy() 
disp51 = pd.DataFrame(pd.read_csv('Disp_trial_'+str(Nonl_nodes[i])+'.out',delimiter=" ", header = None)).to_numpy() 
reac51 = pd.DataFrame(pd.read_csv('Reac_trial_'+(str(Nonl_nodes[i]))+'.out',delimiter=" ", header = None)).to_numpy() 

#plt.plot(disp5)

#%%
#ND = pd.DataFrame(pd.read_csv('GHB_bridge_model_ODB\EQ1\NodeDisp_All.out',delimiter=" ", header = None)).to_numpy()
#input_parameters = (70.0, 500., 2.)
#pf, sfac_a, tkt = input_parameters
#opsv.plot_defo(1000,1, fmt_interp='b-', az_el=(6., 30.),fig_wi_he=(50,200))
#%%
opsplt.plot_model()
