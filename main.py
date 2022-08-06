import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import os 



def get_endswith_extension(infile, 
                           extention = ".txt"):
    _, _, files = next(os.walk(infile))
    txt_files = []
    for filename in files:
        if filename.endswith(extention):
            txt_files.append(filename)
    
    return txt_files




def get_date_from_filename(filename: str) -> datetime.datetime:
    
    """Convert FPI filename (with date and site) into date format.""" 
    s = filename.split('_')[2].split('.')[0]
 
    return datetime.date(year = int(s[0:4]), 
                         month = int(s[4:6]),
                         day = int(s[6:8]))




class FabryPerot(object):
    
    def __init__(self, infile, filename):
        
    
        df = pd.read_csv(infile + filename, 
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
                (df['AZM'] == -90) & (df['ELM'] == 45), #Oeste
                (df['AZM'] == 0) & (df['ELM'] == 90),  #Zenite
                (df['AZM'] == -179.8) & (df['ELM'] == 90), #Zenite
                (df['AZM'] == 0.3) & (df['ELM'] == 89.8), #Zenite
                (df['AZM'] == 180.0) & (df['ELM'] == 90), #Zenite
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

        choices = ['north', 'north', 'north', 
               'south', 'south', 'south', 
               'east', 'east', 'east',
               'zenith','zenith', 'zenith', 
               'zenith', 'zenith', 'zenith',
               'CVNB', 'CVNB', 'CVNA', 'CVSA', 
               'CVSB', 'CVSB', 'INA', 'INA', 'INB', 'INB']
    
        df['dir'] = np.select(conditions, choices, default = np.nan)
        
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
                                  infer_datetime_format=True)
        
        other_cols = ['recno', 'kindat', 'kinst', 'gdalt', 
                      'dgdalt', 'ut1_unix', 'ut2_unix', 
                      'wavlen', 'rlel', 'drlel', 'doppl_ref']
        
        
        self.df = df.drop(names + other_cols, axis=1) 
        
        
    
    @property    
    def temp(self):
        
        return self.df.loc[:, ["tn", "dtn", "dir"]]
    
    @property
    def wind(self):
        return self.df.loc[:, ["vn"]]

infile = "Database/Cariri/2013/Abril/"

filename = get_endswith_extension(infile)[0]

date = get_date_from_filename(filename)

df = FabryPerot(infile, filename).temp




def datetime_to_float(df: pd.DataFrame) -> pd.DataFrame:
    
    df = df.resample('1min').last().interpolate()

    date = df.index.date[0]

    hour = df.index.hour.values
    minute = df.index.minute.values / 60
    second = df.index.second.values / 3600
    
    hour = np.where(hour >= 9, hour, hour + 24)

    df["time"] = np.array(hour + second + minute)
    
    df["time"] = df["time"].apply(lambda x: np.round(x, 2))    

    return df.resample('10min').asfreq()

ee = df.loc[df.dir == "east", :]

ee1 = datetime_to_float(ee)


ee["tn"].plot()

ee1["tn"].plot()
print(ee1)