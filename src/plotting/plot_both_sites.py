import datetime as dt
import os
import FabryPerot as fp
import settings as s
import matplotlib.pyplot as plt




def plot_average(
        ax, df, di, 
        sample = "10min", 
        marker = "s",
        color = "k"):
    
    args = dict(marker = marker,
                lw = 2, 
                fillstyle = "none")

    avg30 = fp.running_avg(df, Dir = di)
    
    ax.plot(avg30, **args,
            label = f"Média ({sample})")
    
    


def plot_directions2(
        ax, 
        path, 
        col = 0,
        parameter = "vnu"
        ):
    
    if "car" in path:    
        ax[0, col].set_title("Cariri")
    else:
        ax[0, col].set_title("Cajazeiras")
        
    if parameter == "vnu":
        df = fp.FPI(path).wind
    else:
        df = fp.FPI(path).temp
        
    coords = {
        "zon": ("east", "west"), 
        "mer": ("north", "south")
        }
    
    names = ["zonal", "meridional"]
    
    for i, coord in enumerate(coords.keys()):
        
        plot_average(
               ax[i, col], df, coord, 
               sample = "10min", 
               marker = "s",
               color = "k"
               )
        for direction in coords[coord]:
            
            ds = df.loc[(df["dir"] == direction)]
            
            ax[i, col].errorbar(
                ds.index, 
                ds[parameter], 
                yerr = ds[f"d{parameter}"], 
                label = direction
                )
        ax[i, col].legend(loc = "upper right", ncol = 2)
        ax[i, col].set(ylabel = f"Vento {names[i]} (m/s)", 
                  ylim = [-200, 200])
        ax[i, col].axhline(0, color = "k", linestyle = "--")
        
    s.format_time_axes(
            ax[1, col], hour_locator = 1, 
            day_locator = 1, 
            tz = "UTC"
            )



def get_datetime_fpi(filename):
    s = filename.split('_')
    obs_list = s[-1].split('.') 
    date_str = obs_list[0]
    return dt.datetime.strptime(
        date_str, "%Y%m%d")

def same_dates_in_sites(year = 2013):
    caj = "database/FabryPerot/caj/"
    car = "database/FabryPerot/2012/"
    
    out = []
    
    for f1 in os.listdir(caj):
        caj_dt = get_datetime_fpi(f1)
    
        for f2 in os.listdir(car):
    
            car_dt = get_datetime_fpi(f2)
            
            if ((car_dt == caj_dt) and 
                (car_dt.year == 2013)):
                car_infile = os.path.join(car, f2)
                caj_infile = os.path.join(caj, f1)
                
                out.append(tuple((car_infile, caj_infile)))
    
    return out
            
        
         
def plot_both_sites(f1, f2):
    
    fig, ax = plt.subplots(
        nrows = 2, 
        ncols= 2,
        figsize = (12, 8), 
        sharex = True, 
        sharey = True, 
        dpi = 300)

    plt.subplots_adjust(hspace = 0.05)

    for col, path in enumerate([f1, f2]):
        plot_directions2(
                ax, 
                path, 
                col = col,
                parameter = "vnu"
                )

    return fig 




def save_img(fig, 
             save_in):
    
    plt.ioff()
    fig.savefig(save_in, 
                dpi = 300, 
                pad_inches = 0, 
                bbox_inches = "tight")
    plt.clf()   
    plt.close()
    return 


for infiles in same_dates_in_sites(year = 2013):
    f1, f2 = infiles
    
    fig = plot_both_sites(f1, f2)
    
    
    try:
        FigureName = fp.date_from_filename(f1).strftime("%Y%m%d.png")
        save_in = "D:\\plots2\\FPI\\"
        print("saving...", FigureName)
        save_img(fig, os.path.join(save_in, FigureName))
    except:
        continue
    