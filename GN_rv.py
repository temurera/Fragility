# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 19:20:18 2021

@author: erayt
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import invgauss
from scipy.stats import norm
from scipy.stats import lognorm

def GN_rv(mu,sigma,N):
    #np.random.seed(a=None, version=2)
    #mu = 15
    #sigma = 100
    asd = np.random.uniform(low=0.0, high =1.0, size=[1,N])
    asd1 = np.random.uniform(low=0.0, high =1.0, size=[1,N])
    #asd = np.random.normal(mu,sigma,size=[1,10000])
    #asd = np.random.lognormal(mu,sigma,size=[1,1000])
    #asd2 = invgauss.cdf(asd[0,:], mu)
    
    #asd2 = np.random.uniform(low=0.0, high =1.0, size=[1,N])
    asd2 = norm.ppf(asd[0,:],mu,sigma)
    asd3 = norm.ppf(asd[0,:],mu,sigma)
    asd4 = norm.ppf(asd1[0,:],mu,sigma)
    #asd2 = lognorm.ppf(asd[0,:],mu,sigma)
    #plt.figure(figsize=(12, 9))
    #plt.plot(asd[0,:])
    
    plt.figure(figsize=(12, 9))
    count, bins, ignored = plt.hist(asd[0,:], 100, density=True)
    plt.figure(figsize=(12, 9))
    count, bins, ignored = plt.hist(asd2[:,], 100, density=True)
    
    return asd,asd2,asd3,asd4

[asd,asd2,asd3,asd4] = GN_rv(15, 100, 10000)

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

Lgn_new = LOGN_rv(15, 0.033, 1000)