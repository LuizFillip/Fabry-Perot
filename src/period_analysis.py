import base as b 
import numpy as np 
import pandas as pd 


infile = 'FabryPerot/data/periods/'
def load_mean(v = 'vnu'):
    
    wd = b.load(infile + f'{v}.txt')
    
    wd[v] = wd.mean(axis = 1)
    
    return wd.loc[:, [v]]


def get_similar():
    
    cols = ['vnu', 'tn']
    
    wd =  load_mean('vnu')
    tn =  load_mean('tn')

    df = wd.join(tn).dropna()
    
    df['diff'] = (df[cols[0]] - df[cols[1]]).abs()
    
    return df.loc[df['diff'] <= 0.1]

#
