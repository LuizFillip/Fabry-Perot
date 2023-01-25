import matplotlib.pyplot as plt
import setup as s
import matplotlib.dates as dates
from core import load




def filter_resample(infile):
    
    df = load(infile)
    
    df = df.loc[(df.index.hour >= 20) |
                 (df.index.hour <= 8)]


    df = df.loc[(df["mer"] > -100) &
                (df["zon"] > -10)]

    df = df.resample("3H").mean() 

    return df.loc[df.index.hour == 21]

def main():

    modeled = "database/HWM/cariri_winds_2013.txt"
    observed = "database/processed_2013.txt"
    

    df1 = filter_resample(modeled)
    
    df = filter_resample(observed)
    
    fig, ax = plt.subplots(figsize = (14, 6), 
                           nrows = 2, 
                           ncols = 2,
                           sharex = True, 
                           sharey =  'col')
    s.config_labels()
    plt.subplots_adjust(hspace = 0.1, 
                        wspace = 0.1)
    
    coord = ["zon", "mer"]
  
    for num in range(2):
        
        ax[0, num].bar(df.index, df[coord[num]],
                       color = "k", label = "FPI (Cariri)")
        
        ax[1, num].bar(df1.index, df1[coord[num]], 
                       color = "k", label = "HWM-14")
        
        ax[1, num].legend(loc = "upper right")
        ax[0, num].legend(loc = "upper right")
        
    ax[0,0].set(ylim = [-10, 160], 
                title = "Vento zonal")
    ax[0,1].set(title = "Vento meridional")
    
    ax[0,1].xaxis.set_major_formatter(dates.DateFormatter('%b'))
    ax[0,1].xaxis.set_major_locator(dates.MonthLocator(interval = 1))
    
    fig.text(0.46, 0.05, "Meses (2013)")
    fig.text(.085, 0.4, "Velocidade (m/s)", 
             rotation = "vertical")
    
main()