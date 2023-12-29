import data_util.data_util_main as D
import matplotlib.pylab as plt
import numpy as np

import pymc as pm
import dataclasses

from typing import List, Dict

@dataclasses.dataclass
"""dataclass to specify the configure to run MCMC
"""
class FileConfigMCMC:
    alpha:float = 9.2
    curr_omg:float = 0.1
    amp:List[float] = [0.5,0.8,1.0,1.5]
    dir_prefix:str = "1D_9.2_relx200_Rn" #directory's name
    dt:float = 0.01
    fit_range:int = 3
    prefix_1d:str = "C:/Users/linch/Downloads/Diffusion_Elastic/Elastic_Hexagon/2022_1D-Restart/"

@dataclasses.dataclass
class PyMCConfig:
    mu_alpha:float = -0.0016
    mu_beta:float = -0.0168
    samples:int = 1000

def load_response_list(cfg:FileConfigMCMC) -> List[List[float]]:
    response_2d_list = []

    for a in cfg.amp:
        out_phase_file = cfg.prefix_1d + cfg.dir_prefix+"/out_o"+str(cfg.curr_omg)+"A"+str(a) \
        +"_ap"+str(cfg.alpha)+".txt"
        curr_obs = D.read_list(out_phase_file)
        response_2d_list.append(curr_obs)

    # Transposing the list
    transposed_list = [[row[i] for row in response_2d_list] for i in range(len(response_2d_list[0]))]

    return transposed_list

def run_pymc(transposed_list:List[List[float]], file_cfg:FileConfigMCMC,
            run_cfg:PyMCConfig) -> Dict[str, float]:
    basic_model = pm.Model()
    a = file_cfg.amp

    with basic_model:

        alpha = pm.Normal('alpha', mu=run_cfg.mu_alpha, sigma=0.1)
        beta = pm.Normal('beta', mu=run_cfg.mu_beta, sigma=0.1)
        sigma = pm.HalfNormal('sigma', sigma=1)

        # One likelihood for each set of repeated measurements
        for i in range(100):
            pm.Normal('response_{}'.format(i), mu=alpha + beta*a, sigma=sigma, observed=transposed_list[i])

        # MCMC sampling
        trace = pm.sample(1000, return_inferencedata=True)

    map_estimate = pm.find_MAP(model=basic_model)
    return map_estimate

if __name__ == '__main__':
    file = FileConfigMCMC()
    run = PyMCConfig()
    res = load_response_list(file)
    estimate = run_pymc(res, file, run)

    print(estimate['sigma'])




