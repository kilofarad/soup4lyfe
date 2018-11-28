import technicalIndicators as ti
import datetime
import pandas as pd

symbol = 'BTC'
comparison_symbol = 'USD'
default_date = '2018-11-27'
class ti_test():

    def test1(self):
        print('TEST 1 - Create Moving Avg DF')
        try:
            df = ti.daily_price_historical(symbol, comparison_symbol)
            df = ti.time_range(df)
            df = ti.convert2stockstats(df)
            df = ti.create_moving_avg_df(df)
            print(df.head())
            df.to_csv('data/{}-{}.csv'.format(symbol, datetime.datetime.today().strftime('%Y-%m-%d')))
        except Exception as e:
            print(e)

    def test2(self):
        print('TEST 2 - Read in csv as pandas dataframe')
        try:
            df = pd.read_csv('data/{}-{}.csv'.format(symbol, default_date))
            df = ti.convert2stockstats(df)
            print(df.head())
        except Exception as e:
            print(e)

    def test3(self):
        print('TEST 3 - Add Default MACD')
        try:
            df = pd.read_csv('data/{}-{}.csv'.format(symbol, default_date))
            df = ti.convert2stockstats(df)
            df = ti.create_indicator_df(df, 'macd')
            print(df.head())
        except Exception as e:
            print(e)

    def test4(self):
        print('TEST 4 - Add 14-Day RSI')
        try:
            df = pd.read_csv('data/{}/{}-{}.csv'.format(symbol, symbol, default_date))
            df = ti.convert2stockstats(df)
            df = ti.create_indicator_df(df, 'rsi_14')
            print(df.head())
        except Exception as e:
            print(e)

    def test5(self):
        print('TEST 5 - Add Default Bollinger Bands')
        try:
            df = pd.read_csv('data/{}/{}-{}.csv'.format(symbol, symbol, default_date))
            df = ti.convert2stockstats(df)
            df = ti.create_indicator_df(df, 'boll')
            print(df.head())
        except Exception as e:
            print(e)

    def test6(self):
        print('TEST 6 - Add Average True Range')
        try:
            df = pd.read_csv('data/{}/{}-{}.csv'.format(symbol, symbol, default_date))
            df = ti.convert2stockstats(df)
            df = ti.create_indicator_df(df, 'atr')
            print(df.head())
        except Exception as e:
            print(e)

    def test7(self):
        print('TEST 7 - Add On-Balance Volume')
        try:
            df = pd.read_csv('data/{}/{}-{}.csv'.format(symbol, symbol, default_date))
            df = ti.convert2stockstats(df)
            df = ti.add_obv(df)
            print(df.head())
        except Exception as e:
            print(e)

    def test8(self):
        print('TEST 8 - Combine All Indicators')
        try:
            df = pd.read_csv('data/{}/{}-{}.csv'.format(symbol, symbol, default_date))
            df = ti.convert2stockstats(df)
            indicators = ['macd', 'rsi_14', 'boll', 'atr'] # add obv later!
            for i in indicators:
                df = ti.create_indicator_df(df, i)
            print(df.head())
            #df.to_csv('data/{}-{}.csv'.format(symbol, default_date))
        except Exception as e:
            print(e)

    def test9(self):
        print('TEST 8 - Combine All Indicators and Output to CSV')
        try:
            df = pd.read_csv('data/{}/{}-{}.csv'.format(symbol, symbol, default_date))
            df = ti.convert2stockstats(df)
            indicators = ['macd', 'rsi_14', 'boll', 'atr'] # add obv later!
            for i in indicators:
                df = ti.create_indicator_df(df, i)
            #print(df.head())
            df.to_csv('data/{}-{}.csv'.format(symbol, default_date))
        except Exception as e:
            print(e)

if __name__ == '__main__':
    x = ti_test()
    x.test1()
    x.test2()
    x.test3()
    x.test4()
    x.test5()
    x.test6()
    #x.test7()
    x.test8()
    x.test9()

    print('TESTS COMPLETE!')

