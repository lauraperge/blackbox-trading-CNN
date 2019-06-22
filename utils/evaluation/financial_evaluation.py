import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
import os


def financial_evaluation(initial_capital, prices, varname, ):
    """ 
    Turns a pandas dataset to a univariate time series if the variable name and date index is given by their column name.

    Parameters
    -------------------------------
        data : pandas.DataFrame
            input data

        varname : string
            name of column to turn into univariate time series
        
        dataname : string
            name of column to be used as index for time series - must be datetime
    
    Returns
    ------------------------------
        data : pandas.Series
            pandas timeseries object (univariate)
    """
