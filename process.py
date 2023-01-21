from core import FabryPerot
import os 
import datetime as dt
from utils import file_attrs 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import setup as s
import matplotlib.dates as dates



    
    
def running_avg(df, 
                Dir = "zonal", 
                sample = "30min"):
    
    coords = {"zonal": ("west", "east"), 
             "merid": ("north", "south")}
    
    up, down = coords[Dir] 

    fp = df.loc[(df["dir"] == up) | 
                (df["dir"] == down), "vnu"]
    
    chunk = fp.resample(sample).mean().to_frame()
    
    return chunk.rename(columns = {"vnu": Dir})

def concat_dir(df, method = "polynomial"):
    out = []
    for coord in ["zonal", "merid"]:
        out.append(running_avg(df, Dir = coord))
    return pd.concat(out, axis = 1)



def process_all_data(infile):
    
    _, _, files = next(os.walk(infile))

    out = []
    
    for filename in files:
    
        date = file_attrs(filename).date
        
        print("processing...", date)
        df = FabryPerot(infile + filename).wind
          
        out.append(concat_dir(df))
    
    return pd.concat(out)



#def main():
infile = "database/2013/"

res = process_all_data(infile)
res["time"] =  datetime_to_float(res)
res["day"] = res.index.date
s.config_labels()
    
    
print(res)
    
#main()

#%%

def plot(res, coord = "zonal"):
    
    year = res.index[0].year

    df = pd.pivot_table(res, 
                        values = coord, 
                        columns = "day", 
                        index = "time")
    
    df = df.interpolate()
    fig, ax = plt.subplots(figsize = (10, 6))
    
    
    X, Y = np.meshgrid(df.columns, df.index)
    Z = df.values
    img = ax.pcolormesh(X, Y, Z, 
                        vmax = 250, 
                        vmin = -150, 
                        cmap = "jet") 
    
    if coord != "zonal": coord = "meridional"
    
    s.colorbar_setting(img, ax, 
                       ticks = np.arange(-100, 250, 50), 
                       label = "Velocidade (m/s)")
    
    ax.set(title = f"Vento {coord} para {year}",
           ylabel = "Hora (UT)", 
           xlabel = "Meses"
           )
    
    ax.xaxis.set_major_formatter(dates.DateFormatter('%b'))
    ax.xaxis.set_major_locator(dates.MonthLocator(interval = 1))
    
    return fig, ax


fig, ax = plot(res, coord = "zonal")