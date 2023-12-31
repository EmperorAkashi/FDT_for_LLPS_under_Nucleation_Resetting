import dataclasses
from typing import List, Dict

@dataclasses.dataclass
class FittingFileConfig:
    """dataclass to specify the configure to load response files
    """
    alpha:float = 9.2
    curr_omg:float = 0.1
    amp:List[float] = [0.5,0.8,1.0,1.5]
    relx:int = 200
    dir_prefix:str = "1D_9.2_relx"+str(relx)+"_Rn" #directory's name
    dt:float = 0.01
    fit_range:int = 3
    prefix_1d:str = "C:/Users/linch/Downloads/Diffusion_Elastic/Elastic_Hexagon/2022_1D-Restart/"

@dataclasses.dataclass
class SeqFittingConfig:
    omg:List[float] = [0.1,0.2,0.5,1.0,2.0,3.0]
    avg_list:bool = False #whether to use averaged reponses for fitting
    sample:int = 1000
    fit_range:int = 3
