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

#This script produces the model of a cable stayed bridge and the result of the modal analysis.
#Eray Temur

wipe()


# model build
model('basic','-ndm',3, '-ndf',6)
a = 4
#create nodes
exec(open("./NodeCoord.py").read())
exec(open("./Section.py").read())
exec(open("./Beam_Int.py").read())
exec(open("./Material_02.py").read())
exec(open("./Boundary.py").read())
exec(open("./Gt.py").read())
exec(open("./Elements_1.py").read())

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

recorder('Node', '-file', 'MODAL_Node_NodeEigen_EigenVec_1_PY.out', '-time','-nodeRange', 1, 1001, '-dof', 1, 2, 3, 4, 5, 6, 'eigen1')
record()
#create nodes
#exec(open("Elements.py").read())
#opsplt.plot_model()  # command from Get_Rendering module
#opsv.plot_model()  # command from ops_vis module

opsplt.plot_modeshape(1, 1000)
#plot_modeshape(3, 3000)

#analyze

#printA('-file','trial.txt')

#### Display the active model with node tags only
opsplt.plot_model("nodes")
plt.xlim([-100, -60])
plt.ylim([-10, 10])