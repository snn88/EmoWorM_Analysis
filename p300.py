import os
import mne
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# load a sample epoch file
epo = mne.read_epochs('./EPO/1001_PV0-epo.fif', proj=False, add_eeg_ref=False)
epo.info['picks'] = None
epo.pick_channels(epo.ch_names[:64])

# convert time to milliseconds
t = epo.times*1e3

# load the layout file
lout = mne.channels.read_layout('biosemi.lay')

# load the erp data
erp = np.load('evo-all.npy')
erp *= 1e6  # convert to microvolts
'''
# remove some time indices
tix = np.logical_and(t > 0, t < 500)
t = t[tix]
erp = erp[:, :, :, tix]
'''
# run the two way anova
f, p = mne.stats.f_mway_rm(erp, [2, 2])
f, p = f.reshape(3, 64, -1), p.reshape(3, 64, -1)

# plot the fmap
fig = plt.figure()
for n in range(64):
    ax = fig.add_axes(lout.pos[n])
    ax.plot(t, f[:, n].T)
    ax.set_ylim((0, f.max()))

# plot the erps
fig = plt.figure()
for n in range(64):
    ax = fig.add_axes(lout.pos[n])
    for m, c in enumerate(['c', 'm', 'b', 'r']):
        ax.plot(t, erp[:, m, n].mean(0), c)
    ax.set_ylim((erp.mean(0).min(), erp.mean(0).max()))

plt.show() 
