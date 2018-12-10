"""
original code by Pawel Lachowicz, QuantAtRisk.com,
adapted by Vangelis@sanzprophet.com
adapted again by B^)
"""

import pandas as pd
import json
from bs4 import BeautifulSoup
import requests
import os
import time as mod_time

#You can set your own paths here to save a text file with the list of coins
dp = os.getcwd()
if not os.path.exists(os.path.join(dp,'csv')):
    os.makedirs(os.path.join(dp,'csv'))
dataPath = os.path.join(dp,'csv')
#load csv of cryptocurrencies
def get_currencies_list():
    url = 'https://min-api.cryptocompare.com/data/all/coinlist'
    response = requests.get(url)

    if response.status_code ==  200:
        response = response.json()
        coins = response['Data']

    return list(coins.keys())

portfolio = get_currencies_list()
#set base currency
tsym = 'USD'

####################################################
#Cryptocompare has no data for these currencies
bad_fsym = []#'MIOTA','LKK','ETHOS','GXS','ACT','KCS']
portfolio = [ fsym for fsym in portfolio if fsym not in bad_fsym ]

def fetchCryptoOHLC(fsym, tsym):
    # function fetches a crypto price-series for fsym/tsym and stores
    # it in pandas DataFrame

    cols = ['timestamp', 'open', 'high', 'low', 'close','volume']
    lst = ['time', 'open', 'high', 'low', 'close','volumeto']


    df = pd.DataFrame(columns = cols)
    url = "https://min-api.cryptocompare.com/data/histoday?fsym=" + fsym + "&tsym=" + tsym +'&allData=true'
    response = requests.get(url)

    print(response)
    if response.status_code ==  200 :
        soup = BeautifulSoup(response.content, "html.parser")
        dic = json.loads(soup.prettify())
        data = pd.DataFrame(dic['Data'])
        if data.shape == (0,0):
            print(soup)
            return None
        data['time'] = data.apply(lambda x: mod_time.strftime('%Y%m%d',mod_time.gmtime(x.time)),axis = 'columns')

    else: #if error response is not 200. problem return empty df (this needs work)
        data = None

    return data

for fsym in portfolio:
    data = fetchCryptoOHLC(fsym, tsym) #i.e. fetchCryptoOHLC('ETH', 'USD')
    if data is None:
        continue
    timerange = list(data['time'].iloc[[0,-1]])
    fileend = fsym+' '+timerange[0]+'-'+timerange[1]+'.csv'
    print(fileend)
    data.to_csv(os.path.join(dataPath,fileend),',')
############################################################
