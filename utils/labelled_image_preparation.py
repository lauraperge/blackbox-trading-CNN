import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
import os
from sklearn.preprocessing import MinMaxScaler

from labels.trading_strategies import local_min_max
from transform.gramian_angular_field import GASF, GADF
from transform.recurrence_plot import RP


def data_to_labelled_img(data, column_name, label_window_size, image_window_size, image_trf_strat):
    """Turns data into series of images with labels defining a trading strategy. 
    Made to suit the input of the CNN in Tensorflow.

    Parameters
    -------
        data :  pandas (time) series
            input data

        column_name : str
            name of column in df to transform

        label_window_size : int 
            the window size for data labelling (needs to be odd, should be smaller than length of series)
        
        image_window_size : int
            the window size for image creation (should be smaller than length of series, but more than half of the label window size)
            (please note that the TP transformation will result in images of size (image_window_size-1, image_window_size-1))

        image_trf_strat : ('GASF', 'GADF', 'RP')
            the image transformation strategy, either 'GASF', 'GADF' or 'RP'
            'GASF' - Gramian Angular Summation Field
            'GADF' - Gramian Angular Difference Field
            'RP' - Recurrence Plot.

    Returns
    -----------------------------------------
        labelled_pd : pd.dataframe
            data with new column of labels

        images : np.array
            array of transformed matrices according to transformation setting
        
        image_labels : np.array
            array of labels for each image, with one-hot encoding
        
        label_names :
            dictionary linking strategy name to column index in image_labels

    """
    if image_window_size < np.ceil(label_window_size/2):
        print('image_window_size must be >= np.ceil(label_window_size/2), please choose a grater image window size.')
        return()
    else:    
        series = np.array(data[column_name].values)
        labelled_np, labelled_pd, ws, original = local_min_max(
            series, label_window_size)

        # get one-hot encoding for the labels
        image_labels = np.array(pd.get_dummies(labelled_pd.Strategy))[
            (image_window_size-1):(-np.int(label_window_size/2)), :]
        # for saving which column is which
        label_colnames = np.array(pd.get_dummies(labelled_pd.Strategy).columns)

        # images from first datapoint to (last_idx - floor(label_window_size/2))
        if image_trf_strat == "GASF":
            # transformation
            images,  phi, r, scaled_ts, ts = GASF(
                series[:-np.int(label_window_size/2)], image_window_size)
            images = np.array(images)
        elif image_trf_strat == "GADF":
            # transformation
            images,  phi, r, scaled_ts, ts = GADF(
                series[:-np.int(label_window_size/2)], image_window_size)
            images = np.array(images)

        elif image_trf_strat == 'RP':
            # transformation
            images, serie = RP(series[:-np.int(label_window_size/2)], image_window_size)
            images = np.array(images)

        else:
            print('Please define the image_trf_strat: GASF, GADF or RP')
            return()

        # Label names (as column name for image labels) 
        
        label_names = {np.int(np.argwhere(label_colnames == "Sell")) : "Sell",
                       np.int(np.argwhere(label_colnames == "Buy")) : "Buy",
                       np.int(np.argwhere(label_colnames == "Hold")) : "Hold"
                        }
        return(labelled_pd, images, image_labels, label_names)


# dta = pd.DataFrame(data=np.array(
#     [1, 23, 4, 5, 6, 46, 2, 1.2, 4, 6, 18, 23, 4, 5, 7, 56, 1, 1.7]), columns=["Series"])

# labelled_pd, images, image_labels, label_names = data_to_labelled_img(
#     data=dta, column_name="Series", label_window_size=3, image_window_size=5, image_trf_strat="GASF")

# print(labelled_pd)
# print(images)
# print(image_labels)
# print(label_names)