import os
import datetime as dt
from typing import Iterable, List, Optional, Union
from tqdm import tqdm 
import pandas as pd

import FabryPerot as fp
import base as b

DIRECTIONS = ["west", "east", "south", "north"]

# Quais colunas usar para cada parâmetro
PARAM_COLS = {
    "vnu": ["vnu", "dvnu", "time"],
    "rle": ["rle", "drle", "time"],
    "tn":  ["tn",  "dtn",  "time"],
}


def _ensure_datetime_index(df: pd.DataFrame) -> pd.DataFrame:
    """Garante index datetime, ordenado e sem duplicatas."""
    if not isinstance(df.index, pd.DatetimeIndex):
        raise TypeError("O DataFrame precisa ter DatetimeIndex.")
    df = df.sort_index()
    df = df.loc[~df.index.duplicated(keep="first")]
    return df


def resample_new_index(
    ds: Union[pd.Series, pd.DataFrame],
    freq: str = "10min",
) -> Union[pd.Series, pd.DataFrame]:
    """
    Reindexa para uma grade temporal regular e interpola.

    - Cria um DateTimeIndex regular de start->end com passo `freq`
    - Reindexa e interpola no tempo
    - Retorna na frequência exata (asfreq)
    """
    if isinstance(ds, pd.Series):
        ds = ds.to_frame(ds.name or "value")

    ds = _ensure_datetime_index(ds)

    if ds.empty:
        return ds

    start = ds.index[0].replace(minute=0, second=0, microsecond=0)
    end = ds.index[-1]

    new_index = pd.date_range(start=start, end=end, freq=freq)
    out = ds.reindex(ds.index.union(new_index)).interpolate(method="time")
    out = out.reindex(new_index)

    # volta Series se era Series
    return out if out.shape[1] > 1 else out.iloc[:, 0]


def sep_direction(
    df: pd.DataFrame,
    direction: str,
    parameter: str = "vnu",
    freq: str = "10min",
) -> pd.Series:
    """
    Separa uma direção (west/east/south/north) e 
    devolve a série interpolada
    do parâmetro escolhido.
    """
    if parameter not in PARAM_COLS:
        raise ValueError(f"parameter inválido: {parameter}. Use {list(PARAM_COLS)}")

    cols = PARAM_COLS[parameter]
    needed = set(cols + ["dir"])
    missing = needed - set(df.columns)
    if missing:
        raise KeyError(f"Faltam colunas no df: {missing}")

    ds = df.loc[df["dir"] == direction, cols]

    # Se a coluna "time" aqui é redundante (pois index já é datetime), ok manter.
    # Vamos garantir índice datetime.
    ds = _ensure_datetime_index(ds)

    s = resample_new_index(ds, freq=freq)
    # s pode ser DataFrame/Series; queremos só a coluna do parâmetro
    return s[parameter] if isinstance(s, pd.DataFrame) else s


def interpol_directions(
    df: pd.DataFrame,
    parameter: str = "vnu",
    wind_threshold: float = 400,
    freq: str = "10min",
) -> pd.DataFrame:
    """
    Para cada direção em DIRECTIONS:
      - seleciona e interpola o parâmetro
      - junta em um DataFrame com colunas = direções
    """
    df = _ensure_datetime_index(df)

    # filtro de outliers só para vnu (como no seu código)
    if parameter == "vnu" and "vnu" in df.columns:
        df = df.loc[df["vnu"].between(-wind_threshold, wind_threshold)]

    series_list: List[pd.DataFrame] = []

    for direction in DIRECTIONS:
        try:
            ts = sep_direction(df, direction, parameter=parameter, freq=freq)
            series_list.append(ts.rename(direction).to_frame())
        except (KeyError, ValueError, TypeError):
            # direção ausente ou parâmetro inválido/sem dados
            continue

    if not series_list:
        return pd.DataFrame()

    return pd.concat(series_list, axis=1)


def get_time_avg(data: Iterable[pd.DataFrame]) -> pd.DataFrame:
    """
    Recebe uma lista/iterável de DataFrames (por noite, por arquivo, etc.)
    e retorna o perfil médio por horário (time float) para cada direção.
    """
    out = []

    for df in data:
        try:
            out.append(interpol_directions(df, parameter="vnu"))
        except (TypeError, KeyError, ValueError):
            continue

    if not out:
        return pd.DataFrame()

    df = pd.concat(out).sort_index()
    df = _ensure_datetime_index(df)

    df["time"] = df.index.to_series().map(b.dn2float)
    df["day"] = df.index.day

    out_dir = []
    for col in DIRECTIONS:
        if col not in df.columns:
            continue

        pivot = pd.pivot_table(
            df,
            columns="day",
            index="time",
            values=col,
            aggfunc="mean",
        )
        out_dir.append(pivot.mean(axis=1).rename(col).to_frame())

    return pd.concat(out_dir, axis=1) if out_dir else pd.DataFrame()


