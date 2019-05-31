## By github.com/devitrylouis/imaging_time_series/blob/master/gramian_angular field.py

import math
import numpy as np 
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt 

# Gramian Angular Summation Field transformation for various window size in time series
def GASF(serie, window_size=None, standardize_out = False):
    """Compute the Gramian Angular Summation Field of a time series with sliding windows of size window_size if defined, if not defined one image is created.
    
    Parameters
    ------------------------
        serie : list or numpy array
            time series to turn into GASF matrices

        window_size :  int
            size of windows of time series to use as input for GASF matrices

        standardize_out : bool (default = False)
            whether the resulting image should be standardized between 0 and 1 (minmax scaler)

    Returns
    ------------------------
        gasfs : list of matrices of floats
            matrices of transformed values for each window (GASF matrix)

        phis : list of np.arrays of floats
            arrays of angles in windows (transformed from windows in series)
        
        r : list of arrays of ints
            radiuses
        
        scaled_serie : list of array of floats
            input series after scaling in each window

        serie: np.array
            original input serie (reshaped)
    """

    if (window_size != None) & (len(serie) < window_size):
        print('Image window size should not exceed the length of the data.')
        return()
    elif window_size == len(serie):
        return GASF_nowindow(serie, standardize_out=standardize_out)
    elif window_size != None:
        ## Technical arrays, variables
        serie2 = np.array(serie)
        index_set = np.arange(len(serie2))[:-(window_size-1)]

        gasfs = []
        phis = []
        rs = []
        scaled_series = []

        for idx in index_set:
            g, p, r, ss, ser = GASF_nowindow(
                serie2[idx:(idx + window_size)], standardize_out=standardize_out)
            gasfs.append(g)
            phis.append(p)
            rs.append(r)
            scaled_series.append(ss)
        
        return(gasfs, phis, rs, scaled_series, serie)
    else:
        print('No window size were defined, therefore the GASF is for the whole input series.')
        return GASF_nowindow(serie, standardize_out=standardize_out)

# Gramian Angular Summation Field transformation (for entire input series)
def GASF_nowindow(serie, standardize_out = False):
    """Compute the Gramian Angular Summation Field of a time series (no PAA smoothing)
    
    Parameters
    ------------------------
        serie : list or numpy array
            time series to turn into GASF
        
         standardize_out : bool (default = False)
            whether the resulting image should be standardized between 0 and 1 (minmax scaler)
    
    Returns
    ------------------------
        gasf :  matrix of floats
            matrix of transformed values (GASF matrix)

        phi : np.array of floats
            array of angles (transformed from series)
        
        r : array of ints
            radius
        
        scaled_serie : array of floats
            input series after scaling

        serie: np.array
            original input serie (reshaped)
    """
    # Right Array Type
    serie = np.array([serie]).reshape(-1, 1)

    # Min-Max scaling to [-1, 1] (!)
    scaler = MinMaxScaler(feature_range=(-1, 1), copy=True)
    scaler.fit(serie)
    scaled_serie = scaler.transform(serie)

    # Fixing floating point inaccuracy
    scaled_serie = np.where(scaled_serie >= 1., 1., scaled_serie)
    scaled_serie = np.where(scaled_serie <= -1., -1., scaled_serie)

    # Polar encoding
    phi = np.arccos(scaled_serie)
    # Note: the computation of r is not necessary
    r = np.linspace(0, 1, len(scaled_serie))

    # GAF Computation (every term of the matrix)
    gasf = tabulate(phi, phi, cos_sum)

    if standardize_out == True:
        scaler = MinMaxScaler(feature_range=(0, 1), copy=True)
        scaler.fit(gasf)
        gasf = scaler.transform(gasf)

        # Fixing floating point inaccuracy
        gasf = np.where(gasf >= 1., 1., gasf)
        gasf = np.where(gasf <= 0., 0., gasf)

    return(gasf, phi, r, scaled_serie, serie)



