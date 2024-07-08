import FabryPerot as fp
import pandas as pd
import os 
import base as b


DIRECTIONS = ['west', 'east', 'south', 'north']

def resample_new_index(ds, freq = '10min'):
    
    times = ds.index
    
    start = times[0].replace(minute = 0, second = 0) 
    end = times[-1] #.replace(minute = 0, second = 0) 
    
    df1 = pd.DataFrame(
        index = pd.date_range(start, end, freq = freq)
        )
    
    df = pd.concat([ds, df1], axis = 1).interpolate()
        
    return df.resample(freq).asfreq()


def sep_direction_(df, seq,  parameter = 'vnu'):
    
    if parameter == 'vnu':
        cols = ['vnu', 'dvnu', 'time']
        
    elif parameter == 'rle':
        cols = ['rle', 'drle', 'time']
        
    else:
        cols = ['tn', 'dtn', 'time']
                
    ds = df.loc[df['dir'] == seq, cols]
    
    return resample_new_index(ds, freq = '10min')[parameter]

def interpol_directions(
        df, 
        parameter = 'vnu',
        wind_threshold = 400):
    
    if parameter == 'vnu':
        
        df = df.loc[~(
            (df['vnu'] > wind_threshold) | 
            (df['vnu'] < -wind_threshold))
            ]
    
    out =  []
    for seq in DIRECTIONS:
        # try:
        ts = sep_direction_(df, seq, parameter = parameter)
        
        out.append(ts.to_frame(seq))
      
    return pd.concat(out, axis = 1)



        
def join_days(ref_date, in_month = True, parameter = 'tn'):
    
    infile = 'database/FabryPerot/cj/'
    
    if in_month:
        files = fp.file_of_the_month(ref_date, infile)
    else:
        files =  fp.get_window_of_dates(ref_date)


    out = []
    for filename in files:
        f = os.path.join(infile, filename)
        out.append(interpol_directions(f, parameter))
        
    df = pd.concat(out).sort_index()
    
    df['time'] = df.index.to_series().apply(b.dn2float)
    df['day'] = df.index.day
    df = df.loc[~df.index.duplicated()]
    return df



def join_days1():
    infile = 'database/FabryPerot/car/'

    files = os.listdir(infile)

    out = []

    for file in files:
        df1 = fp.FPI(infile + file).wind
        # try:
        out.append(
            interpol_directions(df1, parameter = 'vnu'))
        # except:
        #     continue 
        
    df = pd.concat(out)

    df['doy'] = df.index.day_of_year


    df.to_csv('database/FabryPerot/mean')
    
    return df


join_days1()