#!/usr/bin/env python
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
from pathlib import Path
import matplotlib.pyplot as plt
import h5py
import rapplot

import matplotlib as mpl
# Set Matplotlib parameters
mpl.rcParams['font.size'] = 15
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.serif'] = 'Times'
mpl.rcParams['text.usetex'] = False
mpl.rcParams['figure.figsize'] = 6, 10
mpl.rcParams['figure.subplot.left'] = .1
mpl.rcParams['figure.subplot.right'] = .9
mpl.rcParams['figure.subplot.bottom'] = .1
mpl.rcParams['figure.subplot.top'] = .9
mpl.rcParams['lines.linewidth'] = 2.5
mpl.rcParams['lines.markersize'] = 10
mpl.rcParams['lines.markeredgewidth'] = 1.5
mpl.rcParams['axes.linewidth'] = 1.0
mpl.rcParams['xtick.major.size'] = 4.0
mpl.rcParams['ytick.major.size'] = 4.0
mpl.rcParams['xtick.minor.size'] = 3.0
mpl.rcParams['ytick.minor.size'] = 3.0
mpl.rcParams['xtick.major.pad'] = '5'
mpl.rcParams['ytick.major.pad'] = '5'
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'

#font = {'family' : 'normal',
 #       'size'   : 16}

#matplotlib.rc('font', **font)

ind = int(sys.argv[1])
print(ind)
#need to know the data_ids
data_id = rapplot.read_data_id("output",ind)

#Computing relevant constants
M=5e6 * rapplot.MSUN
d=8 * rapplot.KPC

rg = (rapplot.G*M/rapplot.SPEED_OF_LIGHT**2.)

mas = (rg/d)* rapplot.MAS_IN_DEG

Tunit =rg/rapplot.SPEED_OF_LIGHT

halfrange=20 #in rg

#read data
min,max,image = rapplot.read_data("output",ind,data_id)

#plot data
plt.figure(figsize=(6,5),dpi=1000,facecolor='w')
fig, axs = plt.subplots(1,1,figsize=(6,5))

stokes_ind=0 #we want stokes I

rapplot.plot_data_stokes(image, min, max, stokes_ind, data_id, fig, axs, halfrange, mas, label="$I/I_{max}$", cmap="afmhot")

#rapplot.plot_data_stokes(image,min,max,1,data_id,fig,axs[1][0],halfrange,mas,label="Stokes Q",cmap="RdBu")
#
#rapplot.plot_data_stokes(image,min,max,2,data_id,fig,axs[0][1],halfrange,mas,label="Stokes U",cmap="RdBu")

#rapplot.plot_data_stokes(image,min,max,3,data_id,fig,axs[1][1],halfrange,mas,label="Stokes V",cmap="RdBu")

fig.suptitle('t=%.01lf [M]'%(ind*10.),fontsize=20)

#axs[0][0].set_xlabel(r"x [mas]")
#axs[0][0].set_ylabel(r"y [mas]")

#axs[0][0].set_xlim(-0.1,0.1)
#axs[0][0].set_ylim(-0.1,0.1)
axs.set_xlabel(r"x [mas]",fontsize=15)
axs.set_ylabel(r"y [mas]",fontsize=15)

axs.set_xlim(-0.1,0.1)
axs.set_ylim(-0.1,0.1)

# Set font size for numerical labels (tick labels) on both axes
axs.tick_params(axis='both', which='major', labelsize=15)

# Adjust font size of color bar's numerical labels if a color bar exists
#if 'cbar' in locals():
#cbar.ax.tick_params(labelsize=14)
#axs[1][0].set_xlabel(r"x [mas]")
#axs[1][0].set_ylabel(r"y [mas]")

#axs[1][0].set_xlim(-0.1,0.1)
#axs[1][0].set_ylim(-0.1,0.1)

#axs[0][1].set_xlabel(r"x [mas]")
#axs[0][1].set_ylabel(r"y [mas]")

#axs[0][1].set_xlim(-0.1,0.1)
#axs[0][1].set_ylim(-0.1,0.1)

#axs[1][1].set_xlabel(r"x [mas]")
#axs[1][1].set_ylabel(r"y [mas]")

#axs[1][1].set_xlim(-0.1,0.1)
#axs[1][1].set_ylim(-0.1,0.1)

plt.tight_layout()
Path("figures/").mkdir(parents=True, exist_ok=True)
print("figures/"+"img_%d.png"%ind)
plt.savefig("figures/img_%d.png"%ind, transparent=False,dpi=400)
plt.clf()

image.close()

