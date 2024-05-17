import dataclasses
from typing import Optional, Tuple, List
import omegaconf

@dataclasses.dataclass
class Langevin1DConfig:
    Nsteps:int = 50000    
    dt:float = 0.1                              
    gamma:float = 10.0
    R_init:float = 1.0
    R_thre:float = 0.2
    c_inf_v:float = 0.1
    c:float = 1.0
    c_eq:float = 0.7
    c_inf:float = 1.0
    alpha:float = 0.2
    gamma_bar:float = 0.1
    omg:float = omegaconf.MISSING 
    amp:float =  omegaconf.MISSING
    disp_path:str = omegaconf.MISSING
    radi_path:str = omegaconf.MISSING
    tau:int = 10
    

@dataclasses.dataclass
class NucleationConfig:
    tau:int = 10
    D:float = 0.83
    k:float = -0.17
    x_0:float = 2.61

@dataclasses.dataclass
class Langevin1DRunConfig:
    omg_list:List[float] = omegaconf.MISSING
    amp_list:List[float] = omegaconf.MISSING
    base_path:str = omegaconf.MISSING
    langevin:Langevin1DConfig = Langevin1DConfig()
    nucleation:NucleationConfig = NucleationConfig()
    num_repeat:int = 1000
