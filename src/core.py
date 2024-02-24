import numpy as np
import pandas as pd
import datetime as dt

class FPI(object):
    
    def __init__(self, infile):

        df = pd.read_csv(infile, delim_whitespace=True)

        hours = df.HOUR.values
        minutes = df.MIN.values / 60
        seconds = df.SEC.values / 3600

        hours = np.where(hours >= 9, hours, hours + 24)

        df["time"] = hours + minutes + seconds

        conditions = [
            (df["AZM"] == 0.2) & (df["ELM"] == 45),  # Norte
            (df["AZM"] == 0) &   (df["ELM"] == 45),  # Norte
            (df["AZM"] == 0.3) & (df["ELM"] == 45),  # Norte
            (df["AZM"] == 180.0) & (df["ELM"] == 45),  # Sul
            (df["AZM"] == -179.8) & (df["ELM"] == 45),  # Sul
            (df["AZM"] == -179.7) & (df["ELM"] == 45),  # Sul
            (df["AZM"] == 90.0) & (df["ELM"] == 45),  # Leste
            (df["AZM"] == 89.8) & (df["ELM"] == 45),  # Leste
            (df["AZM"] == -90.0) & (df["ELM"] == 45),  # Oeste
            (df["AZM"] == 0) & (df["ELM"] == 90),  # Zenite
            (df["AZM"] == -179.8) & (df["ELM"] == 90),  # Zenite
            (df["AZM"] == 0.3) & (df["ELM"] == 89.8),  # Zenite
            (df["AZM"] == 180.0) & (df["ELM"] == 90.0),  # Zenite
            (df["AZM"] == 0) & (df["ELM"] == 89.5),  # Zenite
            (df["AZM"] == 180.0) & (df["ELM"] == 71.3),  # Zenite
            (df["AZM"] == -30.9) & (df["ELM"] == 55.6),  # VC Norte Car
            (df["AZM"] == -30.9) & (df["ELM"] == 55.2),  # VC Norte Car
            (df["AZM"] == 59.1) & (df["ELM"] == 55.6),  # VC Norte Caj
            (df["AZM"] == 149.1) & (df["ELM"] == 55.6),  # VC Sul Caj
            (df["AZM"] == -120.9) & (df["ELM"] == 55.6),  # VC Sul Car
            (df["AZM"] == -120.9) & (df["ELM"] == 55.1),  # VC Sul Car
            (df["AZM"] == 104.1) & (df["ELM"] == 64.2),  # VC centro Caj
            (df["AZM"] == 104.2) & (df["ELM"] == 64.2),  # VC centro Caj
            (df["AZM"] == -75.9) & (df["ELM"] == 64.2),  # VC centro Car
            (df["AZM"] == -78.8) & (df["ELM"] == 64.2),  # VC centro Car
        ]

        names = [
            "north",
            "north",
            "north",
            "south",
            "south",
            "south",
            "east",
            "east",
            "west",
            "zenith",
            "zenith",
            "zenith",
            "zenith",
            "zenith",
            "zenith",
            "CVNB",
            "CVNB",
            "CVNA",
            "CVSA",
            "CVSB",
            "CVSB",
            "INA",
            "INA",
            "INB",
            "INB",
        ]

        df["dir"] = np.select(
            conditions, 
            names,
            default = np.nan
            )

        names = ["year", "month", "day", 
                 "hour", "minute", "second"]
        
        if 'vnu' not in df.columns:
            df = df.rename(
                columns = {'VNHLU': 'vnu', 
                           'DVNHLU': 'dvnu'}
                )

        for num, elem in enumerate(df.columns):
            if num < 6:
                df.rename(
                    columns={elem: 
                             names[num]}, inplace=True)
            else:
                df.rename(
                    columns={elem: 
                             elem.lower()}, inplace=True)

        df.index = pd.to_datetime(
            df[names], infer_datetime_format=True)

        # other_cols = [
        #     "recno",
        #     "kindat",
        #     "kinst",
        #     "gdalt",
        #     "dgdalt",
        #     "ut1_unix",
        #     "ut2_unix",
        #     "wavlen",
        #     "rlel",
        #     "drlel",
        #     "doppl_ref",
        # ]

        # df = df.drop(names + other_cols, axis=1)
        
            
        
        df.loc[
            (df["dir"] == "east") | 
            (df["dir"] == "west"), "vnu"] = self.zonal(
            df["vnu"], df["elm"], df["azm"]
        )

        df.loc[
            (df["dir"] == "north") |
            (df["dir"] == "south"), "vnu"
        ] = self.meridional(df["vnu"], df["elm"], df["azm"])
        
        
        self.df = df

    @staticmethod
    def meridional(vnu, elm, azm):
        A = np.radians(azm)
        E = np.radians(elm)
        return vnu / (np.cos(E) * np.cos(A))

    @staticmethod
    def zonal(vnu, elm, azm):
        A = np.radians(azm)
        E = np.radians(elm)
        return vnu / (np.cos(E) * np.sin(A))

    @property
    def temp(self):
        return self.df.loc[:, ["tn", "dtn", "dir", "time"]]

    @property
    def wind(self):
        return self.df.loc[:, ["vnu", "dvnu", "dir", "time"]]





def load_FPI(
        infile, 
        lim_zon = (-10, 300), 
        lim_mer = (-120, 120)
        ):

    """
    Load processed data (FPI pipeline) from
    running average of zonal (east and west)
    and meridional (north and south) directions
    """

    df = pd.read_csv(infile, index_col=0)
    df.index = pd.to_datetime(df.index)



    df = df.loc[
          (df["zon"] > lim_zon[0])
        & (df["zon"] < lim_zon[-1])
        & (df["mer"] > lim_mer[0])
        & (df["mer"] < lim_mer[-1]),
        :,
    ]
    return df

# infile = 'FabryPerot/data/FPI/bfp220303g.7100.txt'

# df = FPI(infile).wind

# for col in df['dir'].unique():
    
#     df.loc[df['dir'] == col, ['vnu']].plot()