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
        label_window_size : int 
            the window size for data labelling (needs to be odd, should be smaller than length of series)
        
        image_window_size : int
            the window size for image creation (should be smaller than length of series)

        image_trf_strat : ('GAF', 'RP')
            the image transformation strategy, either 'GAF' or 'RP'.

        Returns: [data with new column of labels, images with respective labels, input data]
    """
    if len(data) < label_window_size:
        print('Label window size should not exceed the length of the data.')
        return()
    elif len(data) < image_widow_size:
        print('Image window size should not exceed the length of the data.')
        return()
    else:
        # if window size is fine
        data_labelled = local_min_max(data)
        if image_trf_strat == "GAF":
            
        elif image_trf_strat == 'RP':
        else:
            print('Please define the image_trf_strat: GF - for Gramian Angular Field, or RP - for recurrence plot')
            return()
