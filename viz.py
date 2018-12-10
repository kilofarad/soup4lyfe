import numpy as np
import pandas as pd
import scikit as sk
import technicalIndicators as ti

from datetime import date
from bokeh.io import curdoc
from bokeh.layouts import column, row, widgetbox, gridplot
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral11
from bokeh.models.ranges import Range1d
from bokeh.models.widgets import DateRangeSlider, TextInput, Div
from bokeh.plotting import figure

# Set up data
X, ret = sk.load_X_returns('Data/BTC/BTC-2018-11-27-sent.csv', ['close', 'high', 'low', 'volumefrom', 'volumeto', 'open', 'title_sent_pos', 'title_sent_neg', 'title_sent_neu', 'title_sent_compound', 'bdy_sent_pos', 'bdy_sent_neg', 'bdy_sent_neu', 'bdy_sent_compound'] )
df = pd.read_csv('Data/BTC/BTC-2018-11-27.csv')

from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.dummy import DummyClassifier

models = [RandomForestClassifier(), ExtraTreesClassifier(), SVC(), MLPClassifier(), DummyClassifier()]
model_strs = ['random_forest', 'extra_trees', 'svc', 'mlp', 'dummy']

for model, model_str in zip(models, model_strs):
    df[model_str + '_returns'] = sk.test_returns(X, ret, df, model)

tech_strs = ['rsi', 'trix', 'wr']
other_args = [(23, 24, 3, 4, 40, 60), (12, 13, 3, 4, 0, 0), (29, 30, 5, 6, 50, 50)]
for tech_str, other_arg in zip(tech_strs, other_args):
    brute_results = ti.brute_force_opt(df, tech_str, *other_arg, dupe_bool = True, ma = True if tech_str == 'trix' else False)
    mask = (brute_results[3]['signal'] == 'Sell')
    full_df = brute_results[3].loc[mask]
    full_df = full_df[['timestamp', 'close_pct_change']]
    full_df.columns = ['timestamp', tech_str + '_returns']
    df = df.merge(full_df, how = 'left', on = 'timestamp')
#transfer desired columns into a cleaned-up dataframe for our source
cleaned_up = pd.DataFrame()
for col in X.columns:
    cleaned_up[col] = X[col]
for model_col in model_strs:
    cleaned_up[model_col + '_returns'] = df[model_col + '_returns'].replace(np.nan, 0)
    cleaned_up[model_col + '_cumulative_returns'] = np.cumsum(cleaned_up[ model_col + '_returns' ])
for tech_str in tech_strs:
    cleaned_up[tech_str + '_returns'] = df[tech_str + '_returns']
    cleaned_up[tech_str + '_cumulative_returns'] = np.cumsum(cleaned_up[ tech_str + '_returns' ].replace(np.nan, 0))
cleaned_up['timestamp'] = pd.to_datetime(df.timestamp)
source = ColumnDataSource(cleaned_up)

# define important info for our plots
titles = [ 'Daily Open/Close Prices', 'Volume', 'Daily High/Low Prices', 'Body Sentiment Analysis', 'Title Sentiment Analysis', 'Modelled Strategy Daily Returns', 'Modelled Strategy Cumulative Returns', 'Technical Indicator Returns', 'Technical Indicator Cumulative Returns' ]
to_plot = [ ['open', 'close'], ['volumeto'], ['high', 'low'], ['bdy_sent_pos', 'bdy_sent_neg', 'bdy_sent_neu', 'bdy_sent_compound'], ['title_sent_pos', 'title_sent_neg', 'title_sent_neu', 'title_sent_compound'] , [model + '_returns' for model in model_strs], [model + '_cumulative_returns' for model in model_strs] , [tech + '_returns' for tech in tech_strs], [tech + '_cumulative_returns' for tech in tech_strs]]
scatter = [ False, False, False, False, False, True, False, True, False ]

plots = []
# Set up plot
for cols, title, scatter in zip(to_plot, titles, scatter):
    if plots:
        plot = figure(plot_height=400, plot_width=800, x_axis_type = 'datetime', title=title, 
                    x_range=plots[0].x_range, tools="crosshair,pan,reset,save,box_zoom")
    else:
        plot = figure(plot_height=400, plot_width=800, x_axis_type = 'datetime', title=title,
              tools="crosshair,pan,reset,save,box_zoom")
    colors = Spectral11[0:len(cols)]
    for index, col in enumerate(cols):
        if scatter:
            plot.scatter('timestamp', col, source=source, color = colors[index], legend = str(col).title().replace('_', ' '))
        else:
            plot.line('timestamp', col, source=source, color = colors[index], legend = str(col).title().replace('_', ' '), line_width=3, line_alpha=0.6)
        plot.legend.click_policy="hide"
    plots.append(plot)

texty = Div(text="""<h1>Welcome to your interactive analytics platform.</h1>
<br />
<div style="width: 700px;overflow-x: visible;">To get started, look to the top right of the page for the Pan and Box Zoom tools. These will help you zoom and scroll through the data across the seven different data streams that are currently visualized. If you want to hide a series, click its entry in the legend.</div>""", width=800, height=400)

plots.insert(0, texty)
grid = gridplot(plots, ncols = 2)

style_str = 'width: 180px; height: 50px; line-height: 50px; display: inline-block; text-decoration: none; text-align: center; padding: 0; margin: 0;'

div_str = '<a style="%s" href="/technical">Technical Returns</a><a style="%s" href="/viz">ML & Other Indicators</a>' % (style_str, style_str)

navbar = Div(text=div_str, width = 400, height = 50)
# Set up widgets
text = TextInput(title="title", value='my sine wave')
date_range = DateRangeSlider(title="date range", start=date(2018, 2, 1), end=date(2018, 11, 27),
                           value=(date(2018, 8, 1), date(2018, 11, 27)), step=1)


# Set up callbacks
def update_title(attrname, old, new):
    plot.title.text = text.value

text.on_change('value', update_title)

def update_data(attrname, old, new):
    r = Range1d(start = date_range.value[0], end = date_range.value[1])

for w in [date_range]:
    w.on_change('value', update_data)

# Set up layouts and add to document
inputs = widgetbox(text, date_range)

curdoc().add_root(column(navbar, grid))
curdoc().title = "Visualization"
