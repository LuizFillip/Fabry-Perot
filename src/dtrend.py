import pandas as pd
import FabryPerot as fp
from astropy.timeseries import LombScargle
from scipy.signal import find_peaks
from tqdm import tqdm 
import os

def dtrend_(ds):

    avg = ds.rolling('1H').mean(center = True)
    
    ds['dtrend'] = ds - avg
    
    y = ds['dtrend'].values
    t = ds['time'].values 
    
    return y, t

def LS(t, y):
    
    ls = LombScargle(t, y)
    
    frequency, power = ls.autopower(
            minimum_frequency = 1 / 5,
            maximum_frequency = 1 / 1.1,
            samples_per_peak = 100
            )
        
    period = 1 / frequency
    
    return period, power

def peaks_periods(infile, col = 'tn'):
    
    if col == 'vnu':
        df = fp.FPI(infile).wind
    else:
        df = fp.FPI(infile).temp
        
    out = {
        'south' : [], 
        'north': [], 
        'east': [], 
        'west': []
        }
    
    
    for j, sector in enumerate(out.keys()):
        
        ds = df.loc[df['dir'] == sector]
        
        t, y = dtrend_(ds[col])
        
        period, power = LS(t, y)
        
        points = find_peaks(power, height = 0.01)
            
        for i in points[0]:
            out[sector].append(period[i])
    
    return out



def diff_values(valor1, valor2):  
    return abs(valor1 - valor2)

def list_cond(
        p1, p2, p3, p4, 
        threshold = 0.1
        ):
    
    diff_list = [
        diff_values(p1, p2),
        diff_values(p1, p4),
        diff_values(p2, p3),
        diff_values(p3, p4)
        ]

    return [t for t in diff_list if t <= threshold]
    
def check_similiarities(infile, col = 'tn'):
    
    out = peaks_periods(infile, col)

    dic = []
                
    for p1 in out['east']:
        for p2 in out['west']:
            for p3 in out['north']:
                for p4 in out['south']:
                    
                    if len(list_cond(p1, p2, p3, p4)) == 4:
                        
                        dic.append([p1, p2, p3, p4])
       
    index = len(dic) * [fp.fn2dn(infile)]
    
    return pd.DataFrame(
        dic, columns = list(out.keys()), 
        index = index
        )



def run(path, col = 'tn'):

    out = []
    
    for fname in tqdm(os.listdir(path), col):
        
        infile = os.path.join(
            path, fname)
        try:
           out.append(
               check_similiarities(
                   infile, 
                   col
                   )
               )
        except:
            continue
        
    return pd.concat(out).sort_index()

