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

df = df.resample("3H").mean()
hours = list(np.unique(df.index.hour))

df = df.loc[df.index.hour == 21]

fig, ax = plt.subplots(nrows = 2, 
                       sharex = True)



ax[0].bar(df.index, df["mer"])
ax[1].bar(df.index, df["zon"])

