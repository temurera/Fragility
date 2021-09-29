# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 18:53:47 2020

@author: erayt
"""

# Material "4000Psi":    matTag    E    v    <rho> 
nDMaterial("ElasticIsotropic",1,  +2.485558E+07,  +2.000000E-01,  +2.402770E+00) 

# Material "A416Gr270":    matTag    E    <eta>    <Eneg>  
uniaxialMaterial("Elastic", 2, +1.965006E+08, +0.000000E+00) 

# Material "A615Gr60":    matTag    E    <eta>    <Eneg>  
uniaxialMaterial("Elastic", 3,  +1.999480E+08,  +0.000000E+00) 

# Material "A992Fy50":    matTag    E    <eta>    <Eneg>  
uniaxialMaterial("Elastic",4,  +1.999480E+08,  +0.000000E+00)

# Material "Rigid4Release":    matTag    E    <eta>    <Eneg>  
uniaxialMaterial("Elastic",5,  +1.000000E+12,  +0.000000E+00) 

# Material "St":    matTag    E    <eta>    <Eneg>  
uniaxialMaterial("Elastic",6,  +1.999480E+08,  +0.000000E+00) 

# Material "St_Cable":    matTag    E    <eta>    <Eneg>  
uniaxialMaterial("Elastic",7, +1.999480E+08,  +0.000000E+00) 

#exec(open("./GeoTran.py").read())


