import numpy as np
import hydra
import config as cf

@hydra.main(config_path=None, config_name='langevin_1d', version_base='1.1' ) 
def main(config: cf.Langevin1DConfig):
    pass