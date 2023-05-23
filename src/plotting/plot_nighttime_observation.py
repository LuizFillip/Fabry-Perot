import matplotlib.pyplot as plt
import FabryPerot as fp
import os
import settings as s


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
    
    
    

def plot_directions(ax,
        path, parameter = "vnu"
        ):
    
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
               ax[i], df, coord, 
               sample = "10min", 
               marker = "s",
               color = "k"
               )
        for direction in coords[coord]:
            
            ds = df.loc[(df["dir"] == direction)]
            
            ax[i].errorbar(
                ds.index, 
                ds[parameter], 
                yerr = ds[f"d{parameter}"], 
                label = direction
                )
        ax[i].legend(loc = "upper right", ncols = 3)
        ax[i].set(ylabel = f"Vento {names[i]} (m/s)", ylim = [-150, 150])
        ax[i].axhline(0, color = "k", linestyle = "--")




def plot_nighttime_observation(
        path, 
        parameter = "vnu"
        ):
    
        
    fig, ax = plt.subplots(nrows = 2, 
                           figsize = (8, 8), 
                           sharex = True, 
                           sharey = True, 
                           dpi = 300)
    
    plt.subplots_adjust(hspace = 0.05)
    
    
    plot_directions(ax, path, parameter = parameter)
    
    s.format_time_axes(
            ax[1], hour_locator = 1, 
            day_locator = 1, 
            tz = "UTC"
            )

    if "car" in path:    
        ax[0].set_title("Cariri")
    else:
        ax[0].set_title("Cajazeiras")
    return fig, ax 
        
def main():
    
    infile = "database/FabryPerot/2013/"
    files = os.listdir(infile)

    filename = files[2]
    path = os.path.join(infile, filename)
    path = 'database/FabryPerot/2012/minime01_car_20130502.cedar.005.txt'
    path = 'database/FabryPerot/caj/minime02_caj_20130502.cedar.001.hdf5.txt'
    plot_nighttime_observation(path)

main()

