import data_util.data_util_main as D
import data_util.config as cf
import numpy as np
import hydra
import omegaconf
import json

@hydra.main(config_path=None, config_name='response', version_base='1.1' ) 
def main(config: cf.ResponseCalcConfig):
    # Convert OmegaConf to a Python dictionary
    config_dict = omegaconf.OmegaConf.to_container(config, resolve=True)

    # Save the configuration to a JSON file
    with open('response_calc.json', 'w') as f:
        json.dump(config_dict, f, indent=4)

    for o in config.omg_list:
        resp_in = []
        resp_out = []
        for a in config.amp_list:
            curr_file = 'Disk_r-1D-ap' + str(config.alpha)+'-r0Re-Nu' + str(config.tau) + '-' + str(a)+'o'+str(o)+'_ceq'+str(config.c_eq)+'_thre'+str(config.R_thre)+'.txt'
            trj = D.read_2d(curr_file)

            in_phase = []
            out_phase = []
            for i in range(len(trj)):
                in_, out_ = D.fourier_comp(trj[i], o, config.dt)
                in_phase.append(in_)
                out_phase.append(out_)
            np.savetxt('in_o'+str(o)+ 'A'+str(a)+'_ap' + str(config.alpha)+'.txt',in_phase)
            np.savetxt('out_o'+str(o)+ 'A'+str(a)+'_ap' + str(config.alpha)+'.txt',out_phase)
            mu_in = np.mean(in_phase)
            mu_out= np.mean(out_phase)
            resp_in.append(mu_in)
            resp_out.append(mu_out)
            np.savetxt('in_omg'+str(o)+'_ap' + str(config.alpha)+'_list.txt', resp_in)
            np.savetxt('out_omg'+str(o)+'_ap' + str(config.alpha)+'_list.txt', resp_out)

if __name__ == '__main__':
    from hydra.core.config_store import ConfigStore
    cs = ConfigStore()
    cs.store('response', node=cf.ResponseCalcConfig)
    main()

