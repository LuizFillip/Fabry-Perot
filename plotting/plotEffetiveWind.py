import setup as s
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from wind_equations import CarrascoEquation, PauloEquation, run_igrf

def load(infile):
    df = pd.read_csv(infile, index_col = "time")
    
    try:
        del df["Unnamed: 0"]
    except:
        pass
    
    df.index = pd.to_datetime(df.index)
    return df

def compute_winds(df, func = CarrascoEquation):
    d, i = run_igrf(year = 2013)

    return func(df.zon, df.mer, d, i).to_frame(name = "u")

def sel_interval(u, b):
    e = b + timedelta(hours = 11)
    return u.loc[(u.index >= b) & (u.index <= e)]


def main():
    
    infile = "database/HWM/cariri_winds_2013.txt"
    
    
    df = load(infile)
    
    b = datetime(2013, 1, 1, 21, 0)
    
    args = dict(lw = 2)
    u = sel_interval(
        compute_winds(df, func = PauloEquation), b
        )
    
    fig, ax = plt.subplots(figsize = (8, 4))
    
    ax.plot(u, **args,
            label = "$(U_\phi \cos D + U_\\theta \sin D ) \cos I$")
    
    u2 = sel_interval(
        compute_winds(df, func = CarrascoEquation), b
        )
    
    ax.plot(u2, **args,
            label = "$U_\\theta \cos D + U_\phi \sin D$")
    
    ax.set(ylabel = "Velocidade (m/s)", 
           xlabel = "Hora universal (UT)")
    
    ax.legend()
    
    s.format_axes_date(ax, time_scale="hour", interval = 2)

main()