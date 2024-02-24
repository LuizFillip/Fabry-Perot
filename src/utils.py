import datetime as dt
import os

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
    
