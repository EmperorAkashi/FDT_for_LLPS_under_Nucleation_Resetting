import data_util.data_util_main as D
import matplotlib.pylab as plt
import numpy as np

import pymc as pm
import dataclasses

from typing import List, Dict, Tuple
import data_util.config as CFG

def fit_single(amp_list:List[float], intg_out:List[float], fit_range:int) -> List[float]:
    """here amp and intg_out can be averaged or flattened,
    the resulted linear regress should be equivalent
    return: 2-elements list [slope, intercept]
    """
    fit_out = np.polyfit(amp_list[:fit_range], intg_out[:fit_range],1)
    return fit_out

def load_response_single_freq(cfg:CFG.FittingFileConfig) -> List[List[float]]:
    """load list of out phase measurements with different amplitude
    i.e. each amplitude should have 1k observations, 
    the loaded list should has a shape n_amp x n_measure
    noticed to make sure the measures in linear response region
    we only use amp <1.5 for fitting
    """
    response_2d_list = []

    for a in cfg.amp:
        out_phase_file = cfg.prefix_1d + cfg.dir_prefix+"/out_o"+str(cfg.curr_omg)+"A"+str(a) \
        +"_ap"+str(cfg.alpha)+".txt"
        curr_obs = D.read_list(out_phase_file)
        response_2d_list.append(curr_obs)

    return response_2d_list

def flat_to_one_d(cfg:CFG.FittingFileConfig, 
                  responses:List[List[float]]) -> Tuple[List[float],List[float]]:
    """flats the 2D list response/observations to 1D as y,
    manually generate 1D amplitutes to match the size of responses as x
    i.e. repeat each x 1k times as each x has 1k observations y
    """
    n = len(responses[0])
    x = [a for a in cfg.amp for _ in range(n)]
    y = [item for sublist in responses for item in sublist]

    return x, y

def get_rss_std(fitted:List[float], responses:List[List[float]], 
            cfg:CFG.FittingFileConfig) -> float:
    """get residual sum of squares (rss) and standard deviation
    @arg slope, intercept are fitted value from a single linear fitting
    (can be a fitting by using averaged response or not)
    """
    slope, intercept = fitted

    amp_fit = cfg.amp[:cfg.fit_range]
    response_fit = responses[:cfg.fit_range]
    m, n = len(response_fit), len(response_fit[0])

    total_res = 0
    for i in range(len(amp_fit)):
        y_hat = amp_fit[i]*slope + intercept
        for o in response_fit[i]:
            total_res += (y_hat - o)**2

    var = total_res/(m*n - 2)
    return np.sqrt(var)

def run_seq_fitting(seq_cfg:CFG.SeqFittingConfig) -> Tuple[List[float], List[float]]:
    """get rss and std for all omega
    return: mean and std list for different omega (the frequencies)
    """
    m, n = seq_cfg.fit_range, seq_cfg.sample
    std_list = []
    mean_list = []
    for o in seq_cfg.omg:
        curr_cfg = CFG.FittingFileConfig()
        curr_cfg.curr_omg = o
        load_curr_list = load_response_single_freq(curr_cfg)
        curr_x, curr_y = flat_to_one_d(curr_cfg, load_curr_list)
        fitted = fit_single(curr_x[:m*n], curr_y[:m*n], m*n)
        std = get_rss_std(fitted, load_curr_list, curr_cfg)

        std_list.append(std)
        mean_list.append(fitted[0])

    return mean_list, std_list