def join_days(
    ref_date: dt.datetime,
    infile: str,
    in_month: bool = True,
    p: str = "tn",
) -> pd.DataFrame:
    """
    Junta vários dias (arquivos) em um único DataFrame interpolado.

    Corrige o bug do seu código original: você setava infile duas vezes.
    """
    if in_month:
        files = fp.file_of_the_month(ref_date, infile)
    else:
        files = fp.get_window_of_dates(ref_date)

    out = []
    for filename in files:
        fpath = os.path.join(infile, filename)
        try:
            # aqui assumo que você na verdade queria ler o arquivo e gerar df
            # se interpol_directions espera DataFrame, troque por fp.FPI(...).<param>
            # Ex.: fpi = fp.FPI(fpath) ; df_param = getattr(fpi, p)
            fpi = fp.FPI(fpath) if os.path.isfile(fpath) else fp.FPI(infile + filename)
            df_param = getattr(fpi, p)  # p: 'tn'/'vnu'/'rle'
            out.append(interpol_directions(df_param, parameter=p))
        except Exception:
            continue

    if not out:
        return pd.DataFrame()

    df = pd.concat(out).sort_index()
    df = _ensure_datetime_index(df)

    df["time"] = df.index.to_series().map(b.dn2float)
    df["day"] = df.index.day
    return df


def get_mean_in_day(df: pd.DataFrame, vl: str) -> pd.DataFrame:
    """
    Calcula componente zonal (W/E) e meridional (S/N) para um parâmetro.
    """
    ds = interpol_directions(df, parameter=vl)

    # só calcula se existir as colunas necessárias
    if not set(["west", "east"]).issubset(ds.columns):
        ds[f"{vl}_zonal"] = pd.NA
    else:
        ds[f"{vl}_zonal"] = ds[["west", "east"]].mean(axis=1)

    if not set(["south", "north"]).issubset(ds.columns):
        ds[f"{vl}_merid"] = pd.NA
    else:
        ds[f"{vl}_merid"] = ds[["south", "north"]].mean(axis=1)

    return ds[[f"{vl}_merid", f"{vl}_zonal"]]


def concat_parameters(fpi: "fp.FPI") -> pd.DataFrame:
    """
    Junta vnu/tn/rle em um DataFrame com meridional+zonal para cada parâmetro.
    """
    out = []
    for vl in ["vnu", "tn", "rle"]:
        df_param = getattr(fpi, vl)
        out.append(get_mean_in_day(df_param, vl))
    return pd.concat(out, axis=1)


def save_averages(
    infile: str = "database/FabryPerot/cac/",
    skip_day: Optional[int] = 20,
) -> pd.DataFrame:
    """
    Processa os arquivos do mês e retorna um DataFrame final concatenado.
    (Você pode depois salvar com df.to_csv/to_parquet, etc.)
    """
    files = os.listdir(infile)
    
    desc = 'save avg'
    out = []
    for file in tqdm(files, desc):
        try:
            dn = fp.fn2dn(file)
            if dn.year == 2025:
                # if skip_day is not None and dn.day == skip_day:
                #     continue
                fpi = fp.FPI(os.path.join(infile, file))
                out.append(concat_parameters(fpi))
        except Exception:
            continue

    return pd.concat(out) if out else pd.DataFrame()

def caj_fn2dn(file, site = 'bfp', code = 7100):
    
    if 'hdf5' in file:
        fmt = f'{site}%y%m%dg.{code}.hdf5.txt'
    else:
        fmt = f'{site}%y%m%dg.{code}.txt'
  
    return dt.datetime.strptime(file, fmt)

from pathlib import Path

# infile  = Path("database/FabryPerot/cac/")

# files = list(infile.glob('*.txt')) 

# out = []
# for file in tqdm(files):

#     try:
        
#         dn = caj_fn2dn(file.name)
        
    
#         if dn.year == 2025:
#             print(dn)
#             fpi = fp.FPI(file)
#             out.append(concat_parameters(fpi))
#     except:
#         continue
       
# df = pd.concat(out)
# df 