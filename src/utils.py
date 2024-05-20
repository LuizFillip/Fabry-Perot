import datetime as dt
import os
import pandas as pd 

def dn_to_filename(dn, site = 'bfp', code = 7100):
    
    fmt = f'{site}%y%m%dg.{code}.txt'
    return dn.strftime(fmt)

def filename_to_dn(file, site = 'bfp', code = 7100):
    fmt = f'{site}%y%m%dg.{code}.txt'
    return dt.datetime.strptime(file, fmt)

def file_of_the_month(dn, infile):
    files = os.listdir(infile)
    out = []
    for file in files:
        month =  filename_to_dn(file).month
        if dn.month == month:
            
            out.append(file)
    
    return out


def date_to_filename(year, month, day, 
                     TYPE = "004", 
                     site = "car"):

    dn = dt.date(year, month, day).strftime("%Y%m%d")
    return f"minime01_{site}_{dn}.cedar.{TYPE}.txt"


def fn2dn(filename):
    
    try:
    
        s = filename.split('_')
        obs_list = s[-1].split('.')
        date_str = obs_list[0]
        
    except:
        p = os.path.split(filename)[-1]
        s = p.split('_')
        obs_list = s[-1].split('.')
        date_str = obs_list[0]
        
    return dt.datetime.strptime(date_str, "%Y%m%d")
    
def get_window_of_dates(dn, site = 'bfp', code = 7100):
    
    start = dn - dt.timedelta(days = 15)
    end = dn + dt.timedelta(days = 15)
    out = []
    for dn1 in pd.date_range(start, end, freq = '1D'):
        out.append(
            dn_to_filename(
                dn1, site = 'bfp', code = 7100)
            )
    
    return out