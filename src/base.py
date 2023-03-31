from FabryPerot.core import resample_and_interpol, FabryPerot
import pandas as pd
from build import paths as p
from FabryPerot.utils import time2float
import os 


def running_avg(df, Dir, Type = "vnu"):
    
    coords = {"zon": ("west", "east"), 
              "mer": ("north", "south")}
    
    up, down = coords[Dir] 
    
    fp = df.loc[(df["dir"] == up) | 
                (df["dir"] == down), [Type]]
     
    return resample_and_interpol(
        fp)[Type].to_frame(name = Dir)


def concat_directions(df):
    out = []
    for coord in ["zon", "mer"]:
        out.append(running_avg(df, Dir = coord))
    return pd.concat(out, axis = 1)


def reindex_and_separe(df, Dir = "zon"):
    dn = df.index.date[0]
    print("processing...", dn)
    df.index = time2float(df.index.time, sum24 = True)
    return df[Dir].to_frame(name = dn)

def get_monthly_mean(Dir = "zon", 
                     year = 2013):
    
    year = str(year)
    
    f = p("FabryPerot")

    out = []
    for infile in f.get_files_in_dir(year):
        
        try:
            df = concat_directions(FabryPerot(infile).wind)
            if len(df) < 71:
                out.append(
                    reindex_and_separe(df, Dir = Dir))
            else:
                pass
        except:
            continue

    df = pd.concat(out, axis = 1)
    
    name_to_save = f"{Dir}_{year}.txt"
    save_in = os.path.join(f.get_dir("avg"), 
                           name_to_save)
    
    df.to_csv(save_in, index = True)

    return df





   
    