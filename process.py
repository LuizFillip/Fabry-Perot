from FabryPerot.core import FabryPerot
import os 
from FabryPerot.fpi_utils import file_attrs
import pandas as pd
from build import paths as p
    
def running_avg(df, 
                Dir = "zon", 
                sample = "10min"):
    
    coords = {"zon": ("west", "east"), 
              "mer": ("north", "south")}
    
    up, down = coords[Dir] 

    fp = df.loc[(df["dir"] == up) | 
                (df["dir"] == down), "vnu"]
    
    chunk = fp.resample(sample).mean().to_frame()
    
    return chunk.rename(columns = {"vnu": Dir})

def concat_dir(df):
    
    out = []
    for coord in ["zon", "mer"]:
        out.append(running_avg(df, Dir = coord))
    f = pd.concat(out, axis = 1)
    f.index.name = "time"
    return f



def run_year(year = 2013):
    
    year = str(year)
    
    files = p("FabryPerot")

    out = []
    
    for filename in files.get_files_in_dir(year):
        
        f = os.path.split(filename)[-1]
        
        date = file_attrs(f).date
        print("processing...", date)
        out.append(concat_dir(FabryPerot(filename).wind))
     
    df = pd.concat(out)
    
    save = os.path.join(p("FabryPerot").root, 
                        "PRO", 
                        f"{year}.txt")
    
    df.to_csv(save, index = True)
    
    return df



def main():

    df = run_year()
    
    print(df)
    

