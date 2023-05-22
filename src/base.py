import FabryPerot as fp
import pandas as pd
from utils import time2float
import os


def running_avg(df, Dir, Type="vnu"):

    coords = {"zon": ("west", "east"), "mer": ("north", "south")}

    up, down = coords[Dir]

    ds = df.loc[(df["dir"] == up) | (df["dir"] == down), [Type]]

    return fp.resample_and_interpol(ds)[Type].to_frame(name=Dir)


def concat_directions(df):
    out = []
    for coord in ["zon", "mer"]:
        out.append(running_avg(df, Dir=coord))
    return pd.concat(out, axis=1)


def reindex_and_separe(df, Dir="zon"):
    dn = df.index.date[0]
    print("processing...", dn)
    df.index = time2float(df.index.time, sum24=True)
    return df[Dir].to_frame(name=dn)


def get_monthly_mean(infile, Dir="zon", year=2013):

    year = str(year)

    out = []
    for filename in os.listdir(infile):
        path = os.path.join(infile, filename)
        try:
            df = concat_directions(fp.FabryPerot(path).wind)
            if len(df) < 71:
                out.append(reindex_and_separe(df, Dir=Dir))
            else:
                pass
        except:
            continue

    df = pd.concat(out, axis=1)

    name_to_save = f"{Dir}_{year}.txt"
    save_in = os.path.join(infile, name_to_save)

    df.to_csv(save_in, index=True)

    return df
