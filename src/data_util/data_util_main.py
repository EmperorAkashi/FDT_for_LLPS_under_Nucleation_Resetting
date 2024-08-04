import numpy as np
import matplotlib.pylab as plt
from scipy.optimize import leastsq

from typing import List, Tuple
import data_util.config as cf

"Can be used to read a 1d list, such as r^2, potential energy et.al."
def read_list(file:str) -> List[float]:
    with open(file) as f:
        lines = f.readlines()
    print(len(lines))
    str_row = []
    for i in range(len(lines)):
        row = lines[i].strip()
        str_row.append(row)
    trj = [float(i) for i in str_row]
    return trj

"Can be used to analyze 2d list, such as Gaussians and disk's coord"
def read_2d(file:str) -> List[List[float]]:
    with open(file) as f:
        lines = f.readlines()
    str_row = []
    for i in range(len(lines)):
        row = lines[i].strip().split()
        str_row.append(row)

    trj = []
    for i in range(len(str_row)):
        coord = [float(j) for j in str_row[i]]
        trj.append(coord)
    
    return trj

"convert a 1D list to a str (for file saving purpose)"
def float_to_str(curr_list:List[float]) -> str:
    ans = ""
    
    for f in curr_list:
        ans += str(f) + " "
        
    return ans + "\n"

"process files into a 2D list of string"
def read_single_file_str(filename:str) -> List[List[str]]:
    with open (filename) as f:
        lines = f.readlines()
    trj = []
    for s in lines:
        r = s.strip().split()
        trj.append(r)
    return trj

"extract the coordinates of top row of Gaussian bumps"
def read_drop_file(filename:str) -> List[List[str]]:
    with open (filename) as f:
        lines = f.readlines()
    trj = []
    for s in lines:
        r = s.strip().split()
        trj.append(r)
    interval = int(trj[0][0])
    head_line = 2
    total = len(trj)
    num = total//(interval + head_line)
    top = []
    for step in range(0, total, (interval+head_line)):
        x_drop = float(trj[step+37+head_line][1])
        top.append(x_drop)   
    return top

def death_timestamp(trj:List[float]) -> List[float]:
    """
    @brief: record all death events' timestamps
    @args:
    trj: a single list of time series of radius or 1d displacemnt
    i.e. a 1D list
    """
    hit = []
    iter_ = 0
    while iter_ < len(trj):
        if trj[iter_] == 0:
            hit.append(iter_)
            while trj[iter_] == 0 and iter_ < len(trj) - 1:
                iter_ += 1
            hit.append(iter_)
        iter_ += 1
    return hit

def life_period(hit_list:List[float]) -> List[float]:
    """
    hit_list: list of passage time spot processed by death_t
    """
    fpt = []
    hit_list.insert(0,0)
    for i in range(0,len(hit_list)-1,2):
        fpt.append(hit_list[i+1]-hit_list[i])
    return fpt

def get_all_life_t(trj_2d:List[List[float]]) -> List[float]:
    """@return: and ensemble of life time of a list of trajectories 
    """
    life_ensemble = []
    for t in trj_2d:
        curr = death_timestamp(t)
        life = life_period(curr)
        life_ensemble += life

    return life_ensemble

def get_fpt_hist(life_ensemble:List[float],
                bin_num:int, range_min:int, range_max:int) -> Tuple[List[float],List[float]]:
    """@return: discrete x-axis from mid of bins; normalized pdf
    """
    n, bins, patch = plt.hist(life_ensemble, bins = bin_num, range = [range_min, range_max])
    #here 200 is picking mid of each bin and 100 is the predefined timestep size 
    bin_mid = [(bins[i] + bins[i+1])/200 for i in range(len(bins) - 1)]
    total_count = np.sum(n)
    pdf = n / total_count

    return bin_mid, pdf

def fourier_comp(trj:np.ndarray, omega:float, dt:float) -> Tuple[float, float]:
    """@brief: calculate in phase&out phase of a time series
    here we refer to the 1D displacement of the simulated trajectory
    """
    in_phase = 0
    out_phase = 0

    for i in range(len(trj)):
        in_phase += trj[i]*np.sin(omega*i*dt)*2/len(trj)
        out_phase += trj[i]*np.cos(omega*i*dt)*2/len(trj)
    return in_phase, out_phase

def get_acf(trj_path:str, cfg:cf.ACFCCalcConfig) -> None:
    trj_batch = read_2d(trj_path)[cfg.range_min:cfg.range_max]
    m = len(trj_batch)

    if cfg.file_option == "displacement":
        output = 'acf_list' + "_" + "ap_" + str(cfg.alpha) + "_" + str(cfg.file_order) + ".txt"
    else:
        output = 'radi_acf_list' + "_" + "ap_" + str(cfg.alpha) + "_" + str(cfg.file_order) + ".txt"


    f = open(output, 'w+')

    for i in range(m):
        trj_i = trj_batch[i]
        acf_i = auto_corr(trj_i)
        f.write(float_to_str(acf_i))
    f.close()


def auto_corr(x:List[float]) -> List[float]:
    corr = []
    m = np.mean(x)

    for i in range(len(x) - 1):
        prod = []
        for j in range(len(x) - i):
            prod.append(x[j]*x[j+i] - m**2)
        avg = np.mean(prod)
        corr.append(avg)
    return corr
