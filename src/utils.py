import os
import datetime as dt
import numpy as np
from translate import Translator

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

def time2float(time_array, sum24 = False):
    out = []

    for arr in time_array:
        
        hour = (arr.hour + 
                arr.minute / 60)
        if sum24:
            if hour < 20:
                hour += 24
        
        out.append(hour)
    return out

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

def date_from_filename(filename):
    
    s = filename.split('_')
    obs_list = s[-1].split('.')
    
    # self.intr = s[0]
    # self.site = s[1]
    # self.number = obs_list[1]
    
    date_str = obs_list[0]
    return dt.datetime.strptime(date_str, "%Y%m%d").date()
    
    
    

def translate(string):
    translator= Translator(to_lang="pt")
    return translator.translate(string)