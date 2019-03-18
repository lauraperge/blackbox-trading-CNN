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
                df = pd.concat([pd.read_csv(f, encoding='latin1')
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

def create_cleaned_set(file_with_path, varname, datename, freq = None, datetime_last = None, length = None):
    """Run all chosen transformations on the data.
    
    Parameters
    -------
        file_with_path : string
            first defining strings of name of data file with path
        
        varname :  string
            name of column of dataset to keep
        
        datename : string
            name of column representing date-time in dataset
        
        freq : (default = None)
            'BH' - business hour
            'H' - hour
            'T', 'min' - minute
            'S' - second
            'L', 'ms' - milliseconds
            'U', 'us' - microseconds
            'N' - nanoseconds
            define the frequency of the data
        
        datetime_last : (default = None)
            date of the last data point if data should be downsized
        
        length : (default = None)
            length of dataset if data should be downsized
    """
    
    # read in data (concatenate multiple files if necessary)
    df = read_concat_file(file_with_path)

    # turn into ts
    df = univar_ts(df, varname, datename)

    # change frequency if required
    if freq != None:
        df = spec_sample(df, freq, length)
    
    # cut end of data if required
    if datetime_last != None:
        df = df.loc[:datetime_last]
    
    return(df)



## Report
def report():
 ## read data
    dataname = str(input('Please type in the name of the data with path! '))
    print('Report of data: ')
    print('Reading in...')
    df = read_concat_file(dataname)
    print(df.head())

 ## time series
    varname = str(input('Please type in the name of the variable you wish to transform into a time series! '))
    datename = str(input('Please type in the name of the variable representing the date-time! '))
    newdf = univar_ts(df, varname = varname, datename = datename)

 ## report existing
    print('The number of missing values (might show missing period): ' +
          str(newdf.isnull().sum()))
    print('The head: ')
    print(newdf.head())
    print('The length is: ' + str(len(newdf)))

    newdf.plot(grid=True)
    plt.show()

 ## restrict, check
    newdf2 = newdf.copy()

    try:
        datetime_res = str(input(
            'If you want to see the data up to a specific date-time, pls type in as yyyy-mm-dd hh:mm:ss. '))
        newdf2 = newdf2.loc[:datetime_res]  # '2018-08-23 01:50:00'
    except:
        print('No date given.')

    try:
        length = input('Do you want to restrict data for the first N values? If yes, pls type in the number. ' )
        newdf2 = newdf2.iloc[:(length-1), :]
    except:
        print('No number given. ')

    ## report this
    print('The number of missing values after transformation (might show missing period): ' +
          str(newdf2.isnull().sum()))
    print('The head: ')
    print(newdf2.head())
    print('The length is: ' + str(len(newdf2)))

    newdf2.plot(grid=True)
    plt.show()
 
 ## resample, check
    newdf3 = newdf.copy()
    try:
        freq = str(input('The original data will be downsampled to 10 min freq, if not asked otherwise to check for missing period. If you have a specific frequency in mind, type in (e.g. 5T means 5 min) '))
        newdf3 = spec_sample(newdf3, freq = freq)
    except:
        newdf3 = spec_sample(newdf3, freq='10T')

    print('The number of missing values after transformation to preferred frequency (might show missing period): ' + str(newdf3.isnull().sum()))
    print('The head: ')
    print(newdf3.head())
    print('The length is: ' + str(len(newdf3)))


    newdf3.plot(grid = True)
    plt.show()

# report()
