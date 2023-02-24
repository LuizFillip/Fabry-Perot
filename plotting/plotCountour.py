import setup as s
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fpi_utils import datetime_to_float



def pivot_format(df, 
                 values = 0, 
                 start = 20, 
                 end = 8):
    
    df = df.loc[(df.index.hour >= start) |
                 (df.index.hour <= end)]
    
    df["time2"] = datetime_to_float(df)
    df["day"] = df.index.date

    return pd.pivot_table(df,
                          values = values, 
                          index = "time2", 
                          columns = "day")



def plotContourf(u):
    u2 = pivot_format(u)
    
    fig, ax = plt.subplots(figsize = (10, 4))
    
    s.config_labels()
    
    img = ax.contourf(u2.columns,
                      u2.index, 
                      u2.values, 
                      60, 
                      cmap = "jet")
      
    label = "$(U_\\theta \cos D + U_\phi \sin D ) \sin I$"
    
    ax.set(title = label, 
           xlabel = "Meses", 
           ylabel = "Hora universal")
    
    vmin, vmax, step = -40, 20, 10
    
    s.colorbar_setting(
        img, 
        ax, 
        ticks = np.arange(vmin, 
                          vmax + step, 
                          step), 
        label = "Velocidade (m/s)"
        )
    
    s.format_axes_date(ax)