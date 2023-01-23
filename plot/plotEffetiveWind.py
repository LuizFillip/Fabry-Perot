import setup as s
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dates
from wind_equations import CarrascoEquation, run_igrf
from utils import datetime_to_float
pd.options.mode.chained_assignment = None 

infile = "database/HWM/cariri_winds_2013.txt"

df = pd.read_csv(infile, index_col = "time")

df.index = pd.to_datetime(df.index)

#df = df.resample("1H").mean()

d, i = run_igrf(year = 2013)

u = CarrascoEquation(df.zon, df.mer, d, i).to_frame()

def pivot_format(df, values = 0):
    df = df.loc[(df.index.hour >= 20) |
                 (df.index.hour <= 8)]
    
    df["time2"] = datetime_to_float(df)
    df["day"] = df.index.date

    return pd.pivot_table(df,
                          values = values, 
                          index = "time2", 
                          columns = "day")


u2 = pivot_format(u)

fig, ax = plt.subplots(figsize = (10, 4))

img = ax.contourf(u2.columns,
            u2.index, 
            u2.values, 60, cmap = "jet")


label = "$(U_\\theta \cos D + U_\phi \sin D ) \sin I$"

ax.set(title = label, 
       xlabel = "Meses", 
       ylabel = "Hora universal")

vmin, vmax, step = -40, 20, 10
s.colorbar_setting(
    img, ax, 
    ticks = np.arange(vmin, 
                      vmax + step, 
                      step), 
    label = "Velocidade (m/s)"
    )

ax.xaxis.set_major_formatter(dates.DateFormatter('%b'))
ax.xaxis.set_major_locator(dates.MonthLocator(interval = 1))
#ax.legend()
 
