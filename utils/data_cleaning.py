import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
import os

def read_concat_file(file_with_path, sep = ","):
    """
    Read in all files starting with "file" string ending in ".csv" or ".txt", concatenate and return as pandas dataframe.
    """

    # Look for files
    files = glob.glob(file_with_path + '*')

    if len(files) > 0:
     ## found some files

        #extension
        type = os.path.splitext(files[0])[1]

        if(type == ".csv"):
         ## CSV
            if len(files) > 1:
             ## if more files
                df = pd.concat([pd.read_csv(f, encoding='latin1')
                            for f in glob.glob(file_with_path + '*.csv')], ignore_index=True)
            else:
             ## if one file
                df = pd.read_csv(files[0],encoding='latin1')
            return(df)
        elif(type == ".txt"):
         ## TXT
            if len(files) > 1:
              ## if more files
                df = pd.concat([pd.read_csv(f, encoding='latin1', header = None)
                               for f in glob.glob(file_with_path + '*.txt')], ignore_index=True)
            else:
              ## if one file
                df = pd.read_csv(files[0], encoding='latin1', header=None)
            return(df)
        else:
            return("Could not recognize type.")
    else:
        return("No files with the given name.")

def univar_ts (data, varname, datename):
    """ 
    Turns a pandas dataset to a univariate time series if the variable name and date index is given by their column name.
    """
    data_new = data.copy()
    data_new = data_new[[varname, datename]]
    data_new.set_index(pd.to_datetime(data_new[datename]), inplace=True)
    data_new = data_new[[varname]]
    return(data_new)

def spec_sample(data, freq, length = None):
    """
    Samples the data, with the given frequency (last element) and the user can set how long of a series should be returned.
    """

    if length == None:
        return(data.resample(freq).last())
    elif isinstance(length, int) == True:
        return(data.resample(freq).last().iloc[:(length-1),:])
    else:
        return('Error.')

# def sliding window(data, size):
#     pd.rolling
# df = read_concat_file('../data/gemini')
# newdf = univar_ts(df, varname = 'Close', datename = 'Date')
# newdf = spec_sample(newdf, freq = '10T', length = 10)
# print(newdf)

# plt.figure(figsize=(12, 7), frameon=False, facecolor='brown', edgecolor='blue')
# plt.title('')
# plt.xlabel('minutes')
# plt.ylabel('price')
# plt.plot(df[[9]])
# plt.legend()
# plt.show()