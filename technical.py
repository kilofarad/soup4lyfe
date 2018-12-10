import numpy as np
import pandas as pd

from datetime import date
from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox, column
from bokeh.models import ColumnDataSource, Span
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

client_select = Select(title="Client:", value="BTC", options=tickers)
#hit_date = DateRangeSlider(title="Date Range: ", start=date(2018, 1, 1), end=date.today(),
 #                          value=(date(2018, 8, 1), date(2018, 9, 1)), step=1)
#hit_input = TextInput(value="", title="Comment:")


explanation = Div(text = '''
                        <b>General Explanation of Crossover Trading with Moving Averages</b><br>
                        <em>For each indicator featured here...</em>
                        <li>Trades are only taken in the direction of the trend. For an uptrend only take longs. For a downtrend only take shorts (puts).</li>
                        <li>During a downtrend the indicator must move above a certain bound (the green dashed lines) to indicate a pullback. When the indicator crosses back below its moving average (can be at any number, as long as the indicator is or was above the bound) go short.</li>
                        <li>During an uptrend the indicator must move below a certain bound to indicate a pullback. When the RSI crosses back above its moving average (can be at any number, just as long as indicator is or was below the bound) go long.</li>
                        <br>
                        <em>For Relative Strength Index (RSI)</em>, we use an upper bound of 60 and a lower bound of 40.<br>
                        <em>For Triple Exponential Averages (TRIX)</em>, we use a center bound of 0.<br>
                        <em>For Williams Percentage R (WPR)</em>, we use a center bound of 50.
                        <br><br>
                        <em>RSI = 100 – [100 / ( 1 + (Average of Upward Price Change / Average of Downward Price Change ) ) ]</em>
                        <br><br>
                        <em>The TRIX is calculated using a triple smoothed exponential moving average (equal to three consecutive exponential moving averages). <br>
                        TRIX = Difference between the previous and current moving average values</em>
                        <br><br>
                        <em>WPR = (highest high – closing price) / (highest high – lowest low) * -100</em>
                        
                        
                        
                         ''', width = 400, height = 375)
# RSI
brute_results_rsi = ti.brute_force_opt(df, 'rsi', 23, 24, 3, 4, 40, 60, dupe_bool=True)
rsi = Div(text='''
                <b>Optimized Relative Strength Index</b>
                <br>
                Optimal Windows for (RSI Moving Avg, Simple Moving Avg): {}
                <br>
                Optimized RSI Cumulative Trade Returns: {}%
                <br><br>
               
                '''.format(brute_results_rsi[0], round(brute_results_rsi[2]*100, 2)),
            width=400, height=70)

mask_rsi = (brute_results_rsi[3]['signal'] == 'Sell')
rsi_df = brute_results_rsi[3].loc[mask_rsi]


rsi_src = brute_results_rsi[4]
rsi_src['timestamp'] = pd.to_datetime(rsi_src['timestamp'])
rsi_src = ColumnDataSource(rsi_src)
rsi_p = figure(x_axis_type='datetime', title='Optimized Relative Strength Indicator')
rsi_p.line('timestamp', 'ma', source = rsi_src, color = 'blue', legend = 'RSI Moving Average')
rsi_p.line('timestamp', 'rsi_23', source = rsi_src, color = 'red', legend = 'RSI')
upper_bound = Span(location=60, dimension='width', line_color='green', line_width=0.5, line_dash = 'dashed')
lower_bound = Span(location=40, dimension='width', line_color='green', line_width=0.5, line_dash = 'dashed')
rsi_p.renderers.extend([upper_bound, lower_bound])
rsi_p.legend.location = "top_right"
rsi_p.legend.click_policy = "mute"
rsi_p.yaxis.axis_label = "RSI"
rsi_p.xaxis.axis_label = "Date"
#print(rsi_ma_df.head())
#rsi_df['color'] = 'white'
#rsi_p = tv.plot_crypto_spread(rsi_df)

