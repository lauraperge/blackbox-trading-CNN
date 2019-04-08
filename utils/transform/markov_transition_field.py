import math
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from pyts.image import MarkovTransitionField as MTF

# Markov Transition Field Transformation
# def MTF(serie, window_size=None):
#     """Compute the Markov Transiiton Field of a time series with sliding windows of size window_size if defined, if not defined one image is created.
    
#     Parameters
#     ------------------------
#         serie : list or numpy array
#             time series to turn into GASF matrices

#         window_size :  int
#             size of windows of time series to use as input for GASF matrices

#     Returns
#     ------------------------
#         mtfs : list of matrices of floats
#             matrices of transformed values for each window (GASF matrix)

#         phis : list of np.arrays of floats
#             arrays of angles in windows (transformed from windows in series)
        
#         r : list of arrays of ints
#             radiuses
        
#         scaled_serie : list of array of floats
#             input series after scaling in each window

#         serie: np.array
#             original input serie (reshaped)
#     """

def transition_mat(X_binned):
    n = 1 + max(X_binned) # states labelled as ints from 0

    M = np.zeros((n,n))

    for (i,j) in zip(X_binned, X_binned[1:]):
        M[i, j] += 1
    print(M)
    #make probs
    for idx, rowsum in enumerate(M.sum(axis=1)):
        if rowsum != 0:
            M[idx, :] = M[idx, :]/rowsum
    
    return M


if __name__ == "__main__":
    bins = [0, 1, 2, 3, 2, 0, 0, 0, 3, 2, 1, 2, 3, 1, 1, 1,
            2, 2, 0, 2, 3, 3, 1, 2, 0, 1, 3, 2, 1, 2, 0, 1, 3, 2]
    m = transition_mat(bins)
    print(m)
    print(np.matmul(m,m))
    
