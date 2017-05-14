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


def knowndistr():
    return ['norm', 'lognorm']


def _distrargs(type):
    reqargs = {'norm'       : [],
               'lognorm'    : ['shp']
               }
    return reqargs[type]

def _distrkeys(type):
    # define the keys required for each distribution
    reqkeys = {'norm'       : ['loc', 'scale'],
               'lognorm'    : ['scale']
               }
    return reqkeys[type]


def _distrkeysync(type,dict,direction='chart'):
    # define the key mappings for each distribution

    if direction == 'chart':
        if type == 'norm':
            dict['loc'] = dict['mu']
            dict['scale'] = dict['std']
        elif type == 'lognorm':
            dict['scale'] = np.exp(dict['mu'])
    elif direction == 'trib':
        pass
    else:
        pass
    return dict

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


def blankreturn(kstats, func, type, input):
    # function if necessary values are not submitted, returns blanks to prevent crash
    print(func+": "+type+' '+input+" Unknown - blankreturn")
    kstats.update({'mean':'#N/A', 'var':'#N/A', 'skew':'#N/A', 'kurtosis':'#N/A'})
    return kstats


def invdistr(type,**kwargs):
    """
    invdistr - handler for all distribution types to simplify widgetFDTable mostly
    :param type: string - type of distribution to calculate for from [norm, lognorm, 
    :param kwargs: necessary inputs to calculate distribution, most distribution need two or more data points entered as
                    probabilties p0= , p1= , p2= , p3= , ... with matching
                    values       f0= , f1= , f2= , f3= , ...
    :return: kstats a dictionary containing all the inverse distribution outputs
    """
    kstats = {               # fill a blank kstats to include values not submitted in **kwargs
            'mu'    : None,  # mu
            'std'   : None,  # standard deviation
            'mean'  : None,  # mean of the distribution
            'var'   : None,  # variance
            'shp'   : None}  # shape factor for some scipy distributions

    if type in knowndistr():
        if type == 'norm':
            try:
                kstats['mu'], kstats['std'] = invNormPpf(kwargs['f0'], kwargs['p0'], kwargs['f1'], kwargs['p1'])
            except NameError:
                kstats = blankreturn(kstats, 'invdistr', type, 'Missing Value')
        elif type == 'lognorm':
            try:
                kstats['mu'], kstats['std'], kstats['shp'] = invLogNormPpf(kwargs['f0'], kwargs['p0'],
                                                                           kwargs['f1'], kwargs['p1'])
            except NameError:
                kstats = blankreturn(kstats, 'invdistr', type, 'Missing Value')
    else:  # unknown distribution submitted
        kstats = blankreturn(kstats,'invdistr', type,'Distribution')
    return kstats


def distrstats(type,**kwargs):
    """
    distrstats - handler for all distribution types to simplify widgetFDTable mostly
    :param type: string - type of distribution to calculate for from [norm, lognorm, 
    :param kwargs: necessary inputs to calculate statistics, mainly mu, std & shp but others where necessary
    :return: kstats - dictionary of distribution statistics
    """
    kstats = {               # fill a blank kstats to include values not submitted in **kwargs
            'mu'    : None,  # mu
            'std'   : None,  # standard deviation
            'mean'  : None,  # mean of the distribution
            'var'   : None,  # variance
            'shp'   : None}  # shape factor for some scipy distributions
    kstats.update(kwargs)    # update kstats with inputs

    if type in knowndistr():
        if type == 'norm':  # normal distribution
            try:
                kstats['mean'], kstats['var'], kstats['skew'], kstats['kurtosis'] = \
                    stats.norm.stats(loc=kstats['mu'], scale=kstats['std'],moments='mvsk')
            except (TypeError,AttributeError):
                kstats = blankreturn(kstats, 'distrstats', type, 'Value')
        elif type == 'lognorm':  # lognormal distribution
            try:
                kstats['mean'], kstats['var'], kstats['skew'], kstats['kurtosis'] = \
                    stats.lognorm.stats(kstats['shp'], scale=np.exp(kstats['mu']), moments='mvsk')
            except (TypeError, AttributeError):
                kstats = blankreturn(kstats, 'distrstats', type, 'Value')
    else:  # unknown distribution submitted
        kstats = blankreturn(kstats, 'distrstats', type,'Distribution')
    return kstats


def distrpdf(type, n, **kwargs):
    """
    distrpdf - handler for all distribution types to simplify widgetFDChart mostly
    :param type: string - type of distribution to calculate for from [norm, lognorm,
    :param n: the number of samples in the returned ppf function dictionary
    :param kwargs: necessary inputs to calculate statistics, mainly mu, std & shp but others where necessary
    :return: ppf - of distribution 'type'
    """
    kstats = {               # fill a blank kstats to include values not submitted in **kwargs
            'mu'    : None,  # mu
            'std'   : None,  # standard deviation
            'mean'  : None,  # mean of the distribution
            'var'   : None,  # variance
            'shp'   : None}  # shape factor for some scipy distributions
    kstats.update(kwargs)    # update kstats with inputs

    pmin=0.01; pmax=0.99

    data_dict = dict()
    if type in knowndistr():
        kstats = _distrkeysync(type,kstats)
        try:
            dargs = {kstats[key] for key in _distrargs(type)}
        except TypeError:
            dargs = ()
        try:
            dkwargs = {key: kstats[key] for key in _distrkeys(type)}
        except TypeError:
            dkwargs = ()

        if type == 'norm':  # normal distribution
            # calculate X space
            xmin = stats.norm.ppf(pmin, **dkwargs)
            xmax = stats.norm.ppf(pmax, **dkwargs)
            data_dict['X'] = np.linspace(xmin, xmax, n)
            # calculate distr
            data_dict['Y'] = stats.norm.pdf(data_dict['X'], **dkwargs)
        elif type == 'lognorm':  # lognormal distribution
            # calculate X space
            xmin = stats.lognorm.ppf(pmin, *dargs, **dkwargs)
            xmax = stats.lognorm.ppf(pmax, *dargs, **dkwargs)
            data_dict['X'] = np.linspace(xmin, xmax, n)
            # calculate distr
            data_dict['Y'] = stats.lognorm.pdf(data_dict['X'], *dargs, **dkwargs)
    return data_dict