import requests
import datetime
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from math import pi

from stockstats import StockDataFrame # DEPENDENCY -- run pip install stockstats to install


def daily_price_historical(symbol, comparison_symbol, all_data=True, exchange=''):
    '''
    :params symbol: srt cryptoasset ticker e.x. BTC
    :params comparison_symbol: str ticker to compare to e.x. USD
    :params all_data: bool get all data
    :params exchange: str token exchange ticker

    :returns pandas dataframe

    Accesses the CryptoCompare API and returns a pandas dataframe of all historical data
    '''
    url = 'https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym={}&all_data={}' \
        .format(symbol.upper(), comparison_symbol.upper(), all_data)
    if exchange:
        url += '&e={}'.format(exchange)
    if all_data:
        url += '&allData=true'
    page = requests.get(url)
    data = page.json()['Data']
    df = pd.DataFrame(data)
    df['timestamp'] = [datetime.datetime.fromtimestamp(d) for d in df.time]
    return(df)

def time_range(df, start = '2018-02-01'):
    '''

    :param df: pandas dataframe containing timestamp data
    :param start: start date to subset information from to present
    :return: pandas dataframe containing data from start date to present

    Function for subsetting data based on time
    '''
    start_date = pd.to_datetime(start) # need to make sure everything is a datetime object
    mask = (df['timestamp'] > start_date)
    return(df.loc[mask])

def convert2stockstats(df):
    '''

    :param df: pandas dataframe
    :return: StockStatsDataFrame -- this is effectively the same as a pandas dataframe with hidden indicator data

    Allows us to use the StockStats library
    '''
    return(StockDataFrame.retype(df))

def create_indicator_df(df, indicator):
    '''

    :param df: pandas dataframe containing StockDataFrame for cryptoassets
    :param indicator: str code for indicator
    :return: pandas dataframe with indicator information

    Function for adding indicator information to a dataframe
    '''
    df[indicator] = df.get(indicator)
    return(df)

def create_moving_avg_df(df, col = 'close', short_period = '5', long_period = '50'):
    '''

    :param df: pandas dataframe with cryptoasset data
    :param col: str column to calculate moving average on
    :param short_period: short moving average window
    :param long_period: long moving average window
    :return: pandas dataframe with calculated moving averages
    '''
    short_sma = col + '_' + short_period + '_sma'
    short_ema = col + '_' + short_period + '_ema'

    long_sma = col + '_' + long_period + '_sma'
    long_ema = col + '_' + long_period + '_sma'

    df[short_sma] = df.get(short_sma)
    df[long_sma] = df.get(long_sma)
    df[short_ema] = df.get(short_ema)
    df[long_ema] = df.get(long_ema)

    return(df)


def get_col_index(df, indicator):
    '''

    :param df: pandas dataframe
    :param indicator: str name of indicator
    :return: int index location of indicator in header
    '''
    cols = list(df)
    return(cols.index(indicator))

def crossover(df, idx, col1, col2):
    '''

    :param df: pandas dataframe with cryptoasset information
    :param idx: row index
    :param col1: str label of first line (e.x. macd line)
    :param col2: str label of second line (e.x. macds for macd signal line)
    :return: str either 'Buy', 'Sell', or 'Hold'

    This is used to check for trading signal crossovers between two lines
    '''
    if idx == 0:
        return ("Hold")

    prev1 = df.iloc[idx - 1, col1]
    prev2 = df.iloc[idx - 1, col2]
    curr1 = df.iloc[idx, col1]
    curr2 = df.iloc[idx, col2]

    if prev1 < prev2 and curr2 <= curr1: # buy signal -- crossing on uptrend
        return("Buy")
    elif prev1 > prev2 and curr2 >= curr1: # sell signal -- crossing on downtrend
        return("Sell")
    else:
        return("Hold")

