# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 20:44:58 2021

@author: erayt
"""

#from openseespy.opensees import *
#import openseespymac.opensees as ops
import numpy as np
import matplotlib.pyplot as plt
from openseespy.opensees import *
#import openseespy.postprocessing.Get_Rendering as opsplt
#import openseespy.postprocessing.ops_vis as opsv
import pandas as pd
wipe()


# model build
model('basic','-ndm',2, '-ndf',3)
L = 162.89
node(1,0.,0.)
node(2,0.,L)
fix(1,1,1,1)
transTag  = 1
#geometric Transformation
geomTransf('Linear',transTag)


#Structural and Phsysical Parameters
g = 9.81
deckweight = 25000
EI = 25000000000
fy = 355000
dt = 0.005
eqk = 'RSN117601.AT2'
factor = 25
damp = 0.05
eqksteps = 6999
deckmass = deckweight/g

b = 0.1281
mass(2, deckmass, deckmass,0) 


#Materials 
uniaxialMaterial('Steel01', 1, fy, EI, b)
uniaxialMaterial('Elastic', 2, EI)

section('Aggregator',1,2, 'P',1, 'Mz') # combine axial and flexural behavior into one section (no P-M interaction here)
element('nonlinearBeamColumn',1,1,2,10,1,transTag)
recorder('Node', '-file', 'DFree_py.out', '-time','-node', 2, '-dof', 1, 2, 3, 'disp')
recorder('Node', '-file', 'Dbase_py.out', '-time','-node', 1, '-dof', 1, 2, 3,'disp')
recorder('Node', '-file', 'Rbase_py.out', '-time','-node', 1, '-dof', 1, 2, 3, 'reaction')

omega = np.array(eigen('-fullGenLapack', 1),dtype=float)**0.5
print(" w = ",omega)

T_sec = 2*np.pi/omega
print(" Period of the structure = ",T_sec)

record()

#Analysis Details
Tol = 1.0e-6
timeSeries('Path',2,'-dt',dt,'-filePath', eqk,'-factor', factor)
pattern('UniformExcitation',2,1,'-accel',2)
rayleigh(0,0,0,(2*(damp/omega[0])))

wipeAnalysis()
constraints('Plain')
numberer('Plain')
system('SparseGeneral','-piv')
test('NormDispIncr',Tol,1000)
algorithm('ModifiedNewton')
integrator('Newmark',0.5,0.25)
analysis('Transient')
analyze(eqksteps,dt)
print("time history has been carried out")


## Plotting the Time History RESULTS!!!
disp = pd.DataFrame(pd.read_csv('DFree_py.out',delimiter=" ", header = None)).to_numpy()
force = pd.DataFrame(pd.read_csv('Rbase_py.out',delimiter=" ", header = None)).to_numpy()
disp1 = pd.DataFrame(pd.read_csv('DFree.out',delimiter=" ", header = None)).to_numpy()
force1 = pd.DataFrame(pd.read_csv('Rbase.out',delimiter=" ", header = None)).to_numpy()
#record_EQ = pd.DataFrame(pd.read_csv('RSN117601.AT2',delimiter="  ", header = None)).to_numpy()
#record_EQ1 = pd.read_csv('RSN117601.AT2',delimiter="  ", header = None)
plt.figure(figsize=(12, 9))

plt.plot(disp[:,0],disp[:,1])
plt.plot(disp1[:,0],disp1[:,1])
plt.legend(["PY","OpenSEES"])

plt.figure(figsize=(12, 9))

plt.plot(disp[:6500,1],-force[:6500,1])
plt.plot(disp1[:6500,1],-force1[:6500,1])
plt.legend(["PY","OpenSEES"])











