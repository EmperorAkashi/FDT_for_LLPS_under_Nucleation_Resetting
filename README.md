# Liquid Liquid Phase Separation (LLPS) under Nucleation Resetting
This repository hosts a project focused on exploring the dynamics of liquid-liquid phase separation (LLPS) in an elastic filament-confined system. 
The project integrates concepts from nucleation theory, resetting processes in active systems, and non-equilibrium statistical mechanics. 
Key aspects include the study of droplet behaviors under thermal fluctuations, the impact of resetting dynamics on phase separation, and the analysis of fluctuation-dissipation relations (FDR) and large deviation theory (LDT). 
We offer both C++ and Python source codes for the productive run of Langevin dynamics, addressing our complex system. 
The repository also features Python scripts for data analysis, including visualization of autocorrelation functions in frequency domains, and the application of MCMC Bayesian regression to understand droplet dynamics in an effective potential context. 
The project aims to bridge theoretical concepts with computational modeling to deepen the understanding of LLPS in biological and physical systems.

# Get started
### Installation of our custom package
if you are on UCLA's Hoffman2, you need to load the anaconda interactively first:

`module load anaconda3`

then creating a virtual environment, i.e.

`conda create -n env_name` 

in your terminal. Then activate the environment via:

`conda activate env_name`

In the environment, first, install our package:

`pip install -e .`
