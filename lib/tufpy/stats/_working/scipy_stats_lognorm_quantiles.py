# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
from scipy.stats import lognorm
from scipy.special import erfinv
import matplotlib.pyplot as plt

sqrt2=np.sqrt(2)

F1=50; F2=97.6; P1=0.1; P2=0.9
dF=np.log(F2/F1)
erff=sqrt2*(erfinv(2*P2-1)-erfinv(2*P1-1))
var = dF/erff; shp = var
mu = np.log(F1)-var*sqrt2*erfinv(2*P1-1)
scal=np.exp(mu)

print('Input P1,P2,F1,F2:\n',P1,P2,F1,F2)
print('Calc: Var, Shp, mu:\n',var,shp,scal)

p1=lognorm.cdf(F1,shp,scale=scal)
p2=lognorm.cdf(F2,shp,scale=scal)
f1=lognorm.ppf(P1,shp,scale=scal)
f2=lognorm.ppf(P2,shp,scale=scal)

print('Input P1,P2,F1,F2:\n',p1,p2,f1,f2)

fig, ax = plt.subplots(1, 1)
x = np.linspace(lognorm.ppf(0.001,shp,scale=scal),\
                lognorm.ppf(0.999,shp,scale=scal), 1000)
ax.plot([F1,F1],[0,lognorm.pdf(F1,shp,scale=scal)],'k-')
ax.plot([F2,F2],[0,lognorm.pdf(F2,shp,scale=scal)],'k-')
ax.plot(x, lognorm.pdf(x,shp,scale=scal),'r-',\
          lw=2, alpha=1, label='norm pdf')

