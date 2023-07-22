import numpy as np
import config as cf
from typing import List

def trans_r(dt:float, r:float, k:float, gamma:float, R:float, 
            step:int, A:float, omg:float) -> float:
    """effective 1D translation of the droplet
    where the effective spring constant k_sp = k*4*pi*R_bar^2
    is the proxy of 2D lattice field
    """
    ext_F  = -k*4*np.pi*R**2*r
    stoc_F = np.random.randn()/np.sqrt(dt) *np.sqrt(2*gamma)
    vels = ext_F + 1*stoc_F + A*AC_force(step*dt,omg)
    r += vels*dt/gamma
    return r

def u_int(k:float, R:float, r:float) -> float:
    """effective potential energy of the droplet
    """    
    U = 0.5*np.pi*(4*k*r**2*R**2 + 0.5*k*R**4)
    return U

def growth_rate(R0:float, R1:float, R:float, Uin:float, 
                alpha:float, area:float, epsilon:float) -> float:
    """effective growth rate of the droplet
    args:
    R0: constant chemical potential of infinity reservior
    R1: constant chemical potential of the minority phase
    alpha: constant dewetting parameter
    area: area of the droplet
    epsilon: constant of surface tension
    """
    rate = (1/R)*(R0 - R1*np.exp(alpha*Uin/R**2 + (epsilon*area)/R) + 0*2*np.sqrt(area)*R1*R*np.random.randn())
    return rate

def ac_force(t:float, omega:float) -> float:
    """ac force to test the FDT
    """
    return np.sin(omega*t)

def possion_lag(tau_step:int) -> int:
    """random nucleation time after droplet evaporate
    """
    return -tau_step*np.log(np.random.uniform(0,1))
