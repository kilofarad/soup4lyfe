import numpy as np
import pandas as pd
import scikit as sk
import technicalIndicators as ti

from bokeh.io import curdoc
from bokeh.layouts import column, gridplot
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral11
from bokeh.models.widgets import Div
from bokeh.plotting import figure

# Set up data
X, ret = sk.load_X_returns('Data/BTC/BTC-2018-11-27-sent.csv', ['close', 'high', 'low', 'volumefrom', 'volumeto', 'open', 'title_sent_pos', 'title_sent_neg', 'title_sent_neu', 'title_sent_compound', 'bdy_sent_pos', 'bdy_sent_neg', 'bdy_sent_neu', 'bdy_sent_compound'] )
df = pd.read_csv('Data/BTC/BTC-2018-11-27.csv')

#Import all of the classifiers we want to test
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.dummy import DummyClassifier

#Define these for programmatic evaluation
models = [RandomForestClassifier(), ExtraTreesClassifier(), SVC(), MLPClassifier(), DummyClassifier()]
model_strs = ['random_forest', 'extra_trees', 'svc', 'mlp', 'dummy']

#calculate returns
for model, model_str in zip(models, model_strs):
    df[model_str + '_returns'] = sk.test_returns(X, ret, df, model)

#calculate the returns for the technical indicators
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

#transfer over the parameters used to train our ML models
for col in X.columns:
    cleaned_up[col] = X[col]

#transfer over returns and calculate cumulative returns while we're at it
for model_col in model_strs:
    cleaned_up[model_col + '_returns'] = df[model_col + '_returns'].replace(np.nan, 0)
    cleaned_up[model_col + '_cumulative_returns'] = np.cumsum(cleaned_up[ model_col + '_returns' ])
for tech_str in tech_strs:
    cleaned_up[tech_str + '_returns'] = df[tech_str + '_returns']
    cleaned_up[tech_str + '_cumulative_returns'] = np.cumsum(cleaned_up[ tech_str + '_returns' ].replace(np.nan, 0))

#make sure our timestamp is a datetime!
cleaned_up['timestamp'] = pd.to_datetime(df.timestamp)

#finally, wrap it up in a bokeh data source object
source = ColumnDataSource(cleaned_up)

# define titles, columns, and scatter vs line for our plots
titles = [ 'Daily Open/Close BTC-USD Prices',
            'Volume (USD)',
            'Daily High/Low BTC-USD Prices',
            'Body Sentiment Analysis',
            'Title Sentiment Analysis',
            'ML Strategy Daily Percent Returns',
            'ML Strategy Cumulative Percent Returns',
            'Technical Indicator Percent Returns',
            'Technical Indicator Cumulative Percent Returns' ]

cols_to_plot = [ ['open', 'close'],
            ['volumeto'],
            ['high', 'low'],
            ['bdy_sent_pos', 'bdy_sent_neg', 'bdy_sent_neu', 'bdy_sent_compound'],
            ['title_sent_pos', 'title_sent_neg', 'title_sent_neu', 'title_sent_compound'] ,
            [model + '_returns' for model in model_strs],
            [model + '_cumulative_returns' for model in model_strs] ,
            [tech + '_returns' for tech in tech_strs],
            [tech + '_cumulative_returns' for tech in tech_strs]]

legend_labels = [ ['open', 'close'],
                ['volumeto'],
                ['high', 'low'],
                ['positive', 'negative', 'neutral', 'compound'],
                ['positive', 'negative', 'neutral', 'compound'] ,
                [model for model in model_strs],
                [model for model in model_strs] ,
                [tech for tech in tech_strs],
                [tech for tech in tech_strs]]

scatter = [ False,
            False,
            False,
            False,
            False,
            True,
            False,
            True,
            False ]

plots = []
# Set up plot
for cols, title, scatter, legend_lab in zip(cols_to_plot, titles, scatter, legend_labels):
    if plots:
        plot = figure(plot_height=400, plot_width=800, x_axis_type = 'datetime', title=title,
                    x_range=plots[0].x_range, tools="crosshair,pan,reset,save,box_zoom")
    else:
        plot = figure(plot_height=400, plot_width=800, x_axis_type = 'datetime', title=title,
              tools="crosshair,pan,reset,save,box_zoom")
    colors = Spectral11[0:len(cols)]
    for index, col in enumerate(cols):
        if scatter:
            plot.scatter('timestamp', col, source=source, color = colors[index], legend = str(legend_lab).title().replace('_', ' '))
        else:
            plot.line('timestamp', col, source=source, color = colors[index], legend = str(legend_lab).title().replace('_', ' '), line_width=3, line_alpha=0.6)
        #that sweet, sweet click to hide series in the legend
        plot.legend.click_policy="hide"
    plots.append(plot)

#setting up our welcome message
texty = Div(text="""<h1>Welcome to your interactive analytics platform.</h1>
<br />
<div style="width: 700px;overflow-x: visible;">To get started, look to the top right of the page for the Pan and Box Zoom tools.
These will help you zoom and scroll through the data across the seven different data streams that are currently visualized.
If you want to hide a series, click its entry in the legend.</div>""", width=800, height=400)
plots.insert(0, texty)

#group our plots (and our welcome message) on a 2-column grid
grid = gridplot(plots, ncols = 2)

#these three lines are our navbar,
style_str = 'width: 180px; height: 50px; line-height: 50px; display: inline-block; text-decoration: none; text-align: center; padding: 0; margin: 0;'
div_str = '<a style="%s" href="/technical">Technical Returns</a><a style="%s" href="/viz">ML & Other Indicators</a>' % (style_str, style_str)
navbar = Div(text=div_str, width = 400, height = 50)

#add our navbar abouve our grid and make that our page
curdoc().add_root(column(navbar, grid))
curdoc().title = "Visualization"
