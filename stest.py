import scikit as sk

X, returns = sk.load_X_returns('data/BTC/BTC-2018-11-27.csv')

def bf(X, returns):
    data = []
    for max_classes in range(1,5):
        for hold_cutoff in np.arange(0.01, 0.07, 0.03):
            y = returns.apply( lambda x: sk.kat(x, hold_cutoff, max_classes) ).values
            y_tr, y_pr = sk.model_cross_val_predict(X, y)
            ret = returns.values[30:]
            sr = sk.sharpe_ratio(y_tr/max_classes, ret)
            sr_pr = sk.sharpe_ratio(y_pr/max_classes, ret)
            data.append( tuple([sr, sr_pr, max_classes, hold_cutoff]) )
    return data

import matplotlib.pyplot as plt
data_ = list()
for a in range(3):
    print(a)
    data = bf(X, returns)
    data_.append(data)
    for sr, sr_pr, mc, hc in data:
        if sr_pr > 0:
            plt.plot(mc, hc, 'ko', ms = sr_pr*500, alpha = 0.3)
        else:
            plt.plot(mc, hc, 'ro', ms = sr_pr*-500, alpha = 0.3)

plt.show()


