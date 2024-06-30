# Data location and access packages:
import earthaccess                                 # 0.6.1

# Analysis packages:
import xarray as xr                                # 2023.9.0
import numpy as np                                 # 1.26.0

# Visualization packages:
import matplotlib.pyplot as plt                    # 3.8.0

# Part 1: Authenticate, Locate IMERG data files, and load data
earthaccess.login() # Login with your credentials

# Locate data file information, which includes endpoints, on Earthdata Cloud:
precip_results = earthaccess.search_data(
    short_name="GPM_3IMERGHH", # GPM IMERG Final Precipitation L3 Half Hourly 0.1 degree x 0.1 degree V07 (GPM_3IMERGHH) at GES DISC
    cloud_hosted=True,
    bounding_box = ('-170','-70','100','0'), # Crossing International Dateline
    temporal=("2023-02-01", "2023-03-01"), # Tropical Cyclone Gabrielle
    )

# Part 2
#opens granules and load into xarray dataset
ds = xr.open_mfdataset(earthaccess.open(precip_results), combine='nested', decode_times=False)
