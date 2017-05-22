'''
distr.py

Antony Hallam
2017-04-26
'''

import warnings
import numpy as np
from scipy import stats
from scipy.special import erfinv

from tufpy.utils import strictly_increasing

'''
Local Variables
'''
# Calculate local sqrt of 2
_sqrt2 = np.sqrt(2)


def _distrnames():
    # returns a dictionary of all the names of the known distributions
    return {'norm'          : 'Normal',
            'lognorm'       : 'Log-Normal'
            }


def knowndistr():
    return list(_distrnames().keys())


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


def _distrinputs(type):
    # define the input values required for each distribution
    reqinputs = {'norm'     : ['mu', 'std'],
                 'lognorm'  : ['mu', 'shp']}
    return reqinputs[type]


def _distrkeysync(type,dict,direction='chart'):
    # define the key mappings for each distribution

    if direction == 'chart':
        if type == 'norm':
            dict['loc'] = dict['mu']
            dict['scale'] = dict['std']
        elif type == 'lognorm':
            dict['scale'] = np.exp(dict['mu'])
    elif direction == 'trib':
        if type == 'norm':
            dict['mu'] = dict['loc']
            dict['std'] = dict['scale']
        elif type == 'lognorm':
            dict['mu']=np.log(dict['std'])
    else:
        pass
    return dict


def _distrmapargs(type,indict):
    kstats = _distrkeysync(type, indict)
    try:
        dargs = {kstats[key] for key in _distrargs(type)}
    except TypeError:
        dargs = ()
    try:
        dkwargs = {key: kstats[key] for key in _distrkeys(type)}
    except TypeError:
        dkwargs = ()
    return dargs, dkwargs

def invNormPpf(f1, p1, *f2p2,  mu = None):
    """Use two known points to calculate a normal continuous distribution.

    The value (f1) and percentage probability (p1) of the first point.
    The value (f2) and percentage probability (p2) of the second point.
    The value of the mean can be used instead of (f2) and (p2)
    
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
    if mu == None:
        f2 = f2p2[0]; p2 = f2p2[1]
        std = (f1 - f2) / (_sqrt2 * (erfinv(2 * p1 - 1) - erfinv(2 * p2 - 1)))
        mu = f1 - std * _sqrt2 * erfinv(2 * p1 - 1)
    else:
        std = (f1 - mu)/(_sqrt2 * erfinv(2 * p1 - 1))

    return mu, std


def invLogNormPpf(f1, p1, *f2p2,  mu = None, shp = None):
    """Use two known points to calculate a log-normal continuous distribution.

    The value (f1) and percentage probability (p1) of the first point.
    The value (f2) and percentage probability (p2) of the second point.
    THe value of the mean can be used instead of (f2) and (p2)
    
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
    if mu == None and shp == None:
        f2 = f2p2[0]; p2 = f2p2[1]
        df=np.log(f2/f1)
        erff_part = _sqrt2 * (erfinv(2 * p2 - 1) - erfinv(2 * p1 - 1))
        shp = df / erff_part
        std = np.log(f2 - f1) / erff_part
        mu = np.log(f1) - shp * _sqrt2 * erfinv(2 * p1 - 1)
    elif mu != None and shp == None: #TODO not sure if these next elifs are right
        shp = (mu - np.log(f1)) / (-1.0 * _sqrt2 * erfinv(1 * p1 - 1))
        std = -999
    elif mu == None and shp != None:
        mu = np.log(f1) - shp * _sqrt2 * erfinv(2 * p1 - 1)
        std = -999


    return mu, std, shp


def blankreturn(func, type, input):
    # function if necessary values are not submitted, returns blanks to prevent crash
    print(func+": "+type+' '+input+" Unknown - blankreturn")
    #kstats.update({'mean':'#N/A', 'var':'#N/A', 'skew':'#N/A', 'kurtosis':'#N/A'})
    return None


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
        try:
            if type == 'norm' and kwargs['mu'] is None:
                kstats['mu'], kstats['std'] = invNormPpf(kwargs['f1'], kwargs['p1'], kwargs['f2'], kwargs['p2'])
            elif type == 'norm' and kwargs['mu'] is not None:
                kstats['mu'], kstats['std'] = invNormPpf(kwargs['f1'], kwargs['p1'], mu=kwargs['mu'])
            elif type == 'lognorm':
                kstats['mu'], kstats['std'], kstats['shp'] = invLogNormPpf(kwargs['f0'], kwargs['p0'],
                                                                           kwargs['f1'], kwargs['p1'])
        except (NameError, KeyError):
                kstats = blankreturn('invdistr', type, 'Missing Value')
    else:  # unknown distribution submitted
        kstats = blankreturn('invdistr', type,'Distribution')
    return kstats