def bound_crossover(df, idx, col1, col2, lower_bound = 40, upper_bound = 60):
    '''

    :param df: pandas dataframe containing indicator info
    :param idx: row index
    :param col1: str label of first line (e.x. RSI)
    :param col2: str label of second line (e.x. Moving Average of RSI)
    :param lower_bound: int indicator lower bound (e.x. 40 for RSI)
    :param upper_bound: int indicator upper bound (e.x. 60 for RSI)
    :return: str either 'Buy', 'Sell', or 'Hold'

    This is used to check for trading signal crossovers between two lines with intermediary bounds
    '''
    if idx == 0:
        return ("Hold")

    prev1 = df.iloc[idx - 1, col1]
    prev2 = df.iloc[idx - 1, col2]
    curr1 = df.iloc[idx, col1]
    curr2 = df.iloc[idx, col2]

    #print(prev1)

    if prev1 < prev2 and curr2 <= curr1 and prev1 <= lower_bound: # buy signal -- crossing on uptrend
        return("Buy")
    elif prev1 > prev2 and curr2 >= curr1 and prev1 >= upper_bound: # sell signal -- crossing on downtrend
        return("Sell")
    else:
        return("Hold")


def rsi_signal(rsi):
    '''
    DEPRECATED

    :param rsi: float rsi value
    :return: buy, sell, or hold

    RSI signal using just bounds.
    '''
    try:
        # print(rsi)
        if rsi >= 60:  # Buy signal
            return ("Buy")
        elif rsi <= 40:  # Sell signal
            return ("Sell")
        else:
            return ("Hold")
    except Exception as e:
        print(e)
        return ("Hold")

def remove_duplicates(df, signal_col):
    '''

    :param df: pandas dataframe containing buy or sell signals -- after being filtered by filter_signals()
    :param signal_col: str label of column with trading signals ('Buy', 'Sell')
    :return: pandas dataframe with alternating 'Buy' and 'Sell' signals

    This allows us to follow a holding strategy by removing consecutive 'Buy' or 'Sell' signals.
    E.x., 'Buy', 'Buy', 'Sell', 'Sell', 'Buy' becomes 'Buy', 'Sell', 'Buy'
    '''
    other_df = df.iloc[0:1] # Dataframe to append alternating signals to
    prev_signal = 'Buy' # Need first signal to be 'Buy', assuming that we're entering
    for index, row in df.iterrows():
        if row[signal_col] == 'Sell' and prev_signal == 'Buy': # Alternate from Buy to Sell!
            prev_signal = 'Sell'
            other_df = other_df.append(row, ignore_index = True)
        elif row[signal_col] == 'Buy' and prev_signal == 'Sell': # Alternate from Sell to Buy!
            prev_signal = 'Buy'
            other_df = other_df.append(row, ignore_index = True)
    return(other_df)

def filter_signals(df, col = 'signal', buy = 'Buy', sell = 'Sell'):
    '''

    :param df: pandas dataframe containing signal column with buy, sell, or hold
    :param col: str label column with signal data
    :param buy: str term for buy
    :param sell: str term for sell
    :return: pandas dataframe only containing rows with 'Buy' or 'Sell' signals, starting with a 'Buy' signal

    Filters out just 'Buy' and 'Sell' signals
    '''
    mask = (df[col] == buy) | (df[col] == sell) # Select rows using a mask
    df = df.loc[mask]
    try:
        x = 0
        # Need first signal to be buy for entering the market (can't sell if there are 0 assets)
        # This while loop goes through the first set of rows until a buy signal is hit
        while df[col].iloc[x] == sell:
            #print('skip')
            x += 1
        df = df.iloc[x:]
    except Exception as e:
        print(e)
    return(df)

def sharpe_ratio(returns, rrr = 0):
    '''

    :param returns: array of returns
    :param rrr: risk-free rate of return
    :return: calculated sharpe ratio
    '''

    ra_rb = abs(returns) - rrr
    num = np.mean(ra_rb)
    den = np.std(ra_rb)
    if den == 0:
        return 0
    return num/den

def calc_sharpe(filtered_df, col = 'close'):
    '''
    :param filtered_df: pandas dataframe containing just buy and sell signals -- filtered with filter_signals()
    :param col: str label column to calculate sharpe on
    :returns: Calculated time-series for a column
    '''
    filtered_df = filtered_df[['close', 'open', 'high', 'low']]
    filtered_df = filtered_df.pct_change()
    return(sharpe_ratio(filtered_df[col]))

