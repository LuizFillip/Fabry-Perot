import matplotlib.pyplot as plt
from FabryPerot import FabryPerot
from FabryPerot.src.base import running_avg





def plotErrobar(ax, 
                df, 
                up, 
                par = "vnu"):
    
    label = up.title()
    
    args = dict(capsize = 2, lw = 1.5)
    
    zon = df.loc[(df["dir"] == up)]

    ax.errorbar(zon.index, 
                zon[par], 
                yerr = zon[f"d{par}"], 
                **args, 
                label = label)
    
    ax.legend()
    
    ax.grid()
    
    
def plot_average(ax, df, di, sample = "10min", 
            marker = "s",
            color = "k"):
    
    args = dict(marker = marker,
                color = color, 
                lw = 2, 
                fillstyle = "none")

    avg30 = running_avg(df, Dir = di[:3])
    
    ax.plot(avg30, 
            **args,
            label = f"Média ({sample})")
    
    ax.legend()
    
    
def plot_attrs(ax, df):
    names = ["zonal", "meridional"]
    for i, ax in enumerate(ax.flat):
        
        di = names[i]
        
        plot_average(ax, df, di)
          
        ax.set(title =  f"Vento {di}")
        ax.axhline(0, color = "r", linestyle = "--")

def plot_nighttime_observation(infile, 
                               Type = "wind"):
    
    if Type == "wind":
        df = FabryPerot(infile).wind
    else:
        df = FabryPerot(infile).temp
        
    fig, ax = plt.subplots(ncols = 2, 
                           figsize = (14, 4), 
                           sharex = True, 
                           sharey = True)
    
    plt.subplots_adjust(wspace = 0.05)
    
    s.config_labels(fontsize = 15)
    
    coor = {"zon": ("east", "west"), 
            "mer": ("north", "south")}
    
    for up, down in zip(coor["zon"], coor["mer"]):
        
        plotErrobar(ax[0], df, up)
       
        plotErrobar(ax[1], df, down)
      
        
    ax[0].set(ylabel = "Velocidade (m/s)")
    
    s.format_axes_date(ax[0], time_scale = "hour", 
                       interval = 2)
    
    fig.text(0.85, -0.15, "Hora universal (UT)", 
             transform = ax[0].transAxes)
    
    date = df.index[0].strftime("%d/%m/%Y")
    fig.suptitle(f"Cariri - {date}")
    
    plot_attrs(ax, df)
    
    plt.show()
    
    return fig, ax 
        
def main():
        
    
    infile = files[1]
    
    plot_nighttime_observation(infile)

# main()

import os

files = os.listdir("database/FabryPerot/2013/")

files