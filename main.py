import pandas as pd
from FabryPerot.utils import file_attrs
from build import paths as p
import os
from FabryPerot.core import FabryPerot
from FabryPerot.base import concat_directions
import time

def run_year(year = 2013):
    
    year = str(year)
    
    files = p("FabryPerot")

    out = []
    
    for filename in files.get_files_in_dir(year):
        
        f = os.path.split(filename)[-1]
        
        print("processing...", file_attrs(f).date)
        try:
            out.append(concat_directions(
                FabryPerot(filename).wind))
        except Exception:
            continue
     
    df = pd.concat(out)
    
    save = os.path.join(p("FabryPerot").root, 
                        "PRO", 
                        f"{year}.txt")
    
    df.to_csv(save, index = True)
    
    return df

start = time.time()


run_year()


print("%s" % (time.time() - start))