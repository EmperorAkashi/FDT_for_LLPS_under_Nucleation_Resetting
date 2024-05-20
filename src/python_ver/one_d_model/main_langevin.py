import numpy as np
import hydra
import json
import omegaconf

import python_ver.one_d_model.config as cf
import python_ver.one_d_model.langevin1d as L

@hydra.main(config_path=None, config_name='langevin_1d', version_base='1.1' ) 
def main(config: cf.Langevin1DRunConfig):
    # Convert OmegaConf to a Python dictionary
    config_dict = omegaconf.OmegaConf.to_container(config, resolve=True)

    # Save the configuration to a JSON file
    with open('langevin.json', 'w') as f:
        json.dump(config_dict, f, indent=4)

    omg_list = config.omg_list
    amp_list = config.amp_list
    # we keep the net for loop call of the main langevin function
    # as we want to keep the recorded yaml file with all frequencies & amplitute 
    # used in a single batch of simulation
    for o in omg_list:
        for a in amp_list:
            curr_config = config.langevin
            curr_config.amp = a
            curr_config.omg = o

            disp_path = config.base_path + \
            'Disk_r-1D-ap' + str(curr_config.alpha)+'-r0Re-Nu' + str(curr_config.tau) + '-' + str(curr_config.amp)+'o'+str(curr_config.omg)+'_ceq'+str(curr_config.c_eq)+'_thre'+str(curr_config.R_thre)+'.txt'
            radi_path = config.base_path + \
            'Radius-1D-ap' + str(curr_config.alpha)+'-r0Re-Nu' + str(curr_config.tau) + '-' + str(curr_config.amp)+'o'+str(curr_config.omg)+'_ceq'+str(curr_config.c_eq)+'_thre'+str(curr_config.R_thre)+'.txt'

            curr_config.disp_path = disp_path
            curr_config.radi_path = radi_path

            for _ in range(config.num_repeat):
                L.langevin_1d(curr_config)

if __name__ == '__main__':
    from hydra.core.config_store import ConfigStore
    cs = ConfigStore()
    cs.store('langevin_1d', node=cf.Langevin1DRunConfig)
    main()