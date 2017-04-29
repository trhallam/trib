'''
test_distr.py

Antony Hallam
2017-04-29


test functions for distr.py
'''

import numpy as np
from scipy.stats import norm
from scipy.special import erfinv
import matplotlib.pyplot as plt

from . import lib

def checkValue(var,varname,val):
    '''
    Checks a value is true and prints a validations statement.
    '''
    if (var==val):
        print(varname,'\t PASS')
    else:
        print(varname,'\t FAIL')
        
        
#normal distribution
F1=60; F2=80; P1=0.2; P2=.6
mu, std = lib.distr.invNormPpf(F1,P1,F2,P2)
checkValue(mu,'invNormPpf\tmu',75.372521841182774)
checkValue(std,'invNormPpf\tstd',18.26536834856481)

#lognormal distribution
F1=20; F2=50; P1=0.2; P2=.8
mu, std = lib.distr.invLogNormPpf(F1,P1,F2,P2)
checkValue(mu,'invLogNormPpf\tmu',21.700598690831079)
checkValue(std,'invLogNormPpf\tstd',2.0206223690573575)