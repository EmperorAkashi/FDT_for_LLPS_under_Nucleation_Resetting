import dataclasses
from typing import Optional, Tuple, List
import omegaconf

@dataclasses.dataclass
class Langevin1DConfig:
    Nsteps:int = 50000    
    dt:float = 0.01                              
    U0:float = 3.0                         
    Sigma:float = 3.0
    gamma:float = 1.5
    k:float = 0.017          #spring for the naived harmonic potential
    R:float = 1.0
    R1:float = 0.08
    R0:float = 0.8
    alpha:float = 5.0
    area:float = 0.3,
    epsilon:float = 0.00
    omg:float = omegaconf.MISSING 
    amp:float =  omegaconf.MISSING
    relx_t:int = 100

class Langevin1DRun:
    omg_list:List[float] = omegaconf.MISSING
    amp_list:List[float] = omegaconf.MISSING
    langevin:Langevin1DConfig = Langevin1DConfig()
