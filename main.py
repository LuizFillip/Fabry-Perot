import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as dates
from glob import glob
from datetime import datetime, timedelta, time

# you could also import date instead of datetime and use that.

infile = "minime01_car_20111101.cedar.001.txt"




def filename_to_date(infile):
    
    """
    Converte o local de data do nome do arquivo 
    do FPI no formato datetime
    Paramêtros:
        infile: Nome do arquivo
    
    """
    var = infile.split('_')
    
    s = var[2].split('.')[0]
    
    date = datetime(year = int(s[0:4]), 
                    month = int(s[4:6]),
                    day = int(s[6:8]))

    return date

def ReadData(filename, parameter = ['TN']):
    
    df = pd.read_csv(filename, delim_whitespace = True)
    
    #Renemeie a colunas do tempo e data para facilitar na conversão
    #datetime
    df.rename(columns = {'YEAR': 'year', 'MONTH': 'month', 'DAY': 'day', 
                             'HOUR':'hour', 'MIN':'minute', 'SEC': 'second'}, 
              inplace = True)

    datetime = ['year', 'month', 'day', 'hour', 'minute', 'second']

    df.index = pd.to_datetime(df[datetime], infer_datetime_format=True)
    
    #Filtrp para remover os dados com erro 
    df = df.loc[~(((df['TEMP_ERR'] == 2) & (df['WIND_ERR'] == 2)) | 
                  ((df['TN'] > 1300)| (df['TN'] < 600))| (df['DTN'] > 50) | 
                  (df['VNU'] > 400)) , :]

    
    df = df.loc[:, parameter + ['AZM', "ELM"]]

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

    choices = ['Norte', 'Norte', 'Norte', 'Sul', 'Sul', 'Sul', 
               'Leste', 'Leste', 'Oeste',
               'Zenite','Zenite', 'Zenite', 'Zenite', 'Zenite', 'Zenite',
              'CVNB', 'CVNB', 'CVNA', 'CVSA', 'CVSB', 'CVSB', 
              'INA', 'INA', 'INB', 'INB']
    
    df['CDL'] = np.select(conditions, choices, default=np.nan)
    
    if 'VNU' in parameter:
    
         df.loc[(df['CDL'] == 'Leste') | 
                (df['CDL'] == 'Oeste'), 'VNU'] = (df['VNU'] / 
                                                  (np.cos(np.deg2rad(df['ELM']))*
                                                   np.sin(np.deg2rad(df.AZM))))

         df.loc[(df['CDL'] == 'Norte') | 
                (df['CDL'] == 'Sul'), 'VNU'] = (df['VNU'] / 
                                                (np.cos(np.deg2rad(df['ELM']))*
                                                 np.cos(np.deg2rad(df.AZM))))
    
   
    
    return df

def datetime_to_current(dataframe, 
                        parameter = ['TN'], 
                        interpolated = True, 
                        nondate = True):
    
    if interpolated == True:
        dataframe = dataframe.resample('10min').last().interpolate()
    else:
        dataframe = dataframe
    
    datetime = dataframe.index.values
    

    date = dataframe.index.date[0]

    values = dataframe.index.hour.values
    minute = dataframe.index.minute.values / 60
    second = dataframe.index.second.values / 3600
    
    hour = np.where(values >= 9, values, values + 24)

    dataframe.index = np.array(hour + second + minute)
    
    
    if nondate == False:
        dataframe = dataframe.loc[:, parameter]
        dataframe.rename(columns = {i : date for 
                                    i in dataframe.columns}, 
                    inplace = True)
        
        dataframe.index = dataframe.index.to_series().apply(
            lambda x: np.round(x,2))
    else:
        dataframe.index = pd.to_datetime(datetime)
        

    return dataframe



def current_to_datetime(dataframe): 
    

    if isinstance(dataframe, pd.DataFrame):
        doub = dataframe.index.values
    else:
        doub = doub
    
    extract_times = []
    
    for num in range(len(doub)):
        
        
        dt = dataframe.columns.values[0]
        
        combined = datetime.combine(dt, tm)
        
        extract_times.append(combined)
        
        
    dataframe.index = extract_times
    
    return dataframe


def monthToNum(shortMonth):
    return {
        'jan': 1,
        'fev': 2,
        'mar': 3,
        'abr': 4,
        'mai': 5,
        'jun': 6,
        'jul': 7,
        'ago': 8,
        'set': 9, 
        'out': 10,
        'nov': 11,
        'dez': 12
        }[shortMonth]

def current_to_time(number):
    string_list = str(number).split('.')
    hour = int(string_list[0])

    minutes = round(int(string_list[1]) / 100 * 60)
    
    if minutes < 10:
        minutes = minutes * 10

    if (hour > 23):
        hour = hour - 24
        #dt = dt + timedelta(days = 1)        

    tm = time(int(hour), int(minutes))
    
    return tm


def test():
    path = "C:\\Users\\LuizF\\Google Drive\\Cariri\\Cariri\\2013\\Agosto\\"

    files = glob(path + "/*.txt")
    
    
    for filename in files:
        print(filename)
        
        df = ReadData(filename)
        
        print(df.groupby("CDL").count()["TN"])
        
        print(df.loc[df['CDL'] == 'nan', :])
        
        
