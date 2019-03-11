import math
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform

# Recurrence Plot transformation funtion


def recurrence_plot(serie):
    """Compute the Recurrence Plot of a time series"""
    # 2D phase space trajectories (s)
    new_serie = np.transpose(np.array((serie[:-1], serie[1:])))
    
    # R matrix: distances between pairs - NO THRESHOLDING
    distances = squareform(pdist(new_serie, 'euclidean'))

    return(distances)

# RP_mat = recurrence_plot([1.4,32,36,4, 15, 2])
# print(RP_mat)
# plt.imshow(RP_mat, cmap="Greys")
# plt.show()

# plt.imsave('test.png', RP_mat, dpi=1200, cmap="Greys")
