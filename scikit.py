import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler, RobustScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV, cross_val_predict, TimeSeriesSplit
from sklearn.metrics import confusion_matrix
from scipy.stats import describe

def model_cross_val_predict(X, y, model = MLPClassifier(), robust = False):
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

def load_X_returns(csv, X_cols):
    df = pd.read_csv(csv).dropna()
    df = df[ np.all(df != np.inf, axis = 1) ] #remove rows with infinite values
    X = df[ X_cols ] if X_cols else pd.DataFrame()
    returns = (df.close - df.open)/df.open 
    X['returns'] = returns
    returns = returns.shift(-1).dropna()
    X = X.iloc[:X.shape[0] - 1]
    return X, returns


def kat(p_return, hold_cutoff = 0.01, max_classes=3):
    return np.sign(p_return)*max_classes if np.abs(p_return) > hold_cutoff else np.trunc(p_return/hold_cutoff*max_classes) 


def sharpe_ratio(y, returns, rrr = 0):
    y = pd.Series(y)
    a = pd.Dataframe()
    a['Movement'] = y
    a['Return'] = a
    ra_rb = 0
    num = np.mean(ra_rb)
    den = np.std(ra_rb)
    if den == 0:
        return 0
    return num/den

'''
def bsh(p_return, hold_cutoff = 0.01, hc_buy = 0.01, hc_sell = 0.01):
    '0 is sell 1 is buy'
    if hold_cutoff != 0.01:
        hc_buy = hold_cutoff
        hc_sell = hold_cutoff
    
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
