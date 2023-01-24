import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import setup as s
import matplotlib.dates as dates
from core import load


modeled = "database/HWM/cariri_winds_2013.txt"
observed = "database/processed_2013.txt"

coord = "zon"

df = load(observed)

df = df.loc[(df.index.hour >= 20) |
             (df.index.hour <= 8)]


df = df.loc[(df["mer"] > -100) &
            (df["zon"] > -10)]

df = df.resample("3H").mean()


hours = list(np.unique(df.index.hour))
df = df.loc[df.index.hour == 21]

fig, ax = plt.subplots(figsize = (8, 6), 
                       nrows = 2, 
                       sharex = True)

plt.subplots_adjust(hspace = 0.1)

coords = ["zon", "mer"]
texts = ["(a)", "(b)"]
names = ["Zonal","Meridional"]


for num, ax in enumerate(ax.flat):
    ax.bar(df.index, df[coords[num]], color = "k")
    ax.set(ylabel = f"{names[num]} (m/s)")
    ax.text(0.01, 0.85, texts[num], 
            transform = ax.transAxes)
    
    
ax.xaxis.set_major_formatter(dates.DateFormatter('%b'))
ax.xaxis.set_major_locator(dates.MonthLocator(interval = 2))
