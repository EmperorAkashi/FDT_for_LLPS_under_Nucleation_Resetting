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

def process_trajectories(traj_path:str, base_cfg:cf.ACFCCalcConfig) -> None:
    logger = logging.getLogger(__name__)
    logger.info("current acf traj: ", traj_path)
    logger.debug("Debug level log")

    with ProcessPoolExecutor() as executor:
        futures = []
        for i in range(0, base_cfg.num_trj, base_cfg.batch_size):
            cfg = replace(base_cfg, file_order=i // base_cfg.batch_size,
                          range_min=i, range_max=min(i + base_cfg.batch_size, base_cfg.num_trj))

            futures.append(executor.submit(D.get_acf, traj_path, cfg))

        for future in futures:
            future.result()

def concatenation_avg(config:cf.ACFCCalcConfig) -> None:
    # specify all calculated acf via wildcard matching
    if config.file_option == "displacement":
        pattern = "acf_list_ap_" + str(config.alpha) + "_*.txt"
    else:
        pattern = "radius_acf_list_ap_" + str(config.alpha) + "_*.txt"

    file_list = glob.glob(pattern)
    combined_data = []

    # Read data from each file and append to a list
    for filename in sorted(file_list):
        data = np.loadtxt(filename)
        if not combined_data:
            combined_data = data # init the data with the first chunk
        else:
            combined_data = np.vstack((combined_data, data))

    combined_data = np.array(combined_data)
    print("check the 3rd dim is : ", len(combined_data[0][0]))
    np.savetxt("acf_ap"+str(config.alpha)+"_cat.txt", combined_data)

    acf_avg = np.mean(combined_data, axis=0)
    np.savetxt("acf_avg_ap"+str(config.alpha)+".txt", acf_avg)


@hydra.main(config_path=None, config_name='acf', version_base='1.1' ) 
def main(config: cf.ACFCCalcConfig):
    print("Hydra run directory:", hydra.utils.get_original_cwd())

    # Convert OmegaConf to a Python dictionary
    config_dict = omegaconf.OmegaConf.to_container(config, resolve=True)
    dataclass_config = cf.ACFCCalcConfig(**config_dict)  

    if config.file_option == "displacement":
        json_file = 'acf_calc.json'
    else:
        json_file = 'acf_calc_radi.json'
    # Save the configuration to a JSON file
    with open(json_file, 'w') as f:
        json.dump(config_dict, f, indent=4)

    if config.file_option == "displacement":
        file = 'Disk_r-1D-ap' + str(config.alpha)+'-r0Re-Nu' + str(config.tau) + '-' + str(0.0)+'o'+str(0.0)+'_ceq'+str(config.c_eq)+'_thre'+str(config.R_thre)+'.txt'
    else:
        file = 'Radius-1D-ap' + str(config.alpha)+'-r0Re-Nu' + str(config.tau) + '-' + str(0.0)+'o'+str(0.0)+'_ceq'+str(config.c_eq)+'_thre'+str(config.R_thre)+'.txt'
    process_trajectories(file, dataclass_config)
    concatenation_avg(dataclass_config)

if __name__ == '__main__':
    from hydra.core.config_store import ConfigStore
    cs = ConfigStore()
    cs.store('acf', node=cf.ACFCCalcConfig)
    main()


