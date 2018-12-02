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
tickers = ['BTC', 'ETH', 'DASH']

x = tiu.ti_test()

# HIT TYPES

hit_select = Select(title="Client:", value="Dash", options=tickers)
hit_date = DateRangeSlider(title="Date Range: ", start=date(2018, 1, 1), end=date.today(),
                           value=(date(2018, 8, 1), date(2018, 9, 1)), step=1)
hit_input = TextInput(value="", title="Comment:")

hit_inputs = column(hit_select, hit_date, hit_input)

div1 = Div(text="<b>RSI Optimal Parameters (RSI Rolling Windows, Moving Average Windows)</b>: {}".format(x.test17()[0]),
width=200, height=100)

div2 = Div(text="<b>RSI Sharpe Ratio</b>: {}".format(round(x.test17()[1], 4)),
width=200, height=100)

div3 = Div(text="<b>Optimized RSI Cumulative Trade Returns</b>: {}".format(round(x.test17()[2], 4)),
width=200, height=100)

hit_outputs = column(div1, div2, div3)
hits_tab = Panel(child = row(hit_inputs, hit_outputs), title = "REPORT")
#hits_tab = Panel(child=row(hit_select, hit_input, hit_month, hit_year, hits_hbar, hits_pie), title="HITS")



tabs = Tabs(tabs = [hits_tab])

curdoc().add_root(tabs)
#curdoc().add_root(row(hits_hbar, hits_pie))
curdoc().title = "Trade Strat"