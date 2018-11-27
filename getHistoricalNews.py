import os
import pandas as pd
import cryptocompare as cc

dp = os.getcwd()
if not os.path.exists(os.path.join(dp,'news')):
    os.makedirs(os.path.join(dp,'news'))
dataPath = os.path.join(dp,'news')

portfolio = cc.get_currencies_list()
print(portfolio)

for coin in portfolio:
    print(coin)
    df = cc.fetchNewsPerCoin(coin)
    print(df.shape)
    df.to_csv(os.path.join(dataPath, coin + '.csv'), index=False)
