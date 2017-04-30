# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
from scipy.stats import norm
from scipy.special import erfinv
import matplotlib.pyplot as plt

from . import lib
from lib import distr

sqrt2=np.sqrt(2)

F1=60; F2=80; P1=0.2; P2=.5
func = F1-F2
erfpart = sqrt2*(erfinv(2*P1-1)-erfinv(2*P2-1))

std = func/erfpart
mu = F1-std*sqrt2*erfinv(2*P1-1)

print(func,erfpart,mu,std)

fig, ax = plt.subplots(1, 1)
x = np.linspace(norm.ppf(0.001,loc=mu,scale=std),\
                norm.ppf(0.999,loc=mu,scale=std), 1000)
ax.plot([F1,F1],[0,norm.pdf(F1,loc=mu,scale=std)],'k-')
ax.plot([F2,F2],[0,norm.pdf(F2,loc=mu,scale=std)],'k-')
ax.plot(x, norm.pdf(x,loc=mu,scale=std),'r-',\
          lw=2, alpha=1, label='norm pdf')