import base as b 
import numpy as np 
import pandas as pd 


infile = 'FabryPerot/data/periods/'
def load_mean(v = 'vnu'):
    
    wd = b.load(infile + f'{v}.txt')
    
    wd[v] = wd.mean(axis = 1)
    
    return wd.loc[:, [v]]


def get_similar():
    
    cols = ['vnu', 'tn']
    
    wd =  load_mean('vnu')
    tn =  load_mean('tn')

    df = wd.join(tn).dropna()
    
    df['diff'] = (df[cols[0]] - df[cols[1]]).abs()
    
    return df.loc[df['diff'] <= 0.1]

#

def fs(timestamps):

    time_intervals = np.diff(timestamps)
    
    # Calculate the mean time interval to estimate fs
    mean_time_interval = np.mean(time_intervals)
    
    # Calculate the sampling frequency (fs) as the inverse of the mean time interval
    return 1 / mean_time_interval

def dtrend(ds, fs):

    avg = ds.rolling('1H').mean(center = True)
    
    ds['dtrend'] = ds - avg
    
    y = ds['dtrend'].values
    
    lowcut = 1 / 5
    highcut = 1 / 1.5


    nyquist = 0.5 * fs
    lowcut_normalized = lowcut #/ nyquist
    highcut_normalized = highcut #/ nyquist

    # Design the filter using scipy.signal
    b, a = signal.butter(
        4, [lowcut_normalized, highcut_normalized], 
        btype='band')

    # Apply the filter to the data
    filtered_data = signal.lfilter(b, a, y)
    return filtered_data

def lomb_scargle(ax, t, y):
    
    ls = LombScargle(t, y)
    
    frequency, power = ls.autopower(
            minimum_frequency = 1 / 5,
            maximum_frequency = 1 / 1.5,
            samples_per_peak = 100
            )
        
    period = 1 / frequency
    
    points = find_peaks(power, height = 0.01)
    
    ax.plot(period, power)
    for i in points[0]:
        
        ax.scatter(period[i], power[i])