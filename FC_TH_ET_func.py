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

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import invgauss
from scipy.stats import norm
from scipy.stats import lognorm
import math

def GN_rv(mu,sigma,N):
    #np.random.seed(a=None, version=2)
    #mu = 15
    #sigma = 100
    asd = np.random.uniform(low=0.0, high =1.0, size=[1,N])
    #asd = np.random.normal(mu,sigma,size=[1,10000])
    #asd = np.random.lognormal(mu,sigma,size=[1,1000])
    #asd2 = invgauss.cdf(asd[0,:], mu)
    
    asd2 = norm.ppf(asd[0,:],mu,sigma)
    #asd2 = lognorm.ppf(asd[0,:],mu,sigma)
    #plt.figure(figsize=(12, 9))
    #plt.plot(asd[0,:])
    
    plt.figure(figsize=(12, 9))
    count, bins, ignored = plt.hist(asd[0,:], 100, density=True)
    plt.figure(figsize=(12, 9))
    count, bins, ignored = plt.hist(asd2[:,], 100, density=True)
    
    return asd2

#gn_new = GN_rv(15, 100, 10000)

gn_new = GN_rv(250000000, 1, 100000) 

def LOGN_rv(mu,sigma,N):
    #np.random.seed(a=None, version=2)
    #mu = 15
    #sigma = 100
    asd = np.random.uniform(low=0.0, high =1.0, size=[1,N])
    #asd = np.random.normal(mu,sigma,size=[1,10000])
    #asd = np.random.lognormal(mu,sigma,size=[1,1000])
    #asd2 = invgauss.cdf(asd[0,:], mu)
    
    #asd2 = norm.ppf(asd[0,:],mu,sigma)
    asd2 = lognorm.ppf(asd[0,:],np.log(mu),sigma)
    #plt.figure(figsize=(12, 9))
    #plt.plot(asd[0,:])
    
    plt.figure(figsize=(12, 9))
    count, bins, ignored = plt.hist(asd[0,:], 100, density=True)
    plt.figure(figsize=(12, 9))
    count, bins, ignored = plt.hist(asd2[:,], 100, density=True)
    return asd2

#Lgn_new = LOGN_rv(15, 0.033, 1000)






# _____________________________model build____________________________________

#Structural and Phsysical Parameters



