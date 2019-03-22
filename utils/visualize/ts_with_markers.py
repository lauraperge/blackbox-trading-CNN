import matplotlib.pyplot as plt
import pandas as pd
import numpy as np 

def plot_ts_markers(data, main_col, by_col, to_mark, color, marker_type):
    """Plots a time series in the main_col, with markers according to by_col, marking only the to_mark categories.

    Parameters
    --------------------------
        data : pandas.DataFrame
            input data
        
        main_col : string
            name of column that contains series for plotting
        
        by_col : string
            name of column to use for choosing markers
        
        to_mark : list of strings
            entries to mark
        
        color : list of strings
            color for each entry in to_mark
        
        marker_type : list of strings
            type of marker for each entry to mark
            "." - point
            "," - pixel
            "o" - circle
            "v" - triangle down
            "^" - triangle up
            "<" - triangle left
            ">"  triangle right (see matplotlib markers)
    
    Returns
    ---------------------------
        plot : matplotlib.pyplot.Figure object
            plot of series with markers
    """

    if len(to_mark) != len(color):
        raise Exception(
            'Please make sure that you assign one color to each marker type in to_mark.')
    elif len(to_mark) != len(marker_type):
        raise Exception(
            'Please make sure that you assign one marker type to each marker type in to_mark.')
    else:
        
        fig, ax1 = plt.subplots()
        ax1.plot(data.index, data[main_col], '-b')
        for idx, m in enumerate(to_mark):
            
            marker = data.loc[data[by_col] == m, main_col]
            
            ax1.plot(marker.index, marker, color = color[idx], marker = marker_type[idx], linestyle = 'None')
            fig.autofmt_xdate()
        fig.show()
        return(fig)   


# dta = pd.DataFrame({"series": [1, 23, 4, 5, 6, 46, 2, 1.2, 4, 6, 18, 23, 4, 5, 7, 56, 1, 1.7], "labels": ["l", "f", "h", "h", "h", "l", "h", "h", "f", "h", "h", "l", "h", "h", "l", "l", "h", "f"]})
# fig = plot_ts_markers(data = dta,
#         main_col = 'series',
#         by_col = "labels",
#         to_mark = ["l", "f"],
#         color = ['r', 'g'],
#         marker_type = ['v', '^']
#         )
#fig.savefig('test.png')