def calc_returns(filtered_df, col = 'close', return_df = False):
    '''
    KATRINA'S VERSION OF CALC RETURNS
    Split up to avoid merge conflicts.

    :param filtered_df: pandas dataframe containing alternating buy and sell signals -- filtered with filter_signals() and remove_duplicates()
    :param col: str label column to calculate returns on
    :param return_df: bool of whether or not to return a dataframe
    :return: either a list of returns or a pandas dataframe with pct_change()

    Function for calculating returns
    '''
    df = filtered_df[['close', 'open', 'high', 'low']]
    df = df.pct_change()
    if return_df:
        filtered_df[col + '_pct_change'] = df[col]
        return filtered_df
    selected = df[col].tolist()
    returns_list= []
    for x in range(1, len(selected), 2): # Because there are no returns on a 'Buy' signal, we need to take every other pct_change() calculation
        returns_list.append(selected[x])

    return(returns_list)

def calc_returns2(filtered_df):
    '''
    KEVIN'S VERSION OF CALC RETURNS
    Split up to avoid merge conflicts.

    :param filtered_df: pandas dataframe containing alternating buy and sell signals -- filtered with filter_signals() and remove_duplicates()
    :return: list of returns on close price and a pandas dataframe with close_pct_change()

    Function for calcuating returns and dataframe on close
    '''

    filtered_df['close_pct_change'] = filtered_df['close'].pct_change()

    selected = filtered_df['close_pct_change'].tolist()
    returns_list= []
    for x in range(1, len(selected), 2):
        returns_list.append(selected[x])

    filtered_df = filtered_df[['close','open','high', 'low', 'signal','close_pct_change','timestamp']]
    return(returns_list, filtered_df)

def create_crossover_df(df, lin1, lin2):
    '''

    :param df: pandas dataframe containing indicator data
    :param lin1: str label of first line (e.x. 'macd')
    :param lin2: str label of second line (e.x. 'macds')
    :return: pandas dataframe containing crossover trade signals

    Calculates crossover trading signals when no bounds are involved
    '''
    col1 = get_col_index(df, lin1)
    col2 = get_col_index(df, lin2)
    c = []
    for x in range(len(df['timestamp'])): # create crossover
        c.append(crossover(df, x, col1, col2))
    c = pd.Series(c)
    df = df[['close', 'open', 'high', 'low', lin1, lin2]] # subset desired data
    df = df.assign(signal=c.values) # add signal column
    return(df)

def create_bound_crossover_df(df, lin1, n = 5, low = 40, up = 60):
    '''

    :param df: pandas dataframe containing indicator data
    :param lin1: str label of indicator (e.x. 'rsi')
    :param n: int rolling window period for moving average of selected indicator
    :param low: int lower bound
    :param up: int upper bound
    :return: pandas dataframe containing crossover trade signals

    Calculates crossover trading signals when bounds are involved.
    We default to working with simple moving averages for crossovers.
    '''
    col1 = get_col_index(df, lin1)
    df['MA'] = df[lin1].rolling(window=n).mean() # calculate moving average
    #col2 = 'MA'
    col2 = get_col_index(df, 'MA')
    c = []
    for x in range(len(df['timestamp'])): # calculate bound crossover
        c.append(bound_crossover(df, x, col1, col2, lower_bound = low, upper_bound = up))
    c = pd.Series(c)
    df = df[['close', 'open', 'high', 'low', lin1, 'MA', 'timestamp']] # subset desired data
    df = df.assign(signal=c.values) # add signal column
    return(df)



def cumulative_returns(returns_list, output = True):
    '''

    :param returns_list: list of returns
    :param output: bool of whether or not to print out information
    :return: cumulative sum of all returns

    This function lets us know how successful our backtested indicators were over time.
    '''
    trade_sum = sum(returns_list)
    if output:
        print('Trade Sum: {}'.format(trade_sum))
        if trade_sum > 0:
            print('Positive Return!')
        elif trade_sum < 0:
            print('Negative Return!')
        else:
            print('No Return!')

    return(trade_sum)

