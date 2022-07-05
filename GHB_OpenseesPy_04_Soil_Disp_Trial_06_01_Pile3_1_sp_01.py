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


Est = 200000000
#plt.plot(Est[0,:])
# model build

P_s = 1
Es = 0.3091327
# model build
model('basic','-ndm',3, '-ndf',6)
a = 4
#create nodes
'''
node(1,0,0,31,'-ndf'  ,6)
node(163,0,0,28.91819,'-ndf'  ,6)
node(80,1.98346,1.3025,28.91819,'-ndf'  ,6)
node(81,1.98346,-1.3025,28.91819,'-ndf'  ,6)
node(82,-2.013232,1.3025,28.91819,'-ndf'  ,6)
node(83,-2.013232,-1.3025,28.91819,'-ndf'  ,6)
node(180,-2.3,-2.3,18,'-ndf'  ,6)
node(181,2.3,-2.3,18,'-ndf'  ,6)
node(182,-2.3,2.3,18,'-ndf'  ,6)
node(183,2.3,2.3,18,'-ndf'  ,6)
node(17,0,0,-17.6,'-ndf'  ,6)

node(69,0,0,18,'-ndf'  ,6)

node(152,4.6,4.6,18,'-ndf'  ,6)
node(153,4.6,4.6,-17.6,'-ndf'  ,6)
node(154,-4.6,4.6,18,'-ndf'  ,6)
node(155,-4.6,4.6,-17.6,'-ndf'  ,6)
node(156,4.6,-4.6,18,'-ndf'  ,6)
node(157,4.6,-4.6,-17.6,'-ndf'  ,6)'''
node(158,-4.6,-4.6,18,'-ndf'  ,6)
node(159,-4.6,-4.6,-17.6,'-ndf'  ,6)










#exec(open("./Node_Coord_13.py").read())
exec(open("./Section_13.py").read())
exec(open("./Beam_Int_13_2.py").read())
exec(open("./Materials_13.py").read())
#exec(open("./Boundary_13.py").read())
exec(open("./GeoTran_13.py").read()) 
#exec(open("./Elements_13_2.py").read())


