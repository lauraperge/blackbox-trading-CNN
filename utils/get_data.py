import bitfinex
import datetime
import time
from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd


def fetch_bitfinex_data(start=1230764400000.0, 
                        stop=1556661600000.0, 
                        symbol='btcusd', 
                        interval = '1m', 
                        tick_limit = 1000, 
                        step=60000000):

    """Get bitfinex data. 
    Source:
    https://medium.com/coinmonks/how-to-get-historical-crypto-currency-data-954062d40d2d

    
    Parameters
    -------
        start : float (default = 1230764400000.0 (2009.01.01. 00:00))
            start time of interval in milliseconds since 1970
        
        stop :  float (default = 1556661600000.0 (2019.05.01. 00:00))
            end time of interval in milliseconds since 1970
        
        symbol : string (default = 'btcusd')
            currency pair,default: BTCUSD
        
        interval : string (default = '6m')
            temporal resolution
            '1m' 
            '3m' 
            '6m' 
            '1D'

        tick_limit : int (default = 1000)
            number of returned data points per batch
        
        step : int (default = 180000000 (for '3m' interval))
            step size in milliseconds, no. of data points we should ask for in each of the smaller queries

    Returns
    ----------------
        data: arrays of floats    
    
    """
    # Create api instance
    api_v2 = bitfinex.bitfinex_v2.api_v2()
    data = []
    start = start - step
    while start < stop:
        start = start + step
        end = start + step
        res = api_v2.candles(symbol=symbol, interval=interval,
                             limit=tick_limit, start=start,
                             end=end)
        data.extend(res)
        time.sleep(2)
    return data


def get_stock_data(tickers=['^IXIC', '^N225', '^GSPC', 'SPY', 'EWJ', 'EWU', 'EWG'],
                    source = 'yahoo',
                    start_date = '1970-01-02',
                    end_date = '2019-05-01'
                    ):
    """Get stock data.
    
    Parameters
    -------
        tickers : list of strings (default = ['^IXIC', '^N225', '^GSPC', 'SPY', 'EWJ', 'EWU', 'EWG'])
            ticker symbols of chosen assets
        
        source :  string (default = 'yahoo')
            source of data
        
        start_date : string (default = '1970-01-02')
            start date
        
        end_date : string (default = '2019-05-01')
            end date

    Returns
    ----------------
        data: pandas dataframe  
    
    """
    # Getting just the adjusted closing prices. This will return a Pandas DataFrame
    # The index in this DataFrame is the major index of the panel_data.
    close = data.DataReader(tickers, source, start_date, end_date)['Close']

    # Getting all weekdays between start and end
    all_weekdays = pd.date_range(start=start_date, end=end_date, freq='B')

    # How do we align the existing prices in adj_close with our new set of dates?
    # All we need to do is reindex close using all_weekdays as the new index
    close = close.reindex(all_weekdays)
    first_valid_locs = close.apply(lambda col: col.first_valid_index())
    for col in close:
        print("{} starts on {} it has {} complete and {} missing observations.".format(col, 
                                                                                       first_valid_locs[col],
                                                                                       close[col].count(),
                                                                                       close[col].loc[first_valid_locs[col]:].isnull().sum(axis = 0)
                                                                                    )
             )

    print("Missing values are imputed after the start date with the last valid price.")

    # Reindexing will insert missing values (NaN) for the dates that were not present
    # in the original set. To cope with this, we can fill the missing by replacing them
    # with the latest available price for each instrument.
    close = close.fillna(method='ffill')

    return close


def get_fx_data(tickers=['DEXJPUS', 'DEXCHUS', 'DEXCAUS', 'DEXUSUK', 'DEXKOUS', 'DEXMXUS', 'DEXBZUS', 'DEXUSAL'],
                   source='fred',
                   start_date='1970-01-02',
                   end_date='2019-05-01'
                   ):
    """Get stock data.
    
    Parameters
    -------
        tickers : list of strings (default = ['DEXJPUS', 'DEXCHUS', 'DEXCAUS', 'DEXUSUK', 'DEXKOUS', 'DEXMXUS', 'DEXBZUS', 'DEXUSAL'])
            ticker symbols of chosen assets
        
        source :  string (default = 'yahoo')
            source of data
        
        start_date : string (default = '1970-01-02')
            start date
        
        end_date : string (default = '2019-05-01')
            end date

    Returns
    ----------------
        data: pandas dataframe  
    
    """
    # Getting just the adjusted closing prices. This will return a Pandas DataFrame
    # The index in this DataFrame is the major index of the panel_data.
    close = data.DataReader(tickers, source, start_date, end_date)

    first_valid_locs = close.apply(lambda col: col.first_valid_index())
    for col in close:
        print("{} starts on {} it has {} complete and {} missing observations.".format(col,
                                                                                       first_valid_locs[col],
                                                                                       close[col].count(
                                                                                       ),
                                                                                       close[col].loc[first_valid_locs[col]:].isnull().sum(
                                                                                           axis=0)
                                                                                       )
              )

    print("Missing values are imputed after the start date with the last valid price.")

    # Reindexing will insert missing values (NaN) for the dates that were not present
    # in the original set. To cope with this, we can fill the missing by replacing them
    # with the latest available price for each instrument.
    close = close.fillna(method='ffill')

    return close

if __name__ == "__main__":
    # data = fetch_bitfinex_data()
    data = get_fx_data()
    print(data)
