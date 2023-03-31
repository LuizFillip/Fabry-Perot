import datetime as dt
import os

from FabryPerot.core import FabryPerot
from FabryPerot.base import running_avg
import setup as s
import matplotlib.pyplot as plt

def save_img(fig, 
             save_in):
    
    plt.ioff()
    fig.savefig(save_in, 
                dpi = 100, 
                pad_inches = 0, 
                bbox_inches = "tight")
    plt.clf()   
    plt.close()
    return 



def plot_time_series(ax, fpi_file, title = "Cariri"):
    
    wind = FabryPerot(fpi_file).wind
    avg = running_avg(wind, Dir = "zon")
    ax.plot(avg, 
            lw = 2, 
            color = "k", 
            label = "Média")
    
    for up in ("east", "west"):
        
        zon = wind.loc[(wind["dir"] == up)]
        
        ax.errorbar(zon.index, 
                    zon["vnu"], 
                    yerr = zon["dvnu"], 
                    label = up, 
                    capsize = 3)
    
    ax.axhline(0, color = "r", linestyle = "--")
    ax.legend(loc = "upper right")                  
    
    ax.set(title = title,
           ylim = [-50, 250],
           xlabel = "Hora universal", 
           ylabel = "Velocidade zonal (m/s)")
    
    s.format_axes_date(ax, time_scale= "hour", 
                       interval = 1)
    
def plot_both_sites(date, 
                    car_infile, 
                    caj_infile):
    
    fig, ax = plt.subplots(ncols = 2, 
                           figsize = (12, 6), 
                           sharey = True, 
                           sharex = True)

    plot_time_series(ax[0], car_infile, title = "Cariri")
    plot_time_series(ax[1], caj_infile, title = "Cajazeiras")
        
    fig.suptitle(date.strftime("%d/%m/%Y"))
    
    return fig 

def get_datetime_fpi(filename):
    s = filename.split('_')
    obs_list = s[-1].split('.') 
    date_str = obs_list[0]
    return dt.datetime.strptime(
        date_str, "%Y%m%d")

caj = "database/FabryPerot/caj/"
car = "database/FabryPerot/2012/"

for f1 in os.listdir(caj):
    caj_dt = get_datetime_fpi(f1)

    for f2 in os.listdir(car):

        car_dt = get_datetime_fpi(f2)
        
        if ((car_dt == caj_dt) and 
            (car_dt.year == 2013)):
            car_infile = os.path.join(car, f2)
            caj_infile = os.path.join(caj, f1)
            
            try:
                fig = plot_both_sites(car_dt, 
                                car_infile, 
                                caj_infile)
                
                save_in = "C:\\plot2\\"
                
                save_img(fig, 
                         os.path.join(save_in, 
                                      f1.replace("txt", "png")))
            except:
                continue

    