def get_returns(df, sig = 'signal', duplicates = False, return_df = False): # more complete implementation
    '''

    :param df: pandas dataframe containing trade signals
    :param sig: str label of column with trade signals
    :param duplicates: bool of whether or not to remove consecutive signals
    :param return_df: (DEPRECATED) bool for returning dataframe using Katrina's version of calc returns. Now using Kevin's (calc_returns2())
    :return: tuple containing a list of returns and a filtered pandas dataframe with alternating buy and sell signals with timestamps

    Used to calculate total returns and get a dataframe with time data (so that the results can be plotted)
    '''
    df = filter_signals(df, col = sig)
    if duplicates:
        df = remove_duplicates(df, sig)

    return(calc_returns2(df))

def brute_force_opt(df, indicator, param1_lower, param1_upper, param2_lower, param2_upper, lower, upper,
                    sig_col = 'signal', dupe_bool = False, ma = False):
    '''

    :param df: pandas dataframe containing CryptoCompare price data
    :param indicator: str name of indicator to use from StockStats
    :param param1_lower: int lower bound for rolling window of selected indicator (although can be any numerical column)
    :param param1_upper: int upper bound for rolling window of selected indicator (although can be any numerical column)
    :param param2_lower: int lower bound for rolling window of moving average (although can be any numerical column)
    :param param2_upper: int upper bound for rolling window of moving average (although can be any numerical column)
    :param lower: int lower bound for selected indicator (e.x. 40 for RSI)
    :param upper: int upper bound for selected indicator (e.x. 60 for RSI)
    :param sig_col: str label column with signal data
    :param dupe_bool: bool for whether or not to remove consecutive signals
    :param ma: bool for whether or not to add an 'sma' indicator in the indicator name (sma stands for simple moving average)
    :return: tuple containing ( tuple of optimal rolling windows, float sharpe ratio, float cumulative returns,
                                pandas dataframe of filtered dataframe, copy of original crossover dataframe )

    Brute Force Optimization algorithm for finding optimal rolling window parameters for crossover indicators involving moving averages.
    This is done by checking every combination of rolling windows.
    Conceptually, works similarly to  a Grid Search.

    Objective: Maximize sum of returns
    Constraints: Rules of indicator
    Decision Variables: Returns

    '''
    sub_df = df[['close', 'open', 'high', 'low', 'timestamp']] # subset desired data
    sub_df = convert2stockstats(sub_df) # convert to StockStats dataframe
    param1_win = list(range(param1_lower, param1_upper)) # create range of rolling windows to test for selected indicator
    param2_win = list(range(param2_lower, param2_upper)) # create range of rolling windows to test moving average of selected indicator
    max = 0

    # Iterate through all possibilites using a nested for loop -- hence why this is 'brute force'

    for win1 in param1_win:

        # Add indicator information
        if ma:
            df = create_indicator_df(sub_df, '{}_{}_{}'.format(indicator, win1, 'sma'))
        else:
            df = create_indicator_df(sub_df, '{}_{}'.format(indicator, win1))
        for win2 in param2_win:

            # Calculate crossover information
            if ma:
                copy_df = create_bound_crossover_df(df, '{}_{}_{}'.format(indicator, win1, 'sma'), win2, lower, upper)
            else:
                copy_df = create_bound_crossover_df(df, '{}_{}'.format(indicator, win1), win2, lower, upper)

            # Get list of returns and a filtered dataframe
            returns_list, filtered_df = get_returns(copy_df, sig = sig_col, duplicates = dupe_bool, return_df = True)

            # Calculate cumulative returns
            total_returns = cumulative_returns(returns_list, output=False)

            # Check to see if a new maximum is found
            if total_returns > max:
                optim = (win1, win2)
                sr = calc_sharpe(copy_df)
                head = filtered_df
                max = total_returns
                orig_df = copy_df

    return(optim, sr, max, head, orig_df)






