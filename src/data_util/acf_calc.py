import data_util.data_util_main as D
import data_util.config as cf
import numpy as np
import hydra
import omegaconf
import json

@hydra.main(config_path=None, config_name='acf', version_base='1.1' ) 
def main(config: cf.ACFCalcConfig):
    # Convert OmegaConf to a Python dictionary
    config_dict = omegaconf.OmegaConf.to_container(config, resolve=True)

    # Save the configuration to a JSON file
    with open('acf_calc.json', 'w') as f:
        json.dump(config_dict, f, indent=4)

    file = 'Disk_r-1D-ap' + str(config.alpha)+'-r0Re-Nu' + str(config.tau) + '-' + str(0.0)+'o'+str(0.0)+'_ceq'+str(config.c_eq)+'_thre'+str(config.R_thre)+'.txt'
    D.get_acf(file, config)

if __name__ == '__main__':
    from hydra.core.config_store import ConfigStore
    cs = ConfigStore()
    cs.store('acf', node=cf.ACFCalcConfig)
    main()

    