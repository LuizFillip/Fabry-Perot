import base as b 
import pandas as pd 
import FabryPerot as fp
import datetime as dt 


def load_month_avgs():
    
    df = b.load('FabryPerot/data/201512')

    df['time'] = df.index.to_series().apply(b.dn2float)
    df['day'] = df.index.day
    
    # df = df.loc[df.index.day.isin([13, 16, 18, 19])]
    return df.loc[~df.index.duplicated()]

def get_mean_std(df, vl, coord):
    
    co = coord[:5].lower()
    
    ds = pd.pivot_table(
        df, 
        values = f'{vl}_{co}', 
        columns ='day', 
        index = 'time'
        )
    
    ds = pd.concat(
        [ds.mean(axis = 1).to_frame('mean'), 
         ds.std(axis = 1).to_frame('std')],
        axis = 1)
    
    
    dn = dt.datetime(2015, 12, 20)
    
    return b.renew_index_from_date(ds, dn)

def quiettime_winds(coord = 'mer'):
    
    path = 'database/FabryPerot/car/'
    days = [13, 18, 29]
    out = []
    for day in days:
        fn = f'minime01_car_201512{day}.cedar.003.txt'
        df = fp.process_directions(
                path + fn, 
                freq = "10min", 
                parameter = "vnu"
                )
        
        df.index = b.time2float(df.index, sum_from = 20)
        
        out.append(df[coord])
        
    ds = pd.concat(out, axis = 1)
    
    avg = ds.mean(axis = 1) 
    std = ds.std(axis = 1)
    
    ds = pd.concat([avg, std], axis = 1)
    ds.columns = [coord, f'd{coord}']
    return ds 


quiettime_winds(coord = 'mer')