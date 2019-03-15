import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
import os
from sklearn.preprocessing import MinMaxScaler

from labels.trading_strategies import local_min_max
from transform.gramian_angular_field import GASF, GADF
from transform.recurrence_plot import recurrence_plot


def data_to_labelled_img(data, label_window_size, image_widow_size, image_trf_strat):
    """Turns data into series of images with labels defining a trading strategy.

    Parameters
    -------
        data :  pandas (time) series
            input data

        label_window_size : int 
            the window size for data labelling (needs to be odd, should be smaller than length of series)
        
        image_window_size : int
            the window size for image creation (should be smaller than length of series)

        image_trf_strat : ('GASF', 'GADF', 'RP')
            the image transformation strategy, either 'GASF', 'GADF' or 'RP'
            'GASF' - Gramian Angular Summation Field
            'GADF' - Gramian Angular Difference Field
            'RP' - Recurrence Plot.

    Returns
    -----------------------------------------
        data_new:
            data with new column of labels

        images: list of matrices with names
            transformed matrices according to transformation setting with names set to label
        
        images with respective labels, input data]

    """
    series = np.array(data.values)
    series_labelled = local_min_max(series)
    data_new = pd.DataFrame(series_labelled)

    if image_trf_strat == "GASF":
        
    elif image_trf_strat == "GADF":
        
    elif image_trf_strat == 'RP':
    else:
        print('Please define the image_trf_strat: GASF, GADF or RP')
        return()
