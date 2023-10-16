import pandas as pd
import FabryPerot as fp
from astropy.timeseries import LombScargle
from scipy.signal import find_peaks






def peaks_periods(infile, col = 'tn'):
    
    if col == 'vnu':
        df = fp.FPI(infile).wind
    else:
        df = fp.FPI(infile).temp
        
    out = {'south' : [], 'north': [], 
           'east': [], 'west': []}
    
    
    for j, sector in enumerate(out.keys()):
        
        ds = df.loc[df['dir'] == sector]
        
        avg = ds[col].rolling('1H').mean(center = True)
        
        ds['dtrend'] = ds[col] - avg
        
        y = ds['dtrend'].values
        t = ds['time'].values 
        
        ls = LombScargle(t, y)
        
        frequency, power = ls.autopower(
                minimum_frequency = 1 / 5,
                maximum_frequency = 1 / 1.1,
                samples_per_peak = 100
                )
            
        period = 1 / frequency
        
        points = find_peaks(power, height = 0.01)
        
        for i in points[0]:
            out[sector].append(period[i])
    
    return out



def diff_values(valor1, valor2):  
    return abs(valor1 - valor2)

def list_cond(p1, p2, p3, p4):
    
    diff_list = [
        diff_values(p1, p2),
        diff_values(p1, p4),
        diff_values(p2, p3),
        diff_values(p3, p4)
        ]

    return [t for t in diff_list if t <= 0.15]
    
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


path = 'database/FabryPerot/cariri/2013/'
# fname = 'minime01_car_20130101.cedar.005.txt'
from tqdm import tqdm 
import os

def run():

    out = []
    
    for fname in tqdm(os.listdir(path)):
        
        infile = os.path.join(
            path, fname)
        try:
           out.append(
               check_similiarities(
                   infile, col = 'tn')
               )
        except:
            continue
        
    return pd.concat(out)

df = run()

