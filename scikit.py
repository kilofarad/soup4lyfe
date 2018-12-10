import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler, RobustScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV, cross_val_predict, TimeSeriesSplit
from sklearn.metrics import confusion_matrix
from scipy.stats import describe

def model_cross_val_predict(X, y, model = MLPClassifier(), robust = False):
    '''Takes in X and y matrices, along with an sklearn model object and returns predictions
    from the thirtieth day until the end.

    Despite the name, this uses an atypical cross-validation methodology to better suit the time-series data.
    The methodology is based on sklearn's TimeSeriesSplit, but was adapted to retrain the model
    for each daily prediction.'''
    scaler = RobustScaler() if robust else StandardScaler()
    X = X.values.reshape(-1,1)
    y_pr = list()
    y_tr = list()
    for a in np.arange(30, y.shape[0]):
        X_tmp = X[:a]
        y_tmp = y[:a]
        model.fit(X_tmp, y_tmp)
        y_pr.append( model.predict( X[a].reshape(1, -1 ) ) )
        y_tr.append( y[a] )
    return np.array(y_tr), np.array(y_pr)

def load_X_returns(csv, X_cols = []):
    '''Loads X matrix and a corresponding time-shifted next-day returns column to use to generate the y matrix.
    Loads from a given csv path, and only keeps the columns in X_cols if the parameter is present'''
    df = pd.read_csv(csv).dropna()
    df = df[ np.all(df != np.inf, axis = 1) ] #remove rows with infinite values
    X = df[ X_cols ] if X_cols else df
    returns = (df.close - df.open)/df.open
    X['returns'] = returns
    returns = returns.shift(-1).dropna()
    X = X.iloc[:X.shape[0] - 1]
    return X, returns


def kat(p_return, hold_cutoff = 0.01, max_classes=3):
    '''Takes a single percentage return, and returns the class it belongs to.

    The hold_cutoff is the minimum absolute value for a percentage return to be classified
    as a buy/sell instead of a hold.

    The max_classes is the maximum integer value for a class. For 3, there are classes:
    -3, -2, -1, 0, 1, 2, 3.

    The sign of the class returned matches the sign of the percentage return. The integer value for the class
    is the max_classes if abs(p_return) is higher than hold_cutoff. Otherwise, the class cutoffs are evenly distributed,
    and p_returns are always rounded towards zero to the nearest integer class.
    '''
    return np.sign(p_return)*max_classes if np.abs(p_return) > hold_cutoff else np.trunc(p_return/hold_cutoff*max_classes)

def test_returns(X, ret, df, model, daily = True, bucketing = kat, _mc = 3):
    '''Takes a X matrix, returns Series, df of raw data (for compatibility with the ti library).

    Optional parameters are:
    daily: bool used for daily vs swing trading returns
    bucketing: a bucketing function
    _mc: a parameter for when the classes returned by bucketing is not the default [-3,3].'''
    y_tr, y_pr = model_cross_val_predict(X, ret.apply(bucketing), model = model)
    pred = [int(p) for p in y_pr.flatten()]
    if daily:
        pos, neg, zer = (1, -1, 0)
    else:
        pos, neg, zer = ('Sell', 'Buy', 'Hold')
    pred = [pos if p == _mc else ( neg if p == -1*_mc else zer ) for p in pred]
    while len(pred) < df.shape[0]:
        pred.insert(0, 0)
    if daily:
        df['returns'] = pd.Series(pred)*ret
        return df.returns
    else:
        df['signal'] = pred
        returns = ti.get_returns(df, duplicates = True, return_df = True)
        return returns[ returns.signal == 'Sell']

def sharpe_ratio(y, returns, rrr = 0):
    '''Calculates and returns the sharpe ratio'''
    ra_rb = pd.Series(y)*pd.Series(returns)
    num = np.mean(ra_rb) - rrr
    den = np.std(ra_rb)
    if den == 0:
        return 0
    return num/den
