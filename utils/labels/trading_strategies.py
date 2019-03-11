import pandas as pd
import numpy as np

## Local mins and max-es
def local_min_max(serie, window_size):
    """Determines local minimums and maximums in odd sized sliding widows and labels the data accordingly.
        Returns [labelled serie, window size, serie].
    """

    if window_size % 2 ==1:
        ## Technical arrays, variables
        serie = np.array(serie)
        index_set = np.arange(len(serie))
        window_size_use = window_size - 1

        ## For the labels
        print(serie.shape)
        label = np.empty(serie.shape, dtype = "S10")
        label[:] = 'None'

        mid_idx = int(window_size_use/2)
        for idx in index_set[:-window_size_use]:
            #print(serie[idx:(idx + window_size_use)])
            if np.amin(serie[idx:(idx + window_size)]) == serie[idx + mid_idx]:
                label[idx + mid_idx] = 'Buy'
            elif np.amax(serie[idx:(idx + window_size)]) == serie[idx + mid_idx]:
                label[idx + mid_idx] = 'Sell'
            else:
                label[idx + mid_idx] = 'Hold'
            
        serie_labelled = np.transpose(
            np.array((label, serie)))

        return(serie_labelled, window_size, serie)
    else: 
        print('Please define an odd window_size!')
        return(False, window_size, serie)

# labelled, ws, original = local_min_max([1, 223, 3.6, 3, 6, 7, 87, 312, .34,.2, 3], window_size = 3)
# print(labelled)
