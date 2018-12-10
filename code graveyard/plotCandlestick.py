import mpl_finance as fin
from matplotlib import pyplot as plt
#from matplotlib import finance as fin
import pandas as pd
import os

folder  =  os.path.join(os.getcwd(), 'csv')
csvs = [f for f in os.listdir(folder) if f.endswith('.csv')]
outFolder = os.path.join(os.getcwd(), 'img')

for csv in csvs:
    df = pd.read_csv(os.path.join(folder,csv),",")
    ochl = df[['open','close','high','low']]
    rows = len(df.index)
    for i in range(rows//60):
        b = i*60
        e = 60*(i+1)
        ochl60 = ochl.iloc[b:e]
        ochl_tuples = [tuple(x) for x in ochl60.to_records(index = True)]
        fig  =  plt.figure()
        ax  =  plt.axes()
        fin.candlestick_ochl(ax,ochl_tuples)
        filename = csv.split()[0] + ' ' + str(df['time'].iloc[b]) + ' to ' + str(df['time'].iloc[e-1]) + '.png'
        fig.savefig(os.path.join(outFolder,filename))
        plt.close(fig)
