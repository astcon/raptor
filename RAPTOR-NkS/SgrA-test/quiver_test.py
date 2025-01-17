#!/usr/bin/env python
import sys
import numpy as np
import matplotlib
# matplotlib.use('Agg')
from pathlib import Path
import matplotlib.pyplot as plt
import h5py
import rapplot

ind = int(sys.argv[1])

#need to know the data_ids
data_id = rapplot.read_data_id("output",ind)

#Computing relevant constants
M=6.5e9 * rapplot.MSUN
d=16.8e3 * rapplot.KPC

rg = (rapplot.G*M/rapplot.SPEED_OF_LIGHT**2.)

mas = (rg/d)* rapplot.MAS_IN_DEG

Tunit =rg/rapplot.SPEED_OF_LIGHT

halfrange=20 #in rg

#read data
min,max,image = rapplot.read_data("output",ind,data_id)

#plot data
plt.figure(figsize=(6,5),dpi=400,facecolor='w')
fig, axs = plt.subplots(1,1,figsize=(5,7))

stokes_ind=0 #we want stokes I

rapplot.plot_data_quiver_mesh(image,min,max,stokes_ind,data_id,fig,ax=axs,Npix=400,halfrange=20,mas=0.3,label="Stokes",cmap="afmhot",quiver=True)

axs.set_xlabel(r"x [mas]")
axs.set_ylabel(r"y [mas]")

plt.tight_layout()
Path("figures/").mkdir(parents=True, exist_ok=True)
print("figures/"+"quiver_img_%d.png"%ind)
plt.savefig("figures/quiver_img_%d.png"%ind, transparent=False,dpi=500)
plt.clf()

image.close()
