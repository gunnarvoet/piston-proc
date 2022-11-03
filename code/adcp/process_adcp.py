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

# %% [markdown] heading_collapsed=true
# ### Imports

# %% janus={"all_versions_showing": false, "cell_hidden": false, "current_version": 0, "id": "b233107473fbf", "named_versions": [], "output_hidden": false, "show_versions": false, "source_hidden": false, "versions": []} hidden=true
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

# %% [markdown] heading_collapsed=true
# ## SIO1

# %% [markdown] heading_collapsed=true hidden=true
# ### SN3160

# %% hidden=true
a, ds = pp.process("SIO1", 3160)

# %% hidden=true
pp.save_to_nc(ds)

# %% [markdown] heading_collapsed=true hidden=true
# ### SN11181

# %% hidden=true
a, ds = pp.process("SIO1", 11181)

# %% hidden=true
pp.save_to_nc(ds)

# %% [markdown] heading_collapsed=true hidden=true
# ### SN14255

# %% hidden=true
a, ds = pp.process("SIO1", 14255)

# %% hidden=true
pp.save_to_nc(ds)

# %% [markdown] heading_collapsed=true hidden=true
# ### SN4021

# %% hidden=true
a, ds = pp.process("SIO1", 4021)

# %% hidden=true
pp.save_to_nc(ds)

# %% [markdown] heading_collapsed=true
# ## SIO2

# %% [markdown] heading_collapsed=true hidden=true
# ### SN14435

# %% hidden=true
a, ds = pp.process("SIO2", 14435)

# %% hidden=true
pp.save_to_nc(ds)

# %% [markdown] heading_collapsed=true hidden=true
# ### SN13596

# %% hidden=true
a, ds = pp.process("SIO2", 13596, min_pressure=750)

# %% hidden=true
pp.save_to_nc(ds)

# %% [markdown] heading_collapsed=true hidden=true
# ### SN22525

# %% [markdown] hidden=true
# Interpolating over bin 18 since we mask it to get rid of some bad data caused by the steel float at the top.

# %% hidden=true
a, ds = pp.process("SIO2", 22525, interpolate_bin=18)

# %% hidden=true
pp.save_to_nc(ds)

# %% [markdown] heading_collapsed=true
# ## SIO3

# %% [markdown] heading_collapsed=true hidden=true
# ### SN13596

# %% hidden=true
a, ds = pp.process("SIO3", 13596, min_pressure=750)

# %% hidden=true
pp.save_to_nc(ds)

# %% [markdown] heading_collapsed=true hidden=true
# ### SN14435

# %% hidden=true
a, ds = pp.process("SIO3", 14435, min_pressure=30)

# %% hidden=true
pp.save_to_nc(ds)

# %% [markdown] heading_collapsed=true hidden=true
# ### SN22525

# %% hidden=true
a, ds = pp.process("SIO3", 22525, min_pressure=50)

# %% hidden=true
pp.save_to_nc(ds)
