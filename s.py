import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler, RobustScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV, cross_val_predict
from sklearn.metrics import confusion_matrix
from scipy.stats import describe

def model_cross_val_predict(X, y, robust = False):
    scaler = RobustScaler() if robust else StandardScaler()
    model = MLPClassifier()
    model.fit(X, y)
    y_pr = cross_val_predict(model, X, y) 
    return y_pr

def load_X_returns(csv):
    df = pd.read_csv(csv).dropna()
    df = df[ np.all(df != np.inf, axis = 1) ] #remove rows with infinite values
    X = df.drop( df.columns[range(10)], axis = 1 )
    returns = (df.close - df.open)/df.open # y is percentage return. is this the best idea!?
    return X, returns


def kat(p_return, hold_cutoff = 0.01, max_classes=5):
    return np.sign(p_return)*max_classes if np.abs(p_return) > hold_cutoff else np.trunc(p_return/hold_cutoff*max_classes) 


X, returns = load_X_returns('data/BTC/BTC-2018-11-27.csv')

def sharpe_ratio(y, returns, rrr = 0):
    ra_rb = y*returns - rrr
    num = np.mean(ra_rb)
    den = np.std(ra_rb)
    if den == 0:
        return 0
    return num/den
def bf(X, returns):
    data = []
    for max_classes in range(1,6):
        for hold_cutoff in np.arange(0.01, 0.10, 0.01):
            y = returns.apply( lambda x: kat(x, hold_cutoff, max_classes) ).values
            y_pr = model_cross_val_predict(X, y)
            sr = sharpe_ratio(y, returns)
            sr_pr = sharpe_ratio(y_pr, returns)
            data.append( tuple([sr, sr_pr, max_classes, hold_cutoff]) )
    return data

import matplotlib.pyplot as plt
for a in range(9):
    print(a)
    data = bf(X, returns)
    for sr, sr_pr, mc, hc in data:
        if sr_pr > 0:
            plt.plot(mc, hc, 'ko', ms = sr_pr*100, alpha = 0.3)
        else:
            plt.plot(mc, hc, 'ro', ms = sr_pr*-100, alpha = 0.3)

plt.show()

'''
def bsh(p_return, hold_cutoff = 0.01, hc_buy = 0.01, hc_sell = 0.01):
    '0 is sell 1 is buy'
    if hold_cutoff != 0.01:
        hc_buy = hold_cutoff
        hc_sell = hold_cutoff
    if p_return < 0 and p_return*-1 > hc_sell:
        return 0
    if p_return > 0 and p_return > hc_buy:
        return 1

fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(cm)
plt.title('Confusion matrix of the classifier')
fig.colorbar(cax)
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()
'''
# first generate with specified labels
# labels = [ ... ]
# cm = confusion_matrix(ypred, y, labels)

# then print it in a pretty way
# print_cm(cm, labels)

#TODO: sharpe ratio, add emmyemm's nlp, bucket the kat function for classes
