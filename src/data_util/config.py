import dataclasses
from typing import List, Dict

@dataclasses.dataclass
class FittingFileConfig:
    """dataclass to specify the configure to load response files
    """
    alpha:float = 9.2
    curr_omg:float = 0.1
    amp:List[float] = [0.5,0.8,1.0,1.5]
    dir_prefix:str = "1D_9.2_relx200_Rn" #directory's name
    dt:float = 0.01
    fit_range:int = 3
    prefix_1d:str = "C:/Users/linch/Downloads/Diffusion_Elastic/Elastic_Hexagon/2022_1D-Restart/"
