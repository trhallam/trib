'''
test_distr.py

Antony Hallam
2017-04-29


test functions for distr.py
'''

from tufpy.stats import distr
from numpy import array

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
mu, std = distr.invNormPpf(F1,P1,F2,P2)
checkValue(mu,'invNormPpf\tmu',75.372521841182774)
checkValue(std,'invNormPpf\tstd',18.26536834856481)
kstats = distr.distrstats('norm',mu=mu, std=std)
test = {'mu': 75.372521841182774,
        'std': 18.26536834856481,
        'mean': array(75.37252184118277),
        'var': array(333.62368090875316),
        'shp': None, 'skew': array(0.0),
        'kurtosis': array(0.0)}
checkValue(test,'distrstats\tnorm',kstats)

#lognormal distribution
F1=20; F2=50; P1=0.2; P2=.8
mu, std, shp = distr.invLogNormPpf(F1,P1,F2,P2)
checkValue(mu,'invLogNormPpf\tmu',3.4538776394910684)
checkValue(std,'invLogNormPpf\tstd',2.0206223690573575)
kstats = distr.distrstats('lognorm',mu=mu, shp=shp)
test = {'mu': 3.4538776394910684,
        'std': None,
        'mean': array(36.67303790994917),
        'var': array(463.87579692552686),
        'shp': 0.54436051237933258,
        'skew': array(1.9644393645363163),
        'kurtosis': array(7.563393758031713)}
checkValue(test,'distrstats\tlognorm',kstats)

#distrstats badType
kstats = distr.distrstats('norm',mu='he', std=std)
kstats = distr.distrstats('norm',shp=0.5, std=std)
kstats = distr.distrstats('lognorm',shp=0.5, std=std)

