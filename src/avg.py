import FabryPerot as fp
import pandas as pd
import os 
import base as b
import datetime as dt 



DIRECTIONS = ['west', 'east', 'south', 'north']

def sep_direction_(
        df, seq, 
        parameter = 'vnu', 
        reindex = False
        ):
    
    if parameter == 'vnu':
        cols = ['vnu', 'dvnu', 'time']
        
    elif parameter == 'rle':
        cols = ['rle', 'drle', 'time']
        
    else:
        cols = ['tn', 'dtn', 'time']
                
    ds = df.loc[df['dir'] == seq, cols]
    
    ts = fp.resample_and_interpol(ds, freq = '10min')[parameter]
    
    if reindex:
        ts.index = b.time2float(ts.index, sum_from = 20)
    
    return ts


def interpol_directions(
        infile, 
        parameter = 'vnu',
        wind_threshold = 300, 
        temp_threshold = 1500
        ):
    
    if parameter == 'vnu':
        df = fp.FPI(infile).wind
    
        
        df = df.loc[~(
            (df['vnu'] > wind_threshold) | 
            (df['vnu'] < -wind_threshold))
            ]
        
    elif parameter == 'rle':
        
        df = fp.FPI(infile).bright
        
    else:
        df = fp.FPI(infile).temp  
        
    out =  []
    for seq in DIRECTIONS:
        try:
            ts = sep_direction_(df, seq, parameter = parameter)
            
            out.append(ts.to_frame(seq))
      
        except:
            continue
        
    return pd.concat(out, axis = 1)


def resample_new_index(ds, freq = '10min'):
    
    times = ds.index
    
    start = times[0].replace(minute = 0, second = 0) 
    end = times[-1].replace(minute = 0, second = 0) 
    
    df1 = pd.DataFrame(
        index = pd.date_range(start, end, freq = freq)
        )
    
    df = pd.concat([ds, df1], axis = 1).interpolate()
    
    df['time2'] = b.time2float(df.index, sum_from = 20)
    
    return df.resample(freq).asfreq()





        
def join_days(ref_date, in_month = True, parameter = 'tn'):
    
    infile = 'database/FabryPerot/cj/'
    
    if in_month:
        
        files = file_of_the_month(ref_date, infile)
    else:
        
        files = get_window_of_dates(ref_date)


    out = []
    for filename in files:
        f = os.path.join(infile, filename)
        out.append(interpol_directions(f, parameter))
        
    df = pd.concat(out).sort_index()
    
    df['time'] = df.index.to_series().apply(b.dn2float)
    df['day'] = df.index.day
    df = df.loc[~df.index.duplicated()]
    return df



# 

# files = os.listdir(infile)

# dn = dt.datetime(2022, 7, 24)
# infile = 'database/FabryPerot/cj/'
dn = dt.datetime(2022, 7, 24, 21)
infile = 'database/FabryPerot/cj/bfp220724g.7100.txt'
 
df = fp.FPI(infile).bright

seq = 'west'
# ts = sep_direction_(df, seq, parameter = 'rle')

ds = df.loc[df['dir'] == seq]


resample_new_index(ds)