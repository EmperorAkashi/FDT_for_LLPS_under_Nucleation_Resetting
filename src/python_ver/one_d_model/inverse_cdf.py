import numpy as np
from scipy.integrate import quad
from scipy.interpolate import interp1d
from typing import List

def Berne_FPT(x: float, D: float, x_0: float, k: float):
    "express first passage distribution with quadratic potential"
    x = np.array(x)
    sigma = (1 - np.exp(-2*D*k*x))/k
    return 2*D*np.exp(-D*k*x)*abs(x_0)/np.sqrt(2*np.pi*sigma**3)*np.exp(-(x_0*np.exp(-D*k*x))**2/(2*sigma))

"CDF of Berne numerically"
def CDF_Berne_FPT(x_val:float,D:float, x_0:float, k:float) -> List:
    # Integrate the PDF from 0 to x_val
    result, _ = quad(Berne_FPT, 0, x_val, args=(D, x_0, k))
    return result

x_values = np.linspace(0, 35, 1000)
cdf_values = [CDF_Berne_FPT(x_val) for x_val in x_values]

# Create an interpolation of the inverse CDF
inverse_cdf = interp1d(cdf_values, x_values, fill_value="extrapolate")


def sample_from_Berne_FPT():
    # Generate uniform random samples
    u = np.random.rand()
    # Transform them using the inverse CDF
    return inverse_cdf(u)