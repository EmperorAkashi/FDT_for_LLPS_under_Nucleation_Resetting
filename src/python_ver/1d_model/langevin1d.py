import numpy as np
import config as cf
from typing import List
import eom_util as E

def langevin_1d(config:cf.Langevin1DConfig) -> None:
    r = 0.0 # 1d displacement starts from origin by default
    step = 0
    R_curr = config.R_init # init R_ as R
    nucleation = E.PoissonTime(config.tau)

    while step < config.Nsteps and R_curr > config.R_thre:
        step += 1
        r = E.trans_r(config.dt, r, config.alpha, config.c, 
                      R_curr, step,
                      config.amp, config.omg, config.gamma)
        
        u_current = E.u_int(config.c, R_curr, r)

        rate = E.growth_rate(config.c_eq, config.c_inf, R_curr, u_current,
                             config.alpha, config.gamma_bar, 
                             config.c_inf_v)
        
        R_curr += rate

        if R_curr < config.R_thre:
            R_curr = config.R_thre
            r = 0
            t_relx = int(nucleation.get_distri())

            t_cutoff = min(config.Nsteps - step, t_relx)

            