def Opensees_time_history(EIx):
    #reset(EI=EIx)
    wipe()
    g = 9.81
    deckmass = 25000/g
    #EI = 250000000
    EI = EIx
    fy = 355000 
    dt = 0.005 #dt for eq record
    eqk = 'Matched_165-1A_1.txt'
    factor = 2*g
    damp = 0.05 #percent
    eqksteps = 6999
    
    b = 0.01#0.1281
    L = 15.0 #m

    model('basic','-ndm',2, '-ndf',3)
    node(1,0.,0.)
    node(2,0.,L)
    fix(1,1,1,1)
    transTag  = 1
    #geometric Transformation
    geomTransf('Linear',transTag)
    
    
    mass(2, deckmass, deckmass,0) 
    
    
    #Materials 
    #uniaxialMaterial('Steel01', 1, fy, EI, b,0,1,0,1)
    
    uniaxialMaterial('Steel02', 1, fy, EI, 0.1,18,0.0,0.15,0,1,0,1,0.0)
    uniaxialMaterial('Elastic', 2, EI)
    
    
    #uniaxialMaterial('ElasticBilin', 3,EI, 0.05)
    
    section('Aggregator',1,2, 'P',1, 'Mz') # combine axial and flexural behavior into one section (no P-M interaction here)
    element('nonlinearBeamColumn',1,1,2,10,1,transTag)
    recorder('Node', '-file', 'DFree_py.out', '-time','-node', 2, '-dof', 1, 2, 3, 'disp')
    recorder('Node', '-file', 'VFree_py.out', '-time','-node', 2, '-dof', 1, 2, 3, 'vel')
    recorder('Node', '-file', 'AFree_py.out', '-time','-node', 2, '-dof', 1, 2, 3, 'accel')
    recorder('Node', '-file', 'Dbase_py.out', '-time','-node', 1, '-dof', 1, 2, 3,'disp')
    recorder('Node', '-file', 'Rbase_py.out', '-time','-node', 1, '-dof', 1, 2, 3, 'reaction')
    
    omega = np.array(eigen('-fullGenLapack', 1),dtype=float)**0.5
    #print(" w = ",omega)
    
    T_sec = 2*np.pi/omega
    #print(" Period of the structure = ",T_sec)
    
    record()
    
    #____________________________Analysis Details__________________________________
    
    Tol = 1.0e-6
    #Time History
    timeSeries('Path',2,'-dt',dt,'-filePath', eqk,'-factor', factor)
    pattern('UniformExcitation',2,1,'-accel',2)
    
    #Damping
    rayleigh(0,0,0,(2*(damp/omega[0])))
    


    
    #Analysis Commands
    wipeAnalysis()
    constraints('Plain')
    numberer('Plain')
    system('SparseGeneral','-piv')
    test('NormDispIncr',Tol,1000)
    algorithm('ModifiedNewton')
    integrator('Newmark',0.5,0.25)
    analysis('Transient')
    analyze(eqksteps,dt)
    #print("time history has been carried out")
    
    #_______________________________RESULTS________________________________________
    
    ## Plotting the Time History RESULTS!!!
    disp = pd.DataFrame(pd.read_csv('DFree_py.out',delimiter=" ", header = None)).to_numpy()
    vel = pd.DataFrame(pd.read_csv('VFree_py.out',delimiter=" ", header = None)).to_numpy()
    accl = pd.DataFrame(pd.read_csv('AFree_py.out',delimiter=" ", header = None)).to_numpy()
    
    force = pd.DataFrame(pd.read_csv('Rbase_py.out',delimiter=" ", header = None)).to_numpy()
    #disp1 = pd.DataFrame(pd.read_csv('DFree.out',delimiter=" ", header = None)).to_numpy()
    #force1 = pd.DataFrame(pd.read_csv('Rbase.out',delimiter=" ", header = None)).to_numpy()
    #record_EQ = pd.DataFrame(pd.read_csv('RSN117601.AT2',delimiter="  ", header = None)).to_numpy()
    #record_EQ1 = pd.read_csv('RSN117601.AT2',delimiter="  ", header = None)
 
    '''
    plt.figure(figsize=(12, 9))
    
    plt.plot(disp[:,0],disp[:,1])
    #plt.plot(disp1[:,0],disp1[:,1])
    plt.legend(["PY","OpenSEES"])
    
    plt.figure(figsize=(12, 9))
    
    plt.plot(vel[:,0],vel[:,1])
    
    plt.figure(figsize=(12, 9))
    
    plt.plot(accl[:,0],accl[:,1])
    
      
    plt.figure(figsize=(12, 9))
    
    plt.plot(disp[:eqksteps-250,1],-force[:eqksteps-250,1])
    #plt.plot(disp1[:6500,1],-force1[:6500,1])
    #plt.legend(["PY","OpenSEES"])
    
    '''
    
    y = force[0:eqksteps-200,1].astype(np.float)
    
    return np.max(np.abs(y[np.logical_not(pd.isnull(y))]))

    #x[numpy.logical_not(numpy.isnan(x))]

'''
g = 9.81
deckmass = 25000/g
#EI = 250000000
fy = 355000 
dt = 0.005 #dt for eq record
eqk = 'Matched_165-1A_1.txt'
factor = 25*g
damp = 0.05 #percent
eqksteps = 6999

b = 0.01#0.1281
L = 15.0 #m
'''
EI_grv = GN_rv(250000000, 10000000, 1000)

#EI_grv = [250000000,300000000]
Max_force = []

for i in range(len(EI_grv)):

    Max_force.append(Opensees_time_history(EI_grv[i,]))
    #%reset_selective -f Max_force
    #wipe()
    #remove('nodes')
    


plt.figure(figsize=(12, 9))
count, bins, ignored = plt.hist(Max_force, 100, density=True)
    

