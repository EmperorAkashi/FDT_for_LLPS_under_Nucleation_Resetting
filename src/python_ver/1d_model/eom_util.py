import numpy as np
import config as cf
from typing import List
from abc import ABC, abstractmethod
from enum import Enum
import inverse_cdf as CDF


class NucleationOption(Enum):
    poisson, berne_fpt = 1, 2

class NucleationTime(ABC):
    """@brief:
    the abstract class of random number generator
    of different type of re-nucleation time
    """
    @abstractmethod
    def get_distri(self, step:int) -> int:
        pass 

class PoissonTime(NucleationTime):
    def __init__(self, tau_step:int) -> None:
        self.tau = tau_step

    def get_distri(self) -> int:
        """random nucleation time after droplet evaporate
        """
        return int(-self.tau*np.log(np.random.uniform(0,1)))
    
class BerneFPT_Quad(NucleationTime):
    def get_distri(D:float, k:float, x_0:float) -> int:
        return int(CDF.sample_from_Berne_FPT())


def trans_r(dt:float, r:float, alpha:float, c:float, 
            R:float, step:int, A:float, omg:float, gamma:float) -> float:
    """@brief: effective 1D translation of the droplet
    here we use dimensonless units based on the molecular length
    @args:
    alpha: dewetting parameter which indicate the coupling strength 
    between droplet and filaments
    gamma: friction coefficient
    c: prefactor for displacement in the effective potential energy
    omg, A: frequency & amplitude for the extra driving force
    """
    ext_F  = -(8/3)*np.pi*alpha*c*R**3*r
    stoc_F = np.random.randn()/np.sqrt(dt)*np.sqrt(2*gamma)
    vels = (ext_F + stoc_F + A*ac_force(step*dt, omg))/gamma
    r += vels*dt
    return r

def u_int(c:float, R:float, r:float) -> float:
    """effective potential energy of the droplet
    """    
    u = R**2 + c*r**2
    return u

def growth_rate(c_eq:float, c_inf:float, R:float, u_in:float, 
                alpha:float, gamma_bar:float, c_inf_v:float) -> float:
    """effective growth rate of the droplet
    args:
    c_inf: constant chemical potential of infinity reservior
    c_eq: constant chemical potential of the minority phase
    alpha: constant dewetting parameter
    notice:
    gamma_bar: effective surface tension
    c_inf_v: reduced prefactor of c_inf*v, where v is the volume density
    """
    rate = (c_inf_v/R)*(1 - (c_eq/c_inf)*(np.exp(alpha*u_in + gamma_bar/R))) + (1/(2*np.pi*R**3))*(c_inf_v)*np.random.randn()
    return rate

def ac_force(t:float, omega:float) -> float:
    """ac force to test the FDT
    """
    return np.sin(omega*t)


