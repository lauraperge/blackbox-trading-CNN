import math
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform

# Recurrence Plot for various windows in time series
def RP(serie, window_size = None, padding = 0, standardize_out = False):
    """ Compute the Recurrence Plot of a time series (for each sliding window defined by window_size).
   
    Parameters
    -------------------------
        serie : np.array or list

        window_size:  (default = None) int
            size of windows of time series to use as input for GADF matrices

        padding : int (default = 0)
            number of rows/columns of zero padding to be added to the right and bottom

        standardize_out : bool (default = False)
            whether the resulting image should be standardized between 0 and 1 (minmax scaler)
    
    Returns
    --------------------------
        recurrence_plots :  list of matrices
            recurrence plot for each window

        serie : original input series
    """
    if window_size != None:
        if len(serie) < window_size:
            print('Image window size should not exceed the length of the data.')
            return()
        elif window_size == len(serie):
            return recurrence_plot_nowindow(serie, padding=padding, standardize_out=standardize_out)
        else:
    
            ## Technical arrays, variables
            serie2 = np.array(serie)
            index_set = np.arange(len(serie2))[:-(window_size-1)]

            recurrence_plots = []

            for idx in index_set:
                rp, os = recurrence_plot_nowindow(
                    serie2[idx:(idx + window_size)], padding=padding, standardize_out=standardize_out)

                recurrence_plots.append(rp)

            return(recurrence_plots, serie)
    else:
        print(
            'No window size were defined, therefore the GASF is for the whole input series.')
        return recurrence_plot_nowindow(serie, padding = padding , standardize_out=standardize_out)

# Recurrence Plot transformation funtion
def recurrence_plot_nowindow(serie, padding = 0, standardize_out = False):
    """Compute the Recurrence Plot of a time series (for the full input).
    
    Parameters
    ---------------------
        serie : np.array or list

        padding : int (Default = 0)
            number of rows/columns of zero padding to be added to the right and bottom
        
        standardize_out : bool (default = False)
            whether the resulting image should be standardized between 0 and 1 (minmax scaler)

    Returns
    ---------------------
        distances : recurrence plot

        serie : original input series

    """
    # 2D phase space trajectories (s)
    new_serie = np.transpose(np.array((serie[:-1], serie[1:])))
    
    # R matrix: distances between pairs - NO THRESHOLDING
    distances = squareform(pdist(new_serie, 'euclidean'))

    if standardize_out == True:
        scaler = MinMaxScaler(feature_range=(0, 1), copy=True)
        scaler.fit(distances)
        distances = scaler.transform(distances)

        # Fixing floating point inaccuracy
        distances = np.where(distances >= 1., 1., distances)
        distances = np.where(distances <= 0., 0., distances)

    if padding >= 0:
        distances2 = np.zeros((distances.shape[0]+padding,distances.shape[0]+padding))
        distances2[:-1,:-1] = distances

    return(distances2, serie)


if __name__ == "__main__":
    
    RP_mat, ser = RP([1.4,32,36,4, 15, 2], 4, padding = 1, standardize_out=True)
    print(RP_mat)
    for i in RP_mat:
        plt.imshow(i, cmap="Greys")
        plt.show()

    plt.imsave('test.png', RP_mat, dpi=1200, cmap="Greys")
