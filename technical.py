import numpy as np
import pandas as pd

from datetime import date
from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox, column
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput, Panel, Tabs, Select, Button, DateRangeSlider, Paragraph, Div
from bokeh.plotting import figure

import technicalIndicators_unittest as tiu
import technicalIndicators as ti
import technicalVis as tv
import json


# READ IN DATA
symbol = 'BTC'
comparison_symbol = 'USD'
default_date = '2018-11-27'

tickers = ['BTC']
df = pd.read_csv('data/{}/{}-{}.csv'.format(symbol, symbol, default_date))

x = tiu.ti_test()

# HIT TYPES

hit_select = Select(title="Client:", value="BTC", options=tickers)
#hit_date = DateRangeSlider(title="Date Range: ", start=date(2018, 1, 1), end=date.today(),
 #                          value=(date(2018, 8, 1), date(2018, 9, 1)), step=1)
#hit_input = TextInput(value="", title="Comment:")



# RSI
brute_results_rsi = ti.brute_force_opt(df, 'rsi', 23, 24, 3, 4, 40, 60, dupe_bool=True)
rsi = Div(text='''
                <b>Optimal Window for (RSI Moving Avg, Simple Moving Avg)</b>: {}
                <br><br>
                <b>Optimized RSI Cumulative Trade Returns</b>: {}%
                '''.format(brute_results_rsi[0], round(brute_results_rsi[2]*100, 2)),
            width=500, height=70)

mask_rsi = (brute_results_rsi[3]['signal'] == 'Sell')
rsi_df = brute_results_rsi[3].loc[mask_rsi]
#rsi_df['color'] = 'white'
#rsi_p = tv.plot_crypto_spread(rsi_df)

# TRIX
brute_results_trix = ti.brute_force_opt(df, 'trix', 12, 13, 3, 4, 0, 0, dupe_bool=True, ma = True)
trix = Div(text='''
                <b>Optimal Window for (TRIX Moving Avg, Simple Moving Avg)</b>: {}
                <br><br>
                <b>Optimized TRIX Cumulative Trade Returns</b>: {}%
                '''.format(brute_results_trix[0], round(brute_results_trix[2]*100, 2)),
            width=500, height=70)

mask_trix = (brute_results_trix[3]['signal'] == 'Sell')
trix_df = brute_results_trix[3].loc[mask_trix]
#trix_df['color'] = '#46A0C7'
#trix_p = tv.plot_crypto_spread(trix_df)

#WR
brute_results_wr = ti.brute_force_opt(df, 'wr', 29, 30, 5, 6, 50, 50, dupe_bool=True)
wr = Div(text='''
                <b>Optimal Window for (WR Moving Avg, Simple Moving Avg)</b>: {}
                <br><br>
                <b>Optimized WR Cumulative Trade Returns</b>: {}%
                '''.format(brute_results_wr[0], round(brute_results_wr[2]*100, 2)),
            width=500, height=70)
mask_wr = (brute_results_wr[3]['signal'] == 'Sell')
wr_df = brute_results_wr[3].loc[mask_wr]
#wr_df['color'] = '#0C194D'
#wr_p = tv.plot_crypto_spread(wr_df)

# MACD
df = pd.read_csv('data/{}/{}-{}.csv'.format(symbol, symbol, default_date))
col1 = ti.get_col_index(df, 'macd')
col2 = ti.get_col_index(df, 'macds')
c = []
for x in range(len(df['timestamp'])):
    c.append(ti.crossover(df, x, col1, col2))
c = pd.Series(c)
df = df[['close', 'open', 'high', 'low', 'macd', 'macds', 'timestamp']]
df = df.assign(signal=c.values)
df = ti.filter_signals(df)
returns_list, macd_df = ti.calc_returns2(df)
cumulative_returns = ti.cumulative_returns(returns_list)

macd = Div(text='''
                <b>Optimized MACD Cumulative Trade Returns</b>: {}%
                '''.format(round(cumulative_returns*100,2)),
            width=500, height=70)

mask_macd = (macd_df['signal'] == 'Sell')
macd_df = macd_df.loc[mask_macd]


frames = [rsi_df, trix_df, wr_df, macd_df]
colors = ['white','#46A0C7','#0C194D', 'red']
#indicator_df = pd.concat(frames)



p = tv.plot_multiple_spreads(frames, ['RSI', 'TRIX', 'WR', 'MACD'], colors)


#hit_outputs = column(p, rsi, trix, wr, macd)
hit_outputs = column(p)
hit_inputs = column(hit_select, rsi, trix, wr, macd)
hits_tab = Panel(child = row(hit_inputs, hit_outputs), title = "REPORT")
#hits_tab = Panel(child=row(hit_select, hit_input, hit_month, hit_year, hits_hbar, hits_pie), title="HITS")



tabs = Tabs(tabs = [hits_tab])

curdoc().add_root(tabs)
#curdoc().add_root(row(hits_hbar, hits_pie))
curdoc().title = "Trade Strat"