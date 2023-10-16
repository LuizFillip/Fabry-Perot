import pandas as pd
import os
import FabryPerot as fp
from tqdm import tqdm


    
def process_year(
        infile, 
        freq = "2min", 
        parameter = "vnu",
        year = 2013, 
        site = "car"
        ):
    

    files = os.listdir(infile)

    out = []
    for filename in tqdm(files, desc = "run"):
        
        path = os.path.join(infile, filename)
        dn = fp.date_from_filename(filename)

        if dn.year == year:
            try:
                out.append(fp.process_day(
                    path, 
                    freq = freq, 
                    parameter = parameter)
                    )
            except:
                print(filename)
                continue
        
            
    df = pd.concat(out).sort_index()
    
    df = df[~df.index.duplicated()]
    
    df.to_csv(f"database/FabryPerot/{site}_{parameter}_{year}.txt")
    
    return df


def main():

    infile = "database/FabryPerot/2013/"
    process_year(
            infile, 
            freq = "2min", 
            parameter = "vnu",
            year = 2013
            )
    
# main()