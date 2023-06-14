import os
import datetime as dt

def get_endswith_extension(infile, 
                           extention = ".txt"):
    _, _, files = next(os.walk(infile))
    txt_files = []
    for filename in files:
        if filename.endswith(extention):
            txt_files.append(filename)
    
    return txt_files

def date_to_filename(year, month, day, 
                     TYPE = "004", 
                     site = "car"):

    dn = dt.date(year, month, day).strftime("%Y%m%d")
    return f"minime01_{site}_{dn}.cedar.{TYPE}.txt"


def fn2dn(filename):
    
    s = filename.split('_')
    obs_list = s[-1].split('.')
    
    # self.intr = s[0]
    # self.site = s[1]
    # self.number = obs_list[1]
    
    date_str = obs_list[0]
    return dt.datetime.strptime(date_str, "%Y%m%d").date()
    
