## By github.com/devitrylouis/imaging_time_series/blob/master/gramian_angular field.py

import math
import numpy as np 
from sklearn.preprocessing import MinMaxScaler
import matplotlib
import matplotlib.pyplot as plt 

# GAF transformation class

def gramian_angular_field(serie):
    """Compute the Gramian Angular Field of an image"""
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

# ## Not sure about this one yet
# def create_time_series(size, time):
#     """Generate time serie of length size and dynamic with respect to time."""
#     # Generating time series
#     support = np.arange(0, size)
#     serie = np.cos(support + float(time))
#     return(t, series)

# gaf, phi, r, scaled_ts = gramian_angular_field(np.array([[1, 2, 4.35, 2, 5]]).reshape(-1,1))

# plt.imshow(gaf, cmap = "Greys")
# plt.imsave('test.png', gaf, dpi=1200, cmap="Greys")
# plt.show()

# print(gaf)
