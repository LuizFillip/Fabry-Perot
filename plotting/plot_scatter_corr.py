import pandas as pd
import matplotlib.pyplot as plt
from FabryPerot.core import load
from build import paths as p
import datetime as dt
from sklearn.metrics import r2_score

from scipy.optimize import curve_fit


def func(x, a, c):
    return a * x + c


def plot(ax, xdata, ydata):
    ax.plot(xdata, 
             ydata, 
             marker = "o", 
             linestyle = "none", 
             color = "k")
    
    
    popt, pcov = curve_fit(func, xdata, ydata)
    
    y_pred = func(xdata, *popt)
    
    a, c = tuple(popt)
    a, c = round(a, 2), round(c, 2)
    
    r2 = round(r2_score(ydata, y_pred), 2)
    
    ax.plot(xdata, func(xdata, *popt), 
            'r-',
             label = f'$R^2$ = {r2}')
    ax.legend()
    
    return ax
    
def load_and_sel(col = "zon", 
                 time = dt.time(22, 0, 0)):
    

    modeled = p("HWM").files[1]
    observed = p("FabryPerot").get_files_in_dir("processed")
    
    mod = load(modeled)
    obs = load(observed)

    def sel_data(df, time, col):
        df = df.loc[~df.index.duplicated(keep='first')]
        return df.loc[df.index.time == time, col]
    
    df = pd.concat([sel_data(mod, time, col), 
                    sel_data(obs, time, col)], axis = 1)
    
    df.columns = ["HWM", "FPI"]
    
    df = df.dropna()
   
    return  df["FPI"].values, df["HWM"].values


def plot_scatter_corr(time):
        
    col = ["zon", "mer"]
    name = ["zonal", "meridional"]
    
    fig, ax = plt.subplots(nrows = 2, 
                           figsize = (7, 5), 
                           sharex= True)
    
    for n, ax in enumerate(ax.flat):
        
        xdata, ydata = load_and_sel(col[n], time)
        
        ax = plot(ax, xdata, ydata)
        
        ax.text(0., 1.05, name[n].capitalize(), 
                transform = ax.transAxes)
        
        ax.set(ylabel = "HWM", 
               xlabel = "FPI", 
               ylim = [-150, 150], 
               xlim = [-150, 150])
        
        
    fig.suptitle("Cariri - " + str(time))
    

time = dt.time(21, 0, 0)

plot_scatter_corr(time)

