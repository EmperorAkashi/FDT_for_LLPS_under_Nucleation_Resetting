from concurrent.futures import ProcessPoolExecutor
from dataclasses import replace

import data_util.data_util_main as D
import data_util.config as cf
import numpy as np
import hydra
import omegaconf
import json
import glob

import logging

def process_traj_radi(traj_path:str, radi_path, base_cfg:cf.ACFCalcConfig) -> None:
    logger = logging.getLogger(__name__)
    logger.info("current displacement traj: " + traj_path)
    logger.info("current radius traj: " + radi_path)
    logger.debug("Debug level log")

    with ProcessPoolExecutor() as executor:
        futures = []
        for i in range(0, base_cfg.num_trj, base_cfg.batch_size):
            cfg = replace(base_cfg, file_order=i // base_cfg.batch_size,
                          range_min=i, range_max=min(i + base_cfg.batch_size, base_cfg.num_trj))

            futures.append(executor.submit(D.get_cross_corr, traj_path, radi_path, cfg))

        for future in futures:
            future.result()

def concate_avg_cross(config:cf.ACFCalcConfig) -> None:
    # specify all calculated acf via wildcard matching
    pattern = "cross_corr_ap_" + str(config.alpha) + "_*.txt"
    

    file_list = glob.glob(pattern)
    combined_data = []

    # Read data from each file and append to a list
    for filename in sorted(file_list):
        data = np.loadtxt(filename)
        if len(combined_data) == 0:
            combined_data = data # init the data with the first chunk
        else:
            combined_data = np.vstack((combined_data, data))

    combined_data = np.array(combined_data)
    print("check the 2nd dim is : ", len(combined_data[0]))
    np.savetxt("cross_corr_ap"+str(config.alpha)+"_cat.txt", combined_data)

    acf_avg = np.mean(combined_data, axis=0)
    np.savetxt("cross_corr_avg0.0_ap"+str(config.alpha)+"_relx"+str(config.tau)+".txt", acf_avg)

@hydra.main(config_path=None, config_name='acf', version_base='1.1') 
def main(config: cf.ACFCalcConfig):
    print("Hydra run directory:", hydra.utils.get_original_cwd())

    # Convert OmegaConf to a Python dictionary
    config_dict = omegaconf.OmegaConf.to_container(config, resolve=True)
    dataclass_config = cf.ACFCalcConfig(**config_dict)  

    
    json_file = 'cross_corr_calc.json'
    
    # Save the configuration to a JSON file
    with open(json_file, 'w') as f:
        json.dump(config_dict, f, indent=4)

    trj_file = 'Disk_r-1D-ap' + str(config.alpha)+'-r0Re-Nu' + str(config.tau) + '-' + str(0.0)+'o'+str(0.0)+'_ceq'+str(config.c_eq)+'_thre'+str(config.R_thre)+'.txt'
    radi_file = 'Radius-1D-ap' + str(config.alpha)+'-r0Re-Nu' + str(config.tau) + '-' + str(0.0)+'o'+str(0.0)+'_ceq'+str(config.c_eq)+'_thre'+str(config.R_thre)+'.txt'
    
    process_traj_radi(dataclass_config.base_path + trj_file, 
                      dataclass_config.base_path + radi_file,
                      dataclass_config)
    concate_avg_cross(dataclass_config)

if __name__ == '__main__':
    from hydra.core.config_store import ConfigStore
    cs = ConfigStore()
    cs.store('acf', node=cf.ACFCalcConfig)
    main()