'''

element('forceBeamColumn',7,1,163,3,7,'-mass',0,'-iter',10,0.00001)
element('forceBeamColumn',91,83,163,58,91,'-mass',0,'-iter',10,0.00001)
#   Element RIGID:eleTag    NodeI    NodeJ    NIP    secTag    geoTranTag    <-mass massDens>    <-iter maxIters tol> 
element('forceBeamColumn',92,163,82,59,92,'-mass',0,'-iter',10,0.00001)
#   Element RIGID:eleTag    NodeI    NodeJ    NIP    secTag    geoTranTag    <-mass massDens>    <-iter maxIters tol> 
element('forceBeamColumn',93,163,81,60,93,'-mass',0,'-iter',10,0.00001)
#   Element 1_Pile:eleTag    NodeI    NodeJ    NIP    secTag    geoTranTag    <-mass massDens>    <-iter maxIters tol> 
element('forceBeamColumn',106,163,80,69,106,'-mass',0,'-iter',10,0.00001)

element('forceBeamColumn',60,182,82,44,60,'-mass',12.24883,'-iter',10,0.00001)
#   Element Pier-P3-1:eleTag    NodeI    NodeJ    NIP    secTag    geoTranTag    <-mass massDens>    <-iter maxIters tol> 
element('forceBeamColumn',61,180,83,45,61,'-mass',12.24883,'-iter',10,0.00001)
#   Element Pier-P3-1:eleTag    NodeI    NodeJ    NIP    secTag    geoTranTag    <-mass massDens>    <-iter maxIters tol> 
element('forceBeamColumn',62,181,81,46,62,'-mass',12.24883,'-iter',10,0.00001)
#   Element Pier-P3-1:eleTag    NodeI    NodeJ    NIP    secTag    geoTranTag    <-mass massDens>    <-iter maxIters tol> 
element('forceBeamColumn',63,183,80,47,63,'-mass',12.24883,'-iter',10,0.00001)

element('forceBeamColumn',243,69,180,172,243,'-mass',4.07552,'-iter',10,0.00001)
#   Element Kutu_bag:eleTag    NodeI    NodeJ    NIP    secTag    geoTranTag    <-mass massDens>    <-iter maxIters tol> 
element('forceBeamColumn',244,180,158,173,244,'-mass',4.07552,'-iter',10,0.00001)
element('forceBeamColumn',241,152,183,170,241,'-mass',4.07552,'-iter',10,0.00001)
#   Element Kutu_bag:eleTag    NodeI    NodeJ    NIP    secTag    geoTranTag    <-mass massDens>    <-iter maxIters tol> 
element('forceBeamColumn',242,183,69,171,242,'-mass',4.07552,'-iter',10,0.00001)

element('forceBeamColumn',239,69,182,168,239,'-mass',4.07552,'-iter',10,0.00001)
#   Element Kutu_bag:eleTag    NodeI    NodeJ    NIP    secTag    geoTranTag    <-mass massDens>    <-iter maxIters tol> 
element('forceBeamColumn',240,182,154,169,240,'-mass',4.07552,'-iter',10,0.00001)

element('forceBeamColumn',237,156,181,166,237,'-mass',4.07552,'-iter',10,0.00001)
#   Element Kutu_bag:eleTag    NodeI    NodeJ    NIP    secTag    geoTranTag    <-mass massDens>    <-iter maxIters tol> 
element('forceBeamColumn',238,181,69,167,238,'-mass',4.07552,'-iter',10,0.00001)


element('forceBeamColumn',96,152,153,63,96,'-mass',2.458776,'-iter',10,0.00001)
#   Element 1_Pile:eleTag    NodeI    NodeJ    NIP    secTag    geoTranTag    <-mass massDens>    <-iter maxIters tol> 
element('forceBeamColumn',97,154,155,64,97,'-mass',2.458776,'-iter',10,0.00001)
#   Element 1_Pile:eleTag    NodeI    NodeJ    NIP    secTag    geoTranTag    <-mass massDens>    <-iter maxIters tol> 
element('forceBeamColumn',98,156,157,65,98,'-mass',2.458776,'-iter',10,0.00001)'''
#   Element 1_Pile:eleTag    NodeI    NodeJ    NIP    secTag    geoTranTag    <-mass massDens>    <-iter maxIters tol> 
element('forceBeamColumn',99,158,159,66,99,'-mass',2.458776,'-iter',10,0.00001)

'''
element('forceBeamColumn',100,154,158,67,100,'-mass',1.550988,'-iter',10,0.00001)
#   Element Kutu_bag:eleTag    NodeI    NodeJ    NIP    secTag    geoTranTag    <-mass massDens>    <-iter maxIters tol> 
element('forceBeamColumn',101,158,156,68,101,'-mass',4.07552,'-iter',10,0.00001)
#   Element I_bag:eleTag    NodeI    NodeJ    NIP    secTag    geoTranTag    <-mass massDens>    <-iter maxIters tol> 
element('forceBeamColumn',102,156,152,1,102,'-mass',1.550988,'-iter',10,0.00001)
#   Element I_bag:eleTag    NodeI    NodeJ    NIP    secTag    geoTranTag    <-mass massDens>    <-iter maxIters tol> 
element('forceBeamColumn',103,152,154,2,103,'-mass',1.550988,'-iter',10,0.00001)

element('forceBeamColumn',11,69,17,7,11,'-mass',2.458776,'-iter',10,0.00001)
'''

sc = 1
#   Section Comp_gen: secTag E A Iz Iy G J <alphaY> <alphaZ>
#section('Elastic', 104, 200000000, sc*1.08, sc*0.51, sc*0.51, 76923080, 1.933, 0.8074527, 0.8074527)
section('Elastic', 104, 200000000, sc*1.08, sc*0.51, sc*0.51, 76923080, 1.0731, 1, 1)

#   beam Integration
beamIntegration('Lobatto',400,104,10)

exec(open("./P3_1_Geo_2.py").read())


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
NN_P31 = Nonl_nodes[8:9]
Nonl_nodes = NN_P31
for i in range(len(Nonl_nodes)):
    node(int(Nonl_nodes[i]+20000),nodeCoord(Nonl_nodes[i])[0],nodeCoord(Nonl_nodes[i])[1],nodeCoord(Nonl_nodes[i])[2],'-ndf',6)
    rot2DSpringModel(int(20000+i), int(Nonl_nodes[i]+20000), Nonl_nodes[i], 80000)


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

