# Data location and access packages:
import earthaccess                                 # 0.6.1

# Analysis packages:
import xarray as xr                                # 2023.9.0
import numpy as np                                 # 1.26.0
import pandas as pd

# Visualization packages:
import matplotlib.pyplot as plt                    # 3.8.0
from cartopy.crs import EqualEarth, PlateCarree    # 0.22.0

# Part 1: Authenticate, Locate IMERG data files, and load data
earthaccess.login() # Login with your credentials

# Locate data file information, which includes endpoints, on Earthdata Cloud:
opera_results = earthaccess.search_data(
    short_name="OPERA_L3_DIST-ALERT-HLS_V1", # Dyanmic Surface Water Extent
    cloud_hosted=True,
    bounding_box = ('179','-49','165','-34'), # New Zealand
    temporal=("2023-02-05", "2023-02-06"), # Tropical Cyclone Gabrielle
    )

# Part 2
#opens granules and load into xarray dataset
#TODO: Fix open_dataset
ds = xr.open_dataset(earthaccess.open(opera_results[0]),
                       combine='nested',
                       decode_times=False)
