# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.0
#   kernelspec:
#     display_name: Python [conda env:piston-proc-adcp]
#     language: python
#     name: conda-env-piston-proc-adcp-py
# ---

# %% [markdown]
# ### Imports

# %% janus={"all_versions_showing": false, "cell_hidden": false, "current_version": 0, "id": "b233107473fbf", "named_versions": [], "output_hidden": false, "show_versions": false, "source_hidden": false, "versions": []}
# %matplotlib inline
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import xarray as xr
from pathlib import Path
import munch

import velosearaptor
import gvpy as gv

import piston_adcp_proc as pp

# %reload_ext autoreload
# %autoreload 2
# %config InlineBackend.figure_format = 'retina'

# %% [markdown] janus={"all_versions_showing": false, "cell_hidden": false, "current_version": 0, "id": "b15170ac2736e", "named_versions": [], "output_hidden": false, "show_versions": false, "source_hidden": false, "versions": []}
# ## PISTON ADCP Processing

# %%
yml_parameters = Path("./parameters.yml")

# %% [markdown]
# ## SIO2

# %% [markdown] heading_collapsed=true
# ### SN14435

# %% hidden=true
params = velosearaptor.io.parse_yaml_input(yml_parameters, mooring="SIO2", sn=14435)

# %% hidden=true
p = munch.munchify(params)

# %% hidden=true
p.editparams

# %% [markdown] hidden=true
# Set up a processing object.

# %% hidden=true
a = velosearaptor.madcp.ProcessADCPyml(
    yml_parameters,
    mooring="SIO2",
    sn=14435,
    verbose=False,
)

# %% [markdown] hidden=true
# Run the burst averaging

# %% hidden=true
a.burst_average_ensembles()

# %% hidden=true
a.ds.xducer_depth

# %% hidden=true
a.ds.amp.gv.tplot()

# %% hidden=true
a.ds.pg.gv.tplot()

# %% hidden=true
a.ds.where(a.ds.pressure>15).dropna(dim='depth', how="all").dropna(dim='time', how="all").u.plot(yincrease=False)

# %% hidden=true
a.ds.where(a.ds.pressure>15).dropna(dim='depth', how="all").dropna(dim='time', how="all").pg.plot(yincrease=False)

# %% hidden=true
a.ds.where(a.ds.pressure>15).dropna(dim='z', how="all").dropna(dim='time', how="all").amp.plot(yincrease=False)

# %% [markdown] hidden=true
# Get rid of surface stuff

# %% hidden=true
ds = a.ds.where(a.ds.pressure > 15, drop=True)

# %% [markdown] hidden=true
# Get rid of depth levels that have no data

# %% hidden=true
ds = ds.dropna(dim="z", how="all")

# %% hidden=true
ds.amp.gv.tplot()

# %% hidden=true
ds.w.gv.tplot()

# %% hidden=true
ds.u.gv.tplot()

# %% hidden=true
fig, ax = gv.plot.quickfig(fgs=(7, 3))
ds.pressure.plot(yincrease=False, ax=ax)
gv.plot.concise_date(ax)

# %% hidden=true
ds

# %% hidden=true
ds.u_error.gv.tplot()

# %% hidden=true
ds = pp.adjust_variable_names(ds)

# %% hidden=true
ds = pp.add_standard_meta_data(ds)

# %% hidden=true
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(7.5, 3),
                       constrained_layout=True)
ds.xducer_depth.plot(ax=ax, color="0.2")
ds.u.plot(ax=ax)
# ax.invert_yaxis()
ylim = np.min(ax.get_ylim(), 0)
ax.set(ylim=(800, 100))
gv.plot.concise_date(ax)

# %% hidden=true
ds.u_error.gv.tplot()

# %% hidden=true
raw = a.raw.sel(time=slice(ds.time[0], ds.time[-1]))

# %% hidden=true
velosearaptor.adcp.plot_raw_adcp_auxillary(raw)

# %% hidden=true
velosearaptor.adcp.plot_raw_adcp(raw)

# %% hidden=true
a, raw, ds = pp.process("SIO2", 14435)

# %% hidden=true
velosearaptor.adcp.plot_raw_adcp_auxillary(raw)

# %% hidden=true
velosearaptor.adcp.plot_raw_adcp(raw)

# %% [markdown] hidden=true
# Shear looks decent now

# %% hidden=true
ds.u.differentiate(coord='depth').gv.tplot(robust=False, cmap='RdBu')

# %% hidden=true
ds.u.differentiate(coord='depth').gv.tplot(robust=False, cmap='RdBu')

# %% hidden=true
ds.v.differentiate(coord='depth').gv.tplot(robust=False, cmap='RdBu')

# %% hidden=true
ds.v.gv.tplot()

# %% [markdown] heading_collapsed=true
# ### SN13596

# %% hidden=true
a, raw, ds = pp.process("SIO2", 13596, min_pressure=750)

# %% hidden=true
velosearaptor.adcp.plot_raw_adcp_auxillary(raw)

# %% hidden=true
velosearaptor.adcp.plot_raw_adcp(raw)

# %% hidden=true
ds.u.where(ds.u_error<0.02).interpolate_na(dim='depth', limit=2).gv.tplot(robust=True)

# %% hidden=true
ds.u.gv.tplot(robust=True)

# %% hidden=true
ds.pg.gv.tplot(robust=True)

# %% [markdown] heading_collapsed=true
# ### SN22525

# %% hidden=true
mooring = "SIO2"
sn = 22525

# %% hidden=true
params = velosearaptor.io.parse_yaml_input(
    "parameters.yml", mooring=mooring, sn=sn, return_dict=True
)

# %% hidden=true
p = munch.munchify(params)

# %% hidden=true
p.editparams

# %% hidden=true
a, raw, ds = pp.process("SIO2", 22525, apply_pg=False, interpolate_bin=18)

# %% hidden=true
velosearaptor.adcp.plot_raw_adcp_auxillary(raw)

# %% hidden=true
ds.u.gv.tplot(robust=True)

# %% hidden=true
ds.v.differentiate(coord='depth').gv.tplot(robust=True)

# %% hidden=true
ds.pg.gv.tplot()

# %% [markdown]
# ## SIO3

# %% [markdown] heading_collapsed=true
# ### SN13596

# %% hidden=true
a, raw, ds = pp.process("SIO3", 13596, min_pressure=750, start=200, stop=2500)

# %% hidden=true
velosearaptor.adcp.plot_raw_adcp_auxillary(raw)

# %% hidden=true
ax = a.ds.amp.sel(time=slice("2018-10-08", "2018-10-31")).gv.tplot(robust=True)
ax.grid()

# %% hidden=true
ax = a.ds.amp.sel(time=slice("2018-10-08", "2018-11-10")).gv.tplot(vmin=50, vmax=70)
ax.grid()

# %% hidden=true
ax = a.ds.amp.sel(time=slice("2018-10-27", "2018-11-10")).gv.tplot(vmin=50, vmax=70)
ax.grid()

# %% hidden=true
a.burst_average_ensembles(start=4000, stop=4100)

# %% hidden=true
a.ds.u.gv.tplot(robust=True)

# %% hidden=true
a.ds.pg.gv.tplot(robust=True)

# %% hidden=true
