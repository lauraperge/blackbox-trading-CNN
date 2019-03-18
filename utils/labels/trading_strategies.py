import pandas as pd
import numpy as np

## Local mins and max-es
def local_min_max(serie, window_size):
    """Determines local minimums and maximums in odd sized sliding widows and labels the data accordingly.
        For price at local max: Sell,
        For price at local min: Buy,
        Otherwise: Hold,
        Parameters
        ---------------------------------------
            serie :  np.array
                input series
            
            window_size : int (must be odd)
                size of window to use for labelling, must be odd
            
        Return
        ---------------------------------------
            labelled_np : numpy array
                series and calculated labels (Buy, Hold, Sell) in a numpy array
                
            labelled_pd : 
                series and calculated labels (Buy, Hold, Sell) in a pandas DataFrame

            ws : int
                window size

            original : np.array
                orignal input series
    """

    if window_size % 2 ==1:
        ## Technical arrays, variables
        index_set = np.arange(len(serie))
        window_size_use = window_size - 1

        ## For the labels
        label = np.empty(serie.shape, dtype = "S10")
        label[:] = 'None'

        mid_idx = int(window_size_use/2)
        for idx in index_set[:-window_size_use]:
            
            if np.amin(serie[idx:(idx + window_size)]) == serie[idx + mid_idx]:
                label[idx + mid_idx] = 'Buy'
            elif np.amax(serie[idx:(idx + window_size)]) == serie[idx + mid_idx]:
                label[idx + mid_idx] = 'Sell'
            else:
                label[idx + mid_idx] = 'Hold'
        
        # numpy output
        serie_labelled_np = np.array((serie, label)).transpose().reshape(-1,2)

        # pandas output
        serie_labelled_pd = pd.DataFrame(data={'Series': serie, 'Strategy': label})
        serie_labelled_pd ['Strategy'] = serie_labelled_pd['Strategy'].str.decode('utf-8')
        serie_labelled_pd.loc[serie_labelled_pd['Strategy'] == 'None', 'Strategy'] = None

        return(serie_labelled_np, serie_labelled_pd, window_size, serie)
    else: 
        print('Please define an odd window_size!')
        return(False, window_size, serie)

# labelled_np, labelled_pandas, ws, original = local_min_max(np.array([1, 223, 3.6, 3, 6, 7, 87, 312, .34,.2, 3]), window_size = 3)

# print(labelled_pandas)

# print(labelled_np)
