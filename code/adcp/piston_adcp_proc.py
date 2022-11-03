#!/usr/bin/env python
# coding: utf-8

from pathlib import Path

import numpy as np
import velosearaptor


def find_root_dir(child_name="code"):
    cwd = Path(".").absolute()
    name = cwd.name
    while name != child_name:
        parent = cwd.parent
        name = parent.name
    return parent.parent


# We find the root directory based on the fact that it contains the code
# directory.
ROOT_DIR = find_root_dir(child_name="code")


def add_standard_meta_data(ds):
    ds.attrs["time_coverage_start"] = np.datetime_as_string(
        ds.time.isel(time=0).data, "m"
    )
    ds.attrs["time_coverage_end"] = np.datetime_as_string(
        ds.time.isel(time=-1).data, "m"
    )
    for mm in ["min", "max"]:
        ds.attrs[f"geospatial_lon_{mm}"] = f"{ds.attrs['lon']}"
        ds.attrs[f"geospatial_lat_{mm}"] = f"{ds.attrs['lat']}"
    return ds


def process(
    mooring,
    sn,
    min_pressure=20,
    interpolate_bin=None,
    start=None,
    stop=None,
):
    yaml_parameter_file = Path("./parameters.yml")
    a = velosearaptor.madcp.ProcessADCPyml(yaml_parameter_file, mooring, sn)

    # Run the burst averaging
    a.burst_average_ensembles(interpolate_bin=interpolate_bin, start=start, stop=stop)

    # Get rid of surface stuff
    ds = a.ds.where(a.ds.pressure > min_pressure, drop=True)

    # Drop depth levels with all nan. Velosearaptor does this as well, but
    # still leaves bins near the surface
    ds = ds.dropna(dim="depth", how="all")

    # Add meta data that doesn't come with velosearaptor (yet)
    ds = add_standard_meta_data(ds)

    return a, ds


def save_to_nc(ds):
    savepath = ROOT_DIR.joinpath(f"data/proc/adcp/{ds.mooring}")
    savename = f"PISTON_{ds.mooring}_SN{ds.sn}.nc"
    out = savepath.joinpath(savename)
    print(f"saving to {out}")
    ds.to_netcdf(out)


def return_raw(a):
    return a.raw.sel(time=slice(a.ds.time[0], a.ds.time[-1]))
