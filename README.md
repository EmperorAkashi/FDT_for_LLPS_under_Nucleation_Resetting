# Liquid Liquid Phase Separation (LLPS) under Nucleation Resetting
This repository contains a project exploring the dynamics of liquid–liquid phase separation (LLPS) in a confined, elastic filament system, modeled as a phenomenological homogeneous setup.

The project draws on ideas from nucleation theory, resetting dynamics in active systems, and nonequilibrium statistical mechanics. Key focuses include droplet behavior under thermal fluctuations and mechanical coupling, the effects of stochastic resetting on phase separation, and the examination of fluctuation–dissipation relations (FDR) and large deviation theory (LDT).

We provide Python source code for simulating Langevin dynamics in this complex system (see `python_ver/one_d_model/langevin_dynamics.py` for our convention and implementation). Scripts are also included for data analysis, such as visualization of frequency-domain autocorrelations and MCMC-based Bayesian regression to characterize effective droplet potentials.

Overall, the project aims to connect theoretical principles with computational modeling to better understand LLPS in both biological and physical contexts.

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
