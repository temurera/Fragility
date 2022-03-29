# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 22:35:12 2020

@author: erayt
"""

from openseespy.opensees import *
import numpy as np
import matplotlib.pyplot as plt
import openseespy.postprocessing.Get_Rendering as opsplt
import openseespy.postprocessing.ops_vis as opsv
#import openseespy.postprocessing.ops_vis as opsv
import pandas as pd
from datetime import datetime

#This script produces the model of a cable stayed bridge and the result of the modal analysis.
#Eray Temur

starttime = datetime.now()

wipe()

Es = 0.3091327
# model build
model('basic','-ndm',3, '-ndf',6)
a = 4
#create nodes

exec(open("./Node_Coord_13.py").read())
exec(open("./Section_13.py").read())
exec(open("./Beam_Int_13_2.py").read())
exec(open("./Materials_13.py").read())
exec(open("./Boundary_13.py").read())
exec(open("./GeoTran_13.py").read())
#exec(open("./Elements_13_2.py").read())
exec(open("./Elements_13_3.py").read()) #For alteration of nodes for the rotational springs

#   Section Comp_gen: secTag E A Iz Iy G J <alphaY> <alphaZ>
section('Elastic', 104, 200000000, 1.08, 0.51, 0.51, 76923080, 1.933, 0.8074527, 0.8074527)

#   beam Integration
beamIntegration('Lobatto',400,104,5)


exec(open("./Soil_Springs_03_trial.py").read())
exec(open("./Element_under_soil_bc_03_Trial_Disp.py").read())

def rot2DSpringModel(eleID, nodeR, nodeC, K):
    #uniaxialMaterial('Bilin',eleID,K, asPos, asNeg, MyPos, MyNeg, LS, LK, LA, LD, cS, cK, cA, cD, th_pP, th_pN, th_pcP, th_pcN, ResP, ResN, th_uP, th_uN, DP, DN)
    uniaxialMaterial('ElasticBilin',eleID,K, 0.00001*K,0.0001)
    element('zeroLength', eleID, nodeR, nodeC, '-mat', eleID, '-dir', 4)
    element('zeroLength', eleID, nodeR, nodeC, '-mat', eleID, '-dir', 5)
    equalDOF(nodeR, nodeC, 1, 2, 3, 6)
    return

Sec_mod = 0.1871
Fy = 345
#Top nodes of Piles

Nonl_nodes = [138,136,29,150,148,154,152,69,158,156,99,97,98,93,73,89,108,103,104,120,118,119,114,109,112,126,124,125]

for i in range(len(Nonl_nodes)):
    node(int(Nonl_nodes[i]+20000),nodeCoord(Nonl_nodes[i])[0],nodeCoord(Nonl_nodes[i])[1],nodeCoord(Nonl_nodes[i])[2],'-ndf',6)
    rot2DSpringModel(int(20000+i), int(Nonl_nodes[i]+20000), Nonl_nodes[i], Fy*Sec_mod)
    
















'''
constraints('Transformation')
numberer('Plain')
system('UmfPack')
test('NormDispIncr',+1.000000E-12,25,0,2)
algorithm('Newton')
integrator('Newmark',+5.000000E-01,+2.500000E-01)
analysis('Transient')
numb = 12
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

recorder('Node', '-file', 'MODAL_Node_NodeEigen_EigenVec_1_PY.out', '-time','-nodeRange', 1, 1000001, '-dof', 1, 2, 3, 4, 5, 6, 'eigen1')
record()
#create nodes
#exec(open("Elements.py").read())
#opsplt.plot_model()  # command from Get_Rendering module
#opsv.plot_model()  # command from ops_vis module
'''
#for i in range(101, 113):
#    timeSeries('Path', i, '-dt', 0.005, '-filePath','EQ_disp_1_'+str(i)+'.txt','-factor', 1.0)
#Spr_nodes = np.arange(11489,11503,1)
#EQ_rec = np.arange(101,114,1)
'''
fix(11489, 1, 1, 1, 1, 1, 1)
fix(11490, 1, 1, 1, 1, 1, 1)
fix(11491, 1, 1, 1, 1, 1, 1)
'''
#recorder Node -file DFree123.out -time -node 2 -dof 1 2 3 disp;      
recorder('Node', '-file', 'Disp_trial_11192.out', '-time','-node', 11192, '-dof', 1,2,3,4,5,6 , 'disp')




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

EQ_rec = np.concatenate((eq_id,eq_id1,eq_id2,eq_id3),axis=0)
    
P_1 = P22.flatten(order='f')
P_2 = P31.flatten(order='f')
P_3 = P33.flatten(order='f')
P_4 = P34.flatten(order='f')
    
Sup_nodes = np.concatenate((P_1,P_2,P_3,P_4),axis=0)









for i in range(114):#len(Sup_nodes)-1):
    i = 1+i
    print(i)
    
    timeSeries('Path', int(i), '-dt', 0.005, '-filePath','EQ_disp_1_'+str(i)+'.txt','-factor',  100)









cc =0

pattern('MultipleSupport', 1)
for i in range(len(EQ_rec)):#len(Sup_nodes)-1):
    cc = cc +1
    #i = 12
    #print(EQ_rec[i])
    
    #timeSeries('Path', int(EQ_rec[i]), '-dt', 0.005, '-filePath','EQ_disp_1_'+str(EQ_rec[i])+'.txt','-factor', 200.0)
    #timeSeries('Path', 102, '-dt', 0.005, '-filePath','EQ_disp_1_102.txt','-factor', 200.0)
    groundMotion(cc,'Plain','-disp',int(EQ_rec[i]))
    imposedMotion(int(Sup_nodes[i]),1,cc) # node, dof, gmTag    
        

'''
i=0
timeSeries('Path', int(EQ_rec[i]), '-dt', 0.005, '-filePath','EQ_disp_1_'+str(EQ_rec[i])+'.txt','-factor', 200.0)
timeSeries('Path', 102, '-dt', 0.005, '-filePath','EQ_disp_1_102.txt','-factor', 200.0)
#pattern('UniformExcitation', 1, 1, '-disp', 101)
pattern('MultipleSupport',1)
groundMotion(101,'Plain','-disp',101)
imposedMotion(11489,1,101) # node, dof, gmTag
groundMotion(102,'Plain','-disp',102)
imposedMotion(11490,1,102)

i = 12
timeSeries('Path', int(EQ_rec[i]), '-dt', 0.005, '-filePath','EQ_disp_1_'+str(int(EQ_rec[i]))+'.txt','-factor', 200.0)
groundMotion(int(EQ_rec[i]),'Plain','-disp',int(EQ_rec[i]))
imposedMotion(int(Spr_nodes[i]),1,int(EQ_rec[i]))

 
#mass(1489, 1000,1000,1000,0,0,0)

rayleigh(0.0, 0.0, 0.0, 0.000625)

# Delete the old analysis and all it's component objects
#wipeAnalysis()

# Create the system of equation, a banded general storage scheme
system('BandGeneral')

# Create the constraint handler, a plain handler as homogeneous boundary
#constraints('Lagrange', alphaS=1.0, alphaM=1.0)
constraints('Plain')
# Create the convergence test, the norm of the residual with a tolerance of 
# 1e-12 and a max number of iterations of 10
test('NormDispIncr', 1.0e-12,35,0 )

# Create the solution algorithm, a Newton-Raphson algorithm
algorithm('Newton')

# Create the DOF numberer, the reverse Cuthill-McKee algorithm
numberer('RCM')

# Create the integration scheme, the Newmark with alpha =0.5 and beta =.25
integrator('Newmark',  0.5,  0.25 )

# Create the analysis object
analysis('Transient')   # define type of analysis: time-dependent
analyze(5176, 0.005)	 # apply 3995 0.01-sec time steps in analysis

disp = pd.DataFrame(pd.read_csv('Disp_trial.out',delimiter=" ", header = None)).to_numpy() 
#vel = pd.DataFrame(pd.read_csv('VFree_py.out',delimiter=" ", header = None)).to_numpy() 
#accl = pd.DataFrame(pd.read_csv('AFree_py.out',delimiter=" ", header = None)).to_numpy() 

plt.figure()
plt.plot(disp[:,4])
#plt.plot(disp1[:6500,1],-force1[:6500,1])
#plt.legend(["PY","OpenSEES"])

'''

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
Tol = 1e-4
el_tags = getEleTags()

node_tags = getNodeTags()


constraints('Transformation')
numberer('Plain')
system('UmfPack')
test('NormDispIncr',+1.000000E-12,25,0,2)
algorithm('Newton')
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
'''
nels = len(el_tags)

timeV = np.zeros(nPts)

Eds = np.zeros((nPts, nels, 12))
step = -1
while tCurrent < tFinal:
    step=step+1
    timeV[step] = getTime()
    #    ok = op.analyze(1, .01)     
    for i in testT:
        for j in algo: 
            if j < 4:
                algorithm(algo[j], '-initial')
                
            else:
                algorithm(algo[j])
            while ok == 0 and tCurrent < tFinal:
                    
                test(testT[i], Tol, maxNumIter)        
                NewmarkGamma = 0.5
                NewmarkBeta = 0.25
                integrator('Newmark', NewmarkGamma, NewmarkBeta)
                analysis('Transient')
                ok = analyze(1, .005)
                print(i)
                if ok == 0 :
                    tCurrent = getTime()                
                    time.append(tCurrent)
                    reactions()
                    u1.append(nodeDisp(11192,1))
                    u_spr_D.append(nodeDisp(111192,1))
                    u_spr_R.append(nodeReaction(11192,1))
                    u1_R.append(nodeReaction(111192))
                    print(testT[i], algo[j], 'tCurrent=', tCurrent)
                    for el_i, ele_tag in enumerate(el_tags):
                        nd1, nd2 = eleNodes(ele_tag)
                        i_end= []
                        j_end= []
                        for k in range(6):
                            i_end.append(nodeDisp(nd1)[k])
                            j_end.append(nodeDisp(nd2)[k])                            
                        Eds[step, el_i, :] = np.asarray(np.transpose([i_end+j_end])).reshape(12)
                            

#input_parameters = (20.8, 300., 8.)
# input_parameters = (70.0, 500., 2.)

pf, sfac_a, tkt = input_parameters
anim = opsv.anim_defo(Eds, timeV, sfac_a, interpFlag=1, fig_wi_he=(30., 22.))

# 3D is NOT Supported YET! in opsv 

#plt.show()
        
import matplotlib.pyplot as plt
plt.figure(figsize=(8,8))
plt.plot(u_spr_D[0:len(u1)-1],u1_1)
plt.ylabel('Horizontal Displacement of node 3 (in)')
plt.xlabel('Time (s)')
plt.savefig('Horizontal Disp at Node 3 vs time-multiple support excitation-disptime.jpeg', dpi = 500)
plt.show()



'''

disp = pd.DataFrame(pd.read_csv('Disp_trial_11192.out',delimiter=" ", header = None)).to_numpy() 
plt.figure()
plt.plot(disp[1:5000,1])


#input_parameters = (70.0, 500., 2.)
#pf, sfac_a, tkt = input_parameters
#opsv.plot_defo(1000,1, fmt_interp='b-', az_el=(6., 30.),fig_wi_he=(50,200))

opsplt.plot_model()
'''
opsplt.plot_model()

u1_1 = []
for i in range(len(u1_R)-1):
    print(i)
    u1_1.append(u1_R[i+1][0])
    


#analyze
 
#printA('-file','trial.txt')

#### Display the active model with node tags only
#opsplt.plot_model()
#plt.xlim([-90, -65])
#plt.ylim([-10, 10])
#plt.xlim([90, 120])
#plt.ylim([-10, 10])
 '''