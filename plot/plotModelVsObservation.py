import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import setup as s
import matplotlib.dates as dates
from core import load

def plot(
        ax, 
        res, 
        coord = "zon", 
        year = 2013, 
        Type = "observado"
        ):
    
    if coord == "zon": 
        label = "zonal"
        vmin, vmax, step = -100, 200, 50
    else:
        label = "meridional"
        vmin, vmax, step = -100, 100, 50
    
    year = res.index[0].year

    df = pd.pivot_table(res, 
                        values = coord, 
                        columns = "day", 
                        index = "time2")
    
    df = df.interpolate()

    X, Y = np.meshgrid(df.columns, df.index)
    Z = df.values
    img = ax.pcolormesh(X, Y, Z, 
                        vmax = vmax, 
                        vmin = vmin, 
                        cmap = "jet") 
    
    s.colorbar_setting(
        img, ax, 
        ticks = np.arange(vmin, 
                          vmax + step, 
                          step), 
        label = "Velocidade (m/s)"
        )
    
    ax.set(
        title = f"Vento {label} para {year}",
        ylabel = "Hora (UT)", 
        xlabel = "Meses"
           )
    
    ax.text(0.01, 0.9, f"Vento {Type}", 
            transform = ax.transAxes) 
    
    ax.xaxis.set_major_formatter(dates.DateFormatter('%b'))
    ax.xaxis.set_major_locator(dates.MonthLocator(interval = 1))
    
    return ax


def main():

    fig, ax = plt.subplots(figsize = (8, 6), 
                           nrows = 2, 
                           sharey = True,
                           sharex = True)
    
    plt.subplots_adjust(hspace = 0.1)
    
    modeled = "database/HWM/cariri_winds_2013.txt"
    observed = "database/processed_2013.txt"
    
    ax1 = plot(ax[0], load(modeled), coord = "zon", 
               Type = "modelado")
    ax1.set(xlabel = "")
    ax2 = plot(ax[1], load(observed), coord = "zon")
    
    ax2.set(title = "")