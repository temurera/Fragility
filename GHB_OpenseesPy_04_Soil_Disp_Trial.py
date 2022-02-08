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

#This script produces the model of a cable stayed bridge and the result of the modal analysis.
#Eray Temur

wipe()


# model build
model('basic','-ndm',3, '-ndf',6)
a = 4
#create nodes

#exec(open("./Node_Coord_13.py").read())
#exec(open("./Section_13.py").read())
#exec(open("./Beam_Int_13_2.py").read())
#exec(open("./Materials_13.py").read())
#exec(open("./Boundary_13.py").read())
exec(open("./GeoTran_13.py").read())
#exec(open("./Elements_13_2.py").read())

#   Section Comp_gen: secTag E A Iz Iy G J <alphaY> <alphaZ>
section('Elastic', 104, 200000000, 1.08, 0.51, 0.51, 76923080, 1.933, 0.8074527, 0.8074527)

#   beam Integration
beamIntegration('Lobatto',400,104,5)

exec(open("./Soil_Springs_02_trial.py").read())
exec(open("./Element_under_soil_bc_02_Trial_Disp.py").read())
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

'''
fix(11489, 1, 1, 1, 1, 1, 1)
fix(11490, 1, 1, 1, 1, 1, 1)
fix(11491, 1, 1, 1, 1, 1, 1)
'''
#recorder Node -file DFree123.out -time -node 2 -dof 1 2 3 disp;      
recorder('Node', '-file', 'Disp_trial.out', '-time','-node', 1489, '-dof', 1,2,3,4,5,6 , 'disp')

timeSeries('Path', 101, '-dt', 0.005, '-filePath','EQ_disp_1_101.txt','-factor', 2000.0)
timeSeries('Path', 102, '-dt', 0.005, '-filePath','EQ_disp_1_102.txt','-factor', 20.0)

#pattern('UniformExcitation', 1, 1, '-disp', 101)
pattern('MultipleSupport',1)
groundMotion(101,'Plain','-disp',101)
imposedMotion(1489,1,101) # node, dof, gmTag
groundMotion(102,'Plain','-disp',102)
imposedMotion(1489,1,102)

'''
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

nPts = 5176
dt = 0.005
tCurrent = getTime()

# for gravity analysis, load control is fine, 0.1 is the load factor increment (http://opensees.berkeley.edu/wiki/index.php/Load_Control)

testT = {1:'NormDispIncr', 2: 'RelativeEnergyIncr', 3:'EnergyIncr', 4: 'RelativeNormUnbalance',5: 'RelativeNormDispIncr', 6: 'NormUnbalance'}
algo= {1:'KrylovNewton', 2: 'SecantNewton' , 3:'ModifiedNewton' , 4: 'RaphsonNewton',5: 'PeriodicNewton', 6: 'BFGS', 7: 'Broyden', 8: 'NewtonLineSearch'}

#tFinal = TmaxAnalysis
tFinal = nPts*dt
time = [tCurrent]
u3 = [0.0]
u4 = [0.0]
ok = 0
Tol = 1e-8
while tCurrent < tFinal:
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
                
                if ok == 0 :
                    tCurrent = getTime()                
                    time.append(tCurrent)
                    u3.append(nodeDisp(1489,1))
                    u4.append(nodeDisp(1490,1))
                    print(testT[i], algo[j], 'tCurrent=', tCurrent)
        
import matplotlib.pyplot as plt
plt.figure(figsize=(8,8))
plt.plot(time, u3)
plt.ylabel('Horizontal Displacement of node 3 (in)')
plt.xlabel('Time (s)')
plt.savefig('Horizontal Disp at Node 3 vs time-multiple support excitation-disptime.jpeg', dpi = 500)
plt.show()




























#analyze
 
#printA('-file','trial.txt')

#### Display the active model with node tags only
#opsplt.plot_model("nodes")
#plt.xlim([-90, -65])
#plt.ylim([-10, 10])
#plt.xlim([90, 120])
#plt.ylim([-10, 10])
 