import pandas as pd
from FabryPerot.utils import file_attrs
from build import paths as p
import os
from FabryPerot.core import FabryPerot
from FabryPerot.base import concat_directions, get_monthly_mean
import time

def run_year(year = 2013):
    
    year = str(year)
    
    f = p("FabryPerot")

    out = []
    
    for filename in f.get_files_in_dir(year):
                
        print("processing...", 
              file_attrs(os.path.split(filename)[-1]).date)
        try:
            out.append(concat_directions(
                FabryPerot(filename).wind))
        except Exception:
            continue
     
    df = pd.concat(out)
    
    save = os.path.join(f.get_dir("PRO"), 
                        f"{year}.txt")
    
    df.to_csv(save, index = True)
    
    return df


def run_monthly_mean():
    for coord in ["zon", "mer"]:
        get_monthly_mean(Dir = coord)

def main():
    start = time.time()
    
    run_year()
    run_monthly_mean()

    print("%s seconds" % (time.time() - start))
    
main()