import pyIGRF
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates


def CarrascoEquation(zon, mer, d, i):
    D = np.radians(d)
    I = np.radians(i)
    return (zon * np.cos(D) + mer * np.sin(D)) * np.sin(I)

def FagundesEquation(zon, mer, d, i):
    D = np.radians(d)
    I = np.radians(i)
    return (mer * np.cos(D) - zon * np.sin(D)) * np.sin(I)

coords = {"car": (-7.38, -36.528), 
          "for": (-3.73, -38.522)}


site = "car"

lat, lon = coords[site]

lon += 360

alt = 250
year = 2014

d, i, h, x, y, z, f = pyIGRF.igrf_value(lat, lon, 
                                        alt = alt, 
                                        year = year)

infile = "database/HWM/20140101.txt"

df = pd.read_csv(infile, index_col = "time")

df.index = pd.to_datetime(df.index)

df = df.loc[df.site == site, ["mer", "zon"]]

cars = CarrascoEquation(df.zon, df.mer, d, i)
fags = FagundesEquation(df.zon, df.mer, d, i)


fig, ax = plt.subplots(figsize = (10, 4))


ax.plot(cars, lw = 2, label = "$(U_\\theta \cos D + U_\phi \sin D ) \sin I$")
ax.plot(fags, lw = 2, label = "$(U_\phi \cos D - U_\\theta \sin D) \sin I$")

ax.set(ylabel = "Vento efetivo (m/s)", 
       xlabel = "Hora universal")

ax.xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
ax.xaxis.set_major_locator(dates.HourLocator(interval = 1))

ax.legend()