EQ_rec = (eq_id1[0:38])
    
P_1 = P22.flatten(order='f')
P_2 = P31.flatten(order='f')
P_3 = P33.flatten(order='f')
P_4 = P34.flatten(order='f')
    
Sup_nodes = (P_2[0:38])#np.concatenate((P_1,P_2,P_3,P_4),axis=0)





g = 9.81


 #%%
 
 
recorder('Node', '-file', 'Disp_158_.out', '-time','-node', 158, '-dof', 1,2,3,4,5,6 , 'disp')
#recorder('Node', '-file', 'Disp_158_.out', '-time','-node', 158, '-dof', 1,2,3,4,5,6 , 'disp')


g = 9.81
opsplt.createODB("Pier31", "EQ1")


for num in range(39,77):#len(Sup_nodes)-1):
    i = num
    #print(i)
    timeSeries('Path', int(i), '-dt', 0.005, '-filePath','EQQ1_disp_1_'+str(i)+'.txt','-factor',  g*4)



cc =0



direc = int(2)

pattern('MultipleSupport', 2)
for i in range(len(EQ_rec)):#len(Sup_nodes)-1):
    cc = cc +1
    #i = 12
    #print(EQ_rec[i])
    
    #timeSeries('Path', int(EQ_rec[i]), '-dt', 0.005, '-filePath','EQ_disp_1_'+str(EQ_rec[i])+'.txt','-factor', 200.0)
    #timeSeries('Path', 102, '-dt', 0.005, '-filePath','EQ_disp_1_102.txt','-factor', 200.0)
    groundMotion(cc,'Plain','-disp',int(EQ_rec[i]))
    imposedMotion(int(Sup_nodes[i]),1,cc) # node, dof, gmTag    
    imposedMotion(int(Sup_nodes[i]),2,cc) # node, dof, gmTag 
        


#loadConst('-time', 0.0)
maxNumIter = 10
wipeAnalysis()
constraints('Transformation')
numberer('RCM')
system('BandGeneral')

record()

nPts = 5176
dt = 0.005

tCurrent = getTime()
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


opsplt.plot_deformedshape(Model="Pier31", LoadCase="EQ1")

#disp = pd.DataFrame(pd.read_csv('Disp_trial_11192.out',delimiter=" ", header = None)).to_numpy() 
#plt.figure() 
#plt.plot(disp[1:5000,1])

#%%


ani = opsplt.animate_deformedshape(Model="Pier31",LoadCase="EQ1", dt=10,tStart=0.0, tEnd=20, scale=10)
from matplotlib.animation import PillowWriter
writer = PillowWriter(fps=10)
ani.save("Pier311_02.gif", writer=writer) 


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
disp_20150 = pd.DataFrame(pd.read_csv('Disp_20152_d2.out',delimiter=" ", header = None)).to_numpy() 
reac_150 = pd.DataFrame(pd.read_csv('Reac_150_d2.out',delimiter=" ", header = None)).to_numpy() 
reac_20150 = pd.DataFrame(pd.read_csv('Reac_20152_d2.out',delimiter=" ", header = None)).to_numpy() 
ele_618 = pd.DataFrame(pd.read_csv('Element_d2_'+str(int(20000+10))+'.out',delimiter=" ", header = None)).to_numpy() 
disp_1 = pd.DataFrame(pd.read_csv('Disp_1_d2.out',delimiter=" ", header = None)).to_numpy() 


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
disp_158 = pd.DataFrame(pd.read_csv('Disp_158_.out',delimiter=" ", header = None)).to_numpy() 


plt.figure()
plt.plot(disp_158[:,1])
plt.plot(disp_158[:,2])
plt.legend(['dir x','dir y'])

#plt.plot((disp_20150[:,4]))
 #%%
plt.figure()
plt.plot(ele_618[:,5])


#%%


ani = opsplt.animate_deformedshape(Model="GHB_bridge_model",LoadCase="EQ1", dt=10,tStart=0.0, tEnd=20, scale=100)
from matplotlib.animation import PillowWriter
writer = PillowWriter(fps=10)
ani.save("GHB_exampletrOlder_02.gif", writer=writer) 



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
