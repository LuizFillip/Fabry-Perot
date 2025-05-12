import base as b 
import pandas as pd 
import FabryPerot as fp
import datetime as dt 

fn_storm = 'minime01_car_20151220.cedar.003.txt'



def quiet_avg():
    
    path =   'database/FabryPerot/car/'
    
    out = []
    for day in [13, 16, 18, 29]:
        fn = f'minime01_car_201512{day}.cedar.003.txt'
        df = fp.process_directions(
                path + fn, 
                freq = "10min", 
                parameter = "vnu"
                )
        
        df.index = b.time2float(
            df.index, sum_from = 20)
        
        out.append(df['mer'])
        
    ds = pd.concat(out, axis = 1)
    
    ds['u'] = ds.mean(axis = 1) 
    return ds.loc[:, ['u']]





def fl2dn(df, ref_date):
    
    df = df.copy()
    
    out = []
    for num in df.index:
        
        if num >= 24:
            num -= 24 
            days = 1
        else:
            days = 0
            
        out.append(
            ref_date + dt.timedelta(
                hours = num, days = days
                )
            )
    df.index = out
    
    return df


def get_winds_quiet():

    data = quiet_avg()
    
    out = []
        
    for day in [19, 20, 21, 22]:
        ref_date = dt.datetime(2015, 12, day)
    
        out.append(fl2dn(data, ref_date))
            
        
    df = pd.concat(out)
    
    df = df.loc[~df.index.duplicated()]
    
    return df 
    