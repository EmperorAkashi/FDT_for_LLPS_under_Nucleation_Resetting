import data_util.data_util_main as D
import data_util.config as cf
import numpy as np
import hydra
import omegaconf
import json

@hydra.main(config_path=None, config_name='power_spec', version_base='1.1' ) 
def main(config: cf.PowerSpecConfig):
    # Convert OmegaConf to a Python dictionary
    config_dict = omegaconf.OmegaConf.to_container(config, resolve=True)

    # Save the configuration to a JSON file
    with open('power_spec.json', 'w') as f:
        json.dump(config_dict, f, indent=4)

    trj_path = config.base_path + "alpha" + str(config.alpha) + "_tau" + str(config.tau) + "_drive/"
    trj_file = (
        trj_path + "Disk_r-1D-ap" + str(config.alpha) + "-r0Re-Nu" +
        str(config.tau) + "-" + str(config.picked_amp) + "o" +
        str(config.intrinsic_omg) + "_ceq0.7_thre0.2.txt"
    )
    
    powers = D.all_powers(trj_file, config.freq_range, config.step, config.dt)
    np.savetxt('power_spec_omg'+str(intrinsic_omg)+'_ap' + str(config.alpha)+'_list.txt', powers)

    

if __name__ == '__main__':
    from hydra.core.config_store import ConfigStore
    cs = ConfigStore()
    cs.store('power_spec', node=cf.PowerSpecConfig)
    main()

