#!/usr/bin/env python
# coding: utf-8

import scipy as sp
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import xarray as xr
from pathlib import Path
import velosearaptor
import munch


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


def mooring_location(mooring_nr):
    if mooring_nr == 1:
        return 12.3232, 134.7619
    elif mooring_nr == 2:
        return 15.7632, 134.6899
    elif mooring_nr == 3:
        return 15.7612, 134.6883


def process(
    mooring,
    sn,
    min_pressure=20,
    apply_pg=True,
    interpolate_bin=None,
    start=None,
    stop=None,
):
    # params = velosearaptor.io.parse_yaml_input(
    #     "parameters.yml", mooring=mooring, sn=sn, return_dict=True
    # )
    # p = munch.munchify(params)

    # # Set up a processing object. We will take care of the editing parameters in a little bit.
    # a = velosearaptor.madcp.ProcessADCP(
    #     p.data_dir,
    #     meta_data=p.meta_data,
    #     driftparams=p.driftparams,
    #     tgridparams=p.tgridparams,
    #     dgridparams=p.dgridparams,
    #     editparams=p.editparams,
    #     verbose=False,
    # )
    yaml_parameter_file = Path("./parameters.yml")
    a = velosearaptor.madcp.ProcessADCPyml(yaml_parameter_file, mooring, sn)

    # Run the burst averaging
    a.burst_average_ensembles(interpolate_bin=interpolate_bin, start=start, stop=stop)

    # # Apply percent good criterion
    # if apply_pg:
    #     vars2d = ["u", "v", "w", "e", "u_std", "v_std", "w_std", "e_std", "amp", "pg"]
    #     for var in vars2d:
    #         a.ds[var] = a.ds[var].where(a.ds.pg >= p.editparams.pg_limit, other=np.nan)

    # Get rid of surface stuff
    ds = a.ds.where(a.ds.pressure > min_pressure, drop=True)

    # Get rid of depth levels that have no data
    ds = ds.dropna(dim="depth", how="all")

    ds = add_standard_meta_data(ds)

    # fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(7.5, 3),
    #                     constrained_layout=True)
    # ds.xducer_depth.plot(ax=ax, color="0.2")
    # ds.u.plot(ax=ax)
    # # ax.invert_yaxis()
    # ylim = np.min(ax.get_ylim(), 0)
    # ax.set(ylim=(800, 100))
    # gv.plot.concise_date(ax)

    raw = a.raw.sel(time=slice(ds.time[0], ds.time[-1]))
    # velosearaptor.adcp.plot_raw_adcp_auxillary(raw)
    # velosearaptor.adcp.plot_raw_adcp(raw)
    return a, raw, ds
