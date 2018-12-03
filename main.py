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
import json


# READ IN DATA
symbol = 'BTC'
comparison_symbol = 'USD'
default_date = '2018-11-27'

tickers = ['BTC', 'ETH', 'DASH']
df = pd.read_csv('data/{}/{}-{}.csv'.format(symbol, symbol, default_date))

x = tiu.ti_test()

# HIT TYPES

hit_select = Select(title="Client:", value="BTC", options=tickers)
hit_date = DateRangeSlider(title="Date Range: ", start=date(2018, 1, 1), end=date.today(),
                           value=(date(2018, 8, 1), date(2018, 9, 1)), step=1)
hit_input = TextInput(value="", title="Comment:")

hit_inputs = column(hit_select, hit_date, hit_input)

# RSI
brute_results_rsi = ti.brute_force_opt(df, 'rsi', 3, 50, 3, 50, 40, 60, dupe_bool=True)
rsi = Div(text='''
                <b>RSI Optimal Parameters</b>: {}
                <br><br>
                <b>Optimized RSI Cumulative Trade Returns</b>: {}
                '''.format(brute_results_rsi[0], round(brute_results_rsi[2], 4)),
            width=400, height=200)

# TRIX
brute_results_trix = ti.brute_force_opt(df, 'trix', 3, 50, 3, 50, 0, 0, dupe_bool=True, ma = True)
trix = Div(text='''
                <b>TRIX Optimal Parameters</b>: {}
                <br><br>
                <b>Optimized TRIX Cumulative Trade Returns</b>: {}
                '''.format(brute_results_trix[0], round(brute_results_trix[2], 4)),
            width=400, height=200)

# WR
brute_results_wr = ti.brute_force_opt(df, 'wr', 3, 50, 3, 50, 50, 50, dupe_bool=True)
wr = Div(text='''
                <b>WR Optimal Parameters</b>: {}
                <br><br>
                <b>Optimized WR Cumulative Trade Returns</b>: {}
                '''.format(brute_results_wr[0], round(brute_results_wr[2], 4)),
            width=400, height=200)

# MACD
results_macd = x.test15()
macd_df = ti.create_crossover_df(df, 'macd', 'macds')
macd_df = ti.filter_signals(macd_df)
returns_list = ti.calc_returns(macd_df)
macd_returns = ti.cumulative_returns(returns_list)
macd = Div(text='''
                <b>MACD Cumulative Trade Returns</b>: {}
                '''.format(macd_returns),
            width=400, height=200)



hit_outputs = column(rsi, trix, wr, macd)
hits_tab = Panel(child = row(hit_inputs, hit_outputs), title = "REPORT")
#hits_tab = Panel(child=row(hit_select, hit_input, hit_month, hit_year, hits_hbar, hits_pie), title="HITS")



tabs = Tabs(tabs = [hits_tab])

curdoc().add_root(tabs)
#curdoc().add_root(row(hits_hbar, hits_pie))
curdoc().title = "Trade Strat"