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
# ## SIO1

# %% [markdown]
# ### SN3160

# %%
a, ds = pp.process("SIO1", 3160)

# %%
raw = pp.return_raw(a)

# %%
raw = raw.where(raw.pressure > 150, drop=True)

# %%
velosearaptor.adcp.plot_raw_adcp(raw.isel(time=range(11000, 15000)))

# %% [markdown]
# ## SIO2

# %% [markdown]
# ### SN14435

# %%
params = velosearaptor.io.parse_yaml_input(yml_parameters, mooring="SIO2", sn=14435)

# %%
p = munch.munchify(params)

# %%
p.editparams

# %% [markdown]
# Set up a processing object.

# %%
a = velosearaptor.madcp.ProcessADCPyml(
    yml_parameters,
    mooring="SIO2",
    sn=14435,
    verbose=False,
)

# %% [markdown]
# Run the burst averaging

# %%
a.burst_average_ensembles()

# %%
a.ds.amp.gv.tplot()

# %%
a.ds.pg.gv.tplot()

# %%
a.ds.where(a.ds.pressure>20).dropna(dim='depth', how="all").dropna(dim='time', how="all").u.plot(yincrease=False)

# %%
a.ds.where(a.ds.pressure>15).dropna(dim='depth', how="all").dropna(dim='time', how="all").pg.plot(yincrease=False)

# %%
a.ds.where(a.ds.pressure>15).dropna(dim='depth', how="all").dropna(dim='time', how="all").amp.plot(yincrease=False)

# %% [markdown]
# Get rid of surface stuff

# %%
ds = a.ds.where(a.ds.pressure > 15, drop=True)

# %% [markdown]
# Get rid of depth levels that have no data

# %%
ds = ds.dropna(dim="depth", how="all")

# %%
ds.amp.gv.tplot()

# %%
ds.w.gv.tplot()

# %%
ds.u.gv.tplot()

# %%
fig, ax = gv.plot.quickfig(fgs=(7, 3))
ds.pressure.plot(yincrease=False, ax=ax)
gv.plot.concise_date(ax)

# %%
ds.u_error.gv.tplot()

# %%
ds = pp.add_standard_meta_data(ds)

# %%
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(7.5, 3),
                       constrained_layout=True)
ds.xducer_depth.plot(ax=ax, color="0.2")
ds.u.plot(ax=ax)
# ax.invert_yaxis()
ylim = np.min(ax.get_ylim(), 0)
ax.set(ylim=(800, 100))
gv.plot.concise_date(ax)

# %%
raw = a.raw.sel(time=slice(ds.time[0], ds.time[-1]))

# %%
velosearaptor.adcp.plot_raw_adcp_auxillary(raw)

# %%
velosearaptor.adcp.plot_raw_adcp(raw)

# %%
a, ds = pp.process("SIO2", 14435)

# %% [markdown]
# Shear looks decent now

# %%
ds.u.differentiate(coord='depth').gv.tplot(robust=False, cmap='RdBu')

# %%
ds.v.differentiate(coord='depth').gv.tplot(robust=False, cmap='RdBu')

# %%
ds.v.differentiate(coord='depth').gv.tplot(robust=False, cmap='RdBu')

# %%
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

# %% [markdown] heading_collapsed=true
# ### SN14435

# %% hidden=true
a, ds = pp.process("SIO3", 14435, min_pressure=30, start=200, stop=2500)

# %% hidden=true
ds.u.isel(time=range(30)).gv.tplot()

# %% [markdown]
# ### SN22525

# %%
a, ds = pp.process("SIO3", 22525, min_pressure=50)

# %%
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(7.5, 3),
                       constrained_layout=True)
ds.xducer_depth.plot(ax=ax, color="0.2", linewidth=0.3)
ds.u.plot(ax=ax, robust=True)
# ax.invert_yaxis()
ylim = np.min(ax.get_ylim(), 0)
ax.set(ylim=(200, 0))
gv.plot.concise_date(ax)

# %%
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(7.5, 3),
                       constrained_layout=True)
ts = slice("2019-07-01", "2019-09-01")
ds.xducer_depth.sel(time=ts).plot(ax=ax, color="0.2", linewidth=0.3)
ds.u.sel(time=ts).plot(ax=ax, robust=True)
# ax.invert_yaxis()
ylim = np.min(ax.get_ylim(), 0)
ax.set(ylim=(200, 0))
gv.plot.concise_date(ax)

# %%
gv.plot.font_sue_ellen()

# %%
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(7.5, 3),
                       constrained_layout=True)
gv.plot.axstyle(ax)
ts = slice("2019-07-11", "2019-07-25")
ds.xducer_depth.sel(time=ts).plot(ax=ax, color="0.2", linewidth=0.3)
ds.u.sel(time=ts).interpolate_na(dim="depth", limit=3, use_coordinate=False).plot(ax=ax, robust=True)
# ax.invert_yaxis()
ylim = np.min(ax.get_ylim(), 0)
ax.set(ylim=(200, 0), title="WH300 Example")
gv.plot.concise_date(ax)

# %%
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(7.5, 3),
                       constrained_layout=True)
ds.xducer_depth.plot(ax=ax, color="0.2")
ds.v.plot(ax=ax)
# ax.invert_yaxis()
ylim = np.min(ax.get_ylim(), 0)
ax.set(ylim=(150, 0))
gv.plot.concise_date(ax)

# %%
ds

# %%
