# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 22:35:12 2020

@author: erayt
"""

from openseespy.opensees import *
import numpy as np
import matplotlib.pyplot as plt
'''
import openseespy.postprocessing.Get_Rendering as opsplt
import openseespy.postprocessing.Get_Rendering as createODB
import openseespy.postprocessing.ops_vis as opsv'''
#import openseespy.postprocessing.ops_vis as opsv
import pandas as pd
from datetime import datetime

#This script has been developed for nonlinear analysis of a cable-stayed bridge considering soil, geometric and material nonlinearities.

#Eray Temur
wipe()
starttime = datetime.now()

#Uncertain Parameters
sc_num = 0 #from 0 to 4
eq_n = 0 #from 0 to 21


EQ_sc_list = np.array([0.5,1,1.5,2,2.5,3])
EQ_sc = EQ_sc_list[sc_num]
Est_list = 200000000
Ec = 32000000
P_s = 1

EQ_list = np.array([[1,2],
[2,1],
[3,4],
[4,3],
[5,6],
[6,5],
[7,8],
[8,7],
[9,10],
[10,9],
[11,12],
[12,11],
[13,14],
[14,13],
[15,16],
[16,15],
[17,18],
[18,17],
[19,20],
[20,19],
[21,22],
[22,21]])

EQ_d = np.array([ 0.005, 0.01, 0.005, 0.005, 0.005,0.02, 0.01, 0.005, 0.005, 0.02, 0.005])
EQ_dt_list = np.repeat(EQ_d, 2, axis=0)


EQ_rec_ind = EQ_list[eq_n,:]
EQ_dt = EQ_dt_list[eq_n]




# model build
model('basic','-ndm',3, '-ndf',6)
g = 9.81

# Bridge Model Properties
exec(open("./Node_Coord_13.py").read())
exec(open("./Section_13.py").read())
exec(open("./Beam_Int_13_2.py").read())
exec(open("./Materials_13.py").read())
exec(open("./GeoTran_13.py").read()) 

fix(106,0,1,1,0,0,0)
fix(107,0,1,1,0,0,0)
fix(128,0,0,1,0,0,0)
fix(130,0,0,1,0,0,0)
fix(132,0,0,1,0,0,0)
fix(134,0,0,1,0,0,0)
section('Elastic', 104, 200000000, 1.08, 0.51, 0.51, 76923080, 1.0731, 1, 1)
beamIntegration('Lobatto',400,104,10)
exec(open("./Soil_Springs_03_trial.py").read())
exec(open("./Element_under_soil_bc_03_Trial_Disp.py").read())
def rot2DSpringModel(eleID, nodeR, nodeC, K):
    uniaxialMaterial('ElasticPP',eleID+10000,K*(1/0.004375), 0.004375)
    element('zeroLength', eleID+10000, nodeR, nodeC, '-mat', eleID+10000, '-dir', 4)
    element('zeroLength', eleID+20000, nodeR, nodeC, '-mat', eleID+10000, '-dir', 5)
    equalDOF(nodeR, nodeC, 1, 2, 3, 6)
    return
Nonl_nodes = [138,136,29,150,148,154,152,69,158,156,99,97,98,93,73,89,108,103,104,120,118,119,114,109,112,126,124,125]
pile_ele = [86,	85,	10,	95,	94,	97,	96,	11,	99,	98,	618, 626, 616, 614,	610, 612, 624, 620, 622, 638, 634, 636, 632, 628, 630, 644, 640, 642]
for i in range(len(Nonl_nodes)):
    node(int(Nonl_nodes[i]+20000),nodeCoord(Nonl_nodes[i])[0],nodeCoord(Nonl_nodes[i])[1],nodeCoord(Nonl_nodes[i])[2],'-ndf',6)
    rot2DSpringModel(int(i), int(Nonl_nodes[i]+20000), Nonl_nodes[i], 80000)
exec(open("./Elements_13_3.py").read()) #For alteration of nodes for the rotational springs
# Generating Recorders for Nonl Nodes and corresponding elements to read element forces
for jk in range(len(Nonl_nodes)):
    recorder('Node', '-file', 'Disp_'+str(20000+Nonl_nodes[jk])+'_d5.out', '-time','-node', int(20000+Nonl_nodes[jk]), '-dof', 4,5 , 'disp')
    recorder('Element', '-file', 'Element_d2_'+str(int(pile_ele[jk]))+'.out',  '-time', '-closeOnWrite', '-ele', int(pile_ele[jk]), 'force' )

############################# Construction of Support nodes and EQ disp records##########################
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

EQ_rec = np.concatenate((eq_id,eq_id1,eq_id2,eq_id3),axis=0)
    
P_1 = P22.flatten(order='f')
P_2 = P31.flatten(order='f')
P_3 = P33.flatten(order='f')
P_4 = P34.flatten(order='f')
    
Sup_nodes = np.concatenate((P_1,P_2,P_3,P_4),axis=0)
#opsplt.createODB("GHB_bridge_model", "EQ1")

#%% Creating the Dead Load pattern from the masses of the elements
Ele_scripts = (pd.read_csv('Elements_13_3.py',delimiter=",", error_bad_lines=False,warn_bad_lines=False,header = None))
#Drop the first column cause it contains primarily "element('forceBeamColumn'," part/
Elements_Attr = Ele_scripts.loc[:,1:]
#Drop the Nan containing cells it gives you just normally defined elements containing element ID, nodes and mass. Then locate the corresponding column number.
Elements_Attr = Elements_Attr.dropna()


#opsplt.createODB("3DFrame","Gravity")
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
system('BandSPD')
constraints('Plain')
numberer('RCM')
algorithm('Linear')
analysis('Static')
integrator('LoadControl', 0.1)
analyze(10)
#%%

for i in range(114):#len(Sup_nodes)-1):
    i = 1+i
    #print(i)
    timeSeries('Path', int(i+1), '-dt', EQ_dt, '-filePath','EQQ1_disp_'+int(EQ_rec_ind[0])+'_'+str(i)+'.txt','-factor',  g*EQ_sc)
    timeSeries('Path', int(i+115), '-dt', EQ_dt, '-filePath','EQQ1_disp_'+int(EQ_rec_ind[1])+'_'+str(i)+'.txt','-factor',  g*EQ_sc)






loadConst('-time', 0.0)

wipeAnalysis()
constraints('Transformation')
numberer('RCM')
system('BandGeneral')



pattern('MultipleSupport', 4)
cc =0

for i in range(len(EQ_rec)):#len(Sup_nodes)-1):
    cc = cc +1
    #timeSeries('Path', int(EQ_rec[i]), '-dt', 0.005, '-filePath','EQ_disp_1_'+str(EQ_rec[i])+'.txt','-factor', 200.0)
    #timeSeries('Path', 102, '-dt', 0.005, '-filePath','EQ_disp_1_102.txt','-factor', 200.0)
    groundMotion(cc,'Plain','-disp',int(EQ_rec[i])+1)
    imposedMotion(int(Sup_nodes[i]),1,cc) # node, dof, gmTag
    groundMotion(cc+732,'Plain','-disp',int(EQ_rec[i]+115))
    imposedMotion(int(Sup_nodes[i]),2,cc+732) # node, dof, gmTag    

    
        



'''constraints('Transformation')
numberer('RCM')
system('BandGeneral')'''
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


# for gravity analysis, load control is fine, 0.1 is the load factor increment (http://opensees.berkeley.edu/wiki/index.php/Load_Control)

testT = {1:'NormDispIncr', 2: 'RelativeEnergyIncr', 3:'EnergyIncr', 4: 'RelativeNormUnbalance',5: 'RelativeNormDispIncr', 6: 'NormUnbalance'}
algo= {1:'KrylovNewton', 2: 'SecantNewton' , 3:'ModifiedNewton' , 4: 'RaphsonNewton',5: 'PeriodicNewton', 6: 'BFGS', 7: 'Broyden', 8: 'NewtonLineSearch'}

alphaM =0.0811
betaKcurr = 0.0006161
betaKcomm = 0.0006161
betaKinit = 0.0006161
rayleigh(alphaM, betaKcurr, betaKinit, betaKcomm)

node_tags = getNodeTags()

constraints('Transformation')
numberer('RCM')
system('UmfPack')
test('NormDispIncr',+1.000000E-2,10)
algorithm('KrylovNewton')
integrator('Newmark',+5.000000E-01,+2.500000E-01)
analysis('Transient')
numb = 12
# calculate eigenvalues & print results     
numEigen = 12
eigenValues = eigen(numEigen)
#PI = -np.cos(1.0)
analyze(nPts,dt)
endtime = datetime.now()
print("runtime: "+ str(endtime-starttime))

wipe()


 #%% Loading the disp and reac results
 
disp4 = np.zeros([len(Nonl_nodes),nPts+11,2]) 
disp5 = np.zeros([len(Nonl_nodes),nPts+11,3]) 
ele_res = np.zeros([len(Nonl_nodes),nPts+11,13])
for jk in range(len(Nonl_nodes)):
    disp5[jk,:,:] = pd.DataFrame(pd.read_csv('Disp_'+str(20000+Nonl_nodes[jk])+'_d5.out',delimiter=" ", header = None)).to_numpy() 
    #disp4[jk,:,:] = pd.DataFrame(pd.read_csv('Disp_'+str(10000+Nonl_nodes[jk])+'_d4.out',delimiter=" ", header = None)).to_numpy() 
    ele_res[jk,:,:] = pd.DataFrame(pd.read_csv('Element_d2_'+str(int(pile_ele[jk]))+'.out',delimiter=" ", header = None)).to_numpy() 


#%%
'''
for jk in range(len(Nonl_nodes)-10):
    plt.figure()
    plt.plot(disp5[jk,:,2],ele_res[jk,:,5])'''
    