# TRIX
brute_results_trix = ti.brute_force_opt(df, 'trix', 12, 13, 3, 4, 0, 0, dupe_bool=True, ma = True)
trix = Div(text='''
                <b>Optimized TRIX</b>
                <br>
                Optimal Windows for (TRIX Moving Avg, Simple Moving Avg): {}
                <br>
                Optimized TRIX Cumulative Trade Returns: {}%
                '''.format(brute_results_trix[0], round(brute_results_trix[2]*100, 2)),
            width=400, height=70)

mask_trix = (brute_results_trix[3]['signal'] == 'Sell')
trix_df = brute_results_trix[3].loc[mask_trix]

trix_src = brute_results_trix[4]
trix_src['timestamp'] = pd.to_datetime(trix_src['timestamp'])
trix_src = ColumnDataSource(trix_src)
trix_p = figure(x_axis_type='datetime', title='Optimized Triple Exponential Average (TRIX)')
trix_p.line('timestamp', 'ma', source = trix_src, color = 'blue', legend = 'Simple Moving Average')
trix_p.line('timestamp', 'trix_12_sma', source = trix_src, color = 'red', legend = 'TRIX')
middle_bound = Span(location=0, dimension='width', line_color='green', line_width=0.5, line_dash = 'dashed')
trix_p.renderers.extend([middle_bound])
trix_p.legend.location = "top_right"
trix_p.legend.click_policy = "mute"
trix_p.yaxis.axis_label = "TRIX"
trix_p.xaxis.axis_label = "Date"
#trix_df['color'] = '#46A0C7'
#trix_p = tv.plot_crypto_spread(trix_df)



#WR
brute_results_wr = ti.brute_force_opt(df, 'wr', 29, 30, 5, 6, 50, 50, dupe_bool=True)
wr = Div(text='''
                <b>Williams Percentage R</b><br>
                Optimal Windows for (WR Moving Avg, Simple Moving Avg): {}
                <br>
                Optimized WR Cumulative Trade Returns: {}%
                '''.format(brute_results_wr[0], round(brute_results_wr[2]*100, 2)),
            width=450, height=70)
mask_wr = (brute_results_wr[3]['signal'] == 'Sell')
wr_df = brute_results_wr[3].loc[mask_wr]

wr_src = brute_results_wr[4]
wr_src['timestamp'] = pd.to_datetime(wr_src['timestamp'])
wr_src = ColumnDataSource(wr_src)
wr_p = figure(x_axis_type='datetime', title='Optimized Williams Percentage R')
wr_p.line('timestamp', 'ma', source = wr_src, color = 'blue', legend = 'Simple Moving Average')
wr_p.line('timestamp', 'wr_29', source = wr_src, color = 'red', legend = 'WPR')
middle_bound = Span(location=50, dimension='width', line_color='green', line_width=0.5, line_dash = 'dashed')
wr_p.renderers.extend([middle_bound])
wr_p.legend.location = "top_right"
wr_p.legend.click_policy = "mute"
wr_p.yaxis.axis_label = "WPR"
wr_p.xaxis.axis_label = "Date"
#wr_df['color'] = '#0C194D'
#wr_p = tv.plot_crypto_spread(wr_df)

frames = [rsi_df, trix_df, wr_df]
colors = ['white','#46A0C7','#0C194D']
#indicator_df = pd.concat(frames)



p = tv.plot_multiple_spreads(frames, ['RSI', 'TRIX', 'WR'], colors)


#hit_outputs = column(p, rsi, trix, wr, macd)
technical_outputs1 = column(p, rsi_p)
technical_outputs2 = column(trix_p, wr_p)
technical_inputs = column(client_select, rsi, trix, wr, explanation)
technical_tab = Panel(child = row(technical_inputs, technical_outputs1, technical_outputs2), title = "TECHNICAL INDCATORS")
#hits_tab = Panel(child=row(hit_select, hit_input, hit_month, hit_year, hits_hbar, hits_pie), title="HITS")



tabs = Tabs(tabs = [technical_tab])

curdoc().add_root(tabs)
#curdoc().add_root(row(hits_hbar, hits_pie))
curdoc().title = "Trade Strat"