def invdistr2(type, inputdict, flags=False):
    """
    invdistr2 - handler for all distribution types to simplify widgetFDTable mostly
        Key Features:
            - checks the sanity of input parameters and returns flags when they are not ok
            - calculates the inverse distribution of the type specified
    :param type: string - type of distribution to calculate for from [norm, lognorm, 
    :param inputdict: diction of inputs to calculate distribution, most distribution need two or more data points   
                    dictionary has structure {'Inputs':[], 'Values':[]}
                    inputs can be know values (mean, mu, std, shp, probits (0<p<1), ...etc)
                    values must be floats valid for the relevant input
    :return: kstats a dictionary containing all the inverse distribution outputs
    :return: kstats, rowflags if flags=True
    """

    # loop variables
    inval = dict()  # build the dictionary of valid values
    icount = 1      # counter for number of probit values input
    fpsanity = []   # array for probit sanity check
    rowflags = []   # array for output rowflags
    fprows = []     # index of probit rows from greater number of rows

    for i, val in enumerate(inputdict['Input']):  # loop through values in input
        if val != '':  # make sure cell not empty
            try:
                if val in _distrinputs(type):  # known values like mu, std
                    inval[val] = float(inputdict['Value'][i])
                    rowflags.append(1)  # append known value flag
                else:  # unknown value check for decimal input to set f* p* values
                    pc = float(val);
                    fv = float(inputdict['Value'][i])
                    if 0.0 < pc < 1.0:
                        inval['f%d' % icount] = fv
                        inval['p%d' % icount] = 1 - pc
                        icount += 1
                        fpsanity.append([1 - pc, fv]);
                        fprows.append(i)
                        rowflags.append(2)  # append fp type row flag (requires group sanity check)

                    else:  # append bad row flag
                        rowflags.append(9)
            except:  # TODO write some code that changes the colour of the cells to reflect bad inputs
                rowflags.append(9)  # append bad row flag

    # sanity check for fp values
    fpsanity = np.array(fpsanity)
    try:
        fpsanity = fpsanity[fpsanity[:, 1].argsort()]
        if not strictly_increasing(fpsanity[:, 0]):
            for row in fprows:
                rowflags[row] = 9
    except:
        pass

    # calculate kstats for input values fir distribution types
    # standard distribution definition as input - different for each distribution
    cond1 = all([var in inval.keys() for var in _distrinputs(type)])
    # p1 f1 p2 f2 as input
    cond3 = all([var in inval.keys() for var in ['f1', 'p1', 'f2', 'p2']])

    if type == 'norm':
        # mu and p1 f1 as input
        cond2 = all([var in inval.keys() for var in ['mu', 'f1', 'p1']])

    elif type == 'lognorm':
        # mu and p1 f1 as input or shp and p1 f1 as input
        cond2 = all([var in inval.keys() for var in ['mu', 'f1', 'p1']]) or \
                all([var in inval.keys() for var in ['shp', 'f1', 'p1']])

    if cond1:  # check for simple keys
        kstats = dict()
        for key in _distrinputs(type):
            kstats[key] = inval[key]  # add simple keys to kstats
    elif cond2:
        kstats = invdistr(type, **inval)  # use 2 point method to fix distribution
    elif cond3:
        inval['mu'] = None
        kstats = invdistr(type, **inval)  # use 2 point method to fix distribution
    else:
        kstats = None

    if flags:
        return kstats, rowflags
    else:
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
                kstats = blankreturn('distrstats', type, 'Value')
        elif type == 'lognorm':  # lognormal distribution
            try:
                kstats['mean'], kstats['var'], kstats['skew'], kstats['kurtosis'] = \
                    stats.lognorm.stats(kstats['shp'], scale=np.exp(kstats['mu']), moments='mvsk')
            except (TypeError, AttributeError):
                kstats = blankreturn('distrstats', type, 'Value')
    else:  # unknown distribution submitted
        kstats = blankreturn('distrstats', type,'Distribution')
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

    pmin=0.0001; pmax=0.9999

    data_dict = dict()
    if type in knowndistr():
        kstats = _distrkeysync(type, kstats)
        dargs, dkwargs = _distrmapargs(type, kstats)
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

def distrppf(type, a, **kwargs):
    """
    distrppf - handler for all distribution types to simplify XProbitChart mostly
    :param type: string - type of distribution to calculate for from [norm, lognorm,
    :param a: float or float_ar of values between 0 and 1.
    :param kwargs: tbd
    """
    if type in knowndistr():
        #kstats = _distrkeysync(type, kstats)
        #dargs, dkwargs = _distrmapargs(kstats)
        dargs = []; dkwargs = []
        if type == 'norm':  # normal distribution
            ppfar = stats.norm.ppf(a, *dargs, **kwargs)
        elif type == 'lognorm':
            ppfar = stats.lognorm.ppf(a, *dargs, **kwargs)
    
    return ppfar
    
def distrfit(type, a, **kwargs):
    """
    distrfit - handler for all distribution types to simplify widgetIDChart mostsly
    :param type: string - type of distribution to calculate for from [norm, lognorm,
    :param a: array of float values to fit the distribution of type to
    :param kwargs: tbd
    """
    kstats = {               # fill a blank kstats to include values not submitted in **kwargs
            'mu'    : None,  # mu
            'std'   : None,  # standard deviation
            'mean'  : None,  # mean of the distribution
            'var'   : None,  # variance
            'shp'   : None}  # shape factor for some scipy distributions

    if type in knowndistr():
        if type == 'norm':  # normal distribution
            distrMLE = stats.norm.fit(a)
            kstats['mu'] = distrMLE[0]; kstats['mean'] = distrMLE[0]
            kstats['std'] = distrMLE[1]
        elif type == 'lognorm':
            distrMLE = stats.lognorm.fit(a,floc=0)
            kstats['shp'] = distrMLE[0]; kstats['loc'] = distrMLE[1]
            kstats['mu'] = np.log(distrMLE[2])
    
    return kstats

def distrdescribe(a):
    """
    distrdescribe - handler for describe of an array of floats, maps values back to understood dictionary
    :param a: 
    :return: kstats - a dict of known distribution quantities
    """
    kstats = dict()
    istats = stats.describe(a)
    kstats['nsamp'] = istats[0]
    kstats['min'] = istats[1][0]; kstats['max'] = istats[1][1]
    kstats['mean'] = istats[2]; kstats['var'] = istats[3]
    kstats['skew'] = istats[4]; kstats['kurt'] = istats[5]

    kstats['F90'] = stats.scoreatpercentile(a, 10)
    kstats['F50'] = stats.scoreatpercentile(a, 50)
    kstats['F10'] = stats.scoreatpercentile(a, 90)

    return kstats