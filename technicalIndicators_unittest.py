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
        print('TEST 9 - Combine All Indicators and Output to CSV')
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

    def test10(self):
        print('TEST 10 - Get Column Index')
        try:
            df = pd.read_csv('data/{}/{}-{}.csv'.format(symbol, symbol, default_date))
            col_idx = ti.get_col_index(df, 'macd')
            print(col_idx)
            print(list(df)[col_idx])
            if list(df)[col_idx] == 'macd':
                print('Test Success!')
            else:
                print('Test Fail')
        except Exception as e:
            print(e)

    def test11(self):
        print('TEST 11 - Calculate MACD Crossover')
        try:
            df = pd.read_csv('data/{}/{}-{}.csv'.format(symbol, symbol, default_date))
            col1 = ti.get_col_index(df, 'macd')
            col2 = ti.get_col_index(df, 'macds')
            c = []
            for x in range(len(df['timestamp'])):
                c.append(ti.crossover(df, x, col1, col2))
            c = pd.Series(c)
            df = df[['close', 'open', 'high', 'low', 'macd', 'macds']]
            df = df.assign(signal=c.values)
            print(df.head())
        except Exception as e:
            print(e)

    def test12(self):
        print('TEST 12 - Filter Signals')
        try:
            df = pd.read_csv('data/{}/{}-{}.csv'.format(symbol, symbol, default_date))
            col1 = ti.get_col_index(df, 'macd')
            col2 = ti.get_col_index(df, 'macds')
            c = []
            for x in range(len(df['timestamp'])):
                c.append(ti.crossover(df, x, col1, col2))
            c = pd.Series(c)
            df = df[['close', 'open', 'high', 'low', 'macd', 'macds']]
            df = df.assign(signal=c.values)
            df = ti.filter_signals(df)
            print(df.head())
        except Exception as e:
            print(e)

    def test13(self):
        print('TEST 13 - Calculate Returns for MACD Crossover')
        try:
            df = pd.read_csv('data/{}/{}-{}.csv'.format(symbol, symbol, default_date))
            col1 = ti.get_col_index(df, 'macd')
            col2 = ti.get_col_index(df, 'macds')
            c = []
            for x in range(len(df['timestamp'])):
                c.append(ti.crossover(df, x, col1, col2))
            c = pd.Series(c)
            df = df[['close', 'open', 'high', 'low', 'macd', 'macds']]
            df = df.assign(signal=c.values)
            df = ti.filter_signals(df)
            print(df.head())
            returns_list = ti.calc_returns(df)
            print(returns_list)
        except Exception as e:
            print(e)

    def test14(self):
        print('TEST 14 - Calculate Cumulative Returns for MACD Crossover')
        try:
            df = pd.read_csv('data/{}/{}-{}.csv'.format(symbol, symbol, default_date))
            col1 = ti.get_col_index(df, 'macd')
            col2 = ti.get_col_index(df, 'macds')
            c = []
            for x in range(len(df['timestamp'])):
                c.append(ti.crossover(df, x, col1, col2))
            c = pd.Series(c)
            df = df[['close', 'open', 'high', 'low', 'macd', 'macds']]
            df = df.assign(signal=c.values)
            df = ti.filter_signals(df)
            #print(df.head())
            returns_list = ti.calc_returns(df)
            #print(returns_list)
            cumulative_returns = ti.cumulative_returns(returns_list)
        except Exception as e:
            print(e)

    def test15(self):
        print('TEST 15 - Create MACD Crossover Dataframe')
        try:
            df = pd.read_csv('data/{}/{}-{}.csv'.format(symbol, symbol, default_date))
            df = ti.create_crossover_df(df, 'macd', 'macds')
            df = ti.filter_signals(df)
            print(df.head())
            returns_list = ti.calc_returns(df)
            cumulative_returns = ti.cumulative_returns(returns_list)
        except Exception as e:
            print(e)

    def test16(self):
        print('TEST 16 - Create RSI Bound Crossover Dataframe')
        try:
            df = pd.read_csv('data/{}/{}-{}.csv'.format(symbol, symbol, default_date))
            df = ti.create_bound_crossover_df(df, 'rsi_14')
            df = ti.filter_signals(df)
            df = ti.remove_duplicates(df, 'signal')
            print(df.head())
            returns_list = ti.calc_returns(df)
            cumulative_returns = ti.cumulative_returns(returns_list)
        except Exception as e:
            print(e)

    def test17(self):
        print('TEST 17 - Brute Force Optimize RSI')
        #try:
        df = pd.read_csv('data/{}/{}-{}.csv'.format(symbol, symbol, default_date))
        sub_df = df[['close', 'open', 'high', 'low', 'timestamp']]
            #df = ti.convert2stockstats(df)
        sub_df = ti.convert2stockstats(sub_df)
        rsi_win = list(range(3, 50))
        mv_win = list(range(3,50))
        max = 0
        for rs in rsi_win:

            df = ti.create_indicator_df(sub_df, 'rsi_{}'.format(rs))
            #print(copy_df.head())
            #break
            print(rs)
            for mv in mv_win:
                #print(rs)
                copy_df = ti.create_bound_crossover_df(df, 'rsi_{}'.format(rs), mv)
                copy_df = ti.filter_signals(copy_df)
                copy_df = ti.remove_duplicates(copy_df, 'signal')
                #print(df.head())
                returns_list = ti.calc_returns(copy_df)

                cumulative_returns = ti.cumulative_returns(returns_list, output = False)
                if cumulative_returns > max:
                    optim = (rs, mv)
                    sr = ti.calc_sharpe(copy_df)
                    max = cumulative_returns
        print('OPTIM: {}'.format(optim))
        print('SHARPE RATIO: {}'.format(sr))
        print('MAX: {}'.format(max))



        #except Exception as e:
         #   print('ERROR: {}'.format(e))



if __name__ == '__main__':
    x = ti_test()
    #x.test1()
    #x.test2()
    #x.test3()
    #x.test4()
    #x.test5()
    #x.test6()
    #x.test7()
    #x.test8()
    #x.test9()
    #x.test10()
    #x.test11()
    #x.test12()
    #x.test13()
    #x.test14()
    #x.test15()
    #x.test16()
    x.test17()
    #x.test18()

    print('TESTS COMPLETE!')

