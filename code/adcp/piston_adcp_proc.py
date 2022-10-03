#!/usr/bin/env python
# coding: utf-8

import scipy as sp
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import xarray as xr
from pathlib import Path


def add_standard_meta_data(ds):
    for k, v in STD_META.items():
        ds.attrs[k] = v
    ds.attrs["start_time"] = np.datetime_as_string(ds.time.isel(time=0).data, 'm')
    ds.attrs["stop_time"] = np.datetime_as_string(ds.time.isel(time=-1).data, 'm')

    return ds


def mooring_location(mooring_nr):
    if mooring_nr == 1:
        return 12.3232, 134.7619
    elif mooring_nr == 2:
        return 15.7632, 134.6899
    elif mooring_nr == 3:
        return 15.7612, 134.6883


def adjust_variable_names(ds):
    ds = ds.rename(z='depth')
    return ds

STD_META = dict(
    title="PISTON 2018-2019 moored velocity time series",
    project="PISTON, Propagation of Intraseasonal Summer Tropical Oscillations",
    funding="Office of Naval Research",
    version="R0",
    institution="Scripps Institution of Oceanography, SIO",
    author="Matthew Alford & Gunnar Voet",
    author_email="gvoet@ucsd.edu",
    procesing_level="Level 1",
    license="These data may be used freely with acknowledgement to Matthew Alford & Gunnar Voet, SIO",
    netcdf_convention="Classic",
    platform_type="moorings",
    instrument="ADCP",
    # featureType=
    #     profile
    # cdm_data_type=
    #     Profile
    sea_name="Pacific",
    keywords_vocabulary="NASA Global Change Master Directory (GCMD) Science Keywords",
    standard_name_vocabulary="NetCDF Climate and Forecast (CF) Metadata Convention",
    geospatial_lat_units="degree_north",
    geospatial_lon_units="degree_east",
)
