
import pandas as pd

from datetime import date

from bokeh.plotting import figure, show
from bokeh.io import output_notebook, output_file
from bokeh.models import HoverTool, ColumnDataSource, LinearAxis, Range1d, Legend, LabelSet, Label, OpenURL, TapTool
from bokeh.layouts import row
from bokeh.palettes import Blues8, Category20c
from bokeh.core.properties import value
from bokeh.transform import cumsum

import technicalIndicators as ti



def plot_crypto_spread(indicator_df, title = 'Optimized Returns Scatterplot'):
    '''

    :param src: ColumnDataSource object of Vader-processed CryptoCompare News
    :param title: name of plot
    :return: Bokeh figure of scatter plot of CryptoCompare-tracked hits

    Generate spread of Crypto News
    '''
    #print(indicator_df.head())
    indicator_df['timestamp'] = pd.to_datetime(indicator_df['timestamp'])
    src = ColumnDataSource(indicator_df)
    print(src.data.keys())
    print(src.data)
    print(src.data['timestamp'])
    hover = HoverTool(  # Add annotations on hover
        tooltips='''
            <div>
                <div>
                    <span style = "font-weight:bold;">Date:</span>
                    @timestamp{%F}
                </div>
                <div>
                    <span style = "font-weight:bold;">Return</span>
                    @close_pct_change
                </div>
            </div>
            ''',

        formatters={
            'timestamp': 'datetime',  # use 'datetime' formatter for 'date' field
            'close_pct_change': 'printf',  # use 'printf' formatter for 'adj close' field
            # use default 'numeral' formatter for other fields
        },

        # display a tooltip whenever the cursor is vertically in line with a glyph
        mode='vline'
    )
    p = figure(x_axis_type='datetime', title=title)
    p.circle('timestamp', 'close_pct_change', source = src, color = 'color', line_color = 'black', size = 10)
    p.background_fill_color = "#3e3e3e"
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.yaxis.axis_label = "Return"
    p.xaxis.axis_label = "Date"

    p.add_tools(hover)
    return(p)

def plot_multiple_spreads(sources, names, colors, title = 'Optimized Returns Scatterplot'):
    hover = HoverTool(  # Add annotations on hover
        tooltips='''
                <div>
                    <div>
                        <span style = "font-weight:bold;">Date:</span>
                        @timestamp{%F}
                    </div>
                    <div>
                        <span style = "font-weight:bold;">Return</span>
                        @close_pct_change
                    </div>
                </div>
                ''',

        formatters={
            'timestamp': 'datetime',  # use 'datetime' formatter for 'date' field
            'close_pct_change': 'printf',  # use 'printf' formatter for 'adj close' field
            # use default 'numeral' formatter for other fields
        },

        # display a tooltip whenever the cursor is vertically in line with a glyph
        mode='vline'
    )
    p = figure(x_axis_type='datetime', title=title)
    for df, name, color in zip(sources, names, colors):
        #df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        src = ColumnDataSource(df)
        #p.circle(df['timestamp'], df['close_pct_change'], color=color, line_color = 'black', size = 10, legend = name)
        p.circle('timestamp', 'close_pct_change', source = src, color = color, line_color = 'black', size = 10, legend = name)
    p.legend.location = "top_right"
    p.legend.click_policy = "mute"
    p.yaxis.axis_label = "Return"
    p.xaxis.axis_label = "Date"
    p.add_tools(hover)

    return p
