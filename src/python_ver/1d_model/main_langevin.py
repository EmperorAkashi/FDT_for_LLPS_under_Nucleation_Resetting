import numpy as np
import hydra
import config as cf
import langevin1d as L

@hydra.main(config_path=None, config_name='langevin_1d', version_base='1.1' ) 
def main(config: cf.Langevin1DRun):
    omg_list = config.omg_list
    amp_list = config.amp_list

    for o in omg_list:
        for a in amp_list:
            curr_config = config.langevin
            curr_config.amp = a
            curr_config.omg = o

            L.langevin_1d(curr_config)

if __name__ == '__main__':
    from hydra.core.config_store import ConfigStore
    cs = ConfigStore()
    cs.store('train', node=cf.Langevin1DRun)
    main()