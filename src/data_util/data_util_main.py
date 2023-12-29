import numpy as np
import matplotlib.pylab as plt
from scipy.optimize import leastsq

from typing import List

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

def death_t(trj:List[List[float]]) -> List[float]:
    """
    trj: list of time series of radius or 1d displacemnt
    i.e. overall a 2D list
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

def life_t(hit_list:List[float]) -> List[float]:
    """
    hit_list: list of passage time spot processed by death_t
    """
    fpt = []
    hit_list.insert(0,0)
    for i in range(0,len(hit_list)-1,2):
        fpt.append(hit_list[i+1]-hit_list[i])
    return fpt