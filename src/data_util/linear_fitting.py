import data_util.data_util_main as D
import matplotlib.pylab as plt
import numpy as np

import pymc as pm
import dataclasses

from typing import List, Dict, Tuple
import data_util.config as CFG

def fit(amp_list:List[float], intg_out:List[float], fit_range:int) -> List[float]:
    
    fit_out = np.polyfit(amp_list[:fit_range], intg_out[:fit_range],1)
    
    return fit_out

def load_response_single_freq(cfg:CFG.FittingFileConfig) -> List[List[float]]:
    """load list of out phase measurements with different amplitude
    i.e. each amplitude should have 1k observations, 
    i.e. the load list should has a shape n_amp x n_measure
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
    n = len(responses[0])
    x = [a for a in cfg.amp for _ in range(n)]
    y = [item for sublist in responses for item in sublist]

    return x, y

