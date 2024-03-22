import FabryPerot as fp
import pandas as pd
import os 
import base as b



DIRECTIONS = ['west', 'east', 'south', 'north']

def sep_direction_(df, seq, reindex = False):

    ds = df.loc[df['dir'] == seq, 
                ['vnu', 'dvnu', 'time']]
    
    ts = fp.resample_and_interpol(ds, freq = '10min')['vnu']
    
    if reindex:
        ts.index = b.time2float(ts.index, sum24_from = 20)
    
    return ts


def interpol_directions(infile):
        
    df = fp.FPI(infile).wind

    out =  []
    df = df.loc[~((df['vnu'] > 300) | (df['vnu'] < -300))]
    for seq in DIRECTIONS:
        try:
            ts = sep_direction_(df, seq)
            
            out.append(ts.to_frame(seq))
      
        except:
            continue
        
    return pd.concat(out, axis = 1)
        
def join_days(infile):
    
    out = []
    for filename in os.listdir(infile):
    
        out.append(interpol_directions(infile + filename))
        
    df = pd.concat(out).sort_index()
    
    df['time'] = df.index.to_series().apply(b.dn2float)
    df['day'] = df.index.day
    df = df.loc[~df.index.duplicated()]
    return df




