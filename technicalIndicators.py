import requests
import datetime
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from math import pi

from stockstats import StockDataFrame


def daily_price_historical(symbol, comparison_symbol, all_data=True, exchange=''):
    '''
    :params symbol: srt cryptoasset ticker e.x. BTC
    :params comparison_symbol: str ticker to compare to e.x. USD
    :params all_data: bool get all data
    :params limit: int rate limit
    :params aggregate: int increment to aggregate
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

    :param df:
    :param start:
    :return:
    '''
    start_date = pd.to_datetime(start)
    mask = (df['timestamp'] > start_date)
    return(df.loc[mask])

def convert2stockstats(df):
    '''

    :param df:
    :return:
    '''
    return(StockDataFrame.retype(df))

def create_indicator_df(df, indicator):
    '''

    :param df:
    :param indicator:
    :return:
    '''
    df[indicator] = df.get(indicator)
    return(df)

def create_moving_avg_df(df, col = 'close', short_period = '5', long_period = '50'):
    '''

    :param df:
    :param col:
    :param short_period:
    :param long_period:
    :return:
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


def macd_crossover(df, idx):
    '''

    :param df:
    :param idx:
    :return:
    '''
    if idx == 0:
        return ("No Move")
    # print(df.head())
    prev_macd = df.iloc[idx - 1, 10]
    prev_signal = df.iloc[idx - 1, 11]
    current_macd = df.iloc[idx, 10]
    current_signal = df.iloc[idx, 11]

    if prev_signal < prev_macd and current_macd <= current_signal:  # bearish crossover
        return ("Buy")
    elif prev_signal > prev_macd and current_macd >= current_signal:  # bullish crossover
        return ("Sell")
    else:  # no crossover
        return ("No Move")

def crossover(df, idx, col1, col2):
    '''

    :param df:
    :param idx:
    :param col1:
    :param col2:
    :return:
    '''
    if idx == 0:
        return ("No Move")

    prev1 = df.iloc[idx - 1, col1]
    prev2 = df.iloc[idx - 1, col2]
    curr1 = df.iloc[idx, col1]
    curr2 = df.iloc[idx, col2]

    if prev1 < prev2 and curr1 <= curr2: # buy signal
        return("Buy")
    elif prev1 > prev2 and curr1 >= curr2: # sell signal
        return("Sell")
    else:
        return("No Move")


def rsi_signal(rsi):
    '''

    :param rsi:
    :return:
    '''
    try:
        # print(rsi)
        if rsi >= 70:  # Buy signal
            return ("Buy")
        elif rsi <= 30:  # Sell signal
            return ("Sell")
        else:
            return ("No Move")
    except Exception as e:
        print(e)
        return ("No Move")

def remove_rsi_duplicates(df, signal_col):
    '''

    :param df:
    :param signal_col:
    :return:
    '''
    other_df = df.iloc[0:1]
    print(type(other_df))
    prev_signal = 'Buy'
    for index, row in df.iterrows():
        #print(type(row))
        #if row['rsi_signal'] == 'Buy' and prev_signal == '':
         #   prev_signal = 'Buy'
          #  other_df = other_df.append(row, ignore_index = True)
        if row[signal_col] == 'Sell' and prev_signal == 'Buy':
            prev_signal = 'Sell'
            other_df = other_df.append(row, ignore_index = True)
        elif row[signal_col] == 'Buy' and prev_signal == 'Sell':
            prev_signal = 'Buy'
            other_df = other_df.append(row, ignore_index = True)
    return(other_df)

def filter_signals(df, col, buy = 'Buy', sell = 'Sell'):
    '''

    :param df:
    :param col:
    :param buy:
    :param sell:
    :return:
    '''
    mask = (df[col] == buy) | (df[col] == sell)
    return(df.loc[mask])

def calc_returns(filtered_df, col = 'close'):
    '''

    :param filtered_df:
    :param col:
    :return:
    '''
    filtered_df = filtered_df[['close', 'open', 'high', 'low']]
    filtered_df = filtered_df.pct_change()
    selected = filtered_df[col].tolist()
    returns_list= []
    for x in range(0, len(selected), 2):
        returns_list.append(selected[x])

    return(returns_list)


def cumulative_returns(returns_list):
    '''

    :param returns_list:
    :return:
    '''
    trade_sum = sum(returns_list)
    print('Trade Sum: {}'.format(trade_sum))
    if trade_sum > 0:
        print('Positive Return!')
    elif trade_sum < 0:
        print('Negative Return!')
    else:
        print('No Return!')

    return(trade_sum)

def add_obv(df):
    pass


