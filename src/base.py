import FabryPerot as fp
import pandas as pd
import datetime as dt
import numpy as np


def sep_interval(
        ds, 
        dn, 
        delta = dt.timedelta(seconds = 43200)
        ):
    return ds[(ds.index >= dn) & (ds.index <= dn + delta)]

def split_directions(
        df, 
        direction = "zon", 
        parameter = "vnu"
        ):
         
    
    if direction == "zon":
        ds = df.loc[(df["dir"] == "east") | 
                    (df["dir"] == "west"), 
                    [parameter]]
        
    else:
        ds = df.loc[(df["dir"] == "north") | 
                    (df["dir"] == "south"), 
                    [parameter]]
    
    return ds
 
def new_index(df, freq = "2min"):
    check_days = np.unique(df.index.date)

    delta = dt.timedelta(days=1)

    if len(check_days) == 2:
        start = check_days[0]
        end = start + delta

    else:
        start = df.index[0]
        chuck = dt.datetime.combine(start, dt.time(0, 0))
        if start > chuck:
            start = chuck - delta
            end = chuck

        else:
            start = chuck
            end = chuck + delta

    return pd.date_range(f"{start} 21:00", 
                         f"{end} 07:00", 
                         freq = freq)


def resample_and_interpol(df, freq = "2min"):

    df1 = pd.DataFrame(
        index = new_index(df, freq = freq)
        )

    chuck = pd.concat([df, df1], axis = 1
                      ).interpolate()

    return chuck.resample(freq).asfreq()



def process_directions(
        path, 
        freq = "2min", 
        parameter = "vnu"
        ):
    
    """Return zonal and meridonal by
    running avg
    """

    out = []
    
    for direction in ["zon", "mer"]:
        
        if parameter == "vnu":
            data = fp.FPI(path).wind
        else:
            data = fp.FPI(path).temp
            
        df = split_directions(
            data, 
            direction = direction, 
            parameter = parameter
            )
        
        out.append(
            resample_and_interpol(
            df, freq = freq
            ).rename(
                columns = {parameter: direction})
                )
    
                
    return pd.concat(out, axis = 1)




    