import os
import datetime 


def get_endswith_extension(infile, 
                           extention = ".txt"):
    _, _, files = next(os.walk(infile))
    txt_files = []
    for filename in files:
        if filename.endswith(extention):
            txt_files.append(filename)
    
    return txt_files


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


def get_date_from_filename(filename: str) -> datetime.datetime:
    
    """Convert FPI filename (with date and site) into date format.""" 
    s = filename.split('_')[2].split('.')[0]
 
    return datetime.date(year = int(s[0:4]), 
                         month = int(s[4:6]),
                         day = int(s[6:8]))