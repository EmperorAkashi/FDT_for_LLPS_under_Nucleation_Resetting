import numpy as np
import config as cf
from typing import List
import eom_util as E

def langevin_1d(config:cf.Langevin1DConfig) -> None:
    r = 0.0 #1d displacement starts from origin by default
    step = 0
    R_ = config.R # init R_ as R

    while step < config.Nsteps and R_ > 0:
        step += 1
        r = E.trans_r(config.dt, r, config.k, config.gamma, R_, step,
                      config.amp, config.omg)
        u_current = E.u_int(config.k, R_, r)
        u_inter = E.growth_rate(config.R0, config.R1, R_, u_current,
                                config.alpha, config.area, config.epsilon)
