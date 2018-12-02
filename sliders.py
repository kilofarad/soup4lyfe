''' Present an interactive function explorer with slider widgets.
Scrub the sliders to change the properties of the ``sin`` curve, or
type into the title text box to update the title of the plot.
Use the ``bokeh serve`` command to run the example by executing:
    bokeh serve sliders.py
at your command prompt. Then navigate to the URL
    http://localhost:5006/sliders
in your browser.
'''
import numpy as np
import pandas as pd
import scikit as sk
import technicalIndicators as ti

from datetime import date
from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DateRangeSlider, TextInput
from bokeh.plotting import figure

# Set up data
X, ret = sk.load_X_returns('Data/BTC/BTC-2018-11-27.csv', ['close', 'high', 'low', 'volumefrom', 'volumeto', 'open'] )
df = pd.read_csv('Data/BTC/BTC-2018-11-27.csv')

from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.dummy import DummyClassifier

models = [RandomForestClassifier(), ExtraTreesClassifier(), SVC(), MLPClassifier(), DummyClassifier()]
model_strs = ['random_forest', 'extra_trees', 'svc', 'mlp', 'dummy']
'''
for model, model_str in zip(models, model_strs):
    y_tr, y_pr = sk.model_cross_val_predict(X, ret.apply(sk.kat), model = model)
    pred = [int(p) for p in y_pr.flatten()]
    pos, neg, zer = ('Sell', 'Buy', 'Hold')
    pred = [pos if p == 3 else ( neg if p == 3 else zer ) for p in pred]
    while len(pred) < df.shape[0]:
        pred.insert(0, 'Hold')
    df[model_str + '_pred'] = pred
'''
#transfer desired columns into a cleaned-up dataframe for our source
cleaned_up = pd.DataFrame()
for col in X.columns:
    cleaned_up[col] = X[col]
for model_col in model_strs:
    pass #cleaned_up[model_str + '_pred'] = df[model_str + '_pred']
cleaned_up['timestamp'] = pd.to_datetime(df.timestamp)
source = ColumnDataSource(cleaned_up)

# Set up plot
plot = figure(plot_height=400, plot_width=400, title="my sine wave",
              tools="crosshair,pan,reset,save,wheel_zoom")

plot.line('timestamp', 'returns', source=source, line_width=3, line_alpha=0.6)


# Set up widgets
text = TextInput(title="title", value='my sine wave')
date_range = DateRangeSlider(title="date range", start=date(2018, 2, 1), end=date(2018, 11, 27),
                           value=(date(2018, 8, 1), date(2018, 11, 27)), step=1)


# Set up callbacks
def update_title(attrname, old, new):
    plot.title.text = text.value

text.on_change('value', update_title)

def update_data(attrname, old, new):
    plot.x_range = date_range.value

for w in [date_range]:
    w.on_change('value', update_data)

# Set up layouts and add to document
inputs = widgetbox(text, date_range)

curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "Sliders"