# Gramian Angular Difference Field transformation for various window size in time series
def GADF(serie, window_size=None, standardize_out = False):
    """Compute the Gramian Angular Difference Field of a time series with sliding windows of size window_size if defined, if not defined one image is created.
    
    Parameters
    ------------------------
        serie : list or numpy array
            time series to turn into GADF matrices

        window_size :  int
            size of windows of time series to use as input for GADF matrices
        
         standardize_out : bool (default = False)
            whether the resulting image should be standardized between 0 and 1 (minmax scaler)

    Returns
    ------------------------
        gasfs : list of matrices of floats
            matrices of transformed values for each window (GADF matrix)

        phis : list of np.arrays of floats
            arrays of angles in windows (transformed from windows in series)
        
        r : list of arrays of ints
            radiuses
        
        scaled_serie : list of array of floats
            input series after scaling in each window

        serie: np.array
            original input serie (reshaped)
    """

    if (window_size != None) & (len(serie) < window_size):
        print('Image window size should not exceed the length of the data.')
        return()
    elif window_size == len(serie):
        return GADF_nowindow(serie, standardize_out=standardize_out)
    elif window_size != None:
        ## Technical arrays, variables
        serie2 = np.array(serie)
        index_set = np.arange(len(serie2))[:-(window_size-1)]
        
        gadfs = []
        phis = []
        rs = []
        scaled_series = []

        for idx in index_set:
            g, p, r, ss, ser = GADF_nowindow(
                serie2[idx:(idx + window_size)], standardize_out=standardize_out)
            gadfs.append(g)
            phis.append(p)
            rs.append(r)
            scaled_series.append(ss)

        return(gadfs, phis, rs, scaled_series, serie)
    else:
        print(
            'No window size were defined, therefore the GASF is for the whole input series.')
        return GADF_nowindow(serie, standardize_out=standardize_out)

# Gramian Angular Difference Field transformation (for entire input series)
def GADF_nowindow(serie, standardize_out = False):
    """Compute the Gramian Angular Difference Field of a time series (no PAA smoothing)

    Parameters
    ------------------------
        serie : list or numpy array
            time series to turn into GADF
        
         standardize_out : bool (default = False)
            whether the resulting image should be standardized between 0 and 1 (minmax scaler)
    
    Returns
    ------------------------
        gadf :  matrix of floats
            matrix of transformed values (GADF matrix)

        phi : np.array of floats
            array of angles (transformed from series)
        
        r : array of ints
            radius
        
        scaled_serie : array of floats
            input series after scaling

        serie: np.array
            original input serie (reshaped)
    
    """
    # Right Array Type
    serie = np.array([serie]).reshape(-1, 1)

    # Min-Max scaling to [-1, 1] (!)
    scaler = MinMaxScaler(feature_range=(-1, 1), copy=True)
    scaler.fit(serie)
    scaled_serie = scaler.transform(serie)

    # Fixing floating point inaccuracy
    scaled_serie = np.where(scaled_serie >= 1., 1., scaled_serie)
    scaled_serie = np.where(scaled_serie <= -1., -1., scaled_serie)

    # Polar encoding
    phi = np.arccos(scaled_serie)
    # Note: the computation of r is not necessary
    r = np.linspace(0, 1, len(scaled_serie))

    # GAF Computation (every term of the matrix)
    gadf = tabulate(phi, phi, sin_diff)

    if standardize_out == True:
        scaler = MinMaxScaler(feature_range=(0, 1), copy=True)
        scaler.fit(gadf)
        gadf = scaler.transform(gadf)

        # Fixing floating point inaccuracy
        gadf = np.where(gadf >= 1., 1., gadf)
        gadf = np.where(gadf <= 0., 0., gadf)

    return(gadf, phi, r, scaled_serie, serie)


# Tools
def tabulate(x, y, f):
    """Return a table of f(x, y). Useful for Gram-like operations."""
    return( np.vectorize(f)(*np.meshgrid(x, y, sparse = True))) #with vectorize execute function for all combinations, meshgrid to put it in table

def cos_sum(a, b):
    """COS(a + b) to work with tabulate."""
    return(math.cos(a + b))

def sin_diff(a, b):
    """SIN(a-b) to work with tabulate"""
    return(math.sin(a - b))


if __name__ == "__main__":

    gadf, phi, r, scaled_ts, ts = GADF(
        [1, 23, 4, 5, 6, 46, 2, 1.2, 4, 6, 18, 23, 4, 5, 7, 56, 1], 6, standardize_out=True)
    print(gadf)
    for i in gadf:
        plt.imshow(i, cmap = "Greys")
        plt.show()

   
