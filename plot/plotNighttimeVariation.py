import matplotlib.pyplot as plt
import matplotlib.dates as dates
import numpy as np
from core import FabryPerot
import setup as s
from process import running_avg
from utils import translate


def plotErrobar(ax, df, up, trad = False):
    
    if trad:
        label = translate(up).title()
    else:
        label = up.title()
    
    args = dict(capsize = 2, lw = 1.5)
    
    zon = df.loc[(df["dir"] == up)]

    ax.errorbar(zon.index, 
                zon["vnu"], 
                yerr = zon["dvnu"], 
                **args, 
                label = label)
    
    ax.legend()
    
    
def plotAvg(ax, df, di, sample = "30min", 
            label = "30 min", 
            marker = "s",
            color = "k"):
    
    args = dict(marker = marker,
                color = color, 
                lw = 2)

    avg30 = running_avg(df, 
                    Dir = di[:3], 
                    sample = sample)
    
    ax.plot(avg30, 
            **args,
            label = f"Média ({label})")
    
    ax.legend()

def main():
    infile = 'database/2013/minime01_car_20130203.cedar.005.txt'
    
    df = FabryPerot(infile).wind
    
    
    fig, ax = plt.subplots(ncols = 2, 
                           figsize = (16, 6), 
                           sharex = True, 
                           sharey = True)
    
    plt.subplots_adjust(wspace = 0.05)
    
    s.config_labels(fontsize = 15)
    
    coords = {"zon": ("east", "west"), 
             "mer": ("north", "south")}
    
    for up, down in zip(coords["zon"], 
                        coords["mer"]):
        
        plotErrobar(ax[0], df, up, trad = False)
       
        plotErrobar(ax[1], df, down, trad = False)
      
        
    ax[0].set(ylabel = "Velocidade (m/s)", 
              yticks = np.arange(-100, 250, 50), 
              ylim = [-100, 200])
    
    ax[0].xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
    ax[0].xaxis.set_major_locator(dates.HourLocator(interval = 2))
    
    
    fig.text(0.85, -0.15, "Hora universal (UT)", 
             transform = ax[0].transAxes)
    
    date = df.index[0].strftime("%d/%M/%Y")
    fig.suptitle(f"Cariri - {date}")
    
    names = ["zonal", "meridional"]
    
    for i, ax in enumerate(ax.flat):
        
        di = names[i]
        
        plotAvg(ax, df, di)
        plotAvg(ax, df, di, sample="3H", 
                label = "3H", 
                color = "r")
        
        
        ax.set(title =  f"Vento {di}")
        ax.axhline(0, color = "k", linestyle = "--")
        
main()