import pandas as pd
from utils import datetime_to_float
import matplotlib.pyplot as plt
import numpy as np
import setup as s
import matplotlib.dates as dates


infile = "database/HWM/cariri_winds_2013.txt"


df = pd.read_csv(infile, index_col= "time")
df.index = pd.to_datetime(df.index)

del df["Unnamed: 0"]

df["time2"] = datetime_to_float(df)
df["day"] = df.index.date

df = df.loc[(df.index.hour >= 21) |
             (df.index.hour <= 8)]
coord = "zon"
year = 2013
df = pd.pivot_table(df, 
                    values = "zon", 
                    columns = "day", 
                    index = "time2")

df = df.interpolate()
fig, ax = plt.subplots(figsize = (10, 6))


X, Y = np.meshgrid(df.columns, df.index)
Z = df.values
img = ax.pcolormesh(X, Y, Z, 
                    vmax = 250, 
                    vmin = -150, 
                    cmap = "jet")

s.colorbar_setting(img, ax, 
                   ticks = np.arange(-100, 250, 50), 
                   label = "Velocidade (m/s)")

ax.set(title = f"Vento {coord} para {year}",
       ylabel = "Hora (UT)", 
       xlabel = "Meses"
       )

ax.xaxis.set_major_formatter(dates.DateFormatter('%b'))
ax.xaxis.set_major_locator(dates.MonthLocator(interval = 1))