import numpy as np 
import pandas as pd
from datetime import timedelta
from fpi_utils import datetime_to_float


class FabryPerot(object):
    
    def __init__(self, infile):
        
    
        df = pd.read_csv(infile, 
                         delim_whitespace = True)
        
        hours = df.HOUR.values
        minutes = df.MIN.values / 60
        seconds = df.SEC.values / 3600
        
        hours = np.where(hours >= 9, hours, hours + 24)
        
        df["time"] = (hours + minutes + seconds)
        
        conditions = [
                (df['AZM'] == 0.2) & (df['ELM'] == 45), #Norte
                (df['AZM'] == 0) & (df['ELM'] == 45), #Norte
                (df['AZM'] == 0.3) & (df['ELM'] == 45),  #Norte
                (df['AZM'] == 180.0) & (df['ELM'] == 45), #Sul
                (df['AZM'] == -179.8) & (df['ELM'] == 45), #Sul
                (df['AZM'] == -179.7) & (df['ELM'] == 45), #Sul
                (df['AZM'] == 90.0) & (df['ELM'] == 45), #Leste
                (df['AZM'] == 89.8) & (df['ELM'] == 45), #Leste
                (df['AZM'] == -90.0) & (df['ELM'] == 45), #Oeste
                (df['AZM'] == 0) & (df['ELM'] == 90),  #Zenite
                (df['AZM'] == -179.8) & (df['ELM'] == 90), #Zenite
                (df['AZM'] == 0.3) & (df['ELM'] == 89.8), #Zenite
                (df['AZM'] == 180.0) & (df['ELM'] == 90.0), #Zenite
                (df['AZM'] == 0) & (df['ELM'] == 89.5), #Zenite
                (df['AZM'] == 180.0) & (df['ELM'] == 71.3), #Zenite
                (df['AZM'] == -30.9) & (df['ELM'] == 55.6), #VC Norte Car
                (df['AZM'] == -30.9) & (df['ELM'] == 55.2), #VC Norte Car
                (df['AZM'] == 59.1) & (df['ELM'] == 55.6), #VC Norte Caj
                (df['AZM'] == 149.1) & (df['ELM'] == 55.6), #VC Sul Caj
                (df['AZM'] == -120.9) & (df['ELM'] == 55.6), #VC Sul Car
                (df['AZM'] == -120.9) & (df['ELM'] == 55.1), #VC Sul Car
                (df['AZM'] == 104.1) & (df['ELM'] == 64.2), #VC centro Caj
                (df['AZM'] == 104.2) & (df['ELM'] == 64.2), #VC centro Caj
                (df['AZM'] == -75.9) & (df['ELM'] == 64.2), #VC centro Car
                (df['AZM'] == -78.8) & (df['ELM'] == 64.2) #VC centro Car
                ] 

        names = ['north', 'north', 'north', 
               'south', 'south', 'south', 
               'east', 'east', 'west',
               'zenith','zenith', 'zenith', 
               'zenith', 'zenith', 'zenith',
               'CVNB', 'CVNB', 'CVNA', 'CVSA', 
               'CVSB', 'CVSB', 'INA', 
               'INA', 'INB', 'INB']
    
        df['dir'] = np.select(conditions, names, default = np.nan)
        
        names = ['year', 'month', 'day', 
                 'hour', 'minute', 'second']
        
      
        
        for num, elem in enumerate(df.columns):
            if num < 6:
                df.rename(columns  = {elem : names[num]}, 
                          inplace = True)
            else:
                df.rename(columns  = {elem : elem.lower()}, 
                          inplace = True)
        
        
        df.index = pd.to_datetime(df[names], 
                                  infer_datetime_format = True)
        
        other_cols = ['recno', 'kindat', 'kinst', 'gdalt', 
                      'dgdalt', 'ut1_unix', 'ut2_unix', 
                      'wavlen', 'rlel', 'drlel', 'doppl_ref']
        
        
        df = df.drop(names + other_cols, axis = 1) 
                
        df.loc[(df['dir'] == 'east') | 
               (df['dir'] == 'west'), 
               'vnu'] = self.zonal(df['vnu'], df['elm'], df['azm']) 

        df.loc[(df['dir'] == 'north') | 
               (df['dir'] == 'south'), 
               'vnu'] = self.meridional(df['vnu'], df['elm'], df['azm']) 
        
                                     
        self.df = df
    
    @staticmethod
    def meridional(vnu, elm, azm):
        A = np.radians(azm)
        E = np.radians(elm)
        return vnu / (np.cos(E)*np.cos(A))
    @staticmethod
    def zonal(vnu, elm, azm):
        A = np.radians(azm)
        E = np.radians(elm)
        return vnu / (np.cos(E)*np.sin(A))
                                                     
    @property    
    def temp(self):
        
        return self.df.loc[:, ["tn", "dtn", 
                               "dir", "time"]]
    
    @property
    def wind(self):
        
        cond  = ((self.df["vnu"] < 200) & 
                 (self.df["vnu"] > -100) )
        
        return self.df.loc[cond, ["vnu", "dvnu", 
                               "dir", "time"]]


def resample_interpolate(dat, sample = '5min'):
    
    start = dat.index[0].date()
    
    end = start + timedelta(days = 1)  
    
    new_index = pd.date_range(f"{start} 21:00", 
                              f"{end} 08:00", 
                              freq = sample)
    
    chuck = pd.DataFrame(index = new_index)
    
    chuck = pd.concat([dat, chuck], 
                      axis = 1).interpolate()
    
    return chuck.resample(sample).asfreq()


def get_mean(df, zonal = True, sample = "10min"):

    out = []
    
    if zonal:
        coords =  ["west", "east"]
    else:
        coords =  ["north", "south"]
    
    for coord in coords:
        dat = df.loc[(df["dir"] == coord), "vnu"]
        out.append(resample_interpolate(dat))
     
    ds = pd.concat(out, axis = 1)
    return ds.mean(axis = 1).resample(sample).asfreq()

def load(infile, resample = False):
    """Load processed data (FPI pipeline) and 
    HWM-14 model results"""
    
    df = pd.read_csv(infile, index_col = "time")
    df.index = pd.to_datetime(df.index)

    try:
        del df["Unnamed: 0"]
    except:
        pass
    
    if resample:
        df = df.resample("1H").mean()
    
    df["time2"] = datetime_to_float(df)
    df["day"] = df.index.date


    return df.loc[(df.index.hour >= 20) |
                 (df.index.hour <= 8)]



def main():

    infile = "database/2013/minime01_car_20130420.cedar.002.txt"
    
    observed = "database/processed_2013.txt"
    
    df = load(observed)
        
#main()