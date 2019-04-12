import math
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import KBinsDiscretizer
import matplotlib.pyplot as plt

def MTF(serie, window_size, num_bin):
    """Compute the Markov Transiiton Field of a time series with sliding windows of size window_size if defined, if not defined one image is created. (Binned using quantiles)
    The approach gives the transition probabilities between the states of the pairwise observations as if the trf. would be happening in one step.
    It also shows probabilites of transition to previous states in one step.

    Parameters
    ------------------------
        serie : list or numpy array
            time series to turn into a transition matrix
       
        window_size :  int
            size of windows of time series to use as input for GASF matrices

        num_bin : int
            number of quantile bins to create (number of states for markov transition probs)

    Returns
    ------------------------
        mtfs : list of numpy matrices of floats
            Markov Transition Field of input series
        
        series_binned : list of np.arrays of floats
            list of arrays of binned series

        serie : np.array
            orginal input array
    """
    if (window_size != None) & (len(serie) < window_size):
        print('Image window size should not exceed the length of the data.')
        return()
    elif window_size == len(serie):
        return MTF_nowindow(serie, num_bin)
    elif window_size != None:
        ## Technical arrays, variables
        serie2 = np.array(serie)
        index_set = np.arange(len(serie2))[:-(window_size-1)]

        mtfs = []
        series_binned = []

        for idx in index_set:
            
            sb, m = MTF_nowindow(serie2[idx:(idx + window_size)], num_bin)
            
            mtfs.append(m)
            series_binned.append(sb)

        return(mtfs, series_binned, serie)
    else:
        print(
            'No window size were defined, therefore the MTF is for the whole input series.')
        return MTF_nowindow(serie, num_bin)



def MTF_new_nowindow(series, num_bin):
    """NOT IN USE NOW. Compute the Markov Transiiton Field of a time series. (Binned using quantiles)
    The approach only shows transitions to present or future states, so it results ina symmetrical matrix.
    The approach give transition probabilities in multiple time steps if needed.

    Parameters
    ------------------------
        series : list or numpy array
            time series to turn into a transition matrix
        
        num_bin : int
            number of quantile bins to create (number of states for markov transition probs)

    Returns
    ------------------------
        X_binned : np.array
            array of binned series

        mtf : numpy matrix
            Markov Transition Field of input series
    """

    mtf = np.eye(len(series))
    X_binned, W = transition_mat(series, num_bin)
    
    for irow, row in enumerate(X_binned):
        for icol, col in enumerate(X_binned[(irow + 1):]):
            mtf[irow, (irow+icol+1)] = mtf[(irow+icol+1), irow] = np.linalg.matrix_power(W, (icol+1))[row, col]
    
    return X_binned, mtf


def transition_mat(series, num_bin):
    """Compute the Markov Transiiton Matrix of a time series. Binned using quantiles.

    Parameters
    ------------------------
        series : list or numpy array
            time series to turn into a transition matrix
        
        num_bin : int
            number of quantile bins to create (number of states for markov transition probs)

    Returns
    ------------------------
        X_binned : numpy array of ints
            binned series (according to quantiles)

        W : numpy matrix
            Markov Transition Matrix of input series
    """
    series = np.array(series).reshape(-1, 1)
    est = KBinsDiscretizer(
        n_bins=num_bin, encode="ordinal", strategy="quantile")
    est.fit(series)
    X_binned = np.array(est.transform(series), dtype=np.int16)
    n = np.int(1 + max(X_binned))  # states labelled as ints from 0

    W = np.zeros((n, n))

    for (i, j) in zip(X_binned, X_binned[1:]):
        W[i, j] += 1

    #make probs
    for idx, rowsum in enumerate(W.sum(axis=1)):
        if rowsum != 0:
            W[idx, :] = W[idx, :]/rowsum

    return X_binned, W


def MTF_nowindow(series, num_bin):
    """Compute the Markov Transiiton Field of a time series. (Binned using quantiles)
    The approach gives the transition probabilities between the states of the pairwise observations as if the trf. would be happening in one step.
    It also shows probabilites of transition to previous states in one step.

    Parameters
    ------------------------
        series : list or numpy array
            time series to turn into a transition matrix
        
        num_bin : int
            number of quantile bins to create (number of states for markov transition probs)

    Returns
    ------------------------
        X_binned : np.array
            array of binned series

        mtf : numpy matrix
            Markov Transition Field of input series
        
    """

    mtf = np.eye(len(series))
    X_binned, W = transition_mat(series, num_bin)

    for irow, row in enumerate(X_binned):
        for icol, col in enumerate(X_binned):
            mtf[irow, icol] = W[row, col]
    return X_binned, mtf

if __name__ == "__main__":
    series = np.random.normal(0, 2.3, 40)
    m, binned, series = MTF(serie = series, window_size = 20, num_bin = 4)
    for img in m:
        plt.imshow(img, cmap = "Greys")
        plt.show()
    
