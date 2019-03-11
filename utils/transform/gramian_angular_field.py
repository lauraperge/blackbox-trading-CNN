## By github.com/devitrylouis/imaging_time_series/blob/master/gramian_angular field.py

import math
import numpy as np 
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt 

# GAF transformation fct

def gramian_angular_field(serie):
    """Compute the Gramian Angular Field of a time series"""
    # Right Array Type
    serie = np.array([serie]).reshape(-1, 1)

    # Min-Max scaling to [-1, 1] (!)
    scaler = MinMaxScaler(feature_range=(-1, 1), copy=True)
    scaler.fit(serie)
    scaled_serie = scaler.transform(serie)

    # Polar encoding
    phi = np.arccos(scaled_serie)
    # Note: the computation of r is not necessary
    r = np.linspace(0, 1, len(scaled_serie))

    # GAF Computation (every term of the matrix)
    gaf = tabulate(phi, phi, cos_sum)

    return(gaf, phi, r, scaled_serie)


# Tools
def tabulate(x, y, f):
    """Return a table of f(x, y). Useful for Gram-like operations."""
    return( np.vectorize(f)(*np.meshgrid(x, y, sparse = True))) #with vectorize execute function for all combinations, meshgrid to put it in table

def cos_sum(a, b):
    """COS(a + b) to work with tabulate."""
    return(math.cos(a + b))


# gaf, phi, r, scaled_ts = gramian_angular_field([1.4, 32, 36, 4, 15, 2])

# plt.imshow(gaf, cmap = "Greys")
# plt.imsave('test.png', gaf, dpi=1200, cmap="Greys")
# plt.show()

# print(gaf)
