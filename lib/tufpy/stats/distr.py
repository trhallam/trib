'''
distr.py

Antony Hallam
2017-04-26
'''

import warnings
import numpy as np
from scipy import stats
from scipy.special import erfinv

'''
Local Variables
'''
# Calculate local sqrt of 2
_sqrt2 = np.sqrt(2)


def invNormPpf(f1, p1, f2, p2):
    """Use two known points to calculate a normal continuous distribution.

    The value (f1) and percentage probability (p1) of the first point.
    The value (f2) and percentage probability (p2) of the second point.
    
    Returns mean (mu) and standard deviations (std) of the normal distribution.
    
    fx element of Real Numbers
    0 <= px <= 1

    %(before_notes)s

    Notes
    -----
    The mean (mu) and standard deviation (std) of the function are solved for by
    using the two input values as a pair of linear equations to sub in for the
    unknown variables. Start with the normal distribution quantile function::

        F = mu + std*sqrt2*erfinv(2*P-1)
        
    solve for mu for both sets of F1,P1 and F2,P2. Back sub and voila.

    https://en.wikipedia.org/wiki/Normal_distribution
    %(after_notes)s

    %(example)s
    _working\scipy_stats_norm_quantiles.py
    """

    std = (f1 - f2) / (_sqrt2 * (erfinv(2 * p1 - 1) - erfinv(2 * p2 - 1)))
    mu = f1 - std * _sqrt2 * erfinv(2 * p1 - 1)
    return mu, std


def invLogNormPpf(f1, p1, f2, p2):
    """Use two known points to calculate a log-normal continuous distribution.

    The value (f1) and percentage probability (p1) of the first point.
    The value (f2) and percentage probability (p2) of the second point.
    
    Returns mean (mu) and standard deviations (std) of the normal distribution 
    of the log of the variate (read below for use with scipy.lognorm).
    
    fx element of Real Numbers > 0
    0 <= px <= 1

    %(before_notes)s

    Notes
    -----
    The mean (mu) and standard deviation (std) of the function are solved for by
    using the two input values as a pair of linear equations to sub in for the
    unknown variables. Start with the normal distribution quantile function::

        ln(F) = mu + std*sqrt2*erfinv(2*P-1)
        
    solve for mu for both sets of F1,P1 and F2,P2. Back sub and voila.

    https://en.wikipedia.org/wiki/Log-normal_distribution
    http://www.itl.nist.gov/div898/handbook/eda/section3/eda3669.htm
    
    For scipy.lognorm parameters
    loc - No equivalent, this gets subtracted from your data so that 0 becomes 
    the infimum of the range of the data.

    scale - exp μ, where μ is the mean of the log of the variate. (When fitting,
    typically you'd use the sample mean of the log of the data.)

    shape - the standard deviation of the log of the variate.
    
    use outputs mu and std as std=shape factor and scale=np.exp(mu)
    
    %(after_notes)s

    %(example)s
    _working\scipy_stats_lognorm_quantiles.py
    """
    df=np.log(f2/f1)
    erff_part = _sqrt2 * (erfinv(2 * p2 - 1) - erfinv(2 * p1 - 1))
    shp = df / erff_part
    std = np.log(f2 - f1) / erff_part
    mu = np.log(f1) - shp * _sqrt2 * erfinv(2 * p1 - 1)

    return mu, std, shp


def distrstats(type,**kwargs):
    kstats = {
            'mu'    : None, # mu
            'std'   : None, # standard deviation
            'mean'  : None, # mean of the distribution
            'var'   : None, # variance
            'shp'   : None} # shape factor for some scipy distributions

    kstats.update(kwargs)

    def blankreturn(kstats, type, input):
        print("disrtstats: "+type+' '+input+" Unknown - blankreturn")
        kstats.update({'mean':'#N/A', 'var':'#N/A', 'skew':'#N/A', 'kurtosis':'#N/A'})
        return kstats

    if type == 'norm':
        try:
            kstats['mean'], kstats['var'], kstats['skew'], kstats['kurtosis'] = \
                stats.norm.stats(loc=kstats['mu'], scale=kstats['std'],moments='mvsk')
        except (TypeError,AttributeError):
            kstats = blankreturn(kstats, type, 'Value')
    elif type == 'lognorm':
        try:
            kstats['mean'], kstats['var'], kstats['skew'], kstats['kurtosis'] = \
                stats.lognorm.stats(kstats['shp'], scale=np.exp(kstats['mu']), moments='mvsk')
        except (TypeError, AttributeError):
            kstats = blankreturn(kstats, type, 'Value')
    else:
        kstats = blankreturn(kstats,type,'Distribution')

    return kstats