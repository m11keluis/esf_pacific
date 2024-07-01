# Data location and access packages:
import earthaccess                                 # 0.6.1

# Analysis packages:
import xarray as xr                                # 2023.9.0
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Visualization packages:
import matplotlib.pyplot as plt                    # 3.8.0

# Part 1: Authenticate, Locate IMERG data files, and load data
auth = earthaccess.login(strategy="netrc") # works if the EDL login already been persisted to a netrc
if not auth.authenticated:
    # ask for EDL credentials and persist them in a .netrc file
    auth = earthaccess.login(strategy="interactive", persist=True)

#TODO: Update for GPM IMERG Final Precipitation L3 Half Hourly 0.1 degree x 0.1 degree V07 (GPM_3IMERGHH) at GES DISC

doi = '10.5067/GPM/IMERGDF/DAY/07' #IMERG

precip_results = earthaccess.search_data(
    cloud_hosted=True,
    doi=doi,
    bounding_box = ('179','-70','150','-10'),
    temporal=("2023-02-05", "2023-02-16"), # Tropical Cyclone Gabrielle
    )

file_handlers = earthaccess.open(precip_results)
ds = xr.open_mfdataset(file_handlers, decode_coords="all")

# Subset for Region of Interest
ds['lon'] = ds.lon + 180
ds_sub = ds.sel(lat=slice(-70, -10), lon=slice(100,200))

# Plot
fg = ds_sub.precipitation.plot(x='lon', y='lat',col='time', col_wrap=4,
                          transform=ccrs.PlateCarree(),
                          subplot_kws={"projection": ccrs.PlateCarree(central_longitude=180)},
                          cbar_kwargs={"orientation": "horizontal", "shrink": 0.8, "aspect": 40},
                          robust=True,
)
fg.map(lambda: plt.gca().coastlines())
plt.tight_layout()
plt.savefig('/Users/kluis/PycharmProjects/esf/figures/test_fig.png', dpi=300)