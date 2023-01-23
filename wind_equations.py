import pyIGRF
import numpy as np


def CarrascoEquation(zon, mer, d, i):
    D = np.radians(d)
    I = np.radians(i)
    return (zon * np.cos(D) + mer * np.sin(D)) * np.sin(I) #np.cos(I)

def FagundesEquation(zon, mer, d, i):
    D = np.radians(d)
    I = np.radians(i)
    return (mer * np.cos(D) - zon * np.sin(D)) * np.sin(I)


coords = {"car": (-7.38, -36.528), 
          "for": (-3.73, -38.522)}

def run_igrf(site = "car", 
             alt = 250, 
             year = 2014):

    lat, lon = coords[site]
    
    lon += 360
    
    d, i, h, x, y, z, f = pyIGRF.igrf_value(lat, lon, 
                                            alt = alt, 
                                            year = year)
    return d, i 