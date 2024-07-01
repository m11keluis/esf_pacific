# Data location and access packages:
import h5py
import numpy as np
import xarray as xr
from pyhdf.SD import SD, SDC
from pyhdf.HDF import HDF
import pyhdf.VS

tempfile = '/Users/kluis/PycharmProjects/esf/datasets/gretel/precip/2020073013604_73913_CS_2C-PRECIP-COLUMN_GRANULE_P1_R05_E09_F00.hdf'

#TODO Modify function to open CloudSat rain profiles
def open_dataset_hdf(filename, variables=None, drop_variables=[]):

    """
    Modified from https://github.com/brhillman/pycloudsat/blob/master/cloudsat_io.py &
    https://github.com/paula-rj/StratoPy/blob/main/stratopy/cloudsat.py
    :param filename:
    :param variables:
    :param drop_variables:
    :return:
    """
    da_dict = {}

    # First read SD (scientific datasets)
    sd = SD(filename)
    if variables is None:
        data_vars = sd.datasets().keys()
    else:
        data_vars = variables
    for dname in data_vars:

        if dname in drop_variables: continue
        if dname not in sd.datasets().keys(): continue

        sds = sd.select(dname)

        # get (masked) data
        d = np.where(sds[:] != sds.getfillvalue(), sds[:], np.nan)

        # check for more masks
        if 'missing' in sds.attributes():
            d[d == sds.missing] = np.nan

        # unpack data
        if 'offset' in sds.attributes() and 'factor' in sds.attributes():
            d = d / sds.factor + sds.offset

        # coordinate variables...how to do this?! Look for VDATA?
        # just save as DataArray for now, without coordinate variables...
        dims = [sds.dim(i).info()[0] for i in range(len(sds.dimensions()))]

        da_dict[dname] = xr.DataArray(d, dims=dims, attrs=sds.attributes(), name=dname)

        # Close this dataset
        sds.endaccess()

    # Close file
    sd.end()

    # ...now read VDATA...
    hdf = HDF(filename)
    vs = hdf.vstart()
    if variables is None:
        data_vars, *__ = zip(*vs.vdatainfo())
    else:
        data_vars = variables
    for vname in data_vars:

        if vname in drop_variables: continue
        if vname not in [v[0] for v in vs.vdatainfo()]: continue

        # attach vdata
        vd = vs.attach(vname)

        # get vdata info
        nrec, mode, fields, *__ = vd.inquire()
        if nrec == 0:
            vd.detach()
            continue

        # read data
        d = np.array(vd[:]).squeeze()

        # make sure not to overwrite coordinate variables
        if all([vname not in da.dims for v, da in da_dict.items()]):
            da_dict[vname] = xr.DataArray(d)

        vd.detach()

    # clean up
    vs.end()

    # HDF files do not always close cleanly, so close manually
    hdf.close()

    return xr.Dataset(da_dict)

# Read Precipitation File from Cyclone Gretel
temp = open_dataset_hdf(tempfile)