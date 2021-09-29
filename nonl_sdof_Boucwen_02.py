# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 21:03:04 2020

@author: erayt
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


EQx=pd.read_csv('Matched_165-1_A.txt', header = None)
EQx = EQx.values

fs=200
dt=1/fs
Ttot=dt
numberofstep = int(len(EQx))#int(Ttot/dt) 
teq = np.linspace(0,numberofstep*dt,(numberofstep-1))
N  = len(teq)  

# Bouc-Wen parameters
beta=1
gamma=.4
n=6
alpha=0.05


# linear dynamics parameters
k1=12*25000000/(162**3)
m1=2548.41997961264

#Newmark parameters
n_gamma = 1/2 
n_beta = 1/4

#Damping
c1=0.05; 

#Stiffness degradation 
delta_h =0

# inputs
coef=25#100*(1/(beta+ gamma))**(1/n)        #scaling coefficient for the force, 3 times with respect to the yield strength rescribed by the BW model
g=9.81
u=-(coef*1*EQx)*1000#/(np.max(np.abs(EQx*g)))   # Definition of an earthquake force (inpout in g)


agg=u[0:N-1]

y = np.zeros(len(agg))
y_prime = np.zeros(len(agg))
y_PPrime = np.zeros(len(agg))
z = np.zeros(len(agg))
z_prime = np.zeros(len(agg))
defor = np.zeros(len(agg))
Dy_PPrime = np.zeros(len(agg))


for i in range(len(agg)-1):
    y_prime[i+1] = y_prime[i]+(1-n_gamma)*dt*y_PPrime[i]+n_gamma*dt*y_PPrime[i+1]
    y[i+1] = y[i]+dt*y_prime[i]+((1/2)-n_beta)*(dt**2)*y_PPrime[i]+n_beta*(dt**2)*y_PPrime[i+1]
    z[i+1] = z[i]+(1-gamma)*dt*z_prime[i]+gamma*dt*z_prime[i+1]
    eps = agg[i+1] - alpha*k1*y[i+1]-((1-alpha)*k1*z[i+1])-c1*y_prime[i+1]-m1*y_PPrime[i+1]
    while abs(eps)>=10e-10:
        Dy_PPrime[i+1] = eps/(m1+c1*n_gamma*dt + k1*n_beta*(dt**2))
        y_PPrime[i+1] = y_PPrime[i+1]+Dy_PPrime[i+1]
        y_prime[i+1] = y_prime[i+1] + Dy_PPrime[i+1]*n_gamma*dt
        y[i+1] = y[i+1] + Dy_PPrime[i+1]*n_beta*(dt**2)
        defor[i+1] = dt*np.cumsum(np.matmul(y_prime[0:i+1],(z[0:i+1])))
        z_prime[i+1] =(y_prime[i+1]-((beta*abs(y_prime[i+1])*z[i+1]*(abs(z[i+1])**(n-1)))+(gamma*y_prime[i+1]*(abs(z[i+1])**n))))/((1+(delta_h*defor[i+1])))
        z[i+1] = z[i]+(1-gamma)*dt*z_prime[i]+gamma*dt*z_prime[i+1]
        eps = agg[i+1] - alpha*k1*y[i+1]-(1-alpha)*k1*z[i+1]-c1*y_prime[i+1]-m1*y_PPrime[i+1]




plt.figure(figsize=(12, 9))
plt.plot(y,alpha*k1*y+(1-alpha)*k1*z)
#plt.xlim([0, 1])
plt.xlabel(r'$\epsilon$', fontsize=14)
plt.ylabel(r'$\sigma$', fontsize=16)
plt.legend();
plt.figure(figsize=(12, 9))
plt.plot(y)
#plt.plot(agg)
#plt.xlim([0, 1])
plt.xlabel(r'$\epsilon$', fontsize=14)
plt.ylabel(r'$\sigma$', fontsize=16)
plt.legend();