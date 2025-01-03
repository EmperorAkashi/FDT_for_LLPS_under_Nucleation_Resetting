import dataclasses
from typing import List, Dict
import omegaconf

@dataclasses.dataclass
class FittingFileConfig:
    """dataclass to specify the configure to load response files
    """
    alpha:float = 9.2
    curr_omg:float = 0.1
    amp:List[float] = omegaconf.MISSING
    relx:int = 200
    dir_prefix:str = "1D_9.2_relx"+str(relx)+"_Rn" # directory's name
    dt:float = 0.01
    fit_range:int = 3
    prefix_1d:str = "C:/Users/linch/Downloads/Diffusion_Elastic/Elastic_Hexagon/2022_1D-Restart/"

@dataclasses.dataclass
class SeqFittingConfig:
    omg:List[float] = omegaconf.MISSING
    avg_list:bool = False # whether to use averaged reponses for fitting
    sample:int = 1000
    fit_range:int = 3

@dataclasses.dataclass
class ResponseCalcConfig:
    omg_list:List[float] = omegaconf.MISSING
    amp_list:List[float] = omegaconf.MISSING
    dt:float = 0.1
    alpha:float = 0.2
    R_thre:float = 0.1
    tau:int = 10
    c_eq:float = 0.7

@dataclasses.dataclass
class PowerSpecConfig:
    freq_range:List[float] = omegaconf.MISSING
    base_path:str = omegaconf.MISSING
    step:float = 0.5
    dt:float = 0.1
    alpha:float = 0.2
    R_thre:float = 0.1
    tau:int = 10
    c_eq:float = 0.7
    picked_amp:float = 0.5
    intrinsic_omg:float = 0.1

@dataclasses.dataclass
class ACFCalcConfig:
    range_min:int = 0
    range_max:int = 300
    alpha:float = 0.2
    tau:int = 10
    c_eq:float = 0.7
    R_thre:float = 0.1
    file_order:int = 1
    num_trj:int = 1000
    batch_size:int = 100
    file_option:str = "displacement" # the file to be processed, can also be "radius"
    base_path:str = "/u/scratch/l/lin4869/llps_run/outputs/" # default working dir in Hoffman2




