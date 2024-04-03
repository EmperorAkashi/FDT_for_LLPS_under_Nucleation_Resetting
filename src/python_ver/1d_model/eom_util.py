import numpy as np
import config as cf
from typing import List
from abc import ABC, abstractmethod
from enum import Enum
import inverse_cdf as CDF


class NucleationOption(Enum):
    poisson, berne_fpt = 1, 2

class NucleationTime(ABC):
    @abstractmethod
    def get_distri(step:int) -> int:
        pass 

class PoissonTime(NucleationTime):
    def get_distri(tau_step:int) -> int:
        """random nucleation time after droplet evaporate
        """
        return int(-tau_step*np.log(np.random.uniform(0,1)))
    
class BerneFPT_Quad(NucleationTime):
    def get_distri(D:float, k:float, x_0:float) -> int:
        return int(CDF.sample_from_Berne_FPT())


def trans_r(dt:float, r:float, alpha:float, c:float, c_inf_v:float, 
            R:float, step:int, A:float, omg:float) -> float:
    """effective 1D translation of the droplet
    here we use dimensonless units based on the molecular length
    """
    ext_F  = -(1/c_inf_v)*(4/3)*np.pi*alpha*2*c*R**3*r
    stoc_F = np.random.randn()/np.sqrt(dt)*np.sqrt(2)
    vels = ext_F + stoc_F + A*ac_force(step*dt, omg)
    r += vels*dt
    return r

def u_int(c:float, R:float, r:float) -> float:
    """effective potential energy of the droplet
    """    
    u = R**2 + c*r**2
    return u

def growth_rate(c_eq:float, c_inf:float, R:float, u_in:float, 
                alpha:float) -> float:
    """effective growth rate of the droplet
    args:
    c_inf: constant chemical potential of infinity reservior
    c_eq: constant chemical potential of the minority phase
    alpha: constant dewetting parameter
    notice:
    here we do not have a surface tension, the effect of surface tension
    will be modeled as a hitting boundaray
    """
    rate = (1/R)*(1 - (c_eq/c_inf)*np.exp(alpha*u_in)) + (1/2*np.pi*R**3)*(c_eq/c_inf)*np.random.randn()
    return rate

def ac_force(t:float, omega:float) -> float:
    """ac force to test the FDT
    """
    return np.sin(omega*t)


