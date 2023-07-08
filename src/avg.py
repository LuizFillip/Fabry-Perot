import FabryPerot as fp
import pandas as pd
import datetime as dt
from utils import time2float
import os 


def sep_direction_(df, seq, reindex = False):

    ds = df.loc[df['dir'] == seq, 
                ['vnu', 'dvnu', 'time']]
    
    ts = fp.resample_and_interpol(
        ds, freq = '5min')['vnu']
    
    if reindex:
        ts.index = time2float(
            ts.index, sum24_from = 20)
    
    return ts

def fn2dn(filename):
    dn = filename.split('.')[0].split('_')[-1]
    return dt.datetime.strptime(dn, '%Y%m%d')  

        

def interpol_directions(infile):
    
    files = os.listdir(infile)

    out_days = []
    for filename in files:
        dn  = fn2dn(filename)
    
        if (dn.year == 2013):
            
            df = fp.FPI(infile + filename).wind
            
            df = df.loc[~((df['vnu'] < -200) | 
                          (df['vnu'] > 200))]
            
            out_dir =  []
            
            try:
                for seq in ['west', 'east', 
                            'south', 'north']:
                    ts = sep_direction_(df, seq)
                    
                    out_dir.append(ts.to_frame(seq))
                  
            except:
                continue
            
            out_days.append(
                pd.concat(out_dir, axis = 1)
                )
    return pd.concat(out_days).sort_index()

def main():
    infile = 'database/FabryPerot/caj/'
    
    ds = interpol_directions(infile)
    
    # ds.to_csv()
