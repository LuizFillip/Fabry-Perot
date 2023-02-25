from build import paths as p
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from FabryPerot.core import load_FPI



df = pd.read_csv(fpi_file, index_col = 0)

df.index = pd.to_datetime(df.index)

df = pd.pivot_table(df, 
                    index = df.index.time, 
                    columns = df.index.date, 
                    values = "zon")

out = []

for arr in df.index.values:
    
    hour = (arr.hour + 
            arr.minute / 60)
    
    if hour < 20:
        hour += 24
    
    out.append(hour)
    
idx = np.array(out, dtype = np.float64)


df.index = idx

df = df.sort_index()


df.columns = pd.to_datetime(df.columns)



def plot_monthly_averages(df):
    
    fig, ax = plt.subplots(figsize = (10, 10), 
                           nrows = 3, ncols = 2, 
                           sharey = True, 
                           sharex = True)
    
    months = [1, 2, 3, 10, 11, 12]
    
    for m, ax in zip(months, ax.flatten("F")):
    
        df1 = df.loc[:, df.columns.month == m]
        
        dn = df1.columns[0].strftime("%B")
        
        ax.set(title = dn, 
               ylim = [0, 200])
        ax.plot(df1.mean(axis = 1), color = "k", lw = 1.5)
        
        
    fig.text(0.04, 0.35, "Velocidade zonal (m/s)",
             rotation = "vertical", fontsize = 20)
    
    fig.text(0.35, 0.08, "Hora universal (UT)", 
             rotation = "horizontal", fontsize = 20)