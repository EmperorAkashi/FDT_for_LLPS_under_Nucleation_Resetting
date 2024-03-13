import data_util.data_util_main as D
import matplotlib.pylab as plt
import numpy as np

import dataclasses

from typing import List, Dict, Tuple

from scipy.optimize import curve_fit
from scipy.special import gamma
from scipy.stats import levy_stable, lognorm

def Exp_Distr(x: np.ndarray, tau:float):
    "fitting to an exponential distribution"
    return tau * np.exp(-tau * x)

def Berne_FPT(x: float, D: float, x_0: float, k: float):
    "express first passage distribution with quadratic potential"
    x = np.array(x)
    sigma = (1 - np.exp(-2*D*k*x))/k
    return 2*D*np.exp(-D*k*x)*abs(x_0)/np.sqrt(2*np.pi*sigma**3)*np.exp(-(x_0*np.exp(-D*k*x))**2/(2*sigma))

def levy_func(x: np.ndarray, alpha: float, beta: float, loc, scale):
    """fitting to a Levy distribution
    """
    return levy_stable.pdf(x, alpha, beta, loc, scale)

def lognorm_func(x: np.ndarray, s: float, loc, scale):
    """fitting to a Lognorm distribution
    """
    return lognorm.pdf(x, s, loc, scale)