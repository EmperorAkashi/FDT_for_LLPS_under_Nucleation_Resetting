import numpy as np
import python_ver.one_d_model.config as cf
from typing import List
import python_ver.one_d_model.eom_util as E

def langevin_1d(config:cf.Langevin1DConfig) -> None:
    r = 0.0 # 1d displacement starts from origin by default
    step = 0
    R_curr = config.R_init # init R_ as R
    nucleation = E.PoissonTime(config.tau)
    disp_path = config.disp_path
    radi_path = config.radi_path

    file_disp = open(disp_path, 'a')
    file_radi = open(radi_path, 'a')

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

            for _ in range(t_cutoff):
                file_disp.write(str(0) + " ")
                file_radi.write(str(0) + " ")

            step += t_cutoff

        file_disp.write(str(r) + " ")
        file_radi.write(str(R_curr) + " ")

    file_disp.write("\n")
    file_disp.close()
    file_radi.write("\n")
    file_radi.close()

            
