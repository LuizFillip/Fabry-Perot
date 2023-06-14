import FabryPerot as fp
import pandas as pd
import datetime as dt
import numpy as np
from utils import time2float
import os 


def sep_direction_(df, seq):

    ds = df.loc[df['dir'] == seq, 
                ['vnu', 'dvnu', 'time']]
    
    ts = fp.resample_and_interpol(ds, freq = '5min')['vnu']
    
    ts.index = time2float(ts.index, sum24_from = 20)
    
    return ts

def fn2dn(filename):
    dn = filename.split('.')[0].split('_')[-1]
    return dt.datetime.strptime(dn, '%Y%m%d')  

infile = 'database/FabryPerot/caj/'
        
        

files = os.listdir(infile)



north = []

south = []

east = []

west = []

for filename in files:
    dn  = fn2dn(filename)
    
    if (dn.year == 2013) and (dn.month == 3):
        
        df = fp.FPI(infile + filename).wind
        
        df = df.loc[~(df['vnu'] > 200)]
        for seq in ['west', 'east', 'south', 'north']:
            try:
                ts = sep_direction_(df, seq)
                
                vars()[seq].append(ts.to_frame(dn))
            except:
                continue
            
            
import matplotlib.pyplot as plt


fig, ax = plt.subplots(
    nrows = 2, 
    sharex = True, 
    sharey = True
    )

def plot_coord(ax, south
               ):
    ds = pd.concat(south, axis = 1)
    
    ax.plot(ds, color = 'gray')
    
    # dn = pd.to_datetime('2013-03-17').date()
    # ax.plot(ds[dn], color = 'r')
plot_coord(ax[0], south)
plot_coord(ax[1], north)
